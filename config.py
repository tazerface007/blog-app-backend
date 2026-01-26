import os

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///' + os.path.join(BASE_DIR,'instance', 'app.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.getenv("FLASK_DEBUG", "0").lower() in ("1", "true", "yes", "True")
    def __init__(self):
        print(Config.SQLALCHEMY_DATABASE_URI)
