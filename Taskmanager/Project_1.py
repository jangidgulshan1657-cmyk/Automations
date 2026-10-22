
print("---Comand line task manager--")
print("---Type 'help' for instrucitons")


list_of_tasks = []
tasks_done= []

while True:

    user_input = input("\nCommand:")
    parts = user_input.split(" ",1)
    command = parts[0]

    try:
        if command == 'quit':
            print("Bye!!")
            break

        elif command == 'help':
            print("--Always Start with Command!!--")
            print("'add' command for adding the task")
            print("'done command for marking the task done")
            print("'del' for deleting the task")
            print("'list' commnad for listing the tasks")
            print("'quit' for quiting the program")
            continue
        
        elif command == 'add':
            try:
                task = parts[1].strip()
                if task in list_of_tasks:
                    print(f"{task} is Already Exist")
                    
                else:
                    list_of_tasks.append(task)
                    print(f"Success! {task} has been added!!")
            except IndexError:
                   print("You did not give me enough Arguments!")

        elif command == 'done':
            try:
                task = parts[1].strip()         
                if task in list_of_tasks:
                    tasks_done.append(task)
                    print(f"Success! the {task} has been added to done list")
                else:
                    print("Task does not exist")

            except IndexError:
                   print("You did not give me enough Arguments!")

        elif command == 'list':
            not_done_task = []
            for task_item in list_of_tasks:
                if task_item not in tasks_done:
                    not_done_task.append(task_item)

            print(f"{list_of_tasks} is the list of tasks.")
            print(f"{tasks_done} is the tasks done.")
            print(f"{not_done_task} is the list of not done tasks.")
        
        elif command == 'del':
            try:
                task = parts[1].strip()
                if task in list_of_tasks:
                    list_of_tasks.remove(task)
                    print(f"{task} has been removed")                
                elif task in tasks_done:
                    tasks_done.remove(task)
                    print(f"Done {task} has been removed")
                else:
                    print("Task does not Exist!")
            except IndexError:
                print("You did not give me enough Arguments!")
        else:
            print("Please Type valid Command!!")   


    except IndexError:
        print("you didn't give me enough arguments")
    except Exception as e:
        print(f"something went wrong: {e}")
        