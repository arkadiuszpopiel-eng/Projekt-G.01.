"""
NeuroForge - Main FastAPI application.
Serves the web UI and provides API endpoints for chat, model management, and configuration.
"""
import asyncio
import json
import logging
import uuid
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

from .config import load_config, save_config, get_models_dir
from .inference.engine import engine
from .inference.model_manager import (
    list_models, get_model_path, download_model, get_recommended_models
)
from .agent.loop import agent

logger = logging.getLogger("neurostudio")

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown logic."""
    logger.info("NeuroForge starting up...")
    yield
    logger.info("NeuroForge shutting down...")
    await engine.stop()


app = FastAPI(title="NeuroForge", version="0.1.0", lifespan=lifespan)

# Mount static files
app.mount("/css", StaticFiles(directory=str(FRONTEND_DIR / "css")), name="css")
app.mount("/js", StaticFiles(directory=str(FRONTEND_DIR / "js")), name="js")


# ──────────────────────── Pages ────────────────────────

@app.get("/")
async def index():
    return FileResponse(str(FRONTEND_DIR / "index.html"))


# ──────────────────────── Model Management ────────────────────────

@app.get("/api/models")
async def api_list_models():
    """List all available local models."""
    models = list_models()
    return {"models": [m.to_dict() for m in models]}


@app.get("/api/models/recommended")
async def api_recommended_models():
    """List recommended models with download status."""
    return {"models": get_recommended_models()}


class ModelLoadRequest(BaseModel):
    filename: str
    gpu_layers: int = -1
    context_size: int = 8192
    threads: int = 8


@app.post("/api/models/load")
async def api_load_model(req: ModelLoadRequest):
    """Load a model into the inference engine."""
    model_path = get_model_path(req.filename)
    if not model_path:
        raise HTTPException(404, f"Model not found: {req.filename}")

    success = await engine.start(
        model_path,
        gpu_layers=req.gpu_layers,
        context_size=req.context_size,
        threads=req.threads,
    )
    if not success:
        raise HTTPException(500, "Failed to start inference engine. Check logs.")

    return {"success": True, "model": req.filename}


@app.post("/api/models/unload")
async def api_unload_model():
    """Unload the current model."""
    await engine.stop()
    return {"success": True}


class ModelDownloadRequest(BaseModel):
    repo: str
    filename: str


@app.post("/api/models/download")
async def api_download_model(req: ModelDownloadRequest):
    """Download a model from HuggingFace."""
    try:
        path = await download_model(req.repo, req.filename)
        return {"success": True, "path": path}
    except Exception as e:
        raise HTTPException(500, f"Download failed: {str(e)}")


# ──────────────────────── Engine Status ────────────────────────

@app.get("/api/status")
async def api_status():
    """Get current engine and system status."""
    status = await engine.get_status()
    models = list_models()
    config = load_config()
    return {
        "engine": status,
        "models_count": len(models),
        "config": {
            "inference": config.get("inference", {}),
            "router": config.get("router", {}),
        },
    }


# ──────────────────────── Configuration ────────────────────────

@app.get("/api/config")
async def api_get_config():
    return load_config()


class ConfigUpdateRequest(BaseModel):
    config: dict


@app.post("/api/config")
async def api_update_config(req: ConfigUpdateRequest):
    current = load_config()
    _deep_merge(current, req.config)
    save_config(current)
    return {"success": True}


def _deep_merge(base: dict, override: dict):
    for key, value in override.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            _deep_merge(base[key], value)
        else:
            base[key] = value


# ──────────────────────── Chat (WebSocket) ────────────────────────

@app.websocket("/ws/chat")
async def ws_chat(ws: WebSocket):
    """WebSocket endpoint for real-time chat with the agent."""
    await ws.accept()
    session_id = str(uuid.uuid4())

    try:
        await ws.send_json({"type": "session", "session_id": session_id})

        while True:
            data = await ws.receive_json()
            msg_type = data.get("type")

            if msg_type == "message":
                user_msg = data.get("content", "")
                if not user_msg.strip():
                    continue

                async for event in agent.process_message(session_id, user_msg):
                    await ws.send_json(event)

            elif msg_type == "clear":
                agent.clear_conversation(session_id)
                await ws.send_json({"type": "cleared"})

            elif msg_type == "set_session":
                new_id = data.get("session_id")
                if new_id:
                    session_id = new_id

    except WebSocketDisconnect:
        logger.info("WebSocket disconnected: %s", session_id)
    except Exception as e:
        logger.error("WebSocket error: %s", e)
        try:
            await ws.send_json({"type": "error", "message": str(e)})
        except Exception:
            pass


# ──────────────────────── Chat (HTTP fallback) ────────────────────────

class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None


@app.post("/api/chat")
async def api_chat(req: ChatRequest):
    """HTTP endpoint for chat (non-streaming, for simple clients)."""
    session_id = req.session_id or str(uuid.uuid4())
    events = []

    async for event in agent.process_message(session_id, req.message):
        events.append(event)

    text_parts = [e["content"] for e in events if e["type"] == "text"]
    tool_events = [e for e in events if e["type"] in ("tool_call", "tool_result")]

    return {
        "response": "".join(text_parts),
        "tool_events": tool_events,
        "session_id": session_id,
    }


# ──────────────────────── Conversation Management ────────────────────────

@app.get("/api/sessions")
async def api_list_sessions():
    return {"sessions": agent.list_sessions()}


@app.delete("/api/sessions/{session_id}")
async def api_delete_session(session_id: str):
    agent.clear_conversation(session_id)
    return {"success": True}
