import pandas as pd
import requests
from dotenv import load_dotenv
import os
import json
from src.Storage import fetch_csv_from_supabase, fetch_json_from_supabase
class ZipHelper:
    def __init__(self):
        '''
        self.all_vehicle_data = pd.read_csv("res/zipvehiclestats.csv")
        self.all_coordinate_data = pd.read_csv("res/latlondata.csv")
        self.zctajson = json.load(open('res/california_zipcode_borders.json', 'r'))
        '''
        # Fetch data from Supabase Storage
        self.all_vehicle_data = fetch_csv_from_supabase("zipvehiclestats.csv")
        self.all_coordinate_data = fetch_csv_from_supabase("latlondata.csv")
        self.zctajson = fetch_json_from_supabase("california_zipcode_borders.json")

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

        if zipcode not in all_vehicle_zip_codes or int(zipcode) not in zip_code_latlon:
            print("zip not in both csv")
            return False
        else:
            if self.get_zip_border(zipcode) == 'null':
                return False
            print("zip in both csv and in boundries file")
            return True
        
    def get_coodinates(self, zipcode:int):
        zip_code_data = self.all_coordinate_data[self.all_coordinate_data["ZIP"] == zipcode]
        #print(self.all_coordinate_data.dtypes)

        self.lat = zip_code_data["LAT"].to_list()
        self.lon = zip_code_data["LNG"].to_list()
        #print(self.lat)
        #print(self.lon)
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
            #print("Population data:", data)
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
            #print("Population data:", data)
        else:
            print(f"Failed to fetch data: {response.status_code}, {response.text}")
        
        #get the data part of the json
        actual_data = data['data']
        #actual surface area key pair extraction from the json
        cities_json = actual_data['cityAliases']
        city_name_list = cities_json[0]
        specific_city = city_name_list['titleCaseCityName']
        return specific_city
    
    def get_zip_border(self, zipcode):
        data = self.zctajson
        zip_polygon_data = None
        for feature in data['features']:
            if feature["id"] == zipcode: #the right feature json was found
                zip_polygon_data = feature['geometry'] #extract the correct geometry of the json that we found
        data_string = json.dumps(zip_polygon_data)
        #print(data_string)
        return data_string
    