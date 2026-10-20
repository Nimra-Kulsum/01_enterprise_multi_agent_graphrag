"""
Ultra-Low-Latency Real-Time Voice AI Agent
Simulates bidirectional audio streaming, VAD state, and sentence-clause audio chunking.
"""
import asyncio
import time
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn

app = FastAPI(title="Real-Time Voice AI Service", version="1.0.0")

@app.websocket("/ws/voice-stream")
async def voice_stream_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_json({"type": "session_started", "latency_target_ms": 300})
    
    try:
        while True:
            data = await websocket.receive_text()
            t0 = time.perf_counter()
            
            # Simulate Streaming Pipeline: ASR -> LLM -> TTS
            await asyncio.sleep(0.04) # ASR chunk
            transcript = f"User said: {data}"
            
            # LLM streaming tokens
            tokens = ["Hello!", " I", " understand", " your", " query.", " Let", " me", " help."]
            for token in tokens:
                await asyncio.sleep(0.02)
                elapsed = (time.perf_counter() - t0) * 1000
                await websocket.send_json({
                    "type": "audio_chunk",
                    "text_chunk": token,
                    "simulated_pcm_bytes": 1024,
                    "latency_ms": round(elapsed, 1)
                })
                
    except WebSocketDisconnect:
        print("Voice client disconnected.")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8004)
