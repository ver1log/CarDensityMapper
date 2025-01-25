import pandas as pd
import requests
from dotenv import load_dotenv
import os

class ZipHelper:
    def __init__(self):
        self.all_vehicle_data = pd.read_csv("res/zipvehiclestats.csv")
        self.all_coordinate_data = pd.read_csv("res/latlondata.csv")
        self.lat = []
        self.lng = []
        load_dotenv()
    def get_vechicle_num_from_zip(self,zip:str) -> int:
        zip_code_data = self.all_vehicle_data[self.all_vehicle_data["ZIP Code" ] == zip]
        num_vehicles = zip_code_data["Vehicles"].sum()
        return num_vehicles
    
    def is_valid_zip(self, zipcode:str) -> bool:
        all_vehicle_zip_codes = self.all_vehicle_data["ZIP Code"].to_list()
        zip_code_latlon = self.all_coordinate_data["ZIP"].to_list()
        #debug stuff
        print(type(all_vehicle_zip_codes[1]))
        for i in range(0,10):
            print(all_vehicle_zip_codes[i])
        
        if zipcode not in all_vehicle_zip_codes or int(zipcode) not in zip_code_latlon:
            print("zip not in both csv")
            return False
        else:
            print("zip in both csv")
            return True
        
    def get_coodinates(self, zipcode:int):
        zip_code_data = self.all_coordinate_data[self.all_coordinate_data["ZIP"] == zipcode]
        print(self.all_coordinate_data.dtypes)

        self.lat = zip_code_data["LAT"].to_list()
        self.lon = zip_code_data["LNG"].to_list()
        print(self.lat)
        print(self.lon)
        return [self.lat[0], self.lon[0]]
    
    

    def get_surface_area(self, zipcode):
        # Endpoint URL
        url = f"https://global.metadapi.com/zipc/v1/zipcodes/{zipcode}"
        # Headers with the subscription key
        headers = {
            "Ocp-Apim-Subscription-Key": os.environ['api_key']
        }
        # Make the GET request
        response = requests.get(url, headers=headers)
        #check the status code
        if response.status_code == 200:
            data = response.json()
            print("Population data:", data)
        else:
            print(f"Failed to fetch data: {response.status_code}, {response.text}")
        
        #get the data part of the json
        actual_data = data['data']
        #actual surface area key pair extraction from the json
        surface_area = actual_data['landAreaMi2']
        return surface_area
    
    def get_city_name(self, zipcode):
        # Endpoint URL
        url = f"https://global.metadapi.com/zipc/v1/zipcodes/{zipcode}"
        # Headers with the subscription key
        headers = {
            "Ocp-Apim-Subscription-Key": os.environ['api_key']
        }
        # Make the GET request
        response = requests.get(url, headers=headers)
        #check the status code
        if response.status_code == 200:
            data = response.json()
            print("Population data:", data)
        else:
            print(f"Failed to fetch data: {response.status_code}, {response.text}")
        
        #get the data part of the json
        actual_data = data['data']
        #actual surface area key pair extraction from the json
        cities_json = actual_data['cityAliases']
        city_name_list = cities_json[0]
        specific_city = city_name_list['titleCaseCityName']
        return specific_city
    
            
