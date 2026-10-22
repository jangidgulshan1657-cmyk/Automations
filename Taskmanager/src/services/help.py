class Help:
    def __init__(self,data):
        self.data = data
        self.main_commands = data["main_commands"]
        self.settings_commands = data["settings_commands"]

    def print_help_main(self)-> None:
        print("\n------Smart Task Manger -----")
        print("\nFollowing Are the Commands of Each function!! ")
        print(f"\n--To Add task: {', '.join(self.main_commands['add_task'])}")
        print(f"--To Mark task done: {', '.join(self.main_commands['mark_done'])}")
        print(f"--To View list of task: {', '.join(self.main_commands['view_list'])}")
        print(f"--For Deleting the task: {', '.join(self.main_commands['delete_task'])}")
        print(f"--For Help/Instructions: {', '.join(self.main_commands['help'])}")
        print(f"--To Quit the program: {', '.join(self.main_commands['quit'])}")
        print(f"--To Get The Weather Information: {', '.join(self.main_commands['weather'])}")
        print(f"--To Check Tasks That they are risky or not!: {', '.join(self.main_commands['risk_check'])}")
        print(f"--For Settings Mode!!: {', '.join(self.main_commands['settings'])}")
        print(f"--Get AI Task Suggestions: {', '.join(self.main_commands['suggestions'])}")
        print(f"--To get in AI mode! {', '.join(self.main_commands['ai_mode'])} ")

    def print_help_config(self)-> None:
        print("\n-----Settings Mode-----!!")
        print(f"\n--For Adding Outdoor Keyword: {', '.join(self.settings_commands['add_outdoor'])}")
        print(f"--For Adding Weather Conditons: {', '.join(self.settings_commands['add_weather'])}")
        print(f"--Changing temperature Settings: {', '.join(self.settings_commands['change_temp'])}")
        print(f"--View the list of Keyowords in Settings: {', '.join(self.settings_commands['view_config'])}")
        print(f"--Save the Changes!! And Return to Menu: {', '.join(self.settings_commands['back'])}")

    def detect_command(self,user_input:str,command_set:dict)->str| None:
        if not user_input:
            return None
        for command, aliases in command_set.items():
            if user_input in aliases:
                return command
        return None