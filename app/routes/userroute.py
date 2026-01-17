from flask import Blueprint, request, jsonify

user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route('/', methods=['GET'])
def user_profile():
    return jsonify({"message": "Welcome to the User Profile Route!"})