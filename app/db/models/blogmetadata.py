from app.db import db

from datetime import datetime,timezone

class BlogMetadata(db.Model):
    __tablename__ = 'blogmetadata'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    slug = db.Column(db.String(500), unique=True, nullable=False)
    github_path = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    is_published = db.Column(db.Boolean, default=False) 