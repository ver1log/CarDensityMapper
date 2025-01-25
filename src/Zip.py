import pandas as pd




class ZipHelper:
    def __init__(self):
        self.all_data = pd.read_csv("res/zipvehiclestats.csv")

    def get_vechicle_num_from_zip(self,zip:str) -> int:
        area_code_data = self.all_data[self.all_data["ZIP Code" ] == zip]
        num_vehicles = area_code_data["Vehicles"].sum()
        return num_vehicles
    
    def is_valid_zip(self, zip:str) -> bool:
        all_zip_codes = self.all_data["ZIP Code"].to_list()
        #debug stuff
        print(type(all_zip_codes[1]))
        for i in range(0,10):
            print(all_zip_codes[i])
        
        if zip not in all_zip_codes:
            print("zip not in csv")
            return False
        else:
            print("zip in csv")
            return True
            
