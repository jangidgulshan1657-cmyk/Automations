from pathlib import Path
import json
import api_key_test
import urllib.request
import urllib.error

KEY_PATH = Path("Projects/Taskmanager/.env")

api_key = api_key_test.get_key("GROQ_API_KEY",KEY_PATH)

def groq_ai(user_prompt:str):
    #groq url for requesting access to models
    url = "https://api.groq.com/openai/v1/chat/completions"

    #Header for groq model copied
    headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "TaskPlanner/1.0"
    }

    #Content design copied
    payload = {
        "model": "openai/gpt-oss-120b",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful task manager. Return suggestions ONLY as a JSON array of strings {Two words max in Each task e.g. [\"task 1\", \"task 2\"]."
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        "temperature": 0.5
    }

    # headers needs or does not need the encoding they encode in ascii
    # encoding in utf 8 insures that there is tranfer of text or number or symbol not the audio or video file
    data = json.dumps(payload).encode('utf-8')
    
    #"POST" is used for trasmission of data 
    #"GET" only request to get the data and also expects it!!
    req = urllib.request.Request(url,data= data,headers= headers,method = "POST")

    try:
        with urllib.request.urlopen(req,timeout=15) as response:
            #decoding the response!! same as Weather API request
            raw_bytes = response.read()
            text_string = raw_bytes.decode("utf-8")
            content = json.loads(text_string)

            return content
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        print(f"HTTP Error {e.code}: {error_body}")
    except urllib.error.URLError as e:
        print(f"Network Connection Error: {e.reason}")
    except json.JSONDecodeError:
        print("Failed to parse API JSON response.")
    return None



def check_valid_tasks(task_list:list)-> list | None:
    #checking is that the llm return a list or not
    if not isinstance(task_list,list):
        print("")
        return
    
    #checking list empty or not 
    if not task_list:
        print("")
        return

    # chcking that the list has all Strings!!


    valid_tasks = []

    for item in task_list:
        #checking weather it is string or not 
        if not isinstance(item,str):
            print(f"Audit Warning: Dropping non-string item: {item}")
            continue

        #removing white Space!
        cleaned = item.strip()
        if not cleaned:
            continue

        valid_tasks.append(cleaned)

    # last Check!
    if not valid_tasks:
        print("Audit Failure: No valid string tasks remained after cleaning.")
        return None

    return valid_tasks

prompt = "things to do before a bithday party"

raw_list = groq_ai(prompt)

print(raw_list)

validated_tasks = check_valid_tasks(raw_list)

if validated_tasks is None:
    print("Unable to process suggestions.")
else:
    print(f"Audit passed! {len(validated_tasks)} tasks ready for review.")