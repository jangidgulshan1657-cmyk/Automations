import json
from pathlib import Path
from . import task
import urllib.request
import urllib.error

API_PATH = Path("Projects/Taskmanager/.env")

def get_key(var_name:str,file_path:str)-> str | None:
    if not file_path.exists():
        print("\nError: Environment variable File does not exist! or put it on wrong folder!!")
        print("\nPlease make sure its in Right Folder (Taskmananger!)")
        return None

    with open(file_path,'r',encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                var , key = line.split("=",1)
                if var.strip() == var_name:
                    api = key.strip().strip("'\"")
                    return api

    print("\nError: GROQ_API_KEY key Not Found!! \nPlease ADD the API key in .env file like: GROQ_API_KEY = 'your_key_here'")
    return None

def valid_tasks(ai_tasks:list)-> list|None:

    if not ai_tasks:
        return

    if not isinstance(ai_tasks,list):
        return

    valid_tasks = []

    for task in ai_tasks:
        if not isinstance(task,str):
            print(f"\nAudit Warning: Dropping non-string item: {task}")
            continue
        cleaned = task.strip()
        if not cleaned:
            continue

        valid_tasks.append(cleaned)

    if not valid_tasks:
        return
    
    return valid_tasks

    

def groq_ai(user_prompt:str,api_key:str)-> list|None:

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "TaskPlanner/1.0"
    }

    payload ={
        "model": "openai/gpt-oss-120b",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful task manager. Return suggestions ONLY as a JSON array of strings  {Two words max in Each task}, e.g. [\"task 1\", \"task 2\"]."
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        "temperature": 0.5
    }

    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url,data=data,headers=headers,method="POST")

    try:
        with urllib.request.urlopen(req,timeout=15) as response:
            content_string = response.read().decode("utf-8")
            content = json.loads(content_string)
            try:
                result = content["choices"][0]["message"]["content"]
                ai_tasks = json.loads(result)
            except (IndexError,KeyError,ValueError):
                return None
            return ai_tasks

    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8',errors= "replace")
        print(f"HTTPError {e.code} {error_body}")
    except urllib.error.URLError as e:
        print(f"Network Connection Error: {e.reason}")
    except json.JSONDecodeError:
        print("LLM Return Bad json!!")
    return None

def add_suggested_tasks(valid_tasks:list,tasks:list):

    print("Following are the Suggested Tasks!!\n")

    for index,p_task in enumerate(valid_tasks,start=1):
        print(f"Task {index}: {p_task}")

    while True:
        user_input_1 = input("\nDo you wnant to Work with AI suggested tasks!! (y/n)").strip().lower()

        if not user_input_1:
            print("\nPlease Use 'y' or 'n' or 'yes' or 'no'")

        elif user_input_1 in ['y','yes']:
            for index,suggestion in enumerate(valid_tasks,start=1):
                while True:
                    print(f"\nTask {index}: {suggestion}")

                    user_input_2 = input("\nDo you want to ADD the Task ?(y/n)").strip().lower()

                    if not user_input_2:
                        print("\nPlease Use 'y' or 'n' or 'yes' or 'no'")
                    
                    elif user_input_2 in ['y','yes']:
                        print(f"Added Successfully! ")
                        tasks.append({"name":suggestion,"done":False})
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

    task.writing(tasks)
    print("Suggested Tasks. Saved!!")
    return
    

def suggestions(tasks:list):
    print("\nRemember:-----Suggestion Only DSIGN for GROQ API!!------")

    key = get_key("GROQ_API_KEY",API_PATH)
    if not key:
        print("\nPlease Fix the Above: Error!!")
        return


    while True:
        print("Describe Something To Get AI Task Suggestions!!")
        user_prompt = input("\nPrompt: ")

        if not user_prompt:
            print("Prompt Cannot be empty!!")
        else:
            break


    ai_tasks = groq_ai(user_prompt,key)
    validated_tasks = valid_tasks(ai_tasks)

    if validated_tasks is None:
        print("Bad Response: Unable to process suggestions.")
        return
 
    print(f"\nAudit passed! {len(validated_tasks)} tasks ready for review.")
    add_suggested_tasks(validated_tasks,tasks)