# AI Interview Lite

A simple AI video interview system with low-latency real-time communication
between an AI interviewer and a candidate.

This project focuses on the core functionality of a real-time AI interview system,
using in-memory storage for simplicity and quick testing.

## Project Structure

```
/ai-interview-lite
├── backend/
│   ├── main.py           # FastAPI app
│   ├── ai_service.py     # OpenAI integration
│   ├── audio_handler.py  # Audio processing
│   ├── websocket.py      # WebSocket handlers
│   ├── config.py         # API keys
│   └── requirements.txt  # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   ├── components/
│   │   │   ├── InterviewRoom.js
│   │   │   ├── VideoPreview.js
│   │   │   └── AIAvatar.js
│   │   └── services/
│   │       ├── websocket.js
│   │       └── webrtc.js
│   └── package.json
└── README.md
```

## Setup and Running

### Backend

1.  Navigate to the `backend` directory: `cd backend`
2.  Install dependencies: `pip install -r requirements.txt`
3.  Add your OpenAI API key to `backend/config.py`.
4.  Run the server: `uvicorn main:app --reload`

### Frontend

1.  Navigate to the `frontend` directory: `cd frontend`
2.  Install dependencies: `npm install`
3.  Start the development server: `npm start`
