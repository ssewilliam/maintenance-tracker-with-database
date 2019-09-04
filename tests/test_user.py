from base import *


class TestUser(BaseTestCase):
    def test_user_can_register(self):
        """ tests whether a user can register successfully"""

        reg_response = self.register_user(
            "angela", "angela.katumwa@gmail.com", "password")
        reg_response_data = json.loads(reg_response.data.decode())
        self.assertEqual(
            reg_response_data['message'], "user registred successfully")
        self.assertEqual(reg_response.status_code, 201)

        #test whether a user can duplicate their registration
        dub_response = self.register_user(
            "angela", "angela.katumwa@gmail.com", "password")
        dub_response_data = json.loads(dub_response.data.decode())
        self.assertEqual(
            dub_response_data['message'], "email already registered")
        self.assertEqual(dub_response.status_code, 409)

    def test_user_can_login(self):
        """ test registered user can login """

        lg_response = self.login_user("ssewilliam", "password")
        lg_response_data = json.loads(lg_response.data.decode())
        self.assertEqual(
            lg_response_data['message'], "user logged in successfully")
        self.assertEqual(lg_response.status_code, 200)

    def test_unknown_user_login(self):
        """ test un registered user can login """

        self.unknown_demo_user = {
            "username":"ssembuusi",
            "password":"another password"
        }
        lg_response = self.client.post(
            url_for('login'), data=json.dumps(self.unknown_demo_user),  headers={'Authorization': 'Basic c3NlbWJ1dXNpOnBhc3N3b3Jk'})
        lg_response_data = json.loads(lg_response.data.decode())

        self.assertEqual(
            lg_response_data['message'], "unknown user name or password")
        self.assertEqual(lg_response.status_code, 401)

    def test_can_promote_user_right(self):
        """ test if user can be promoted to admin """

        self.assertEqual(
            self.promoted_user['message'], "user promoted successfully")
        self.assertEqual(self.promoted_user['status_code'], 200)
