from app.db import db
from datetime import datetime

class Media(db.Model):
    __tablename__ = 'media'
    id = db.Column(db.Integer, primary_key=True)
    file_url = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50))  # image, table, pdf
    alt_text = db.Column(db.String(255))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
