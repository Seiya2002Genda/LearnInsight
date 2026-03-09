from LearnInsight_ver_01.Backend.Database.ConnectDatabase import ConnectDatabase


class InputUserInformation:
    def __init__(self):
        self.db = ConnectDatabase()
        self.connection = self.db.connect()
        self.cursor = self.connection.cursor()

    def input_user_data(self, user_id, full_name, age, school, grade_level):
        self.cursor.execute("SELECT id FROM user_information WHERE user_id = %s", (user_id,))
        existing = self.cursor.fetchone()

        if existing:
            query = """
            UPDATE user_information
            SET full_name = %s, age = %s, school = %s, grade_level = %s
            WHERE user_id = %s
            """
            self.cursor.execute(query, (full_name, age, school, grade_level, user_id))
            self.connection.commit()
            return existing[0]

        query = """
        INSERT INTO user_information (user_id, full_name, age, school, grade_level)
        VALUES (%s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, (user_id, full_name, age, school, grade_level))
        self.connection.commit()
        return self.cursor.lastrowid

    def get_user_information(self, user_id):
        cursor = self.connection.cursor(dictionary=True)
        query = "SELECT * FROM user_information WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        return cursor.fetchone()

    def close(self):
        self.cursor.close()
        self.db.close()