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

        """ test whether a user can duplicate their registration """
        dub_response = self.register_user(
            "angela", "angela.katumwa@gmail.com", "password")
        dub_response_data = json.loads(dub_response.data.decode())
        self.assertEqual(
            dub_response_data['message'], "user already registered")
        self.assertEqual(dub_response.status_code, 409)

    def test_user_can_login(self):
        """ test registered user can login """

        lg_response = self.login_user("ssewilliam", "password")
        lg_response_data = json.loads(lg_response.data.decode())
        self.assertEqual(
            lg_response_data['message'], "user logged in successfully")
        self.assertEqual(lg_response.status_code, 200)

    def test_can_promote_user_right(self):
        """ test if user can be promoted to admin """

        self.assertEqual(
            self.promoted_user['message'], "user promoted successfully")
        self.assertEqual(self.promoted_user['status_code'], 200)
