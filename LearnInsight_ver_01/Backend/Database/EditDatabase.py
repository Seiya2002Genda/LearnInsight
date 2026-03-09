from LearnInsight_ver_01.Backend.Database.ConnectDatabase import ConnectDatabase


class EditDatabase:
    def __init__(self):
        self.db = ConnectDatabase()
        self.connection = self.db.connect()
        self.cursor = self.connection.cursor()

    def update_record(self, table, column, value, record_id):
        allowed_tables = ["users", "user_information", "learning_information"]
        if table not in allowed_tables:
            return False

        query = f"UPDATE {table} SET {column} = %s WHERE id = %s"
        self.cursor.execute(query, (value, record_id))
        self.connection.commit()
        return self.cursor.rowcount > 0

    def update_multiple_columns(self, table, data, record_id):
        allowed_tables = ["users", "user_information", "learning_information"]
        if table not in allowed_tables or not data:
            return False

        set_clause = ", ".join([f"{key} = %s" for key in data.keys()])
        values = list(data.values())
        values.append(record_id)

        query = f"UPDATE {table} SET {set_clause} WHERE id = %s"
        self.cursor.execute(query, tuple(values))
        self.connection.commit()
        return self.cursor.rowcount > 0

    def close(self):
        self.cursor.close()
        self.db.close()