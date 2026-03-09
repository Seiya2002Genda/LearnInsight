from LearnInsight_ver_01.Backend.Database.ConnectDatabase import ConnectDatabase


class EditLearningInformation:
    def __init__(self):
        self.db = ConnectDatabase()
        self.connection = self.db.connect()
        self.cursor = self.connection.cursor()

    def edit_learning_info(self, learning_id, subject=None, study_time=None, score=None, learning_date=None):
        updates = []
        values = []

        if subject is not None:
            updates.append("subject = %s")
            values.append(subject)
        if study_time is not None:
            updates.append("study_time = %s")
            values.append(study_time)
        if score is not None:
            updates.append("score = %s")
            values.append(score)
        if learning_date is not None:
            updates.append("learning_date = %s")
            values.append(learning_date)

        if not updates:
            return False

        values.append(learning_id)
        query = f"UPDATE learning_information SET {', '.join(updates)} WHERE id = %s"
        self.cursor.execute(query, tuple(values))
        self.connection.commit()
        return self.cursor.rowcount > 0

    def close(self):
        self.cursor.close()
        self.db.close()