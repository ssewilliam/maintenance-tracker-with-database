from flask import Flask, jsonify, jsonify, request, url_for, abort
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import re
from functools import wraps
import datetime
from flask_cors import CORS, cross_origin
app = Flask(__name__)
CORS(app)

app.config.from_object('config.ProductionConfig')
