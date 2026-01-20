from flask import Blueprint, request, jsonify

blog_bp = Blueprint('blog', __name__, url_prefix='/blog')

@blog_bp.route('/', methods=['GET'])
def blog_home():
    return jsonify({"message": "Welcome to the Blog Route!"})