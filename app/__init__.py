from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from .db import db
from config import Config
from flask_migrate import Migrate

load_dotenv()

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    from app.db.models.usermodel import UserModel
    with app.app_context():
        db.create_all()
    # Load configuration from environment variables
    # Blueprint registration
    from app.routes import api_bp
    app.register_blueprint(api_bp)
    return app