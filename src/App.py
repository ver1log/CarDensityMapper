from flask import Flask, render_template, request
from Map import DensityMap
class ApplicationX:
    def __init__(self,theMap:DensityMap):
        self.theMap = theMap
    def startApplication(self):
        app = Flask(__name__, template_folder='../templates')
        
        @app.route('/')
        def index():
            # Generate the HTML for the map
            map_content = self.theMap.my_map._repr_html_()  # Converts the map to an HTML string
            # Pass the HTML to the template
            # Use only the file name without the "templates/" path, split at the / and get the last element of the list(filename)
            return render_template(self.theMap.fileName.split('/')[-1], map_content=map_content)
        

        #if zip code is not already in the database, check somehow
        @app.route("/density", methods=["GET", "POST"])
        def density():
            # Determine how the ZIP code is submitted (POST or GET)
            if request.method == "POST":
                zipcode = request.form.get("zipcode")
            else:  # GET method
                zipcode = request.args.get("zipcode")

            # Validate whether the submission was valid
            if not zipcode or not zipcode.isdigit() or len(zipcode) != 5:
                return "Invalid ZIP code", 400

            # Check if ZIP code exists in the database
            # Assuming `self.database` is a dictionary or similar
            '''
            if zipcode not in self.database:
                return "ZIP code not found in the database", 404
            '''
            if(self.theMap.zip_helper.is_valid_zip(str(zipcode)) == False):
                return "Zipcode not available", 400
            # Render the ZIP code density on the map
            self.theMap.render_zip_code(zipcode)
            map_content = self.theMap.my_map._repr_html_()

            # Render the updated map
            return render_template(self.theMap.fileName.split('/')[-1], map_content=map_content)
        # Start the Flask app
        app.run(debug=True)