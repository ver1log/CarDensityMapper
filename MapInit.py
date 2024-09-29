import folium
import webbrowser

class densityMap:
    #the self is like the "this", it referse to the instance making the call
    #the init part acts like a constructor
    def __init__(self, center, zoom_start):
        self.center = center
        self.zoom_start = zoom_start
    
    def showMap(self):
    #Create the map
        my_map = folium.Map(location = self.center, zoom_start = self.zoom_start)
    #Display the map
        my_map.save("map.html")
        webbrowser.open("map.html")

coords = [32.8246976,-117.438621]
#constructor for the density map object
map = densityMap(center = coords, zoom_start = 5)
map.showMap()