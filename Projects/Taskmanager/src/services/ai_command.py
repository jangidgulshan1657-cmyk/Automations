from . import suggest
from . import task
from . import weather
import json
import urllib.request
import urllib.error


def get_ai_response(current_tasks:list,user_prompt:str,api_key:str)-> dict|None:

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "TaskPlanner/1.0"
    }

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

    payload = {
        "model": "openai/gpt-oss-120b",
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": f"Current tasks: {current_tasks}\nUser instruction: {user_prompt}"
            }
        ],
        "temperature": 0.0  # Kept low (0.0 or 0.1) for deterministic function selection
    }

    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url,data=data, headers= headers,method= "POST")

    try:
        with urllib.request.urlopen(req,timeout=35) as response:
            raw_data = response.read().decode('utf-8')
            text_string = json.loads(raw_data)
            try:
                content_string = text_string["choices"][0]["message"]["content"]
                content = json.loads(content_string)
                return content
            except (IndexError,TypeError,KeyError,json.JSONDecodeError):
                return None
            return None
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8',errors= "replace")
        print(f"HTTPError {e.code} {error_body}")
    except urllib.error.URLError as e:
        print(f"Network Connection Error: {e.reason}")
    except TimeoutError:
        print("\nError: The AI server took too long to respond. Please try again.")
    except json.JSONDecodeError:
        print("LLM Return Bad json!!")
    return None


def valid_response(response:dict):
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
        print("Funtion Not Available!!")
        return False
    return False

# Main logic of AI Mode!!
def ai_mode(tasks: list, city: str, config_data: dict) -> None:
    print("\nRemember:-----AI Mode Only DESIGN for GROQ API!!------")
    print("(Type 'quit' or 'back' to return to the main menu)")

    key = suggest.get_key("GROQ_API_KEY")
    if not key:
        print("\nPlease Fix the Above: Error!!")
        return

    while True:
        prompt = input("\nPrompt (Describe what you want AI to do): ").strip()

        if not prompt:
            print("Prompt Cannot be empty!!")
            continue  # Go back to start of loop
            
        # Handle quitting LOCALLY to save API calls and time
        if prompt.lower() in {"quit", "exit", "back"}:
            print("Exiting AI Mode...")
            break

        response = get_ai_response(tasks, prompt, key)

        if not response or not valid_response(response):
            print("\nInvalid AI Response or Network Error!!")
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
            task.add_task(tasks, args["name"].strip().title())
        
        elif fn_name == "mark_done":
            task.mark_done(tasks, args["task_number"])

        elif fn_name == "delete_task":
            task.delete_task(tasks, args["task_number"])
        
        elif fn_name == "view_list":
            task.view_list(tasks)

        elif fn_name == "weather_check":
            weather.weather_info(city)

        elif fn_name == "risk_check":
            task.risk_check(tasks, city, config_data)
            
        elif fn_name == "unknown":
            print("AI could not map your request to an available function. Try rephrasing.")