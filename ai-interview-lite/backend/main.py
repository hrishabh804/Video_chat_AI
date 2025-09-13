import uuid
import time
from fastapi import FastAPI, WebSocket, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any

# In-memory storage for sessions
sessions: Dict[str, Dict[str, Any]] = {}

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class InterviewCreateRequest(BaseModel):
    job_role: str
    candidate_name: str

@app.post("/interview/create")
async def create_interview(request: InterviewCreateRequest):
    """
    Create a new interview session.
    """
    session_id = str(uuid.uuid4())
    sessions[session_id] = {
        "job_role": request.job_role,
        "candidate_name": request.candidate_name,
        "status": "waiting",
        "questions_asked": [],
        "responses": [],
        "current_question": "",
        "start_time": time.time(),
        "scores": {},
    }
    return {"session_id": session_id, "session_data": sessions[session_id]}

@app.get("/interview/{session_id}")
async def get_interview_session(session_id: str):
    """
    Get details for a specific interview session.
    """
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"session_id": session_id, "session_data": sessions[session_id]}

from .websocket import interview_websocket_handler

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """
    WebSocket endpoint for real-time communication during the interview.
    """
    await interview_websocket_handler(websocket, session_id)
