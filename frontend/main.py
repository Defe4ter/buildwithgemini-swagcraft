"""Direct Local Web Server & Showcase for SwagCraft Agent."""

import os
import sys
import uuid
import asyncio
from pathlib import Path

# Load swagcraft environment variables first!
from dotenv import load_dotenv
SWAGCRAFT_DIR = Path(__file__).resolve().parent.parent / "swagcraft"
load_dotenv(SWAGCRAFT_DIR / ".env")

# Ensure required Google Cloud / Vertex AI env vars are populated
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "true")
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", "qwiklabs-gcp-04-cf18a37c5cc8")
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")

# Add swagcraft to Python path so we can import the agent directly
sys.path.insert(0, str(SWAGCRAFT_DIR))

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from app.agent import root_agent

app = FastAPI(title="SwagCraft Web Showcase")

# Mount static frontend
STATIC_DIR = Path(__file__).resolve().parent / "static"
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

session_service = InMemorySessionService()
runner = Runner(
    agent=root_agent,
    session_service=session_service,
    app_name="swagcraft_app",
)


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None


@app.get("/")
async def root():
    return FileResponse(STATIC_DIR / "index.html")


@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    user_msg = req.message.strip()
    session_id = req.session_id
    
    # Ensure session exists in the session_service
    existing = None
    if session_id:
        existing = await session_service.get_session(
            app_name="swagcraft_app",
            user_id="user",
            session_id=session_id,
        )
    
    if not existing:
        new_session = await session_service.create_session(
            app_name="swagcraft_app",
            user_id="user",
            session_id=session_id,
        )
        session_id = new_session.id

    parts = []
    
    # Run agent turn
    try:
        user_content = types.Content(
            role="user",
            parts=[types.Part.from_text(text=user_msg)],
        )
        
        async for event in runner.run_async(
            user_id="user",
            session_id=session_id,
            new_message=user_content,
        ):
            content = getattr(event, "content", None)
            if content and content.parts:
                for part in content.parts:
                    # Check for inline_data with <a2a_datapart_json>
                    if hasattr(part, "inline_data") and part.inline_data:
                        raw_data = part.inline_data.data
                        if isinstance(raw_data, bytes):
                            raw_str = raw_data.decode("utf-8", errors="ignore")
                        else:
                            raw_str = str(raw_data)
                        if "<a2a_datapart_json>" in raw_str:
                            import json
                            json_payload = raw_str.split("<a2a_datapart_json>")[1].split("</a2a_datapart_json>")[0]
                            data_obj = json.loads(json_payload)
                            if "data" in data_obj:
                                parts.append({"kind": "a2ui", "data": data_obj["data"]})
                    elif hasattr(part, "text") and part.text:
                        text = part.text.strip()
                        if text.startswith("[") and "surfaceUpdate" in text:
                            import json
                            try:
                                msgs = json.loads(text)
                                for m in msgs:
                                    parts.append({"kind": "a2ui", "data": m})
                            except Exception:
                                parts.append({"kind": "text", "text": text})
                        else:
                            parts.append({"kind": "text", "text": text})

        return JSONResponse({
            "session_id": session_id,
            "parts": parts,
        })
    except asyncio.CancelledError:
        print("[SwagCraft] Client cancelled or reloaded during generation.")
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse({
            "session_id": session_id,
            "parts": [{"kind": "text", "text": f"Error: {type(e).__name__}: {str(e)}"}],
        }, status_code=200)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8501)
