# Flask Migration setup
from flask import Flask
from app import create_app, db
from flask_migrate import Migrate, upgrade
from app.db.models import *

app = create_app()
migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run(debug=True)