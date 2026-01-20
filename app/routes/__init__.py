from flask import Blueprint

from .homeroute import home_bp
from .userroute import user_bp
from .blogroute import blog_bp
from .analytics import analytics_bp

api_bp = Blueprint('api', __name__, url_prefix='/api')

api_bp.register_blueprint(home_bp)
api_bp.register_blueprint(user_bp)
api_bp.register_blueprint(blog_bp)
api_bp.register_blueprint(analytics_bp)