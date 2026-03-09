from LearnInsight_ver_01.Backend.Database.ConnectDatabase import ConnectDatabase


class InputLearningInformation:
    def __init__(self):
        self.db = ConnectDatabase()
        self.connection = self.db.connect()
        self.cursor = self.connection.cursor()

    def input_learning_data(self, user_id, subject, study_time, score, learning_date):
        query = """
        INSERT INTO learning_information (user_id, subject, study_time, score, learning_date)
        VALUES (%s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, (user_id, subject, study_time, score, learning_date))
        self.connection.commit()
        return self.cursor.lastrowid

    def get_learning_data_by_user(self, user_id):
        query = """
        SELECT id, user_id, subject, study_time, score, learning_date, created_at, updated_at
        FROM learning_information
        WHERE user_id = %s
        ORDER BY learning_date ASC, id ASC
        """
        self.cursor = self.connection.cursor(dictionary=True)
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.db.close()