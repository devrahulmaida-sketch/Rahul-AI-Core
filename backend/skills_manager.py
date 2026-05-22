import os
import importlib
import inspect
import json
import logging
from typing import List, Dict, Any

logger = logging.getLogger("SkillsManager")

class SkillsManager:
    def __init__(self, skills_dir: str = "backend/skills"):
        self.skills_dir = skills_dir
        self.skills = {}
        self.load_skills()

    def load_skills(self):
        """Dynamically load all skills from the skills directory"""
        if not os.path.exists(self.skills_dir):
            os.makedirs(self.skills_dir)
            return

        for filename in os.listdir(self.skills_dir):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = f"skills.{filename[:-3]}"
                try:
                    # Fix import path for dynamic loading
                    spec = importlib.util.spec_from_file_location(module_name, os.path.join(self.skills_dir, filename))
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    # Find classes that inherit from 'BaseSkill' (to be implemented) or have 'execute' method
                    for name, obj in inspect.getmembers(module):
                        if inspect.isclass(obj) and hasattr(obj, "execute") and name != "BaseSkill":
                            skill_instance = obj()
                            skill_name = getattr(skill_instance, "name", name.lower())
                            self.skills[skill_name] = skill_instance
                            logger.info(f"Loaded skill: {skill_name}")
                except Exception as e:
                    logger.error(f"Failed to load skill {filename}: {e}")

    async def run_skill(self, skill_name: str, **kwargs) -> Any:
        if skill_name in self.skills:
            return await self.skills[skill_name].execute(**kwargs)
        return f"Skill '{skill_name}' not found."

    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        """Return tool definitions for LLM function calling"""
        tools = []
        for name, skill in self.skills.items():
            if hasattr(skill, "get_definition"):
                tools.append(skill.get_definition())
        return tools

# Global instance
skills_manager = SkillsManager()
