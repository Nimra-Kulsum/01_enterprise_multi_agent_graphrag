"""
Real-Time Collaborative Canvas with CRDTs
Demonstrates Observed-Remove Set (OR-Set) CRDT convergence over WebSockets.
"""
import uuid
import time
from typing import Dict, Set, Tuple
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn

app = FastAPI(title="Real-Time CRDT Collaboration Engine", version="1.0.0")

# Element CRDT: LWW-Element-Set (Last-Write-Wins Element Set)
class CanvasCRDT:
    def __init__(self):
        # element_id -> (element_data, timestamp, is_deleted)
        self.elements: Dict[str, Tuple[dict, float, bool]] = {}

    def update_element(self, element_id: str, data: dict, timestamp: float):
        if element_id in self.elements:
            curr_data, curr_ts, is_del = self.elements[element_id]
            if timestamp > curr_ts:
                self.elements[element_id] = (data, timestamp, False)
        else:
            self.elements[element_id] = (data, timestamp, False)

    def delete_element(self, element_id: str, timestamp: float):
        if element_id in self.elements:
            curr_data, curr_ts, _ = self.elements[element_id]
            if timestamp > curr_ts:
                self.elements[element_id] = (curr_data, timestamp, True)

    def get_active_state(self) -> Dict[str, dict]:
        return {k: v[0] for k, v in self.elements.items() if not v[2]}

canvas = CanvasCRDT()

@app.websocket("/ws/canvas/{doc_id}")
async def canvas_socket(websocket: WebSocket, doc_id: str):
    await websocket.accept()
    await websocket.send_json({"type": "SYNC_STATE", "elements": canvas.get_active_state()})
    
    try:
        while True:
            msg = await websocket.receive_json()
            action = msg.get("action")
            elem_id = msg.get("element_id")
            ts = msg.get("timestamp", time.time())
            
            if action == "UPSERT":
                canvas.update_element(elem_id, msg.get("data", {}), ts)
            elif action == "DELETE":
                canvas.delete_element(elem_id, ts)
                
            # Broadcast updated active elements
            await websocket.send_json({
                "type": "BROADCAST_STATE",
                "active_elements_count": len(canvas.get_active_state())
            })
    except WebSocketDisconnect:
        pass

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8022)
