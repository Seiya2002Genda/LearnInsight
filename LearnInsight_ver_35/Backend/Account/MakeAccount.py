import hashlib
import mysql.connector


class MakeAccount:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root1234",
            database="learninsight"
        )
        self.cursor = self.connection.cursor(dictionary=True)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def username_exists(self, username):
        query = "SELECT id FROM users WHERE username = %s"
        self.cursor.execute(query, (username,))
        return self.cursor.fetchone() is not None

    def email_exists(self, email):
        query = "SELECT id FROM users WHERE email = %s"
        self.cursor.execute(query, (email,))
        return self.cursor.fetchone() is not None

    def create_account(self, username, password, email, role):
        if self.username_exists(username):
            return {"success": False, "message": "Username already exists"}
        if self.email_exists(email):
            return {"success": False, "message": "Email already exists"}

        hashed_password = self.hash_password(password)
        query = """
        INSERT INTO users (username, password, email, role)
        VALUES (%s, %s, %s, %s)
        """
        self.cursor.execute(query, (username, hashed_password, email, role))
        self.connection.commit()
        return {"success": True, "message": "Account Created", "user_id": self.cursor.lastrowid}

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()