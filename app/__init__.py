from flask import Flask, app, request, jsonify
import os
from dotenv import load_dotenv
load_dotenv()
from .db import db
from app.utils.task_scheduler import scheduler
from config import Config
from flask_migrate import Migrate
from flask_cors import CORS



migrate = Migrate()

def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    app.config.from_object(Config)
    db.init_app(app)
    scheduler.init_app(app)
    scheduler.start()
    migrate.init_app(app, db)
    from app.db.models.usermodel import UserModel
    from app.db.models.blogmetadata import BlogMetadata
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