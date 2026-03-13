from LearnInsight_ver_35.Backend.Database.ConnectDatabase import ConnectDatabase


class Setting:
    def __init__(self):
        self.db = ConnectDatabase()
        self.connection = self.db.connect()
        self.cursor = self.connection.cursor()

    def create_setting_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL UNIQUE,
            theme VARCHAR(50) DEFAULT 'light',
            language VARCHAR(50) DEFAULT 'english',
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """)
        self.connection.commit()
        return True

    def save_setting(self, user_id, theme, language):
        self.create_setting_table()
        self.cursor.execute("SELECT id FROM settings WHERE user_id = %s", (user_id,))
        existing = self.cursor.fetchone()

        if existing:
            query = "UPDATE settings SET theme = %s, language = %s WHERE user_id = %s"
            self.cursor.execute(query, (theme, language, user_id))
        else:
            query = "INSERT INTO settings (user_id, theme, language) VALUES (%s, %s, %s)"
            self.cursor.execute(query, (user_id, theme, language))

        self.connection.commit()
        return True

    def get_setting(self, user_id):
        self.create_setting_table()
        cursor = self.connection.cursor(dictionary=True)
        query = "SELECT * FROM settings WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        if result:
            return result
        return {"user_id": user_id, "theme": "light", "language": "english"}

    def close(self):
        self.cursor.close()
        self.db.close()