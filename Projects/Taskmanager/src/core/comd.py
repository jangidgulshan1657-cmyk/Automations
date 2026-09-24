import json
from pathlib import Path

COMMAND_PATH = Path('Projects/Taskmanager/data/command.json')


# Iteration and Checking of user Command
def detection(user_input:str,command_map:dict):
    if not user_input:
        return
    for command, aliases in command_map.items():
            if user_input in aliases:
                return command


# Default File 
def default_file_command()-> dict:
    default_data = {"main_commands": {
                    "add_task": ["add", "add task", "new task"],
                    "mark_done": ["done", "mark", "mark done"],
                    "view_list": ["list", "tasks", "view"],
                    "delete_task": ["delete", "remove", "del"],
                    "help": ["help", "commands", "info"],
                    "weather": ["weather", "forecast", "temp"],
                    "risk_check": ["risk", "check", "risk check"],
                    "settings": ["settings", "config", "options"],
                    "quit": ["quit", "exit", "bye"]
                },
            "settings_commands": {
                    "add_outdoor": ["outdoor", "add outdoor", "outdoor keyword"],
                    "add_weather": ["weather", "add weather", "weather condition"],
                    "change_temp": ["temp", "temperature", "change temp"],
                    "view_config": ["view", "list", "show config"],
                    "back": ["back", "return", "menu","quit", "exit", "close"]
                }
                }
    with open(COMMAND_PATH,'w') as f:
        json.dump(default_data,f,indent=4)
    return default_data

# Checking the full Validation of file:
def is_valid_command(data)->bool:
    m_com = data['main_commands']
    s_com = data['settings_commands']

    if not all(isinstance(v,dict) for v in (m_com,s_com)):
        return False

    required_main_keys = {"add_task", "mark_done", "view_list", "delete_task", "help", "weather", "risk_check", "settings", "quit"}
    if not required_main_keys.issubset(m_com.keys()):
        return False
    
    if not all(isinstance(k,list) and all(isinstance(word,str) for word in k) for k in m_com.values()):
        return False
    
    required_setting_keys = {"add_outdoor","add_weather","change_temp","view_config","back",}
    if not required_setting_keys.issubset(s_com.keys()):
        return False
    
    if not all(isinstance(s,list) and all(isinstance(word,str) for word in s) for s in s_com.values()):
        return False


# Loading the Commands
def loading_command()-> dict:    
    if not COMMAND_PATH.exists():
        print("Command File Does not Exist!!\n Creating the file.....")
        data = default_file_command()
        return data

    else:
        try:
            with open(COMMAND_PATH,'r') as f:
                data = json.load(f)
                if not is_valid_command(data):
                    print("The Data has Been Corupted!! Going With Defalaut File...")
                    data = default_file_command()
                    return data
            return data

        except (json.JSONDecodeError,UnicodeDecodeError,OSError):
            print("File has been Currupted!! Going With Defalaut File...")
            data = default_file_command()
            return data   