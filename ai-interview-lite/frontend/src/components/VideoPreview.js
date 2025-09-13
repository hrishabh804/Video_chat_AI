import React, { useRef, useEffect } from 'react';

const VideoPreview = () => {
  const videoRef = useRef(null);

  useEffect(() => {
    // Get user media
    navigator.mediaDevices.getUserMedia({ video: true, audio: true })
      .then(stream => {
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      })
      .catch(err => {
        console.error("Error accessing media devices.", err);
      });
  }, []);

  return (
    <div>
      <h3>Your Camera</h3>
      <video ref={videoRef} autoPlay muted style={{ width: '320px', height: '240px', border: '1px solid black' }} />
    </div>
  );
};

export default VideoPreview;
