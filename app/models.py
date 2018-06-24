from dbDriver import *


class Users(DatabaseConnection):
    __table__ = "users"

    def register(self, username, email, password):
        result = self.insert_record(self.__table__, "(username, email, password, admin)",
                                    "('"+username+"', '"+email+"', '"+password+"', False)")
        if result:
            return True
        return False

    def is_registed(self, where_condition):
        result = self.fetch_all(self.__table__, where_condition)
        if result is not None:
            return True
        return False

    def fetch_user(self, username):
        result = self.fetch_one(
            self.__table__, "WHERE username='{}'".format(username))
        if result:
            return result
        return False

class Requests(DatabaseConnection):
    __table__ = "requests"

    def post_request(self, r_type, r_title, r_description, r_date):
        result = self.insert_record(self.__table__, "(request_type, request_title, request_body, request_date)",
                                    "('"+r_type+"', '"+r_title+"', '"+r_description+"', '"+r_date+"')")
        if result:
            return True
        return False
