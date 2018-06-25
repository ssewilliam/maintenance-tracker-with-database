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

    def post_request(self, token, r_title, r_type, r_body):
        """ use to post a request for alogged in user """

        self.request_data = {
            'title': r_title,
            'type': r_type,
            'description': r_body
        }

        return self.client.post(
            url_for('create_request'), data=json.dumps(self.request_data), content_type='application/json', headers=({"app-access-token": token}))

    def get_token(self):
        """ use to get token after login """

        response = self.login_user("ssewilliam", "password")
        token_data = json.loads(response.data.decode())
        return token_data['token']

    def get_requests(self, token):
        """ use to get requests of logged in user by using a token """

        return self.client.get(
            url_for('get_requests'), headers=({"app-access-token": token}))

    def get_request(self, token, requestId):
        """ use to get their requests by id"""

        return self.client.get(
            url_for('get_request', requestId=requestId), headers=({"app-access-token": token}))

    def update_request(self, token, requestId, r_title, r_type, r_body):
        """ use to update user's request """

        self.request_data = {
            'title': r_title,
            'type': r_type,
            'description': r_body
        }

        return self.client.put(
            url_for('put_request', requestId=requestId), data=json.dumps(self.request_data), content_type='application/json', headers=({"app-access-token": token}))

    def admin_get_requests(self, token):
        """ use to get requests for admin user by using a token """

        return self.client.get(
            url_for('get_requests_admin'), headers=({"app-access-token": token}))

    def admin_promote_user(self, token, username, email):
        """ use to promote a user to admin """

        self.promoted_user = {
            'username': username,
            'email': email
        }
        return self.client.put(url_for('promote_user'), data=json.dumps(
            self.promoted_user), content_type='application/json', headers=({"app-access-token": token}))

    def admin_approve_request(self, token, status, requestId):
        """ use to approve a user's request """

        return self.client.put(url_for('approve_request', requestId=requestId), data=json.dumps(dict(status=status)), headers=({'app-access-token': token}), content_type='application/json')
