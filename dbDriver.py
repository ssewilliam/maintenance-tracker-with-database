import psycopg2
from pprint import pprint
from app import app


class DatabaseConnection:
    database_url = app.config['DATABASE_URL']

    def __init__(self):
        try:
            self.connection = psycopg2.connect(self.database_url)
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
        except Exception as error:
            pprint(error)

    def create_tables(self):
        users_table = "CREATE TABLE IF NOT EXISTS users (id serial PRIMARY KEY,username varchar(50), email varchar(500), password varchar(500),admin bool)"
        request_table = "CREATE TABLE IF NOT EXISTS requests (id serial PRIMARY KEY, userid int, request_type varchar(25),request_title varchar(500), request_body varchar(500), request_date varchar(50),status varchar(25) DEFAULT 'pending' )"
        self.cursor.execute(users_table)
        self.cursor.execute(request_table)

    def insert_record(self, table, *args):
        insert_query = "INSERT INTO {} {} VALUES {}".format(
            table, args[0], args[1])
        if self.cursor.execute(insert_query) is None:
            return True
        return False

    def fetch_all(self, table, condition="ORDER BY id DESC"):
        select_query = "SELECT * FROM {} {}".format(table, condition)
        self.cursor.execute(select_query)
        total_results = self.cursor.fetchall()
        if total_results:
            return total_results
        return None

    def fetch_one(self, table, condition="ORDER BY id DESC"):
        select_query = "SELECT * FROM {} {}".format(table, condition)
        self.cursor.execute(select_query)
        total_results = self.cursor.fetchone()
        if total_results:
            return total_results
        return None

    def update_record(self, table, *args):
        update_query = "UPDATE {} SET {} WHERE {}".format(
            table, args[0], args[1])
        if self.cursor.execute(update_query) is None:
            return True
        return False

    def drop_tables(self):
        drop_users = "DROP TABLE users"
        drop_requests = "DROP TABLE requests"
        self.cursor.execute(drop_users)
        self.cursor.execute(drop_requests)


db = DatabaseConnection()
db.create_tables()
