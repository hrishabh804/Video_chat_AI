class WebRTCService {
  mediaStream;
  mediaRecorder;
  audioChunks = [];

  async startRecording() {
    try {
      this.mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });
      this.mediaRecorder = new MediaRecorder(this.mediaStream, { mimeType: 'audio/webm' });

      this.audioChunks = []; // Clear previous chunks

      this.mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          this.audioChunks.push(event.data);
        }
      };

      this.mediaRecorder.start();
      console.log('MediaRecorder started');
    } catch (error) {
      console.error('Error starting recording:', error);
    }
  }

  stopRecordingAndGetBlob() {
    return new Promise((resolve) => {
      if (this.mediaRecorder && this.mediaRecorder.state === 'recording') {
        this.mediaRecorder.onstop = () => {
          const audioBlob = new Blob(this.audioChunks, { type: 'audio/webm' });
          this.mediaStream.getTracks().forEach(track => track.stop());
          console.log('MediaRecorder stopped');
          resolve(audioBlob);
        };
        this.mediaRecorder.stop();
      } else {
        resolve(null);
      }
    });
  }
}

const webRTCService = new WebRTCService();
export default webRTCService;
