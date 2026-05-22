import datetime
import os
import platform

class SystemSkill:
    name = "system"
    
    async def execute(self, action: str, **kwargs):
        if action == "get_time":
            return f"The current time is {datetime.datetime.now().strftime('%I:%M %p')}."
        elif action == "get_date":
            return f"Today is {datetime.datetime.now().strftime('%A, %B %d, %Y')}."
        elif action == "get_stats":
            import psutil
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            return f"System Status: CPU at {cpu}%, RAM at {ram}%."
        return "Unknown system action."

    def get_definition(self):
        return {
            "name": "system_control",
            "description": "Get system information like time, date, and performance.",
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": ["get_time", "get_date", "get_stats"]
                    }
                },
                "required": ["action"]
            }
        }
