from flask import Flask, render_template
from Map import DensityMap
class ApplicationX:
    def __init__(self,theMap:DensityMap):
        self.theMap = theMap
    def startApplication(self):
        app = Flask(__name__)

        messages = [{'title': 'Message One',
                    'content': 'Message One Content'},
                    {'title': 'Message Two',
                    'content': 'Message Two Content'}
                    ]

        @app.route('/')
        def index():
            # Use only the file name without the "templates/" path
            return render_template(self.theMap.fileName.split('/')[-1], messages=messages)

        # Start the Flask app
        app.run(debug=True)