from LearnInsight_ver_01.Backend.Database.ConnectDatabase import ConnectDatabase


class EditUserInformation:
    def __init__(self):
        self.db = ConnectDatabase()
        self.connection = self.db.connect()
        self.cursor = self.connection.cursor()

    def edit_user_info(self, user_id, full_name=None, age=None, school=None, grade_level=None):
        self.cursor.execute("SELECT id FROM user_information WHERE user_id = %s", (user_id,))
        existing = self.cursor.fetchone()

        if existing:
            updates = []
            values = []

            if full_name is not None:
                updates.append("full_name = %s")
                values.append(full_name)
            if age is not None:
                updates.append("age = %s")
                values.append(age)
            if school is not None:
                updates.append("school = %s")
                values.append(school)
            if grade_level is not None:
                updates.append("grade_level = %s")
                values.append(grade_level)

            if not updates:
                return False

            values.append(user_id)
            query = f"UPDATE user_information SET {', '.join(updates)} WHERE user_id = %s"
            self.cursor.execute(query, tuple(values))
        else:
            query = """
            INSERT INTO user_information (user_id, full_name, age, school, grade_level)
            VALUES (%s, %s, %s, %s, %s)
            """
            self.cursor.execute(query, (user_id, full_name, age, school, grade_level))

        self.connection.commit()
        return True

    def close(self):
        self.cursor.close()
        self.db.close()