from flask import Blueprint, request, jsonify
login_bp = Blueprint('login', __name__, url_prefix='/login')

@login_bp.route('/', methods=['GET'])
def login_route():
    return jsonify({"message": "Welcome to the Login Route!"})


@login_bp.route('/authenticate', methods=['POST'])
def authenticate_user():
    login_info = request.json
    # Placeholder for authentication logic
    if not login_info.get('username') or not login_info.get('password'):
        return jsonify({"message": "Invalid login data"}), 400

    # Here you would typically check the username and password against the database
    # For demonstration, we will just return a success message
    return jsonify({"message": f"User {login_info['username']} authenticated successfully!"})
    

@login_bp.route('/mock', methods=['GET'])
def mock_login():
    # Placeholder for mock login logic
    mock_user = {
        "username": "mockuser",
        "password": "mockpassword"
    }
    return jsonify(mock_user)

@login_bp.route('/logout', methods=['POST'])
def logout_user():
    # Placeholder for logout logic
    return jsonify({"message": "User logged out successfully!"})