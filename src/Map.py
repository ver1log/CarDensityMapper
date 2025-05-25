import folium
import webbrowser
import json
from src.zip_util import ZipHelper
from src.supa_storage import fetch_json_from_supabase

class DensityMap:
    # The self is like the "this"; it refers to the instance making the call
    # The init part acts like a constructor
    # We declare all our members within the constructor, not outside
    def __init__(self, center, zoom_start, fileName, zip_helper:ZipHelper):
        self.center = center
        self.zoom_start = zoom_start
        self.my_map = folium.Map(location=center, zoom_start=self.zoom_start)
        self.fileName = "templates/" + fileName + ".html"
        self.marker_arr = []
        self.zip_helper = zip_helper
        self.zalid_passed_zipcodes = []
        self.db = None
        self.DensityTable = None
        self.boundries_mapping = {}

    def set_database(self, db, DensityTable):
        self.db = db
        self.DensityTable = DensityTable

    def add_density_entry(self, zipcode, x, y, area, number_of_vehicles,color,city_name,jsonboundries):
        if self.db and self.DensityTable:
            new_entry = self.DensityTable(zipcode=zipcode, x=x, y=y, area=area, number_of_vehicles= number_of_vehicles, color=color,city_name= city_name, jsonboundries=jsonboundries)
            self.db.session.add(new_entry)
            self.db.session.commit()
        else:
            print("Database not initialized in DensityMap!")

    def density_entry_exists(self, zipcode):
        """Check if a density entry with the given zipcode exists."""
        if self.db and self.DensityTable:
            query_on_zipcode = self.db.session.query(self.DensityTable).filter(self.DensityTable.zipcode == zipcode)
            return self.db.session.query(query_on_zipcode.exists()).scalar()
        else:
            print("Database not initialized in DensityMap!")
            return False
    
    def get_density_entry(self, zipcode):
        """Retrieve the density entry for a given zipcode."""
        if self.db and self.DensityTable:
            return self.db.session.query(self.DensityTable).filter(self.DensityTable.zipcode == zipcode).first()
        else:
            print("Database not initialized in DensityMap!")
            return None
        
    def show_map(self):
        # Display the map
        self.markArea()

    def reset_zoom_position(self, marker_coords):
        #print("CLEARED")
        self.my_map = folium.Map(location=marker_coords, zoom_start=11) #reset the map
        #self.zalid_passed_zipcodes = [] #make the array of valid zipcodes empty again
        self.markArea() #mark the US again

    def add_marker(self, x: float, y: float, popUpMessage: str):
        folium.Marker(
            location=[x, y],
            tooltip="Click me!",
            popup=popUpMessage,
            icon=folium.Icon(icon="cloud"),
            maxs_bounds=True
        ).add_to(self.my_map)
        
    def markArea(self):
        style = {'color':'grey', 
                'weight':'1', 
                'fillcolor':'black', 
                'fillOpacity':.3}
        
        folium.GeoJson(fetch_json_from_supabase("californiaoutline.json"), name = "USA", style_function = lambda x: style).add_to(self.my_map)

    def render_zip_code(self, zipcode:str)->bool:
        if self.zip_helper.is_valid_zip(zipcode) == False: #invalid zipcode
            return False
        else:#valid zipcode
            zoom_back_coords = self.zip_helper.get_coodinates(int(zipcode))
            if zipcode not in self.zalid_passed_zipcodes: #if the zipcode has not been entered yet, a new zipcode that isnt already rendered
                self.zalid_passed_zipcodes.append(zipcode) #add the valid zipcode to the list so we can pass it as a entry in the db
                zipcodes = self.zalid_passed_zipcodes
                #get the coordinates to zoom back into when the map is cleared
                for a_zipcode in zipcodes:
                    if self.density_entry_exists(a_zipcode) == True: #if the zipcode exists in the database just make a query
                        print('in db\n')
                        zipcode_entry = self.get_density_entry(a_zipcode)
                        marker = folium.Marker(
                        location= [zipcode_entry.x, zipcode_entry.y],
                        tooltip="Click me!",
                        popup= str(a_zipcode) + ", " + str(zipcode_entry.number_of_vehicles) + ", " + str(zipcode_entry.area) + "mi^2, " + zipcode_entry.city_name,
                        icon=folium.Icon(icon="cloud", color = zipcode_entry.color),
                        maxs_bounds=True
                                                )
                        #self.mark_zip_boundries(zipcode_entry.color,zipcode,zipcode_entry.jsonboundries)
                        self.marker_arr.append(marker)
                        self.boundries_mapping[a_zipcode] = [zipcode_entry.color,zipcode_entry.jsonboundries]
                    else:    ##if it is not in the db, add it to the db and make a marker for it
                        print('not in db\n')
                        surface_area = self.zip_helper.get_surface_area(a_zipcode)
                        city_name = self.zip_helper.get_city_name(a_zipcode)
                        number_of_vehicles = str(self.zip_helper.get_vechicle_num_from_zip(a_zipcode))
                        marker_color = self.get_density_color(float(surface_area), int(number_of_vehicles))
                        zip_coordinates = self.zip_helper.get_coodinates(int(a_zipcode))
                        zip_polygon_data = self.zip_helper.get_zip_border(str(a_zipcode))
                        #doesnt work yet, just using as a place holder
                        marker = folium.Marker(
                            location= zip_coordinates,
                            tooltip="Click me!",
                            popup= str(zipcode) + ", " + number_of_vehicles + ", " + str(surface_area) + "mi^2, " + city_name,
                            icon=folium.Icon(icon="cloud", color = marker_color),
                            maxs_bounds=True
                        )
                        self.add_density_entry(zipcode, zip_coordinates[0], zip_coordinates[1], surface_area,number_of_vehicles,marker_color, city_name,zip_polygon_data)
                        #self.mark_zip_boundries(marker_color, str(zipcode), zip_polygon_data)
                        self.marker_arr.append(marker) 
                        self.boundries_mapping[a_zipcode] = [marker_color,zip_polygon_data]
            self.reset_zoom_position(zoom_back_coords) 
            print("ZOOMING INTO ZIP");             
            for markers in self.marker_arr:
                    markers.add_to(self.my_map)
            for key in self.boundries_mapping:
                self.mark_zip_boundries(self.boundries_mapping[key][0],key,self.boundries_mapping[key][1])
                print(f'zipcode:{key}, color:{self.boundries_mapping[key][0]}')
            ##self.my_map.fit_bounds(marker.location) 
            print("INSIDE mapping func")
            print(self.zalid_passed_zipcodes)
            return True

    def get_density_color(self, sqft, num_vehicles): ##-> str:
        #national average for urban areas
        # my goal is to get the most dense places so each zip code will be treated as urban       
        # this will be my ranges
        #    'darkred'
        #    'lightred'
        #    'orange'
        #    'beige'

        density_color = ''
        car_density = num_vehicles/sqft
        if car_density <= 1000:
            print("Low Density (0-1,000 cars/sqmi)")
            density_color ='beige'
        elif car_density <= 2500:
            print("Moderate Density (1,001-2,500 cars/sqmi)")
            density_color ='orange'
        elif car_density <= 5000:
            print("High Density (2,501-5,000 cars/sqmi)") 
            density_color ='lightred'
        else:
            print("Very High Density (5,001+ cars/sqmi)")
            density_color = 'darkred'

        return density_color
    
    def mark_zip_boundries(self, color, zipcode, zip_polygon_data):
        style = {'color':color, 
                'weight':'1', 
                'fillcolor':'black', 
                'fillOpacity':.3}
        if not zip_polygon_data == None: 
            folium.GeoJson(zip_polygon_data, name = zipcode, style_function = lambda x: style).add_to(self.my_map)

    def clear_map(self):
        self.my_map = folium.Map(location=self.center, zoom_start=self.zoom_start) 
        self.marker_arr = []
        print(self.marker_arr)
        self.boundries_mapping = {}
        print(self.boundries_mapping)
        print(self.zalid_passed_zipcodes)
        self.zalid_passed_zipcodes = []
        self.markArea()
        