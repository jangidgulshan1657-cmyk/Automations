from services import weather, task
from services.task import OutdoorManager
from services import suggest, ai_command
from core import comd
from core.config import Config
from core.comd import Command
from pathlib import Path
from services.help import Help


 # main program Loop
FILE_PATH = 'Projects/Taskmanager/data/tasks.json'
COMMAND_PATH = 'Projects/Taskmanager/data/command.json'
CONFIG_PATH = 'Projects/Taskmanager/data/config.json'


def main():
    CommandCl = Command(COMMAND_PATH)
    command_data = CommandCl.data

    hlp = Help(command_data)
    hlp.print_help_main()

    print("\n----[Weather: Please Enter Which City Are you in!!]----")
    url = weather.get_city()
    wth = weather.Weather(url)
    weather_data = wth.data

    configs = Config(CONFIG_PATH)
    config_data = configs.data

    TaskCl = OutdoorManager(FILE_PATH,config_data,weather_data)
    tasks = TaskCl.data



    while True:
            user_input = input("\nMain Command:").strip().lower()
            command = hlp.detect_command(user_input)

            if command == "add_task":
                TaskCl.add_task()
            elif command =="mark_done":
                TaskCl.mark_done()
            elif command == "view_list":
                TaskCl.view_list()
            elif command == "delete_task":
                TaskCl.delete_task()          
            elif command == "help":
                hlp.print_help_main(main_keyword)          
            elif command == "quit":
                TaskCl.writing()
                print("\nChanges Has been Saved. Good bye!")
                break
            elif command == "weather":
                wth.weather_info()
            elif command == "risk_check":
                TaskCl.risk_check(wth)
            elif command == "settings":
                configs.change_config(command_data)
            elif command == "suggestions":
                suggest.suggestions(tasks)
            elif command == "ai_mode":
                ai_command.ai_mode(tasks)
            else:
                print("\nError: Command Not Found Error!! Type 'help' for More Info")

def change_config(command_data:dict)-> None:
    hlp.print_help_config()

    while True:
            user_input = input("\nSettings Command: ").strip().lower()
            command = hlp.detect_command(user_input)

            if command == "add_outdoor":
                add_outdoor()
            elif command == "add_weather":
                add_weather_condition()
            elif command == "change_temp":
                change_temp()
            elif command == "view_config":
                view_list_config()
            elif command == "back":
                writing_config()
                print("Changes has been Updated and Saved!!")
                print(" Returning to Menu.....")
                break
            else:
                hlp.print_help_config()
                print("Error: Command Not Found Error!!")


if __name__ == "__main__":
    main()