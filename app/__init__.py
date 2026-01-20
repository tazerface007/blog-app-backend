from flask import Flask, app, request, jsonify
import os
from dotenv import load_dotenv
load_dotenv()
from .db import db
from config import Config
from flask_migrate import Migrate



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


    # Add Error Handlers

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "error": "Not Found",
            "message": "The requested resource does not exist"
        }), 404
    return app