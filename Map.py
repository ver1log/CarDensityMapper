import folium
import webbrowser

class DensityMap:
    # The self is like the "this"; it refers to the instance making the call
    # The init part acts like a constructor
    # We declare all our members within the constructor, not outside
    def __init__(self, center, zoom_start):
        self.center = center
        self.zoom_start = zoom_start
        self.my_map = folium.Map(location=center, zoom_start=self.zoom_start)

    def showMap(self):
        # Display the map
        self.my_map.save("map.html")
        webbrowser.open("map.html")

    def addMarker(self, x: float, y: float, popUpMessage: str):
        folium.Marker(
            location=[x, y],
            tooltip="Click me!",
            popup=popUpMessage,
            icon=folium.Icon(icon="cloud"),
        ).add_to(self.my_map)


# Coordinates for the map's center
coords = [32.7678, -117.0231]
# Constructor for the DensityMap object
map = DensityMap(center=coords, zoom_start=8)
map.addMarker(32.8246976, -117.438621, "TEST")
map.showMap()