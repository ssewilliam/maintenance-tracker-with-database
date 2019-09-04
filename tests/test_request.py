from base import *


class TestRequest(BaseTestCase):
    def test_user_can_create_requests(self):
        """ test if can create requests """
        
        self.assertEqual(self.posted_request['message'],
                         'request created successfully')
        self.assertEqual(self.posted_request['status_code'], 201)

        # trying to duplicate the request
        response = self.post_request(self.token, "fix the power button",
                                     "repair", "the laptop can turn on")
        self.assertEqual(response['message'],
                         'request title already used')
        self.assertEqual(response['status_code'], 409)

        
        # trying to create request with out token
        response = self.post_request("", "fix the power button",
                                     "repair", "the laptop can turn on")
        self.assertEqual(response['message'],
                         'token is missing')
        self.assertEqual(response['status_code'], 401)

        # trying to create request with expired token
        response = self.post_request("am-expired", "fix the power button",
                                     "repair", "the laptop can turn on")
        self.assertEqual(response['message'],
                         'token is invalid')
        self.assertEqual(response['status_code'], 401)

        # trying to create request with invalid characters in title
        response = self.post_request(self.token, "#fix the power button",
                                     "repair", "the laptop can turn on")
        self.assertEqual(response['message'],
                         'request title is not valid')
        # self.assertEqual(response['status_code'], 400)

        # trying to create request with invalid characters in type
        response = self.post_request(self.token, "fix the power button",
                                     "repair$", "the laptop can turn on")
        self.assertEqual(response['message'],
                         'request type is not valid')
        self.assertEqual(response['status_code'], 400)

        # trying to create request with invalid request type
        response = self.post_request(self.token, "replace the laptop screen",
                                     "repairsds", "the laptop can turn on")
        self.assertEqual(response['message'],
                         'request type is not valid use repair or maintenance')
        self.assertEqual(response['status_code'], 400)

        # trying to create request with out request type
        responsed = self.post_request(self.token, "",
                                     "repair", "the laptop can turn on")
        self.assertEqual(responsed['message'],
                         'request title is not valid')
        self.assertEqual(responsed['status_code'], 400)

    def test_user_can_get_requests(self):
        """ test if user can get all created requests """

        self.assertEqual(self.all_requests['message'], 'returned successfully')
        self.assertEqual(self.all_requests['status_code'], 200)

        # trying to get requests with out token
        response = self.get_requests("")
        self.assertEqual(response['message'],
                         'token is missing')
        self.assertEqual(response['status_code'], 401)

        # trying to get requests with expired token
        response = self.get_requests("am-expired")
        self.assertEqual(response['message'],
                         'token is invalid')
        self.assertEqual(response['status_code'], 401)

        # tying to get requests without posting any
        
    def test_user_can_get_request(self):
        """ test if user can get a created request """

        self.assertEqual(self.one_request['message'], 'returned successfully')
        self.assertEqual(self.one_request['status'], 'OK')
        self.assertEqual(self.one_request['status_code'], 200)

        # trying to get a request with out token
        response = self.get_request("",1)
        self.assertEqual(response['message'],
                         'token is missing')
        self.assertEqual(response['status_code'], 401)

        # trying to get a request with expired token
        response = self.get_request("am-expired",1)
        self.assertEqual(response['message'],
                         'token is invalid')
        self.assertEqual(response['status_code'], 401)

    def test_user_can_update_requests(self):
        """ test user can update their requests """

        self.assertEqual(
            self.updated_request['message'], "request updated successfully")
        self.assertEqual(self.updated_request['status_code'], 200)

        # can user update an un approved request : no
        self.post_request(self.token, "update the graphics drivers",
                          "repair", "the laptop graphics are not upto date")
        result_data = self.update_request(
            self.token, 2, "fix the power button", "repair", "the laptop can turn on or off using this button")

        self.assertEqual(result_data['message'], "request not yet approved")
        self.assertEqual(result_data['status_code'], 400)

        # can user update a  disapproved request : no
        self.admin_manage_request(self.token, "disapprove", '2')

        result_data = self.update_request(
            self.token, 2, "fix the power button", "repair", "the laptop can turn on or off using this button")

        self.assertEqual(result_data['message'],
                         "can not update disapproved request")
        self.assertEqual(result_data['status_code'], 400)

        
        # can user update a request with an invalid title
        result_data = self.update_request(
            self.token, 1, "fix the keyboard%", "repair", "the laptop can turn on or off using this button")

        self.assertEqual(result_data['message'], "request title is not valid")
        self.assertEqual(result_data['status_code'], 400)

        # can user update a request with no title
        result_data = self.update_request(
            self.token, 1, "", "repair", "the laptop can turn on or off using this button")

        self.assertEqual(result_data['message'], "request title is not valid")
        self.assertEqual(result_data['status_code'], 400)

        # can user update a request with an invalid character in type
        result_data = self.update_request(
            self.token, 1, "fix the power button", "repair@", "the laptop can turn on or off using this button")

        self.assertEqual(result_data['message'], "request type is not valid")
        self.assertEqual(result_data['status_code'], 400)

        # can user update a request with no type
        result_data = self.update_request(
            self.token, 1, "fix the power button", "", "the laptop can turn on or off using this button")

        self.assertEqual(result_data['message'], "request type is not valid")
        self.assertEqual(result_data['status_code'], 400)

        # can user update a request with an invalid type
        result_data = self.update_request(
            self.token, 1, "fix the power button", "repairmaintenance", "the laptop can turn on or off using this button")

        self.assertEqual(
            result_data['message'], "request type is not valid use reapir or maintanance")
        self.assertEqual(result_data['status_code'], 400)

    def test_admin_can_get_all_requests(self):
        """ test admin can get all requests """

        self.assertEqual(
            self.all_requests_admin['message'], "returned successfully")
        self.assertEqual(self.all_requests_admin['status_code'], 200)

    def test_admin_can_approve_request(self):
        """ test if admin can approve a request """

        self.assertEqual(self.approved_request['status_code'], 200)
        self.assertEqual(self.approved_request['message'],
                         "request approved successfully")

    def test_admin_can_resolve_request(self):
        """ test if admin can resolve a request """

        self.assertEqual(self.resolved_request['status_code'], 200)
        self.assertEqual(self.resolved_request['message'],
                         "request resolved successfully")

    def test_admin_can_disapprove_request(self):
        """ test if admin can disapprove a request """

        self.assertEqual(self.disapproved_request['status_code'], 200)
        self.assertEqual(self.disapproved_request['message'],
                         "request disapproved successfully")

    def test_unknown_route(self):
        """ test if app handles unknown urls """

        result = self.client.get("/user/request")

        result_data = json.loads(result.data.decode())
        self.assertEqual(result_data['message'], "this page doesnot exist")
        self.assertEqual(result.status_code, 404)

    def test_unsupported_method(self):
        """ test if app handles method not allowed errors """

        result = self.client.get(
            url_for('login'), headers=({"app-access-token": self.token}))
        result_data = json.loads(result.data.decode())
        self.assertEqual(result_data['message'], "method used is invalid")
        self.assertEqual(result.status_code, 405)

    def test_support_when_server_is_down(self):
        """ test if app supports handling server is down error"""

        result = self.client.get(
            url_for('under_maintenance'), headers=({"app-access-token": self.token}))
        result_data = json.loads(result.data.decode())
        self.assertEqual(result_data['message'], "method used is invalid")
        self.assertEqual(result.status_code, 405)
