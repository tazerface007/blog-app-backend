from app.db import db
from datetime import datetime

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    intro = db.Column(db.String(500), nullable=False)
    content = db.Column(db.Text, nullable=False)


    status = db.Column(db.String(50), nullable=False, default='draft')

    # SEO
    # SEO
    meta_title = db.Column(db.String(255))
    meta_description = db.Column(db.String(300))
    meta_keywords = db.Column(db.String(255))

    # Relations
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))

    # Dates
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    published_at = db.Column(db.DateTime)

    is_featured = db.Column(db.Boolean, default=False)