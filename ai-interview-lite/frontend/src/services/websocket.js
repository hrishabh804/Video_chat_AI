class WebSocketService {
  socket;
  onAudioMessage;

  connect(sessionId) {
    const wsUrl = `ws://localhost:8000/ws/${sessionId}`;
    this.socket = new WebSocket(wsUrl);
    this.socket.binaryType = 'arraybuffer';

    return new Promise((resolve, reject) => {
      this.socket.onopen = () => {
        console.log('WebSocket connected');
        resolve();
      };

      this.socket.onmessage = (event) => {
        if (this.onAudioMessage) {
          // The message is expected to be audio data (ArrayBuffer)
          this.onAudioMessage(event.data);
        }
      };

      this.socket.onclose = () => {
        console.log('WebSocket disconnected');
      };

      this.socket.onerror = (error) => {
        console.error('WebSocket error:', error);
        reject(error);
      };
    });
  }

  disconnect() {
    if (this.socket) {
      this.socket.close();
    }
  }

  sendAudio(audioBlob) {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(audioBlob);
    } else {
      console.error('WebSocket is not connected.');
    }
  }

  setOnAudioMessage(callback) {
    this.onAudioMessage = callback;
  }
}

const webSocketService = new WebSocketService();
export default webSocketService;
