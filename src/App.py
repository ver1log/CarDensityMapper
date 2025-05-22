from flask import Flask, render_template, request
from src.Map import DensityMap
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

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
        class DensityTable(self.db.Model):
            zipcode = self.db.Column(self.db.Integer, primary_key=True)
            x = self.db.Column(self.db.Float)
            y = self.db.Column(self.db.Float)
            area = self.db.Column(self.db.Float)
            number_of_vehicles = self.db.Column(self.db.Integer)
            color = self.db.Column(self.db.String(20))
            city_name = self.db.Column(self.db.String(20))
            jsonboundries = self.db.Column(self.db.String)
        
        self.DensityTable = DensityTable  # Store the model class
        self.theMap.set_database(self.db, self.DensityTable) #pass in DB stuff so Map.py can work with it
    
    def startApplicationAndDB(self):
        with self.app.app_context():
            self.db.create_all()
        
        @self.app.route('/')
        def index():
            landing_page_file = "landing_page.html"
            # Use only the file name without the "templates/" path, split at the / and get the last element of the list(filename)
            return render_template(landing_page_file)
        

        #the only time the GET method will be invoked is when we are routing a user, POST will be doing the work
        @self.app.route("/density", methods=["POST","GET"])
        def density():
            # Retrieve the zipcode via form post request
            if request.method == "POST":
                zipcode = request.form.get("zipcode")
            elif request.method == "GET":
                from_landing = request.args.get('from')
                if from_landing == 'landing':
                    print('User came from landing page')
                    map_content = self.theMap.my_map._repr_html_()
                    return render_template(self.theMap.fileName.split('/')[-1], map_content=map_content)

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
                return render_template(self.theMap.fileName.split('/')[-1], map_content=map_content)
            
        
        # Start the Flask app
        #self.app.run(debug=True)
        #self.app.run(host='0.0.0.0', port=8000)

