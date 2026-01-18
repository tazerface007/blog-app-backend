from flask import Blueprint, request, jsonify

user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route('/', methods=['GET'])
def user_profile():
    return jsonify({"message": "Welcome to the User Profile Route!"})


@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    from app.db import db
    session = db.session()
    from app.db.models.usermodel import UserModel
    user = session.get(UserModel, user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    user_data = user.json()
    return jsonify(user_data)


@user_bp.route('/mock', methods=['GET'])
def mock_user():
    from app.db import db
    session = db.session()
    from app.db.models.usermodel import UserModel
    mock_user = UserModel(username="Deepak", email="deepak@example.com")
    session.add(mock_user)
    session.commit()
    return jsonify(mock_user.json())


@user_bp.route('/', methods=['POST'])
def create_user():
    user_info = request.json
    # Placeholder for user creation logic
    created_user = {"id": 1, "username": user_info.get("username"), "email": user_info.get("email")}
    return jsonify(created_user), 201