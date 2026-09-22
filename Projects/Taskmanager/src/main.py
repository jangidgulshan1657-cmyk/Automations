import WeatherModules
import TaskModules

tasks = []

 # main program Loop

def main():
    tasks_local = TaskModules.loading(tasks)
    TaskModules.print_help()
    while True:
            city = input("\nCurrently Which City are You In live In: ").strip()
            if city:
                break
            print("City cannot be Empty!")


    while True:
        try:

            command = int(input("\nPlease Enter the command (1-8):").strip())

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
                print("Changes Has been Saved. Good bye!")
                break
            elif command == 7:
                WeatherModules.weather_info(city)
            elif command == 8:
                TaskModules.risk_check(tasks_local,city)
            else:
                print("Please Enter Valid Command (1-8)")
        
        except ValueError:
            print("Please Enter Valid Number")

if __name__ == "__main__":
    main()