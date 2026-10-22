import json
import urllib.request
import urllib.error
from pathlib import Path
from services.task import OutdoorManager
from services.weather import Weather

class GROQClient:
    def __init__(self,API_PATH:str):
        self.API_PATH = Path(API_PATH)
        self.var_name = "GROQ_API_KEY"
        self.url = "https://api.groq.com/openai/v1/chat/completions"
        self.api_key = self.get_key()    


    def get_key(self)-> str | None:
        if not self.API_PATH.exists():
            print("\nError: Environment variable File does not exist! or put it on wrong folder!!")
            print("\nPlease make sure its in Right Folder (Taskmananger!)")
            return None

        with open(self.API_PATH,'r',encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    var , key = line.split("=",1)
                    if var.strip() == self.var_name:
                        api = key.strip().strip("'\"")
                        return api

        print("\nError: GROQ_API_KEY key Not Found!! \nPlease ADD the API key in .env file like: GROQ_API_KEY = 'your_key_here'")
        return None


    def post(self, system_prompt: str, user_content: str, temperature: float) -> dict | None:
        if not (key:= self.api_key):
            print("\nPlease Fix the Above: Error!!")
            return None

        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "TaskPlanner/1.0"
            }

        payload = {
                "model": "openai/gpt-oss-120b",
                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": user_content
                    }
                ],
                "temperature": temperature  # Kept low (0.0 or 0.1) for deterministic function selection
            }

        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(self.url,data=data, headers= headers,method= "POST")

        raw_data = self.url_req(req)
        return raw_data        


    def url_req(self,req):
        try:
            with urllib.request.urlopen(req, timeout=25) as reponse:
                raw_bytes = reponse.read()                                #Convering Raw bites
                text_data =  raw_bytes.decode('utf-8')                    #Converting in text format
                data = json.loads(text_data)                              #Conveting the string to json 
                return data
        except urllib.error.HTTPError as e:
            print(f"Server returned an error code: {e.code}")
        except urllib.error.URLError as e:
            print(f"Network failure / No internet: {e.reason}")
        except TimeoutError:
            print(f"Error: Requet Timeour!")
        except json.JSONDecodeError:
            print("The server did not send back Valid Json!!")
        return None

    # in a shared place, or as a free function
    def parse_ai_json(self,raw_data, validator):
        try:
            content_string = raw_data["choices"][0]["message"]["content"]
            content = json.loads(content_string)
            return content if validator(content) else None
        except (IndexError, TypeError, KeyError, json.JSONDecodeError):
            return None

class AI_Mode:
    def __init__(self,TaskCl:OutdoorManager,wth:Weather,client:GROQClient):
        self.client = client
        self.Taskfn = TaskCl
        self.Weatherfn =  wth

    def get_ai_response(self,user_prompt:str,)-> dict|None:

        system_prompt = """
        You are a CLI command dispatcher for a task manager. 
        Your job is to read the user request and map it to exactly one available tool/function.

        Available functions:
        1. add_task(name: str) - Adds a new task.
        2. mark_done(task_number: int) - Marks a task completed by its 1-based index.
        3. delete_task(task_number: int) - Deletes a task by its 1-based index.
        4. view_list() - Shows all tasks.
        5. weather_check() - Checks the weather.
        6. risk_check() - Evaluates outdoor tasks against weather.

        Rules:
        - Output MUST be a valid JSON object ONLY.
        - Format:
        {
            "function": "<function_name>",
            "arguments": { "<arg_name>": <arg_value> }
        }
        - If no arguments are needed, "arguments" must be an empty object: {}
        - If the user's intent matches no function, return:
        {
            "function": "unknown",
            "arguments": { "raw": "<original_user_input>" }
        }
        - Do NOT output explanations, markdown wrappers, or extra text.
        """


        user_content = f"Current tasks: {self.Taskfn.data}\nUser instruction: {user_prompt}"

        temperature = 0.0 
        response = self.client.post(system_prompt,user_content,temperature)

        return response


    def is_valid(self,response:dict)->bool:
        if not isinstance(response,dict):
            return False

        required_keys = {"function","arguments"}

        if not required_keys.issubset(response.keys()):
            return False
        
        if not isinstance(response["arguments"],dict):
            return False

        fn_name = response["function"]
        args = response["arguments"]

        if fn_name == 'add_task':
            return 'name' in args and isinstance(args['name'],str) and bool(args["name"].strip())

        if fn_name in {"mark_done","delete_task"}:
            return(
                'task_number' in args
                and isinstance(args["task_number"],int)
                and  not isinstance(args["task_number"],bool)# In python true evaluted to 1 so we need to check bool as bool is subclass of integer
                and args['task_number'] > 0
                )
        
        if fn_name in {'risk_check','weather_check','view_list','quit'}:
            return True
        if fn_name == 'unknown':
            return True
        return False


    # Main logic of AI Mode!!
    def ai_mode(self) -> None:
        print("\nRemember:-----AI Mode Only DESIGN for GROQ API!!------")
        print("(Type 'quit' or 'back' to return to the main menu)")

        while True:
            if not (prompt:= input("\nPrompt (Describe what you want AI to do): ").strip()):
                print("Prompt Cannot be empty!!")
                continue  # Go back to start of loop
                
            # Handle quitting LOCALLY to save API calls and time
            if prompt.lower() in {"quit", "exit", "back"}:
                print("Exiting AI Mode...")
                return

            if not (response:= self.client.parse_ai_json(self.get_ai_response(prompt), self.is_valid)):
                print("Error: Invalid Response!!")
                continue 

            fn_name = response["function"]
            args = response["arguments"]

            print(f"\n[AI Action Plan]: Execute '{fn_name}' with {args}")

            if fn_name in {"delete_task", "mark_done"}:
                confirm = input(f"Confirm execution of {fn_name}? (y/n): ").strip().lower()
                if confirm != "y":
                    print("Action cancelled by user.")
                    continue 


            if fn_name == "add_task":
                self.Taskfn.add_task_ai(args["name"].strip().title())
            
            elif fn_name == "mark_done":
                self.Taskfn.mark_done_ai(args["task_number"])

            elif fn_name == "delete_task":
                self.Taskfn.delete_task_ai(args["task_number"])
            
            elif fn_name == "view_list":
                self.Taskfn.view_list()

            elif fn_name == "weather_check":
                self.Weatherfn.weather_info()

            elif fn_name == "risk_check":
                self.Taskfn.risk_check()
                
            elif fn_name == "unknown":
                print("AI could not map your request to an available function. Try rephrasing.")

class Suggest:
    def __init__(self, TaskCl:OutdoorManager, client: GROQClient):
        self.Taskfn = TaskCl
        self.current_tasks = TaskCl.data
        self.client = client


    def is_valid(self, ai_tasks: list) -> bool:
        return isinstance(ai_tasks, list) and bool(ai_tasks)

    def clean_tasks(self, ai_tasks: list) -> list:
        return [t.strip() for t in ai_tasks if isinstance(t, str) and t.strip()]
                
    def get_ai_response(self,user_prompt:str)-> list|None:

        system_prompt = """You are a helpful task manager. Return suggestions ONLY as a JSON array of strings  
        {Two words max in Each task}, e.g. [\"task 1\", \"task 2\"].""" 
        temperature = 0.5

        response = self.client.post(system_prompt,user_prompt,temperature)

        return response
        
    def add_suggested_tasks(self,validated_tasks:list):

        print("Following are the Suggested Tasks!!\n")

        for index,p_task in enumerate(validated_tasks,start=1):
            print(f"Task {index}: {p_task}")

        while True:
            user_input_1 = input("\nDo you wnant to Work with AI suggested tasks!! (y/n)").strip().lower()

            if not user_input_1:
                print("\nPlease Use 'y' or 'n' or 'yes' or 'no'")

            elif user_input_1 in ['y','yes']:
                for index,suggestion in enumerate(validated_tasks,start=1):
                    while True:
                        print(f"\nTask {index}: {suggestion}")

                        user_input_2 = input("\nDo you want to ADD the Task ?(y/n)").strip().lower()

                        if not user_input_2:
                            print("\nPlease Use 'y' or 'n' or 'yes' or 'no'")
                        
                        elif user_input_2 in ['y','yes']:
                            self.Taskfn.add_task_ai(suggestion)
                            break
                        elif user_input_2 in ['n','no']:
                            break
                        else:
                            print("Please Type Valid Command!!")
                break

            elif user_input_1 in ['n','no']:
                print("Discarded the Suggetions!!")
                return
            else:
                print("Please Type Valid Command!!")

        self.Taskfn.save()
        print("Suggested Tasks. Saved!!")
        return
        

    def suggestions(self)-> None:
        print("\nRemember:-----Suggestion Only DSIGN for GROQ API!!------")

        while True:
            print("Describe Something To Get AI Task Suggestions!!")
            if not (user_prompt:= input("\nPrompt: ")):
                print("Prompt Cannot be empty!!")
                continue
            else:
                break

        if not (response:= self.client.parse_ai_json(self.get_ai_response(user_prompt), self.is_valid)):
            print("Error: There is an Error in AI Response!!")
            return None

        validated_tasks = self.clean_tasks(response)

        if validated_tasks is None:
            print("Bad Response: Unable to process suggestions.")
            return 
    
        print(f"\nAudit passed! {len(validated_tasks)} tasks ready for review.")
        self.add_suggested_tasks(validated_tasks)

