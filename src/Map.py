import folium
import webbrowser
import json

class DensityMap:
    # The self is like the "this"; it refers to the instance making the call
    # The init part acts like a constructor
    # We declare all our members within the constructor, not outside
    def __init__(self, center, zoom_start, fileName):
        self.center = center
        self.zoom_start = zoom_start
        self.my_map = folium.Map(location=center, zoom_start=self.zoom_start)
        self.fileName = "templates/" + fileName + ".html"

    def showMap(self):
        # Display the map
        self.markArea()
        self.my_map.save(self.fileName)
        #webbrowser.open(self.fileName)

    def addMarker(self, x: float, y: float, popUpMessage: str):
        folium.Marker(
            location=[x, y],
            tooltip="Click me!",
            popup=popUpMessage,
            icon=folium.Icon(icon="cloud"),
        ).add_to(self.my_map)
    def markArea(self):
        style = {'color':'grey', 
                'weight':'1', 
                'fillcolor':'black', 
                'fillOpacity':.3}
        
        folium.GeoJson("res/us-states.json", name = "USA", style_function = lambda x: style).add_to(self.my_map)
