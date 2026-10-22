import json
from pathlib import Path
from parent.parent import JsonStore


class Command(JsonStore):
      
    # Default File 
    def default(self)-> dict:
        default_data = {"main_commands": {
                        "add_task": ["add", "add task", "new task"],
                        "mark_done": ["done", "mark", "mark done"],
                        "view_list": ["list", "tasks", "view"],
                        "delete_task": ["delete", "remove", "del"],
                        "help": ["help", "commands", "info"],
                        "weather": ["weather", "forecast", "temp"],
                        "risk_check": ["risk", "check", "risk check"],
                        "settings": ["settings", "config", "options"],
                        "quit": ["quit", "exit", "bye"],
                        "suggestions": ["suggest","suggestion","ai suggestion"],
                        "ai_mode": ["ai mode","ai","ai help"]
                    },
                "settings_commands": {
                        "add_outdoor": ["outdoor", "add outdoor", "outdoor keyword"],
                        "add_weather": ["weather", "add weather", "weather condition"],
                        "change_temp": ["temp", "temperature", "change temp"],
                        "view_config": ["view", "list", "show config"],
                        "back": ["back", "return", "menu","quit", "exit", "close"]
                    }
                    }
        return default_data

    # Checking the full Validation of file:
    def is_valid(self,data)->bool:
        if not isinstance(data, dict):
            return False

        if "main_commands" not in data or "settings_commands" not in data:
            return False

        m_com = data["main_commands"]
        s_com = data["settings_commands"]

        if not isinstance(m_com, dict) or not isinstance(s_com, dict):
            return False

        required_main_keys = {"add_task", "mark_done", "view_list", "delete_task", "help", "weather", "risk_check", "settings", "quit","suggestions","ai_mode"}
        if not required_main_keys.issubset(m_com.keys()):
            return False
        
        if not all(isinstance(k,list) and all(isinstance(word,str) for word in k) for k in m_com.values()):
            return False
        
        required_setting_keys = {"add_outdoor","add_weather","change_temp","view_config","back",}
        if not required_setting_keys.issubset(s_com.keys()):
            return False
        
        if not all(isinstance(s,list) and all(isinstance(word,str) for word in s) for s in s_com.values()):
            return False

        return True

