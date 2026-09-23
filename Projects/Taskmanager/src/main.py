import WeatherModules
import TaskModules
import configmodule

tasks = []
 # main program Loop

def main():
    tasks_local = TaskModules.loading_tasks(tasks)
    config_data = configmodule.loading_conf()

    TaskModules.print_help()
    while True:
            city = input("\nCurrently Which City are You In live In: ").strip()
            if city:
                break
            print("City cannot be Empty!")


    while True:
        try:

            command = int(input("\nMain Command (1-9):").strip())

            if command == 1:
                TaskModules.add_task(tasks_local)
            elif command == 2:
                TaskModules.mark_done(tasks_local)
            elif command == 3:
                TaskModules.view_list(tasks_local)
            elif command == 4:
                TaskModules.delete_task(tasks_local)          
            elif command == 5:
                TaskModules.print_help()          
            elif command == 6:
                TaskModules.writing(tasks_local)
                print("\nChanges Has been Saved. Good bye!")
                break
            elif command == 7:
                WeatherModules.weather_info(city)
            elif command == 8:
                TaskModules.risk_check(tasks_local,city,config_data)
            elif command == 9:
                change_config(config_data)
            else:
                TaskModules.print_help()
                print("\nPlease Enter Valid Command (1-9)")
        
        except ValueError:
            print("\nPlease Enter Valid Number")

def change_config(config_data):

    configmodule.print_help()

    while True:
        try:
            command = int(input("\nSettings Command (1-5):"))

            if command == 1:
                configmodule.add_outdoor(config_data)
            elif command == 2:
                configmodule.add_weather_condition(config_data)
            elif command == 3:
                configmodule.change_temp(config_data)
            elif command == 4:
                configmodule.view_list_config(config_data)
            elif command == 5:
                configmodule.writing_config(config_data)
                print("Changes has been Saved!!")
                break
            else:
                configmodule.print_help()
                print("Please Enter Valid Command (1-5)!!")
        
        except ValueError:
            print("Please Enter Valid Number")


if __name__ == "__main__":
    main()