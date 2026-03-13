from LearnInsight_ver_35.Backend.Database.ConnectDatabase import ConnectDatabase


class TrainData:

    def __init__(self):
        self.db = ConnectDatabase()

    def load_data(self):
        conn = self.db.connect()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                study_time,
                score
            FROM learning_information
            WHERE study_time IS NOT NULL
              AND score IS NOT NULL
        """)

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        x_data = []
        y_data = []

        for row in rows:
            study_time = row["study_time"]
            score = row["score"]

            try:
                study_time = float(study_time)
                score = float(score)
            except (TypeError, ValueError):
                continue

            x_data.append([study_time])
            y_data.append(score)

        return x_data, y_data