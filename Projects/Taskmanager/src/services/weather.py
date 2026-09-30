import urllib.parse
import json
from parent.parent import Url


class Weather(Url):
    def __init__(self,url):
        super().__init__(url)
        self.data = self.safe_data()

    def is_valid(self)-> bool:
        if not self.raw_data:
            return False

        if not isinstance(self.raw_data,dict):
            return False

        req_data = {"current_condition","nearest_area"}

        for req in req_data:
            if req not in self.raw_data.keys():
                return False

        if not isinstance(self.raw_data["current_condition"],list) or not isinstance(self.raw_data["nearest_area"],list):
            return False

        current = self.raw_data["current_condition"][0]
        keys = {'temp_C','uvIndex','weatherDesc'}

        for key in keys:
            if key not in current:
                return False

        desc_list = current["weatherDesc"]

        if not isinstance(desc_list,list):
            return False
        if "value" not in desc_list[0]:
            return False
        
        area = self.raw_data["nearest_area"][0]
        if "country" not in area:
            return False
        if not isinstance(area["country"], list):
            return False

        if 'value' not in area["country"][0]:
            return False
        return True

    def safe_data(self):
        if self.is_valid():
            return self.raw_data
        print("[Invalid Weather Response form the Url]")
        return

    def weather_info(self)-> None:
        if not self.data:
            return 
        current = self.data["current_condition"][0]

        print(f"\nTemperature = {current['temp_C']}°C")
        print(f"UV Index = {current['uvIndex']}")

        desc_list = current["weatherDesc"]           # This is a list
        weather_description = desc_list[0]["value"]  # Grab item 0, then key 'value'
        print(f"Condition = {weather_description}")

        area = self.data["nearest_area"][0]
        country_name = area["country"][0]["value"]
        print(f"Country = {country_name}")

        

def get_city()-> str:
    while True:
        city = input("\nCurrently Which City You live In: ").strip()
        if city:
            break
        print("\nCity cannot be Empty!")

    # urllib.parse.qoute() change the New York to New%20York 
    safe_city = urllib.parse.quote(city)

    url = f"https://wttr.in/{safe_city}?format=j1"
    return url              