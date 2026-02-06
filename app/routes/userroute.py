from flask import Blueprint, json, request, jsonify
import jwt


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
    from app.db.models.usermodel import UserModel
    if not user_info.get('username') or not user_info.get('email'):
        return jsonify({"message": "Invalid user data"}), 400
    
    # sanitize and validate user_info here as needed
    email = str(user_info['email']).strip().lower()
    username = user_info['username'].strip()

    # validate username is already taken
    from app.db import db
    session = db.session()
    existing_user = session.query(UserModel).filter_by(username=username).first()
    if existing_user:
        return jsonify({"message": "Username already taken"}), 400

    if email.count('@') != 1:
        return jsonify({"message": "Invalid email format"}), 400

    new_user = UserModel(username=user_info['username'], email=user_info['email'])
    print(f'{repr(new_user)}')

    from app.db import db
    session = db.session()
    session.add(new_user)
    session.commit()
    created_user = new_user.json()
    return jsonify(created_user), 201

@user_bp.route('/getall', methods=['GET'])
def get_all_users():
    from app.db import db
    session = db.session()
    from app.db.models.usermodel import UserModel
    users = session.query(UserModel.username).all()
    users_list = [user[0] for user in users]
    return jsonify(users_list)


@user_bp.route('/login', methods=['POST'])
def login_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Generate token
    import jwt
    from flask import make_response

    token = jwt.encode({'username': username}, 'your_secret_key', algorithm='HS256')

    resp = make_response(jsonify({'message': 'Login successful'}))
    resp.set_cookie(
        'auth_token',
        token,
        httponly=True,
        samesite='Strict',
        path='/'
    )
    return resp