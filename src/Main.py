from Map import DensityMap
from App import ApplicationX
from ZipUtil import ZipHelper

def main ():
    # Coordinates for the map's center
    coords = [39, -98]
    # Constructor for the DensityMap object    
    map1 = DensityMap(center=coords, zoom_start=4, fileName = "map_templates", zip_helper=ZipHelper())
    map1.add_marker(39, -98, "Center")
    map1.show_map()
    app1 = ApplicationX(map1)
    #map1.showMap()
    app1.startApplication()
    '''
    this is how I want entries in my db to be
    {
    zipcode:12221, //user input
    numVehicles:111111, //csv file summation
    ...dont need this anymore population:23245, //api request
    density: vehicles/population //api request
    area: sqft //api request
    }
    
    '''

 
if __name__ == '__main__':
    main()