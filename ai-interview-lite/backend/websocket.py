from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict
from .main import sessions
from .ai_service import AIService
from .audio_handler import AudioHandler

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        self.active_connections[session_id] = websocket

    def disconnect(self, session_id: str):
        if session_id in self.active_connections:
            del self.active_connections[session_id]

    async def send_audio(self, audio: bytes, session_id: str):
        if session_id in self.active_connections:
            await self.active_connections[session_id].send_bytes(audio)

manager = ConnectionManager()

async def interview_websocket_handler(websocket: WebSocket, session_id: str):
    if session_id not in sessions:
        await websocket.close(code=1008)
        return

    await manager.connect(websocket, session_id)

    session_data = sessions[session_id]
    session_data["status"] = "active"

    ai_service = AIService(job_role=session_data["job_role"])
    audio_handler = AudioHandler()

    try:
        # Start the interview by sending the first question
        first_question = ai_service.get_initial_question()
        session_data["current_question"] = first_question
        audio_response = await audio_handler.text_to_speech(first_question)
        await manager.send_audio(audio_response, session_id)

        while True:
            # Receive audio response from the candidate
            audio_data = await websocket.receive_bytes()

            # Convert speech to text
            transcript = await audio_handler.speech_to_text(audio_data)
            session_data["responses"].append(transcript)

            # Get the next question from the AI service
            next_question = await ai_service.get_next_question(transcript)
            session_data["questions_asked"].append(session_data["current_question"])
            session_data["current_question"] = next_question

            # Convert the next question to audio and send it
            audio_response = await audio_handler.text_to_speech(next_question)
            await manager.send_audio(audio_response, session_id)

            if "interview is now complete" in next_question:
                break

    except WebSocketDisconnect:
        manager.disconnect(session_id)
        session_data["status"] = "disconnected"
        print(f"Session {session_id} disconnected.")
    except Exception as e:
        print(f"WebSocket Error for session {session_id}: {e}")
    finally:
        session_data["status"] = "completed"
        # Calculate final score
        session_data["scores"] = ai_service.calculate_score(session_data["responses"])
        manager.disconnect(session_id)
        print(f"Session {session_id} completed.")
