from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)

    # Load configuration from environment variables
    
    # Blueprint registration
    from app.routes import api_bp
    app.register_blueprint(api_bp)
    return app