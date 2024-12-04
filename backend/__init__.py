from flask import Flask
from .main import app  

# Create and configure the Flask app
def create_app():
    app = Flask(__name__)



    return app
