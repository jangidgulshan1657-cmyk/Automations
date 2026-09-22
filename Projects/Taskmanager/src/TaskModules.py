import json
from pathlib import Path
import WeatherModules

FILE_PATH = Path('Projects/Taskmanager/data/tasks.json')

tasks = []

# printing Help
def print_help():
    print("\n---Always Start with Command!!---")
    print("1. Add task")
    print("2. Mark task done")
    print("3. View list of task")
    print("4. Deleting the task.")
    print("5. for Help/Instructions.")
    print("6. Quit the program.")
    print("7. Enter City Name to get The Weather Cast")
    print("8. Check Tasks That they are risky or not!!")


#loadign the json File or Create if it doesn not Exist
def loading(tasks):
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
        except json.JSONDecodeError:
            print("File has been Currupted!!")
            return []
        except UnicodeDecodeError:
            print("Invalid File")
            return []

# Writing to json
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

def outdoor_detection(tasks):
    outdoor_keywords = ["mow", "garden", "weed", "leaves", "drive", "walk",
    "bike", "park", "store", "groceries", "car", "wash", "paint", "roof","running"]

    outdoor_tasks = []

    for task in tasks:
        task_name = task['name'].lower()
        for keyword in outdoor_keywords:
            if keyword in task_name:
                outdoor_tasks.append(task)
                break

    return outdoor_tasks


# Defining Wheather the Task of outdoor is Risky or not!!
def risk_check(tasks,city):

    url = WeatherModules.safe_url(city)

    data = WeatherModules.getting_data(url)

    if data is None:
        print("[Weather unavailable - risk not checked]")
        print("Printing Normal List")
        view_list(tasks)
        return
    try:
        #gettting the Data form chunk
        temperature = int(data["current_condition"][0]["temp_C"])
        weather_condition = data["current_condition"][0]["weatherDesc"][0]["value"]

        #Checking the Conditions
        temperature_check = (temperature > 35 or temperature < 0)
        condition_check = weather_condition in ["Rain", "Thunder", "Snow"]
        is_risky =  temperature_check or condition_check

        print(f"\n--- Weather Report for {city.title()} ---")
        print(f"Condition: {weather_condition}, Temperature: {temperature}°C")

        if temperature_check:
            print(f"\nAdvisory: Doing Tasks is Risky Due to Extreme Temperature {temperature}C")
        elif condition_check:
            print(f"\nAdvisory: Unfavorable Weather Detected {weather_condition}C")
        else:
            print("Its is Safe to do Outdoor tasks")

        outdoor_tasks = outdoor_detection(tasks)

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