from base import *


class TestUser(BaseTestCase):
    def test_user_can_register(self):
        """ tests whether a user can register successfully"""

        reg_response = self.register_user(
            "ssewilliam", "deriwilliams2008@gmail.com", "password")
        reg_response_data = json.loads(reg_response.data.decode())
        self.assertEqual(
            reg_response_data['message'], "user registred successfully")
        self.assertEqual(reg_response.status_code, 201)

        """ test whether a user can duplicate their registration """
        dup_response = self.register_user(
            "ssewilliam", "deriwilliams2008@gmail.com", "password")
        dup_response_data = json.loads(dup_response.data.decode())
        self.assertEqual(
            dup_response_data['message'], "user already registered")
        self.assertEqual(dup_response.status_code, 409)

    def test_user_can_login(self):
        """ test registered user can login """
        self.register_user(
            "ssewilliam", "deriwilliams2008@gmail.com", "password")
        lg_response = self.login_user("ssewilliam", "password")
        lg_response_data = json.loads(lg_response.data.decode())
        self.assertEqual(
            lg_response_data['message'], "user logged in successfully")
        self.assertEqual(lg_response.status_code, 200)

    def test_can_promote_user_right(self):
        """ test if user can be promoted to admin """

        self.register_user(
            "ssewilliam", "deriwilliams2008@gmail.com", "password")
        token = self.get_token()
        result = self.admin_promote_user(
            token, "ssewilliam", "deriwilliams2008@gmail.com")
        result_data = json.loads(result.data.decode())
        self.assertEqual(result_data['message'], "user promoted successfully")
        self.assertEqual(result.status_code, 200)
