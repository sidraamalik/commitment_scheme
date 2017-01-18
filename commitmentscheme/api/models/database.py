import pymysql


class DBAdapter(object):
    def __init__(self, db_credentials):
        self.credentials = db_credentials
        self.connect()
        self.message = "Error Code: {0}. Query: {1}. Error: {2}."

    def connect(self):
        self.connection = pymysql.connect(
            host=self.credentials["host"],
            user=self.credentials["username"],
            passwd=self.credentials["password"],
            db=self.credentials["database"],
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=False)

    def reconnect(self):
        self.connect()

    def query(self, query, params=None):
        cursor = self.connection.cursor()
        if params is None:
            cursor.execute(query)
        else:
            cursor.execute(query, params)

        result = cursor.fetchall()
        cursor.close()

        if not result:
            result = {}

        return result

    def execute(self, query, params=None):
        cursor = self.connection.cursor()
        if params is None:
            result = cursor.execute(query)
        else:
            result = cursor.execute(query, params)
        cursor.close()

        return result

    def commit(self):
        self.connection.commit()

    def begin(self):
        self.connection.begin()

    def rollback(self):
        self.connection.rollback()

    def affected_rows(self):
        return self.connection.affected_rows()

    def get_insert_id(self):
        return self.connection.insert_id()
