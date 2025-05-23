from flask import Flask, render_template, request
from src.Map import DensityMap
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from src.models.Density import define_density_table

class ApplicationX:
    def __init__(self,theMap:DensityMap):
        self.theMap = theMap
        self.app = Flask(__name__, template_folder='../templates')

        DATABASE_URL = os.getenv('POSTGRES_URL_NON_POOLING')
        if DATABASE_URL.startswith("postgres://"):
            DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
        self.app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
        print("Database URI:", self.app.config['SQLALCHEMY_DATABASE_URI'])

        self.db = SQLAlchemy(self.app)
        migrate = Migrate(self.app, self.db)
        
        self.DensityTable = define_density_table(self.db) # Store the model class
        self.theMap.set_database(self.db, self.DensityTable) #pass in DB stuff so Map.py can work with it
    
    def startApplicationAndDB(self):
        with self.app.app_context():
            self.db.create_all()
        
        @self.app.route('/')
        def index():
            landing_page_file = "landing_page.html"
            # Use only the file name without the "templates/" path, split at the / and get the last element of the list(filename)
            return render_template(landing_page_file)
        
        #main route for displaying densities
        @self.app.route("/density", methods=["POST"])
        def show_density():
            # Retrieve the zipcode via form post request
            print("INSIDE POST!!!!!");
            print("Raw data:", request.data)
            request_json = request.get_json()
            zipcode = request_json.get("zipcode")
            print(f"Received ZIP: {zipcode}")

            # Validate whether the submission was valid
            if not zipcode or not zipcode.isdigit() or len(zipcode) != 5:
                print(zipcode)
                return "Invalid ZIP code", 400

            # Check if ZIP code exists in the database
            if(self.theMap.render_zip_code(zipcode) == False):
                return "Zipcode not available", 400
            else:# Render the ZIP code density on the map, since it has been checked that it is valid at this point
                self.theMap.render_zip_code(zipcode)
                # Generate the HTML for the map
                map_content = self.theMap.my_map._repr_html_()
                #Pass the HTML to the template, and render the updated map
                print("RENDERED ZIPCODE");
                #return render_template(self.theMap.fileName.split('/')[-1], map_content=map_content)
                return map_content
        
        @self.app.route("/density", methods=["GET"])
        def goto_map():
            from_landing = request.args.get('from')
            if from_landing == 'landing':
                print('User came from landing page')
                #self.theMap.clear_map()
                self.theMap.clear_map()
                map_content = self.theMap.my_map._repr_html_()
                return render_template(self.theMap.fileName.split('/')[-1], map_content=map_content)

        #this will be my route that i use to clear the screen and send the user back to the default map 
        @self.app.route("/density", methods=["DELETE"])
        def clear():
            print("inside clear");
            self.theMap.clear_map()
            map_content = self.theMap.my_map._repr_html_()
            #I am returning the map content since the DELETE route does not render the new page, that will be done on the client side
            return map_content
