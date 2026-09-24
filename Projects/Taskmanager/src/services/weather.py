import urllib.request
import urllib.error
import urllib.parse
import json

def getting_data(url:str)-> dict|None:
    if not url:
        print("Url cannot be None")
        return
    try:
        with urllib.request.urlopen(url, timeout=10) as reponse:
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

def organizing_data(information:dict)-> None:
    if not information:
        print("Data is Unable to Display")
        return
    
    try:
        current = information["current_condition"][0]

        print(f"\nTemperature = {current['temp_C']}°C")
        print(f"UV Index = {current['uvIndex']}")

        desc_list = current["weatherDesc"]           # This is a list
        weather_description = desc_list[0]["value"]  # Grab item 0, then key 'value'
        print(f"Condition = {weather_description}")

        area = information["nearest_area"][0]
        country_name = area["country"][0]["value"]
        print(f"Country = {country_name}")

    except (KeyError,IndexError):
        print("To Display Expected data is not found!!")

def safe_url(city:str)-> str:
    # urllib.parse.qoute() change the New York to New%20York 
    safe_city = urllib.parse.quote(city)

    url = f"https://wttr.in/{safe_city}?format=j1"
    return url              

def weather_info(city:str)-> None:
    print("\n------Weather Information--------")

    url = safe_url(city)
    data = getting_data(url)
    organizing_data(data)