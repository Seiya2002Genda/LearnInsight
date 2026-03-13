import mysql.connector

class CreateDatabase:

    def __init__(self):
        self.connection=mysql.connector.connect(
            host="localhost",
            user="root",
            password="root1234"
        )
        self.cursor=self.connection.cursor()

    def column_exists(self,table,column):
        self.cursor.execute(f"SHOW COLUMNS FROM {table} LIKE '{column}'")
        return self.cursor.fetchone() is not None

    def add_column_if_not_exists(self,table,column,definition):
        if not self.column_exists(table,column):
            self.cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")

    def create_database(self):

        self.cursor.execute("CREATE DATABASE IF NOT EXISTS learninsight")
        self.cursor.execute("USE learninsight")

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) UNIQUE,
            password VARCHAR(255),
            email VARCHAR(150) UNIQUE,
            role VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS classes(
            id INT AUTO_INCREMENT PRIMARY KEY,
            class_name VARCHAR(200) NOT NULL,
            teacher_name VARCHAR(100) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS class_memberships(
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            class_name VARCHAR(200) NOT NULL,
            teacher_name VARCHAR(100) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS class_requests(
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            username VARCHAR(100),
            class_name VARCHAR(200),
            teacher_name VARCHAR(100),
            status VARCHAR(50) DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS learning_information(
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            class_name VARCHAR(200),
            subject VARCHAR(200),
            study_time FLOAT,
            score FLOAT,
            learning_date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS assignments(
            id INT AUTO_INCREMENT PRIMARY KEY,
            teacher_name VARCHAR(100) NOT NULL,
            class_name VARCHAR(200) NOT NULL,
            title VARCHAR(255),
            description TEXT,
            url VARCHAR(500),
            file_path VARCHAR(500),
            due_date DATETIME,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS assignment_submissions(
            id INT AUTO_INCREMENT PRIMARY KEY,
            assignment_id INT NOT NULL,
            student_name VARCHAR(100) NOT NULL,
            class_name VARCHAR(200),
            comment TEXT,
            file_path VARCHAR(255),
            grade FLOAT,
            status VARCHAR(50) DEFAULT 'submitted',
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS support_chat(
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT NOT NULL,
            teacher_name VARCHAR(100) NOT NULL,
            sender VARCHAR(20) NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS discussion_topics(
            id INT AUTO_INCREMENT PRIMARY KEY,
            class_name VARCHAR(200) NOT NULL,
            title VARCHAR(255) NOT NULL,
            created_by VARCHAR(100) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS discussion_messages(
            id INT AUTO_INCREMENT PRIMARY KEY,
            topic_id INT NOT NULL,
            message TEXT,
            sender VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        self.add_column_if_not_exists("class_memberships","class_name","VARCHAR(200) NOT NULL DEFAULT ''")
        self.add_column_if_not_exists("class_memberships","teacher_name","VARCHAR(100) NOT NULL DEFAULT ''")
        self.add_column_if_not_exists("class_requests","username","VARCHAR(100)")
        self.add_column_if_not_exists("class_requests","class_name","VARCHAR(200)")
        self.add_column_if_not_exists("class_requests","teacher_name","VARCHAR(100)")
        self.add_column_if_not_exists("class_requests","status","VARCHAR(50) DEFAULT 'pending'")
        self.add_column_if_not_exists("learning_information","class_name","VARCHAR(200)")
        self.add_column_if_not_exists("assignments","class_name","VARCHAR(200) NOT NULL DEFAULT ''")
        self.add_column_if_not_exists("assignment_submissions","class_name","VARCHAR(200)")
        self.add_column_if_not_exists("assignment_submissions","grade","FLOAT")

        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS llm_chat_logs
                            (
                                id
                                INT
                                AUTO_INCREMENT
                                PRIMARY
                                KEY,
                                user_id
                                INT
                                NOT
                                NULL,
                                role
                                VARCHAR
                            (
                                50
                            ),
                                message TEXT,
                                response TEXT,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                                )
                            """)

        self.connection.commit()
        return True

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()