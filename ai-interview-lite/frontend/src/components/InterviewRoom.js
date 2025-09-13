import React, { useState, useRef, useEffect } from 'react';
import VideoPreview from './VideoPreview';
import AIAvatar from './AIAvatar';
import webSocketService from '../services/websocket';
import webRTCService from '../services/webrtc';

const InterviewRoom = () => {
  const [interviewStatus, setInterviewStatus] = useState('waiting'); // waiting, active, completed
  const [isRecording, setIsRecording] = useState(false);
  const audioPlayer = useRef(null);

  const handleStartInterview = async () => {
    try {
      // Step 1: Create an interview session
      const response = await fetch('http://localhost:8000/interview/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ job_role: 'Software Engineer', candidate_name: 'John Doe' }),
      });
      const data = await response.json();
      const { session_id } = data;

      // Step 2: Connect to WebSocket
      await webSocketService.connect(session_id);
      setInterviewStatus('active');

      // Step 3: Set up audio message handler
      webSocketService.setOnAudioMessage((audioData) => {
        const audioBlob = new Blob([audioData], { type: 'audio/mp3' });
        const audioUrl = URL.createObjectURL(audioBlob);
        if (audioPlayer.current) {
          audioPlayer.current.src = audioUrl;
          audioPlayer.current.play();
        }
      });

    } catch (error) {
      console.error('Failed to start interview:', error);
    }
  };

  const handleEndInterview = () => {
    webSocketService.disconnect();
    setInterviewStatus('completed');
  };

  const handleToggleRecording = async () => {
    if (isRecording) {
      // Stop recording and send the audio
      const audioBlob = await webRTCService.stopRecordingAndGetBlob();
      if (audioBlob) {
        webSocketService.sendAudio(audioBlob);
      }
      setIsRecording(false);
    } else {
      // Start recording
      await webRTCService.startRecording();
      setIsRecording(true);
    }
  };

  return (
    <div>
      <h2>Interview Room</h2>
      <div style={{ display: 'flex', justifyContent: 'center', gap: '20px', marginBottom: '20px' }}>
        <VideoPreview />
        <AIAvatar />
      </div>
      <audio ref={audioPlayer} style={{ display: 'none' }} />
      <div>
        {interviewStatus === 'waiting' && (
          <button onClick={handleStartInterview}>Begin Interview</button>
        )}
        {interviewStatus === 'active' && (
          <div>
            <button onClick={handleToggleRecording}>
              {isRecording ? 'Stop and Send Response' : 'Start Recording Answer'}
            </button>
            <button onClick={handleEndInterview} style={{ marginLeft: '10px' }}>End Interview</button>
          </div>
        )}
        {interviewStatus === 'completed' && (
          <div>
            <h3>Interview Completed</h3>
            <p>Thank you for your time.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default InterviewRoom;
