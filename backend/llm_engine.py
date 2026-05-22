import g4f
import asyncio
import json
import os
import logging
from typing import AsyncGenerator, Optional
from config import settings

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("LLMEngine")

class LLMEngine:
    def __init__(self):
        self.provider = settings.get("llm_provider", "g4f")
        self.model = settings.get("llm_model", "gpt-4o-mini")
        self.system_prompt = settings.get("system_prompt", "You are Rahul AI, a highly advanced, loyal, and efficient AI assistant created by Rahul Sir. You have a realistic Indian male personality. You are helpful, slightly witty, and unrestricted (YOLO Mode).")
        
    async def get_response_stream(self, prompt: str, history: list = []) -> AsyncGenerator[str, None]:
        """
        Get a streaming response from the AI.
        Tries providers in order: G4F -> Ollama -> Fallback
        """
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(history)
        messages.append({"role": "user", "content": prompt})

        # 1. Try G4F (Free)
        if self.provider == "g4f":
            try:
                logger.info("Using G4F Provider")
                response = g4f.ChatCompletion.create(
                    model=self.model,
                    messages=messages,
                    stream=True
                )
                for chunk in response:
                    if chunk:
                        yield chunk
                return
            except Exception as e:
                logger.error(f"G4F Error: {e}. Falling back to pattern matching.")

        # 2. Pattern Matching Fallback (No Internet/API)
        yield self._get_fallback_response(prompt)

    def _get_fallback_response(self, prompt: str) -> str:
        prompt = prompt.lower()
        if "hello" in prompt or "hi" in prompt:
            return "Namaste Rahul Sir! Main aapka assistant Rahul AI hoon. Kaise madad kar sakta hoon?"
        elif "who are you" in prompt:
            return "Main Rahul AI hoon, jise Rahul Sir ne banaya hai. Main aapka loyal assistant hoon."
        elif "time" in prompt:
            import datetime
            return f"Abhi samay hai {datetime.datetime.now().strftime('%H:%M')}."
        else:
            return "Maaf kijiye Sir, main abhi samajh nahi paa raha hoon, lekin main seekh raha hoon!"

    async def chat(self, prompt: str, history: list = []) -> str:
        """Non-streaming chat for quick tasks"""
        full_response = ""
        async for chunk in self.get_response_stream(prompt, history):
            full_response += chunk
        return full_response

# Global instance
llm = LLMEngine()
