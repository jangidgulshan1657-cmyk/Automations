from pathlib import Path
import json
import urllib.request
import urllib.error

class JsonStore:
    def __init__(self, path):
        self.path = Path(path)
        self.data = self.load()

    def default(self):# overwrites by Child or Sublclass!!
        raise NotImplementedError

    def is_valid(self,data):
        raise NotImplementedError 

    def save(self):
        self.path.parent.mkdir(parents= True, exist_ok= True)
        with open(self.path,'w',encoding='utf-8') as f:
            json.dump(self.data,f,indent= 4)

    def load(self):
        try:
            with open(self.path,'r',encoding="utf-8") as f:
                data = json.load(f)
                if self.is_valid(data):
                    return data
                print("Invalid structure, using defaults.")
        except FileNotFoundError:
            print("File is missing Creatint It!")
        except (json.JSONDecodeError,UnicodeDecodeError,OSError):
            print("File has been Currupted!! Using Defaults!!")
        self.data =  self.default()
        self.save()
        return self.data

class Url:
    def __init__(self,url):
        self.url = url
        self.raw_data = self.url_req()

    def is_valid(self,data):
        raise NotImplementedError

    def safe_data(self):
        raise NotImplementedError

    def url_req(self):
        try:
            with urllib.request.urlopen(self.url, timeout=10) as reponse:
                raw_bytes = reponse.read()                                #Convering Raw bites
                text_data =  raw_bytes.decode('utf-8')                    #Converting in text format
                data = json.loads(text_data)                              #Conveting the string to json 
                return data
        except urllib.error.HTTPError as e:
            print(f"Server returned an error code: {e.code}")
        except urllib.error.URLError as e:
            print(f"Network failure / No internet: {e.reason}")
        except json.JSONDecodeError:
            print("The server did not send back Valid Json!!")
        return None

