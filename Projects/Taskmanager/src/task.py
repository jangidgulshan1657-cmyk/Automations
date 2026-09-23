import json
from pathlib import Path
import weather

FILE_PATH = Path('Projects/Taskmanager/data/tasks.json')

tasks = []

# printing Help
def print_help(main_commands):
    print("\n------Smart Task Manger -----")
    print("\nFollowing Are the Commands of Each function!! ")
    print(f"\n--To Add task: {', '.join(main_commands['add_task'])}")
    print(f"--To Mark task done: {', '.join(main_commands['mark_done'])}")
    print(f"--To View list of task: {', '.join(main_commands['view_list'])}")
    print(f"--For Deleting the task: {', '.join(main_commands['delete_task'])}")
    print(f"--For Help/Instructions: {', '.join(main_commands['help'])}")
    print(f"--To Quit the program: {', '.join(main_commands['quit'])}")
    print(f"--To Get The Weather Information: {', '.join(main_commands['weather'])}")
    print(f"--To Check Tasks That they are risky or not!: {', '.join(main_commands['risk_check'])}")
    print(f"--For Settings Mode!!: {', '.join(main_commands['settings'])}")


#loadign the json File or Create if it doesn not Exist
def loading_tasks(tasks):
    if not FILE_PATH.exists():
        print("File does not exist! \nCreating the File...")
        default_data = []
        with open(FILE_PATH ,'w') as f:
            json.dump(default_data,f,indent=4)
        return default_data
    
    else:
        try:
            with open(FILE_PATH,'r') as f:
                data = json.load(f)
            if not isinstance(data,list) or not all(isinstance(t,dict) and "name" in t and "done" in t for t in data):
                print("File Structure is not Supported!!")
                return []
            print("Previous File has been loaded successfully!")
            return data
        except (json.JSONDecodeError,UnicodeDecodeError):
            print("Invalid File")
            return []

# Writing to json Tasks
def writing(tasks):
    with open(FILE_PATH,'w') as f:
        json.dump(tasks,f,indent=4)


# ADDing the Task function
def add_task(tasks):
    name = input("\nEnter Task Name:").strip().title()

    if not name:
        print("Task Name Cannot be Empty.")
        return

    for task in tasks:
        if task['name'] == name:
            print(f"This '{name}' task already exist!")
            return

    tasks.append({"name":name,"done": False})
    writing(tasks)
    print(f"Success the {name} has been added to task list")


# Organizing the List of Task
def view_list(tasks):
    # if the task dones not exist dont go further!
    if not tasks:
        print("\nTasks not available!!")
        return
    
    print("\n----Your Tasks!----\n")

    for index, task in enumerate(tasks,start =1):
        status = "[X]" if task["done"] else "[]"
        print(f"{status} {index} {task['name']}")


# Marking the Task done
def mark_done(tasks):
    view_list(tasks)
    if not tasks:#checking agian Whe the task exist or not 
        print("No Tasks to mark done. Please add a task First!!")
        return

    try:
        number = int(input("\nGive me Number of task to Mark done:").strip())
        index = number - 1 # making the index 0 based as we will use the len fucntion to get which task to mark done

        if 0 <= index <len(tasks):
            tasks[index]["done"] = True # getting the index for specifing which task to mark as done
            writing(tasks)
            print(f"Maked the {tasks[index]['name']} as done")
        else:
            print(f"Invalid Task Number {number}")

    except ValueError:
        print("Please enter a valid number")

# Deleting the Task
def delete_task(tasks):
    #Using the same design as mark done
    view_list(tasks)
    if not tasks:
        print("Nothing to Delete. Please Add a task first!!")
        return
    
    try:
        number = int(input("Enter the Task Number To Delete:").strip())
        index = number - 1 # 0 based indexing

        if 0 <= index < len(tasks):
            removed_task = tasks.pop(index)
            writing(tasks)
            print(f"'{removed_task['name']}' successfully deleted!")
        
        else:
            print(f"Invalid Task Number {number}")

    except ValueError:
        print("Please enter a valid number")

def outdoor_detection(tasks,config_data):
    outdoor_keywords = config_data["outdoor_keywords"]

    outdoor_tasks = []

    for task in tasks:
        task_name = task['name'].lower()
        for keyword in outdoor_keywords:
            if keyword in task_name:
                outdoor_tasks.append(task)
                break

    return outdoor_tasks


# Defining Wheather the Task of outdoor is Risky or not!!
def risk_check(tasks,city,config_data):

    url = weather.safe_url(city)

    weather_data = weather.getting_data(url)

    if weather_data is None:
        print("[Weather unavailable - risk not checked]")
        print("Printing Normal List")
        view_list(tasks)
        return
    try:
        #gettting the Data form chunk
        temperature = int(weather_data["current_condition"][0]["temp_C"])
        weather_condition = weather_data["current_condition"][0]["weatherDesc"][0]["value"]

        #Checking the Temperature Conditions
        min_tem = config_data["temperature_bounds"]["min"]
        max_tem = config_data["temperature_bounds"]["max"]

        temperature_check = (temperature > max_tem or temperature < min_tem)

        #Checking the Weather condition
        weather_keywords = config_data["weather_conditions"]
        cond_lower = weather_condition.lower()
        condition_check = any(k.lower() in cond_lower for k in weather_keywords)

        is_risky =  temperature_check or condition_check

        print(f"\n--- Weather Report for {city.title()} ---")
        print(f"Condition: {weather_condition}, Temperature: {temperature}°C")

        if temperature_check:
            print(f"\nAdvisory: Doing Tasks is Risky Due to Extreme Temperature {temperature}C")
        elif condition_check:
            print(f"\nAdvisory: Unfavorable Weather Detected {weather_condition}C")
        else:
            print("Its is Safe to do Outdoor tasks")

        outdoor_tasks = outdoor_detection(tasks, config_data)

        if not outdoor_tasks:
            print("\nThere is no outdoor tasks!!")

        print("\n---Task Evalution !!--- ")

        for index, task in enumerate(tasks,start =1):
            status = "[X]" if task["done"] else "[]"
            is_outdoor = task in outdoor_tasks

            if is_outdoor and is_risky:
                tag = "[Risky: Outdoor]"
            elif is_outdoor:
                tag = "[Safe: Outdoor]"
            else:
                tag = "[Indoor]"

            print(f"{index} {status}{task['name']} {tag} ")

    except (KeyError,IndexError):
        print("Error In Weather Data. Parsing Simple List")
        view_list(tasks)