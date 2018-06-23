from app import *
from app.models import Users
from pprint import pprint

@app.route("/api/v1/auth/signup", methods=['POST'])
def register_user():
    if not request.json:
        return jsonify({
            "message": "invalid request"
        }), 400

    if 'username' not in request.json:
        return jsonify({
            "message": "username is missing"
        }), 400

    if 'email' not in request.json:
        return jsonify({
            "message": "email is missing"
        }), 400

    if 'password' not in request.json:
        return jsonify({
            "message": "password is missing"
        }), 400

    field = request.get_json()

    username = field['username']
    email = field['email']
    password = generate_password_hash(field['password'], method='sha256')

    user = Users()
    if user.is_registed("WHERE email='"+email+"'"):
        return jsonify({
            "message": "user already registered"
        }), 409

    if user.register(username, email, password):
        return jsonify({
            "message": "user registred successfully"
        }), 201

    return jsonify({
        "message": "user registeration failed"
    }), 400


@app.route("/api/v1/auth/login", methods=['POST'])
def login_user():
    auth = request.authorization
    if not auth:
        return jsonify({
            'message': 'Could not verify user',
            'WWW-Authenticate': 'Basic realm="Login required"'
        }), 401

    if not auth.username or not auth.password:
        return jsonify({
            'message': 'Could not verify user',
            'WWW-Authenticate': 'Basic realm="Login required"'
        }), 401

    if auth.username == "":
        return jsonify({
            'message': 'username is empty'
        }), 400

    if auth.password == "":
        return jsonify({
            'message': 'password is empty'
        }), 400

    user = Users()
    user_data = user.fetch_user(auth.username)
    if not user:
        return jsonify({
            "message": "user doesnot exist"
        }), 404
    pprint(user_data)
    if check_password_hash(user_data[3], auth.password):
        token = jwt.encode({'id': user_data[0], 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(minutes=1140)}, app.config['SECRET_KEY'])
        return jsonify({
            'token':token.decode('UTF-8'),
            'message':'user logged in successfully'
        }), 200
    
    return jsonify({
        'message':'username or password doesnot match'
    }), 401