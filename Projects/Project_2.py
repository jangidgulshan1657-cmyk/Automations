import json
from pathlib import Path

FILE_PATH = Path('tasks.json')


def loading():
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


tasks = loading()

def writing():
    with open(FILE_PATH,'w') as f:
        json.dump(tasks,f,indent=4)

def print_help():
    print("\n---Always Start with Command!!---")
    print("1. Add task")
    print("2. Mark task done")
    print("3. View list of task")
    print("4. Deleting the task.")
    print("5. for Help/Instructions.")
    print("6. Quit the program.")

# defining the add task fucntion!

def add_task():
    # getting the input form the user
    name = input("\nEnter Task Name:").strip().title()
    if not name:
        print("Task name Cannot be Empty.")
        return

    for task in tasks:
        if task['name'] == name:
            print(f"This '{name}' task already exist!")
            return

    tasks.append({"name":name,"done": False})
    writing()
    print(f"Success the {name} has been added to task list")
        
# firstly defining the view list to get the structure!

def view_list():
    # if the task dones not exist dont go further!
    if not tasks:
        print("\nTasks not available!!")
        return
    
    print("\n----Your Tasks!----")
    print("[] is not done task")
    print("[X] is the Done Task!\n")


    for index, task in enumerate(tasks,start =1):
        status = "[X]" if task["done"] else "[]"
        print(f"{status} {index} {task['name']}")

def mark_done():
    view_list()
    if not tasks:#checking agian Whe the task exist or not 
        print("No Tasks to mark done. Please add a task First!!")
        return

    try:
        number = int(input("Give me Number of task to Mark done:").strip())
        index = number - 1 # making the index 0 based as we will use the len fucntion to get which task to mark done

        if 0 <= index <len(tasks):
            tasks[index]["done"] = True # getting the index for specifing which task to mark as done
            writing()
            print(f"Maked the {tasks[index]['name']} as done")
        else:
            print(f"Invalid Task Number {number}")

    except ValueError:
        print("Please enter a valid number")

def delete_task():
    #Using the same design as mark done
    view_list()
    if not tasks:
        print("Nothing to Delete. Please Add a task first!!")
        return
    
    try:
        number = int(input("Enter the Task Number To Delete:").strip())
        index = number - 1 # 0 based indexing

        if 0 <= index < len(tasks):
            removed_task = tasks.pop(index)
            writing()
            print(f"'{removed_task['name']}' successfully deleted!")
        
        else:
            print(f"Invalid Task Number {number}")

    except ValueError:
        print("Please enter a valid number")

 # main program Loop

def main():
    print_help()

    while True:
        try:
            command = int(input("\nEnter the Number command to Start:").strip())

            if command == 1:
                add_task()
            elif command == 2:
                mark_done()
            elif command == 3:
                view_list()
            elif command == 4:
                delete_task()          
            elif command == 5:
                print_help()          
            elif command == 6:
                writing()
                print("Changes Has been Saved. Good bye!")
                break
            else:
                print("Please Enter Valid Command")
        
        except ValueError:
            print("Please Enter Valid Number")

if __name__ == "__main__":
    main()