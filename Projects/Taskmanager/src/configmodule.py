import json
from pathlib import Path

CONFIG_PATH = Path('Projects/Taskmanager/data/config.json')

def print_help():
    print("\nPlease, Enter a Command to Procced(1-6)!!")
    print("\n1. For Adding Outdoor Keyword.")
    print("2. For Adding Weather Conditons")
    print("3. Changing temperature Settings.")
    print("4. View the list of Keyowords in Settings.")
    print("5. Return to Menu With Saved Changes!!.")

def view_list_config(config_data):
    outdoor = config_data["outdoor_keywords"]
    temperature = config_data["temperature_bounds"]
    weather = config_data["weather_conditions"]

    print(f"Outdoor Keywords = {outdoor}")
    print(f"Weather Keywords = {weather}")
    print(f"Extereme Temperature = {temperature}")


# Checking the validity of Config file
def is_valid_config(data)->bool:
    if not isinstance(data,dict):
        return False

    required_keys = {"outdoor_keywords", "temperature_bounds", "weather_conditions"}
    if not required_keys.issubset(data.keys()):#checking the required keys in dictionary
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

def default_file():
    default_data = {
            'outdoor_keywords': ["mow", "garden", "weed", "leaves", "drive", "walk",
            "bike", "park", "store", "groceries", "car", "wash", "paint", "roof","running"],
            "temperature_bounds": {"min": 0,"max": 35},
            'weather_conditions':["rain", "thunder", "snow"]
            }
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
    writing_config(config_data)
    print(f"Keyword '{keyword}' has been added Succcessfully")

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
    writing_config(config_data)
    print(f"Keyword '{keyword}' has been added Succcessfully")

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

    writing_config(config_data)
    print("Temperature bounds updated and saved successfully!")
