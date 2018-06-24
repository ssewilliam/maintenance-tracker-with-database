from base import *


class TestRequest(BaseTestCase):
    def test_user_can_create_requests(self):
        """ test if can create requests """
        self.register_user(
            "ssewilliam", "deriwilliams2008@gmail.com", "password")
        token = self.get_token()
        response = self.post(token, "fix the login button", "reapir",
                                     "When you click the login button it only returns you to the same page")                               
        response_data = json.loads(response.data.decode())
        self.assertEqual(response_data['message'],
                         'request created successfully')
        self.assertEqual(response.status_code, 201)
