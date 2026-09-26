from services import weather, task
from services import suggest, ai_command
from core import comd,config

 # main program Loop

def main():
    tasks = task.loading_tasks()
    config_data = config.loading_conf()
    command_data = comd.loading_command()
    main_keyword = command_data["main_commands"]

    task.print_help(main_keyword)
    while True:
            city = input("\nCurrently Which City You live In: ").strip()
            if city:
                break
            print("City cannot be Empty!")


    while True:
            user_input = input("\nMain Command:").strip().lower()
            command = comd.detection(user_input,main_keyword)

            if command == "add_task":
                task.add_task(tasks)
            elif command =="mark_done":
                task.mark_done(tasks)
            elif command == "view_list":
                task.view_list(tasks)
            elif command == "delete_task":
                task.delete_task(tasks)          
            elif command == "help":
                task.print_help(main_keyword)          
            elif command == "quit":
                task.writing(tasks)
                print("\nChanges Has been Saved. Good bye!")
                break
            elif command == "weather":
                weather.weather_info(city)
            elif command == "risk_check":
                task.risk_check(tasks,city,config_data)
            elif command == "settings":
                change_config(config_data,command_data)
            elif command == "suggestions":
                suggest.suggestions(tasks)
            elif command == "ai_mode":
                ai_command.ai_mode(tasks, city, config_data)
            else:
                print("\nError: Command Not Found Error!! Type 'help' for More Info")



def change_config(config_data:dict,command_data:dict)-> None:

    settings_commands = command_data["settings_commands"]
    config.print_help(settings_commands)

    while True:
            user_input = input("\nSettings Command: ").strip().lower()
            command = comd.detection(user_input,settings_commands)

            if command == "add_outdoor":
                config.add_outdoor(config_data)
            elif command == "add_weather":
                config.add_weather_condition(config_data)
            elif command == "change_temp":
                config.change_temp(config_data)
            elif command == "view_config":
                config.view_list_config(config_data)
            elif command == "back":
                config.writing_config(config_data)
                print("Changes has been Updated and Saved!!")
                print(" Returning to Menu.....")
                break
            else:
                config.print_help(settings_commands)
                print("Please Enter Valid Command!!")


if __name__ == "__main__":
    main()