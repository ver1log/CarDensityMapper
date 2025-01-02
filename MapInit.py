import folium
import webbrowser

import folium.map

class DensityMap:
    #the self is like the "this", it referse to the instance making the call
    #the init part acts like a constructor
    #we declare all our members within the constructor not outside
    def __init__(self, center, zoom_start):
        self.center = center
        self.zoom_start = zoom_start
        self.my_map = folium.Map(location = center, zoom_start = self.zoom_start)
    def showMap(self):
    #Display the map
        self.my_map.save("map.html")
        webbrowser.open("map.html")
    def addMarker(self,x:float, y:float, popUpMessage:str):
        folium.Marker(
        location=[x,y],
        tooltip="Click me!",
        popup=popUpMessage,
        icon=folium.Icon(icon="cloud"),).add_to(self.my_map)

coords = [32.7678,-117.0231]
#constructor for the density map object
map = DensityMap(center = coords, zoom_start = 7)
map.addMarker(32.8246976,-117.438621,"Mt. Hood Meadows")


map.showMap()