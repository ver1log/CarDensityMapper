from src.Map import DensityMap
from src.App import ApplicationX
from src.ZipUtil import ZipHelper
import json
'''
def main ():
    # Coordinates for the map's center
    center_coords = [35, -98]
    # Constructor for the DensityMap object    
    map1 = DensityMap(center=center_coords, zoom_start=5, fileName = "map_templates", zip_helper=ZipHelper())
    #map1.add_marker(39, -98, "Center")
    map1.show_map()
    app1 = ApplicationX(map1)
    #map1.showMap()
    app1.startApplicationAndDB()
    app = app1.app
    #database = DensityTable(app1.db.Model)
    
    this is how I want entries in my db to be
    {
    zipcode:12221, //user input
    numVehicles:111111, //csv file summation
    ...dont need this anymore population:23245, //api request
    density: vehicles/population //api request
    area: sqft //api request
    }
    
   
 
 
if __name__ == '__main__':
    main() '''
center_coords = [35, -98]
map1 = DensityMap(center=center_coords, zoom_start=5, fileName="map_templates", zip_helper=ZipHelper())
app1 = ApplicationX(map1)
app1.startApplicationAndDB()

app = app1.app

def main():
    app.run(host='0.0.0.0', port=8000, debug=True)

if __name__ == '__main__':
    main()