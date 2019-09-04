from app import *
from app.models import Users, Requests

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
            "message": "email already registered",
            "username": username,
            "email": email,
        }), 409

    if user.is_registed("WHERE username='"+username+"'"):
        return jsonify({
            "message": "username already registered",
            "username": username,
            "email": email,
        }), 409

    if user.register(username, email, password):
        return jsonify({
            "message": "user registred successfully",
            "username": username,
            "email": email,
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
            'WWW-Authenticate': "Basic realm='Login required'"
        }), 401

    if not auth.username or not auth.password:
        return jsonify({
            'message': 'Could not verify user',
            'WWW-Authenticate': "Basic realm='Login required'"
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
    if not user_data:
        return jsonify({
            "message": "unknown user name or password"
        }), 401


    if check_password_hash(user_data[3], auth.password):
        token = jwt.encode({'uid': user_data[0], 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(minutes=1140)}, app.config['SECRET_KEY'])
        return jsonify({
            'token': token.decode('UTF-8'),
            'message': 'user logged in successfully',
            "is_admin": user_data[4]
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

    r_type = field['type'].lower()
    r_title = field['title'].lower()
    r_description = field['description']
    r_date = str(datetime.datetime.utcnow())
    user_id = str(current_user[0])
    if re.compile("[~!@#$%^&*()-_=+}{]").search(r_title) or r_title =="":
        return jsonify({
            "message":"request title is not valid",
            "user": r_title,
        }),400

    if re.compile("[~!@#$%^&*()-_=+}{]").search(r_type) or r_type == "":
        return jsonify({
            "message":"request type is not valid"
        }),400

    if r_type not in ("repair","maintenance"):
        return jsonify({
            "message":"request type is not valid use repair or maintenance"
        }),400

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

    if _requests is False:
        return jsonify({
            "message":"you have no requests"
        }), 400

    results = []
    for _request in _requests:
        this_request = {
            'id': _request[0],
            'type': _request[2],
            'title': _request[3],
            'description': _request[4],
            'status': _request[6]
        }
        results.append(this_request)
    return jsonify({
        'requests': results,
        'status':'OK',
        'message':'returned successfully'
    }), 200


@app.route("/api/v1/users/requests/<int:requestId>", methods=['GET'])
@token_required
def get_request(current_user, requestId):
    user_id = current_user[0]

    _request = Requests()
    _request = _request.fetch_request_by_id(user_id, requestId)

    if not _request:
        return jsonify({
            'status': 'unkown request id',
            'message': 'request does not exist'
        }), 400
    results = []
    this_request = {
        'id': _request[0],
        'type': _request[2],
        'title': _request[3],
        'description': _request[4],
        'create_date': _request[5],
        'status': _request[6]
    }
    results.append(this_request)
    return jsonify({
        'requests': results,
        'status': 'OK',
        'message':'returned successfully'
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

    r_type = field['type'].lower()
    r_title = field['title'].lower()
    r_description = field['description']
    user_id = str(current_user[0])
    requestId = str(requestId)

    if re.compile("[~!@#$%^&*()-_=+}{]").search(r_title) or r_title == "":
        return jsonify({
            "message": "request title is not valid",
            "user": r_title,
        }), 400

    if re.compile("[~!@#$%^&*()-_=+}{]").search(r_type) or r_type == "":
        return jsonify({
            "message": "request type is not valid"
        }), 400

    if r_type not in ("repair","maintenance"):
        return jsonify({
            "message":"request type is not valid use reapir or maintanance"
        }),400


    _request = Requests()
    request_data = _request.fetch_request_by_id(user_id, requestId)
    if not request_data:
        return jsonify({'message': 'updating request failed, user and request combination doesnot exist'}), 400

    current_status = request_data[6]
    if request_data and current_status == "pending":
        return jsonify({'message': 'request not yet approved'}), 400

    if request_data and current_status == "resolved":
        return jsonify({'message': 'request already resolved'}), 400

    if request_data and current_status == "disapproved":
        return jsonify({'message': 'can not update disapproved request'}), 400

    result = _request.update_request(
        user_id, requestId, r_type, r_title, r_description)

    if result:
        return jsonify({'message': 'request updated successfully'}), 200


@app.route("/api/v1/users", methods=['PUT'])
def promote_user():

    if not request.json:
        return jsonify({
            "message": "request is invalid"
        }), 400

    field = request.get_json()
    if 'promoUsername' not in request.json or field['promoUsername'] == "":
        return jsonify({
            "message": "username is invalid"
        }), 400

    if 'promoEmail' not in request.json or field['promoEmail'] == "":
        return jsonify({
            "message": "email is invalid"
        }), 400

    user = Users()
    user_data = user.fetch_user_with_email(field['promoUsername'],field['promoEmail'])
    if not user_data:

        return jsonify({
            "message":"user does not exist"
        }),400

    user_id = str(user_data[0])

    if user.modify_user(user_id):
        return jsonify({
            "message": "user promoted successfully",
        }), 200

    return jsonify({
        "message": "user promotion failed",
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
        "message":"returned successfully",
        "requests": request_list,
        "counts":len(request_list)
    }), 200


@app.route("/api/v1/requests/<requestId>", methods=['PUT'])
@token_required
def manage_request(current_user, requestId):
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
    if not request.json:
        return jsonify({
            "message": "invalid request"
        }), 400

    field = request.get_json()
    if field['status'] not in ("approve", "resolve", "disapprove"):
        return jsonify({
            "message": "status not valid",
            "help tip": "please use 'approve',resolve or disapprove"
        }), 400

    new_request = _request.update_record(
        "requests", "status='"+field['status']+"d'", "id="+requestId+"")

    if new_request:
        return jsonify({
            "message": "request "+field['status']+"d successfully"
        }), 200
    return jsonify({
        "message": "request not "+field['status'] + "d"
    }), 400


@app.route("/api/server-down",methods=['POST'])
def under_maintenance():
    abort(500)

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({
        'message': 'method used is invalid',
        'status': 'FAILED'
    }), 405


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({
        'message': 'this page doesnot exist',
        'status': 'FAIL'
    }), 404


@app.errorhandler(500)
def server_down(e):
    return jsonify({
        'message': 'server is under maintenance and unable to process your request',
        'status': 'SERVER DOWN'
    }), 500
