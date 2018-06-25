from base import *


class TestRequest(BaseTestCase):
    def test_user_can_create_requests(self):
        """ test if can create requests """

        self.register_user(
            "ssewilliam", "deriwilliams2008@gmail.com", "password")
        token = self.get_token()
        response = self.post_request(token, "fix the login button", "repair",
                                     "When you click the login button it only returns you to the same page")
        response_data = json.loads(response.data.decode())
        self.assertEqual(response_data['message'],
                         'request created successfully')
        self.assertEqual(response.status_code, 201)

        # trying to duplicate the request
        response = self.post_request(token, "fix the login button", "repair",
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
        self.post_request(token, "fix the power button",
                          "repair", "the laptop can turn on")
        result = self.get_requests(token)
        self.assertEqual(result.status_code, 200)

    def test_user_get_request(self):
        """ test if user can get created request """

        self.register_user(
            "ssewilliam", "deriwilliams2008@gmail.com", "password")
        token = self.get_token()
        self.post_request(token, "fix the power button",
                          "repair", "the laptop can turn on")

        response = self.get_request(token, 1)

        response_data = json.loads(response.data.decode())
        self.assertEqual(response_data['status'], 'OK')
        self.assertEqual(response.status_code, 200)

    def test_user_can_update_requests(self):
        """ test user can update their requests """

        self.register_user(
            "ssewilliam", "deriwilliams2008@gmail.com", "password")
        token = self.get_token()
        self.post_request(token, "fix the power button",
                          "repair", "the laptop can turn on")

        result = self.update_request(
            token, 1, "fix the power button", "repair", "the laptop can turn on or off using this button")
        self.assertEqual(result.status_code, 200)

    def test_admin_can_get_all_requests(self):
        """ test admin can get all requests """

        self.register_user(
            "ssewilliam", "deriwilliams2008@gmail.com", "password")
        token = self.get_token()
        self.post_request(token, "fix the power button",
                          "repair", "the laptop can turn on")
        self.post_request(token, "fix the power button",
                          "repair", "the laptop can turn on")

        self.admin_promote_user(token, "ssewilliam",
                                "deriwilliams2008@gmail.com")
        result = self.admin_get_requests(token)
        self.assertEqual(result.status_code, 200)

    def test_admin_can_approve_request(self):
        """ test if admin can approve a request """

        self.register_user(
            "ssewilliam", "deriwilliams2008@gmail.com", "password")
        token = self.get_token()
        self.post_request(token, "fix the power button",
                          "repair", "the laptop can turn on")
        self.admin_promote_user(token, "ssewilliam",
                                "deriwilliams2008@gmail.com")
        result = self.admin_approve_request(token,"approve",'1')
        result_data = json.loads(result.data.decode())
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result_data['message'], "request approved successfully")

    def test_admin_can_resolve_request(self):
        """ test if admin can resolve a request """

        self.register_user(
            "ssewilliam", "deriwilliams2008@gmail.com", "password")
        token = self.get_token()
        self.post_request(token, "fix the power button",
                          "repair", "the laptop can turn on")
        self.admin_promote_user(token, "ssewilliam",
                                "deriwilliams2008@gmail.com")
        result = self.admin_approve_request(token, "resolve", '1')
        result_data = json.loads(result.data.decode())
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result_data['message'],
                         "request resolved successfully")

    def test_admin_can_disapprove_request(self):
        """ test if admin can disapprove a request """

        self.register_user(
            "ssewilliam", "deriwilliams2008@gmail.com", "password")
        token = self.get_token()
        self.post_request(token, "fix the power button",
                          "repair", "the laptop can turn on")
        self.admin_promote_user(token, "ssewilliam",
                                "deriwilliams2008@gmail.com")
        result = self.admin_approve_request(token, "disapprove", '1')
        result_data = json.loads(result.data.decode())
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result_data['message'],
                         "request disapproved successfully")

    
