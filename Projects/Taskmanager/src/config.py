import json
from pathlib import Path

CONFIG_PATH = Path('Projects/Taskmanager/data/config.json')

def print_help(settings_commands):
    print("\n-----Settings Mode-----!!")
    print(f"\n--For Adding Outdoor Keyword: {', '.join(settings_commands['add_outdoor'])}")
    print(f"--For Adding Weather Conditons: {', '.join(settings_commands['add_weather'])}")
    print(f"--Changing temperature Settings: {', '.join(settings_commands['change_temp'])}")
    print(f"--View the list of Keyowords in Settings: {', '.join(settings_commands['view_config'])}")
    print(f"--Save the Changes!! And Return to Menu: {', '.join(settings_commands['back'])}")

def view_list_config(config_data):
    outdoor = config_data["outdoor_keywords"]
    temperature = config_data["temperature_bounds"]
    weather = config_data["weather_conditions"]

    print(f"Outdoor Keywords = {outdoor}")
    print(f"Weather Keywords = {weather}")
    print(f"Extereme Temperature = {temperature}")

def detection(user_input:str,command_map:dict):
    if not user_input:
        return
    for command, aliases in command_map.items():
            if user_input in aliases:
                return command
    

# Checking the validity of Config file
def is_valid_config(data)->bool:
    if not isinstance(data,dict):
        return False

    required_keys = {"outdoor_keywords", "temperature_bounds", "weather_conditions","main_commands","settings_commands"}
    if not required_keys.issubset(data.keys()):
        return False

    if not isinstance(data['outdoor_keywords'],list) or not all(isinstance(k,str) for k in data['outdoor_keywords']):
        return False

    if not isinstance(data["weather_conditions"],list)or not all(isinstance(k,str) for k in data["weather_conditions"]):
        return False
    
    bounds = data['temperature_bounds']
    m_com = data['main_commands']
    s_com = data['settings_commands']

    if not all(isinstance(x,dict) for x in (bounds,m_com,s_com)):
        return False
    
    if 'min' not in bounds or 'max' not in bounds: 
        return False

    if not isinstance(bounds['min'],(int,float)) or not isinstance(bounds['max'],(int,float)):
        return False

    if bounds['min'] > bounds['max']:
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

    return True

def default_file():
    default_data = {
            'outdoor_keywords': ["mow", "garden", "weed", "leaves", "drive", "walk",
                                "bike", "park", "store", "groceries", "car", "wash", 
                                "paint", "roof","running"],
            "temperature_bounds": {"min": 0,"max": 35},

            'weather_conditions':["rain", "thunder", "snow"],

            "main_commands": {
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
                }}
                            
    with open(CONFIG_PATH,'w') as f:
        json.dump(default_data,f,indent=4)
    return default_data

# Loading the conf file
def loading_conf():
    
    if not CONFIG_PATH.exists():
        print("Config File Does not Exist!!\n Creating the file.....")
        data = default_file()
        return data

    else:
        try:
            with open(CONFIG_PATH,'r') as f:
                data = json.load(f)
                if not is_valid_config(data):
                    print("The Data has Been Corupted!! Going With Defalaut File...")
                    data = default_file()
                    return data
            return data

        except (json.JSONDecodeError,UnicodeDecodeError,OSError):
            print("File has been Currupted!! Going With Defalaut File...")
            data = default_file()
            return data           


def writing_config(config_data):
    with open(CONFIG_PATH,'w') as f:
        json.dump(config_data,f,indent=4)


def add_outdoor(config_data):
    outdoor_keywords = config_data["outdoor_keywords"]

    keyword = input("Keyword: ").strip().lower()
    if not keyword:
        print("Keyword Cannot be Empty")
        return
    else:
        for default_keyword in outdoor_keywords:
            if default_keyword == keyword:
                print(f"Keyword '{keyword}' Already Exist")
                return
    outdoor_keywords.append(keyword)
    print(f"Keyword '{keyword}' has been added. Dont forget to Save!!")

def add_weather_condition(config_data):
    weather_keywords = config_data["weather_conditions"]

    keyword = input("Keyword: ").strip().lower()
    if not keyword:
        print("Keyword Cannot be Empty")
        return
    else:
        for default_keyword in weather_keywords:
            if default_keyword == keyword:
                print(f"Keyword '{keyword}' Already Exist")
                return
    weather_keywords.append(keyword)
    print(f"Keyword '{keyword}' has been added. Dont Forgot to change!!")

def change_temp(config_data):
    current_min = config_data["temperature_bounds"]["min"]
    current_max = config_data["temperature_bounds"]["max"]

    while True:
        try:
            raw_min = input("\nMinimum Temp: ")
            current_min = int(raw_min)
            break
        except ValueError:
            print("Please, Enter Valid Number!!")

    while True:
        try:
            raw_max = input("\nMaximum Temp: ")
            current_max = int(raw_max)
            break
        except ValueError:
            print("Please, Enter Valid Number!!")

    if current_min > current_max:
        print(f"Error: Minimum temperature ({current_min}) cannot be higher than maximum ({current_max}). Changes cancelled.")
        return

    config_data["temperature_bounds"]["min"] = current_min
    config_data["temperature_bounds"]["max"] = current_max

    print("Temperature bounds updated. Dont Forget to Save!!")
