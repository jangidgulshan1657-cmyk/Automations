import json
from pathlib import Path
from . import weather
from .weather import Weather
from core import comd,config
from parent.parent import JsonStore

class TaskManager(JsonStore):

    def default(self)->list:
        return []

    def is_valid(self,data:list)-> bool:
        if not isinstance(data,list) or not all(isinstance(t,dict) and "name" in t and "done" in t for t in data):
            return False
        return True
    # Organizing the List of Task
    def view_list(self)-> None:
        # if the task dones not exist dont go further!
        if not self.data:
            print("\nTasks not available!!")
            return
        
        print("\n----Your Tasks!----\n")

        for index, task in enumerate(self.data,start =1):
            status = "[X]" if task["done"] else "[]"
            print(f"{status} {index} {task['name']}")

    def name_check(self,name:str)-> bool:
        if not name:
            return False
        for task in self.data:
            if task['name'] == name:
                return False
        self.data.append({"name":name,"done": False})
        self.save()
        return True

    # ADDing the Task function
    def add_task(self)-> None:
        while True:
            name = input("\nEnter Task Name:").strip().title()
            if self.name_check(name):
                print(f"Success the {name} has been added to task list")
                return
            else:
                print("Error: Task is Empty or Already ExistS!!")

    def add_task_ai(self,name:str)-> None:
        if self.name_check(name):
            print(f"Success the {name} has been added to task list")
            return None
        else:
            print("Error: Task is Empty or Already ExistS!!")
            return None

    # Marking the Task done
    def mark_done(self)-> None:
        self.view_list()
        while True:
            try:
                number = int(input("\nGive me Number of task to Mark done:").strip())
                index = number - 1 # making 1 based index no
                if 0 <= index <len(self.data):
                    self.data[index]["done"] = True
                    self.save()
                    print(f"Maked the {self.data[index]['name']} as done")
                    return
                else:
                    print(f"Invalid Task Number {number}")
            except ValueError:
                print("Please enter a valid number")
                
    def mark_done_ai(self,number:int)-> None:
        index = number - 1 # making 1 based index no
        if 0 <= index <len(self.data):
            self.data[index]["done"] = True
            self.save()
            print(f"Maked the {self.data[index]['name']} as done")
            return None
        else:
            print(f"Invalid Task Number {number}")
            return None


    # Deleting the Task
    def delete_task(self)-> None:
        self.view_list()
        while True:
            try:
                number = int(input("Enter the Task Number To Delete:").strip())
                index = number - 1 # 0 based indexing

                if 0 <= index < len(self.data):
                    removed_task = self.data.pop(index)
                    self.save()
                    print(f"'{removed_task['name']}' successfully deleted!")
                    return None
                else:
                    print(f"Invalid Task Number {number}")

            except ValueError:
                print("Please enter a valid number")
    
    
    def delete_task_ai(self,number:int)-> None:
        index = number - 1 # 0 based indexing

        if 0 <= index < len(self.data):
            removed_task = self.data.pop(index)
            self.save()
            print(f"'{removed_task['name']}' successfully deleted!")
            return None
        else:
            print(f"Invalid Task Number {number}")
            return None


class OutdoorManager(TaskManager):
    def __init__(self,file_path,config_data,weather_data):
        super().__init__(file_path)
        self.config_data = config_data
        self.weather_keywords = self.config_data["weather_conditions"]
        self.outdoor_keywords = self.config_data["outdoor_keywords"]
        self.weather_data = weather_data

    def is_outdoor(self, task) -> bool:
        name = task['name'].lower()
        return any(keyword in name for keyword in self.outdoor_keywords)

    def outdoor_detection(self) -> None:
        if not any(self.is_outdoor(task) for task in self.data):
            print("\nThere is no outdoor tasks!!")
            return

        risky = self.weather_risky()  # call once, not once per task

        print("\n---Task Evaluation !!--- ")

        for index, task in enumerate(self.data, start=1):
            status = "[X]" if task["done"] else "[ ]"

            if not self.is_outdoor(task):
                tag = "[Indoor]"
            elif risky:
                tag = "[Risky: Outdoor]"
            else:
                tag = "[Safe: Outdoor]"

            print(f"{index} {status} {task['name']} {tag}")

       
    def weather_risky(self)-> bool|None:
        if not self.temp_wth_list():
            return None

        temp_wth = self.temp_wth_list()
        temperature = temp_wth[0]
        weather_condition = temp_wth[1]

        min_tem = self.config_data["temperature_bounds"]["min"]
        max_tem = self.config_data["temperature_bounds"]["max"]

        temperature_check = (temperature > max_tem or temperature < min_tem)

        cond_lower = weather_condition.lower()
        condition_check = any(k.lower() in cond_lower for k in self.weather_keywords)

        is_risky =  temperature_check or condition_check
        if is_risky:
            return True
        return False

    def temp_wth_list(self):
        if not self.weather_data:
            return None
        try:
            temperature = int(self.weather_data["current_condition"][0]["temp_C"])
            weather_condition = self.weather_data["current_condition"][0]["weatherDesc"][0]["value"]
            return [temperature,weather_condition]
        except (ValueError):
            return None

    # Defining Wheather the Task of outdoor is Risky or not!!
    def risk_check(self)-> None:
        if not (temp_wth:= self.temp_wth_list()):
            print("Weather Error!!!")
            return None

        temperature,weather_condition = temp_wth  

        if self.weather_risky():
            print(f"\n--- Weather Report for ---")
            print(f"\nAdvisory: Doing Outdoor Tasks is Risky")
            print(f"Condition: {weather_condition}, Temperature: {temperature}°C")
            self.outdoor_detection()

        else:
            print("Its is Safe to do Outdoor tasks")
            self.outdoor_detection()
