from app.db import db
from datetime import datetime,timezone

class Subscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    subscription_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))