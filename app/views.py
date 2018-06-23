from app import *
from app.models import Users


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
    password = field['password']

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
