import asyncio
import json
import logging
import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

# Internal imports
from config import settings
from llm_engine import llm
from tts_engine import tts
from skills_manager import skills_manager

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("RahulAI_Core")

app = FastAPI(title="Rahul AI Server")

# Serve static files from frontend directory
# We'll create the frontend folder next
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")
if not os.path.exists(FRONTEND_DIR):
    os.makedirs(FRONTEND_DIR)

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.get("/")
async def get_index():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("New WebSocket connection established")
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message = json.loads(data)
            msg_type = message.get("type")
            payload = message.get("payload")

            if msg_type == "chat":
                await handle_chat(websocket, payload)
            elif msg_type == "ping":
                await websocket.send_json({"type": "pong"})
            
    except WebSocketDisconnect:
        logger.info("WebSocket connection closed")
    except Exception as e:
        logger.error(f"WebSocket Error: {e}")

async def handle_chat(websocket: WebSocket, text: str):
    """Processes chat messages, generates AI response and audio"""
    logger.info(f"User: {text}")
    
    full_response = ""
    # 1. Notify client that AI is thinking
    await websocket.send_json({"type": "status", "payload": "thinking"})

    # 2. Get AI response stream
    # Note: We'll implement skill-checking logic here later
    try:
        async for chunk in llm.get_response_stream(text):
            full_response += chunk
            # Send text chunks to UI for 'typing' effect
            await websocket.send_json({"type": "text_chunk", "payload": chunk})
        
        # 3. Notify client that thinking is done
        await websocket.send_json({"type": "status", "payload": "speaking"})

        # 4. Generate and stream audio
        # We'll stream the audio file path or the bytes
        # For simplicity in this version, we'll generate the full audio and send the path/event
        audio_file = await tts.generate_audio(full_response)
        
        # In a real streaming scenario, we'd send base64 or a URL
        # Here we send a 'voice' event
        await websocket.send_json({
            "type": "voice", 
            "payload": {
                "text": full_response,
                "audio_url": f"/static/temp_audio.mp3" # Simplified for now
            }
        })
        
        await websocket.send_json({"type": "status", "payload": "idle"})

    except Exception as e:
        logger.error(f"Chat Handling Error: {e}")
        await websocket.send_json({"type": "error", "payload": str(e)})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
