from flask import Flask, jsonify, jsonify, request, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import re
import datetime
app = Flask(__name__)

app.config.from_object('config.ProductionConfig')
