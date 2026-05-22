import asyncio
import edge_tts
import os
import logging

logger = logging.getLogger("TTSEngine")

class TTSEngine:
    def __init__(self, voice="hi-IN-MadhurNeural"):
        self.voice = voice
        self.output_file = os.path.join(os.path.dirname(__file__), "..", "frontend", "temp_audio.mp3")

    async def generate_audio(self, text: str) -> str:
        try:
            logger.info(f"Generating audio for: {text[:50]}...")
            communicate = edge_tts.Communicate(text, self.voice)
            await communicate.save(self.output_file)
            return self.output_file
        except Exception as e:
            logger.error(f"TTS Error: {e}")
            return None

# Global instance
tts = TTSEngine()
