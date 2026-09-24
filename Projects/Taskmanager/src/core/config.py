import json
from pathlib import Path

CONFIG_PATH = Path('Projects/Taskmanager/data/config.json')

def print_help(settings_commands:dict)-> None:
    print("\n-----Settings Mode-----!!")
    print(f"\n--For Adding Outdoor Keyword: {', '.join(settings_commands['add_outdoor'])}")
    print(f"--For Adding Weather Conditons: {', '.join(settings_commands['add_weather'])}")
    print(f"--Changing temperature Settings: {', '.join(settings_commands['change_temp'])}")
    print(f"--View the list of Keyowords in Settings: {', '.join(settings_commands['view_config'])}")
    print(f"--Save the Changes!! And Return to Menu: {', '.join(settings_commands['back'])}")


# View the List of Configs
def view_list_config(config_data:dict)-> None:
    outdoor = config_data["outdoor_keywords"]
    temperature = config_data["temperature_bounds"]
    weather = config_data["weather_conditions"]

    print(f"Outdoor Keywords = {outdoor}")
    print(f"Weather Keywords = {weather}")
    print(f"Extereme Temperature = {temperature}")
    

# Checking the validity of Config file
def is_valid_config(data:dict)->bool:
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

    if not isinstance(bounds,dict):
        return False
    
    if 'min' not in bounds or 'max' not in bounds: 
        return False

    if not isinstance(bounds['min'],(int,float)) or not isinstance(bounds['max'],(int,float)):
        return False

    if bounds['min'] > bounds['max']:
        return False

    return True


# Default file of configiration
def default_file_config()-> dict:
    default_data = {
            'outdoor_keywords': ["mow", "garden", "weed", "leaves", "drive", "walk",
                                "bike", "park", "store", "groceries", "car", "wash", 
                                "paint", "roof","running"],
            "temperature_bounds": {"min": 0,"max": 35},

            'weather_conditions':["rain", "thunder", "snow"],
            }
                            
    with open(CONFIG_PATH,'w') as f:
        json.dump(default_data,f,indent=4)
    return default_data


# Loading the conf file
def loading_conf()-> dict:
    
    if not CONFIG_PATH.exists():
        print("Config File Does not Exist!!\n Creating the file.....")
        data = default_file_config()
        return data

    else:
        try:
            with open(CONFIG_PATH,'r',encoding="utf-8") as f:
                data = json.load(f)
                if not is_valid_config(data):
                    print("The Data has Been Corupted!! Going With Defalaut File...")
                    data = default_file_config()
                    return data
            return data

        except (json.JSONDecodeError,UnicodeDecodeError,OSError):
            print("File has been Currupted!! Going With Defalaut File...")
            data = default_file_config()
            return data           


# Writing to Config File
def writing_config(config_data:dict)-> None:
    with open(CONFIG_PATH,'w') as f:
        json.dump(config_data,f,indent=4)


# Some ADD fuctions
def add_outdoor(config_data:dict)-> None:
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

def add_weather_condition(config_data:dict)-> None:
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

def change_temp(config_data:dict)-> None:
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
