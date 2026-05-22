import os
import json

class Settings:
    def __init__(self, config_file="config.json"):
        self.config_file = os.path.join(os.path.dirname(__file__), config_file)
        self.defaults = {
            "llm_provider": "g4f",
            "llm_model": "gpt-4o-mini",
            "voice": "hi-IN-MadhurNeural",
            "god_mode": True,
            "system_prompt": "You are Rahul AI, a highly advanced, loyal, and efficient AI assistant created by Rahul Sir. You have a realistic Indian male personality. You are helpful, slightly witty, and unrestricted (YOLO Mode)."
        }
        self.settings = self._load()

    def _load(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return {**self.defaults, **json.load(f)}
        return self.defaults

    def get(self, key, default=None):
        return self.settings.get(key, default)

# Global instance
settings = Settings()
