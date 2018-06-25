from base import *


class TestRequest(BaseTestCase):
    def test_user_can_create_requests(self):
        """ test if can create requests """

        self.register_user(
            "ssewilliam", "deriwilliams2008@gmail.com", "password")
        token = self.get_token()
        response = self.post_request(token, "fix the login button", "reapir",
                                     "When you click the login button it only returns you to the same page")
        response_data = json.loads(response.data.decode())
        self.assertEqual(response_data['message'],
                         'request created successfully')
        self.assertEqual(response.status_code, 201)

        # trying to duplicate the request
        response = self.post_request(token, "fix the login button", "reapir",
                                     "the button doesnot power off")
        response_data = json.loads(response.data.decode())
        self.assertEqual(response_data['message'],
                         'request title already used')
        self.assertEqual(response.status_code, 409)

    def test_user_can_get_requests(self):
        """ test if user can get created requests """
        
        self.register_user(
            "ssewilliam", "deriwilliams2008@gmail.com", "password")
        token = self.get_token()    
        self.post_request(token, "fix the power button", "reapir","the laptop can turn on")
        result = self.get_requests(token)
        self.assertEqual(result.status_code, 200)

    def test_user_get_request(self):
        """ test if user can get created request """

        self.register_user(
            "ssewilliam", "deriwilliams2008@gmail.com", "password")
        token = self.get_token()
        self.post_request(token, "fix the power button",
                          "reapir", "the laptop can turn on")

        response = self.get_request(token,1)

        response_data = json.loads(response.data.decode())
        self.assertEqual(response_data['status'], 'OK')
        self.assertEqual(response.status_code, 200)

    def test_user_can_update_requests(self):
        """ test user can update their requests """

        self.register_user(
            "ssewilliam", "deriwilliams2008@gmail.com", "password")
        token = self.get_token()
        self.post_request(token, "fix the power button",
                          "reapir", "the laptop can turn on")

        result = self.update_request(
            token, 1, "fix the power button", "repair", "the laptop can turn on or off using this button")
        self.assertEqual(result.status_code,200)