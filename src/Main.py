from Map import DensityMap
from App import ApplicationX


def main ():
    # Coordinates for the map's center
    coords = [32.7678, -117.0231]
    # Constructor for the DensityMap object    
    map1 = DensityMap(center=coords, zoom_start=8, fileName = "map_templates")
    map1.addMarker(32.7678, -117.0231, "San Deigo")
    map1.showMap()
    app1 = ApplicationX(map1)
    #map1.showMap()
    app1.startApplication()
    

 
if __name__ == '__main__':
    main()