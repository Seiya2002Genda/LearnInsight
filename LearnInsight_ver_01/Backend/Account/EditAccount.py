import mysql.connector
from mysql.connector import Error

class EditAccount:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root1234",
            database="learninsight"
        )
        self.cursor = self.connection.cursor(dictionary=True)

    def update_username(self, user_id, new_username):
        query = "UPDATE users SET username = %s WHERE id = %s"
        self.cursor.execute(query, (new_username, user_id))
        self.connection.commit()
        return self.cursor.rowcount > 0

    def update_email(self, user_id, new_email):
        query = "UPDATE users SET email = %s WHERE id = %s"
        self.cursor.execute(query, (new_email, user_id))
        self.connection.commit()
        return self.cursor.rowcount > 0

    def update_password(self, user_id, hashed_password):
        query = "UPDATE users SET password = %s WHERE id = %s"
        self.cursor.execute(query, (hashed_password, user_id))
        self.connection.commit()
        return self.cursor.rowcount > 0

    def update_role(self, user_id, new_role):
        query = "UPDATE users SET role = %s WHERE id = %s"
        self.cursor.execute(query, (new_role, user_id))
        self.connection.commit()
        return self.cursor.rowcount > 0

    def edit_account(self, user_id, username=None, email=None, password=None, role=None):
        updates = []
        values = []

        if username:
            updates.append("username = %s")
            values.append(username)
        if email:
            updates.append("email = %s")
            values.append(email)
        if password:
            updates.append("password = %s")
            values.append(password)
        if role:
            updates.append("role = %s")
            values.append(role)

        if not updates:
            return False

        query = f"UPDATE users SET {', '.join(updates)} WHERE id = %s"
        values.append(user_id)
        self.cursor.execute(query, tuple(values))
        self.connection.commit()
        return self.cursor.rowcount > 0

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()