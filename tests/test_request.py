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

        self.assertEqual(self.updated_request['message'],"request updated successfully")
        self.assertEqual(self.updated_request['status_code'], 200)

    def test_admin_can_get_all_requests(self):
        """ test admin can get all requests """

        self.assertEqual(self.all_requests_admin['message'], "returned successfully")
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

    
