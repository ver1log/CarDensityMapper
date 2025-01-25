import folium
import webbrowser
import json
from ZipUtil import ZipHelper

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

    def show_map(self):
        # Display the map
        self.markArea()
        #self.my_map.save(self.fileName)
        #webbrowser.open(self.fileName)
    def reset_map(self):
        print("CLEARED")
        self.my_map = folium.Map(location=self.center, zoom_start=self.zoom_start) #reset the map
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
        
        folium.GeoJson("res/us-states.json", name = "USA", style_function = lambda x: style).add_to(self.my_map)
    def render_zip_code(self, zipcode:str):
        #when rendering a zip code clear the previous area codes
        self.reset_map()
        surface_area = self.zip_helper.get_surface_area(zipcode)
        city_name = self.zip_helper.get_city_name(zipcode)
        number_of_vehicles = str(self.zip_helper.get_vechicle_num_from_zip(zipcode))
        #doesnt work yet, just using as a place holder
        marker = folium.Marker(
            location=self.zip_helper.get_coodinates(int(zipcode)),
            tooltip="Click me!",
            popup= str(zipcode) + ", " + number_of_vehicles + ", " + str(surface_area) + ", " + city_name,
            icon=folium.Icon(icon="cloud"),
            maxs_bounds=True
        )

        self.marker_arr.append(marker)
        self.reset_map()
        for markers in self.marker_arr:
                markers.add_to(self.my_map)
        self.my_map.fit_bounds(marker.location) 
        