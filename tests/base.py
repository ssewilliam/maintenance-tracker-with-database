import json
import unittest
from flask import Flask
from pprint import pprint
from app import app, datetime

app.config.from_object('config.DevelopmentConfig')

from app.views import *
from dbDriver import db


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        """ This is the requests test predifined values """

        self.client = app.test_client()
        self.app_context = app.test_request_context()
        self.app_context.push()
        db.create_tables()

    def tearDown(self):
        db.drop_tables()
        # pass

    def register_user(self, username, email, password):
        """ use to register a demo user """

        return self.client.post(
            url_for('register'), data=json.dumps(dict(username=username, email=email, password=password)), content_type='application/json')

    def login_user(self, username, password):
        """ use to login registered users """
        self.demo_user = {
            'username': username,
            'password': password
        }

        return self.client.post(
            url_for('login'), data=json.dumps(self.demo_user),  headers={'Authorization': 'Basic c3Nld2lsbGlhbTpwYXNzd29yZA =='})
