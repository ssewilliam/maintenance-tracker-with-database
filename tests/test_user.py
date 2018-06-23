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
