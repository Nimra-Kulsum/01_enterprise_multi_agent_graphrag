"""
Distributed Inverted-Index Search Engine (Mini-Elasticsearch)
Inverted index construction, BM25 scoring, and multi-term search.
"""
import math
import re
from typing import List, Dict, Set
from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Distributed Inverted-Index Search Engine", version="1.0.0")

class Document(BaseModel):
    doc_id: str
    title: str
    body: str

class SearchResult(BaseModel):
    doc_id: str
    title: str
    score: float

class InvertedIndex:
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.docs: Dict[str, Document] = {}
        self.index: Dict[str, Dict[str, int]] = {} # term -> {doc_id: term_frequency}
        self.doc_lengths: Dict[str, int] = {}
        self.avg_doc_length: float = 0.0

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r'\w+', text.lower())

    def index_document(self, doc: Document):
        self.docs[doc.doc_id] = doc
        tokens = self._tokenize(doc.title + " " + doc.body)
        self.doc_lengths[doc.doc_id] = len(tokens)
        
        for t in tokens:
            if t not in self.index:
                self.index[t] = {}
            self.index[t][doc.doc_id] = self.index[t].get(doc.doc_id, 0) + 1
            
        self.avg_doc_length = sum(self.doc_lengths.values()) / len(self.doc_lengths)

    def search(self, query: str, top_k: int = 5) -> List[SearchResult]:
        query_terms = self._tokenize(query)
        scores: Dict[str, float] = {}
        num_docs = len(self.docs)

        for term in query_terms:
            if term not in self.index:
                continue
            postings = self.index[term]
            df = len(postings)
            idf = math.log((num_docs - df + 0.5) / (df + 0.5) + 1.0)
            
            for doc_id, tf in postings.items():
                doc_len = self.doc_lengths[doc_id]
                numerator = tf * (self.k1 + 1.0)
                denominator = tf + self.k1 * (1.0 - self.b + self.b * (doc_len / (self.avg_doc_length or 1.0)))
                term_score = idf * (numerator / denominator)
                scores[doc_id] = scores.get(doc_id, 0.0) + term_score

        sorted_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        return [
            SearchResult(doc_id=doc_id, title=self.docs[doc_id].title, score=round(score, 3))
            for doc_id, score in sorted_results
        ]

engine = InvertedIndex()
# Seed with sample distributed systems documents
engine.index_document(Document(doc_id="1", title="Raft Consensus Algorithm", body="Raft is a consensus protocol designed for fault-tolerant distributed systems."))
engine.index_document(Document(doc_id="2", title="Consistent Hashing Ring", body="Consistent hashing minimizes key redistribution in distributed cache clusters."))
engine.index_document(Document(doc_id="3", title="LSM Trees and Storage", body="Log-Structured Merge-trees provide high throughput sequential writes for databases."))

@app.get("/api/v1/search", response_model=List[SearchResult])
def search_index(q: str):
    return engine.search(q)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8018)
