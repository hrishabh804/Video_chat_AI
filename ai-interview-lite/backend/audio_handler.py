import openai
from gtts import gTTS
import uuid
import os
import aiofiles
from . import config

# Configure OpenAI API key
openai.api_key = config.OPENAI_API_KEY

TEMP_AUDIO_DIR = "temp_audio"
os.makedirs(TEMP_AUDIO_DIR, exist_ok=True)

class AudioHandler:
    async def speech_to_text(self, audio_data: bytes) -> str:
        """
        Converts speech from audio data to text using Whisper API.
        """
        # Create a temporary file to store the audio data
        temp_audio_path = os.path.join(TEMP_AUDIO_DIR, f"{uuid.uuid4()}.webm")

        async with aiofiles.open(temp_audio_path, "wb") as f:
            await f.write(audio_data)

        try:
            with open(temp_audio_path, "rb") as audio_file:
                transcript = await openai.Audio.atranscribe("whisper-1", audio_file)
            return transcript['text']
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)

    async def text_to_speech(self, text: str) -> bytes:
        """
        Converts text to speech using gTTS and returns the audio data as bytes.
        """
        temp_audio_path = os.path.join(TEMP_AUDIO_DIR, f"{uuid.uuid4()}.mp3")

        try:
            tts = gTTS(text=text, lang='en')
            tts.save(temp_audio_path)

            async with aiofiles.open(temp_audio_path, "rb") as f:
                audio_data = await f.read()

            return audio_data
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)
