from dbDriver import *


class Users(DatabaseConnection):
    __table__ = "users"

    def register(self, username, email, password):
        result = self.insert_record(self.__table__, "(username, email, password, admin)",
                           "('"+username+"', '"+email+"', '"+password+"', False)")
        if result:
            return True
        return False

    def is_registed(self,where_condition):
        result = self.fetch_all(self.__table__, where_condition)
        if result is not None:
            return True
        return False
