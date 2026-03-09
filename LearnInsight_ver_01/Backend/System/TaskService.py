from LearnInsight_ver_01.Backend.Database.ConnectDatabase import ConnectDatabase


class TaskService:

    def get_tasks(self,user_id):

        db = ConnectDatabase()

        conn = db.connect()

        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM tasks WHERE user_id=%s",(user_id,))

        tasks = cursor.fetchall()

        cursor.close()

        conn.close()

        return tasks

    def add_task(self,user_id,task):

        db = ConnectDatabase()

        conn = db.connect()

        cursor = conn.cursor()

        query = "INSERT INTO tasks(user_id,task,status) VALUES(%s,%s,'pending')"

        cursor.execute(query,(user_id,task))

        conn.commit()

        cursor.close()

        conn.close()