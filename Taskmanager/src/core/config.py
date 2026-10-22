import json
from pathlib import Path
from parent.parent import JsonStore


class Config(JsonStore):

    # Default file of configiration
    def default(self)-> dict:
        default_data = {
                'outdoor_keywords': ["mow", "garden", "weed", "leaves", "drive", "walk",
                                    "bike", "park", "store", "groceries", "car", "wash", 
                                    "paint", "roof","running"],
                "temperature_bounds": {"min": 0,"max": 35},

                'weather_conditions':["rain", "thunder", "snow"],
                }
        return default_data
                            
    # Checking the validity of Config file
    def is_valid(self,data:dict)->bool:
        if not isinstance(data,dict):
            return False

        required_keys = {"outdoor_keywords", "temperature_bounds", "weather_conditions",}
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

    # View the List of Configs
    def view_list_config(self)-> None:
        print(f"Outdoor Keywords = {self.data["outdoor_keywords"]}")
        print(f"Weather Keywords = {self.data["weather_conditions"]}")
        print(f"Extereme Temperature = {self.data["temperature_bounds"]}")


    # LOGICS
    # Single responsibility. Don't mix logic, input, and printing.
    def add_keyword(self, key: str, keyword: str) -> bool:
        keyword = keyword.strip().lower()
        if not keyword or keyword in self.data[key]:
            return False
        self.data[key].append(keyword)
        return True

    # Change Temp Logic
    def change_check(self, raw_max: str, raw_min: str) -> bool:
        try:
            current_min = int(raw_min)
            current_max = int(raw_max)
        except ValueError:
            print("Please enter valid numbers!!")
            return False
        if current_min > current_max:
            return False
        self.data["temperature_bounds"]["min"] = current_min
        self.data["temperature_bounds"]["max"] = current_max
        return True
        
    # UI
    # Outdoor ADD
    def add_outdoor(self)-> None:
        keyword = input("Keyword: ").strip().lower()
        if not self.add_keyword("outdoor_keywords",keyword):
            print("Error: Keyword Is empty or Already Exist!")
            return
        print(f"Keyword '{keyword}' has been added. Dont forget to Save!!")


    # Weathe Condition ADD
    def add_weather_condition(self)-> None:
        keyword = input("Keyword: ").strip().lower()
        if self.add_keyword("weather_conditions",keyword):
            print(f"Keyword '{keyword}' has been added. Dont Forgot to change!!")
            return
        print("Error: Keyword Is empty or Already Exist!")

    # Change Temp
    def change_temp(self)-> None:
        current_min = self.data["temperature_bounds"]["min"]
        current_max = self.data["temperature_bounds"]["max"]

        while True:
            raw_min = input("\nMinimum Temp: ").strip()
            raw_max = input("\nMaximum Temp: ").strip() 
            if self.change_check(raw_max,raw_min):
                print("Temperature bounds updated. Dont Forget to Save!!")
                return
            print("Error: There is Empty Input or Min Temp > Max temp")
