import mysql.connector


class ConnectDatabase:
    def __init__(self, database="learninsight"):
        self.database = database
        self.connection = None

    def connect(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database=self.database
        )
        return self.connection

    def cursor(self, dictionary=True):
        if self.connection is None or not self.connection.is_connected():
            self.connect()
        return self.connection.cursor(dictionary=dictionary)

    def close(self):
        if self.connection and self.connection.is_connected():

            self.connection.close()
