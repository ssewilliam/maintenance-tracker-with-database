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

    def test_user_can_get_requests(self):
        """ test if user can get all created requests """

        self.assertEqual(self.one_request['message'], 'returned successfully')
        self.assertEqual(self.one_request['status'], 'OK')
        self.assertEqual(self.one_request['status_code'], 200)

    def test_user_can_get_request(self):
        """ test if user can get a created request """

        self.assertEqual(self.one_request['message'], 'returned successfully')
        self.assertEqual(self.one_request['status'], 'OK')
        self.assertEqual(self.one_request['status_code'], 200)

    def test_user_can_update_requests(self):
        """ test user can update their requests """

        self.assertEqual(
            self.updated_request['message'], "request updated successfully")
        self.assertEqual(self.updated_request['status_code'], 200)

        # can user updated an un approved request : no
        self.post_request(self.token, "update the graphics drivers",
                          "repair", "the laptop graphics are not upto date")
        result_data = self.update_request(
            self.token, 2, "fix the power button", "repair", "the laptop can turn on or off using this button")

        self.assertEqual(result_data['message'], "request not yet approved")
        self.assertEqual(result_data['status_code'], 400)

        # can user updated a disapproved request : no
        self.admin_manage_request(self.token, "disapprove", '2')

        result_data = self.update_request(
            self.token, 2, "fix the power button", "repair", "the laptop can turn on or off using this button")

        self.assertEqual(result_data['message'],
                         "can not update disapproved request")
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
