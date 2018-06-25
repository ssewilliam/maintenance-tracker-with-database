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

    def fetch_user_by_id(self, id):
        result = self.fetch_one(
            self.__table__, "WHERE id={}".format(id))
        if result:
            return result
        return False


class Requests(DatabaseConnection):
    __table__ = "requests"

    def insert_request(self, user_id, r_type, r_title, r_description, r_date):
        result = self.insert_record(self.__table__, "(userid, request_type, request_title, request_body, request_date)",
                                    "('"+user_id+"','"+r_type+"', '"+r_title+"', '"+r_description+"', '"+r_date+"')")
        if result:
            return True
        return False

    def fetch_request(self, user_id, title):
        result = self.fetch_one(
            self.__table__, "WHERE userid={} AND request_title = '{}'".format(user_id, title))
        if result:
            return result
        return False

    def fetch_requests(self,user_id):
        result = self.fetch_all(self.__table__,"WHERE userid={}".format(user_id))
        if result:
            return result
        return False

    def fetch_request_by_id(self, user_id, request_id):
        result = self.fetch_one(
            self.__table__, "WHERE userid={} AND id = '{}'".format(user_id, request_id))
        if result:
            return result
        return False

    def update_request(self, user_id, r_type, r_title, r_description):
        result = self.update_record(self.__table__, "request_type = '"+r_type +
                                        "', request_title = '"+r_title+"', request_body = '"+r_description+"'"," userid = "+user_id+"")
        if result:
            return True
        return False
