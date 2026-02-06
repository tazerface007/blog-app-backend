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

    def to_dict(self):
        """Convert object to a dictionary for JSON serialization."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'slug': self.slug,
            'github_path': self.github_path,
            # Convert datetime to ISO format string
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_published': self.is_published
        }