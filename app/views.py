from app import *
from app.models import Users, Requests
from pprint import pprint


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None

        if 'app-access-token' in request.headers:
            token = request.headers['app-access-token']

        if not token:
            return jsonify({
                'message': 'token is missing'
            }), 401

        try:
            user = Users()
            token_data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = user.fetch_user_by_id(token_data['uid'])
        except:
            return jsonify({
                'message': 'token is invalid'
            }), 401
        return func(current_user, *args, **kwargs)
    return decorated


@app.route("/api/v1/auth/signup", methods=['POST'])
def register():
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
def login():
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
    # pprint(user_data)
    if check_password_hash(user_data[3], auth.password):
        token = jwt.encode({'uid': user_data[0], 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(minutes=1140)}, app.config['SECRET_KEY'])
        return jsonify({
            'token': token.decode('UTF-8'),
            'message': 'user logged in successfully'
        }), 200

    return jsonify({
        'message': 'username or password doesnot match'
    }), 401


@app.route("/api/v1/users/requests", methods=['POST'])
@token_required
def create_request(current_user):
    if not request.json:
        return jsonify({
            "message": "request is invalid"
        }), 400

    if "title" not in request.json:
        return jsonify({
            "message": "title is missing"
        }), 400

    if "type" not in request.json:
        return jsonify({
            "message": "type is missing"
        }), 400

    if "description" not in request.json:
        return jsonify({
            "message": "body is missing"
        }), 400
    field = request.get_json()

    r_type = field['type']
    r_title = field['title']
    r_description = field['description']
    r_date = str(datetime.datetime.utcnow())
    user_id = str(current_user[0])

    _request = Requests()
    if _request.fetch_request(user_id, r_title):
        return jsonify({
            'message': 'request title already used'
        }), 409

    result = _request.insert_request(
        user_id, r_type, r_title, r_description, r_date)

    if result:
        return jsonify({'message': 'request created successfully'}), 201
    return jsonify({'message': 'creating request failed'}), 400


@app.route("/api/v1/users/requests", methods=['GET'])
@token_required
def get_requests(current_user):
    user_id = current_user[0]

    _requests = Requests()
    _requests = _requests.fetch_requests(user_id)

    results = []
    for _request in _requests:
        this_request = {
            'id': _request[0],
            'type': _request[1],
            'title': _request[2],
            'description': _request[3]
        }
        results.append(this_request)
    return jsonify({
        'requests': results
    }), 200


@app.route("/api/v1/users/requests/<int:requestId>", methods=['GET'])
@token_required
def get_request(current_user, requestId):
    user_id = current_user[0]

    _request = Requests()
    _request = _request.fetch_request_by_id(user_id, requestId)

    this_request = {
        'id': _request[1],
        'type': _request[2],
        'title': _request[3],
        'description': _request[4],
        'create date': _request[5]
    }
    return jsonify({
        'request': this_request,
        'status': 'OK'
    }), 200


@app.route("/api/v1/users/requests/<int:requestId>", methods=['PUT'])
@token_required
def put_request(current_user, requestId):
    if not request.json:
        return jsonify({
            "message": "request is invalid"
        }), 400

    if "title" not in request.json:
        return jsonify({
            "message": "title is missing"
        }), 400

    if "type" not in request.json:
        return jsonify({
            "message": "type is missing"
        }), 400

    if "description" not in request.json:
        return jsonify({
            "message": "body is missing"
        }), 400
    field = request.get_json()

    r_type = field['type']
    r_title = field['title']
    r_description = field['description']
    # r_date = str(datetime.datetime.utcnow())
    user_id = str(current_user[0])

    _request = Requests()
    result = _request.update_request(
        user_id, r_type, r_title, r_description)

    if result:
        return jsonify({'message': 'request updated successfully'}), 200
    return jsonify({'message': 'updating request failed'}), 400


@app.route("/api/v1/users", methods=['PUT'])
@token_required
def promote_user(current_user):

    if not request.json:
        return jsonify({
            "message": "request is invalid"
        }), 400

    field = request.get_json()
    if 'username' not in request.json or field['username'] == "":
        return jsonify({
            "message": "username is invalid"
        }), 400

    if 'email' not in request.json or field['email'] == "":
        return jsonify({
            "message": "email is invalid"
        }), 400

    user = Users()
    user_data = user.fetch_user(field['username'])
    # pprint(user_data)
    # pprint("user_data")
    # pprint(user_data[0])
    # admin_right = str(True)
    user_id = str(user_data[0])
    if user.modify_user(user_id):
        return jsonify({
            "message": "user promoted successfully",
        }), 200

    return jsonify({
        "message": "user promoted failed",
    }), 400


@app.route("/api/v1/requests", methods=['GET'])
@token_required
def get_requests_admin(current_user):

    is_admin = current_user[4]
    if is_admin is False:
        return jsonify({
            "message": "operation requires admin rights"
        }), 401

    _requests = Requests()
    total_results = _requests.fetch_all("requests")

    request_list = []
    for _request in total_results:
        this_request = {
            "id": _request[0],
            "user id": _request[1],
            "type": _request[2],
            "title": _request[3],
            "description": _request[4],
        }
        request_list.append(this_request)
    return jsonify({
        "requests": request_list
    }), 200


@app.route("/api/v1/requests/<requestId>", methods=['PUT'])
@token_required
def approve_request(current_user, requestId):
    is_admin = current_user[4]
    if is_admin is False:
        return jsonify({
            "message": "operation requires admin rights"
        }), 401

    _request = Requests()
    if not _request.fetch_one("requests", "WHERE id = "+requestId+""):
        return jsonify({
            "message": "request doesnot exist"
        }), 404

    field = request.get_json()
    if field['status'] not in ("approve", "resolve", "disapprove"):
        return jsonify({
            "message": "status not valid",
            "help tip": "please use 'approve',resolve or disapprove"
        }), 400

    new_request = _request.update_record(
        "requests", "status='"+field['status']+"'", "id="+requestId+"")
    if new_request:
        return jsonify({
            "message": "request "+field['status']+"d successfully"
        }), 200
    return jsonify({
        "message": "request not "+field['status'] + "d"
    }), 400
