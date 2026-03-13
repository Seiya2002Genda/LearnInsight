from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory

from LearnInsight_ver_35.Backend.Account.MakeAccount import MakeAccount

from LearnInsight_ver_35.Backend.Database.CreateDatabase import CreateDatabase
from LearnInsight_ver_35.Backend.Database.ConnectDatabase import ConnectDatabase

from LearnInsight_ver_35.Backend.Information.InputLearningInformation import InputLearningInformation

from LearnInsight_ver_35.Backend.LocalLargeLanguageModel.llm_engine import LocalLLMEngine

from LearnInsight_ver_35.Backend.MachineLearning.learning_model import LearningModel

from LearnInsight_ver_35.Backend.System.MakeLearningDataGraph import MakeLearningDataGraph
from LearnInsight_ver_35.Backend.System.MakeLearningReport import MakeLearningReport
from LearnInsight_ver_35.Backend.System.RecommendLearningPlan import RecommendLearningPlan
from LearnInsight_ver_35.Backend.System.Setting import Setting

import os
from werkzeug.utils import secure_filename
from flask import jsonify

app = Flask(__name__, template_folder="FrontEnd/templates", static_folder="FrontEnd/static")
app.secret_key = "learninsight_secret_key"

CreateDatabase().create_database()

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

learning_model = LearningModel()
llm_engine = LocalLLMEngine()

@app.route("/uploads/<path:filename>")
def download_file(filename):
    if not login_required():
        return redirect(url_for("login"))

    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename,
        as_attachment=False
    )

@app.route("/student/llm-chat", methods=["POST"])
def student_llm_chat():
    if not login_required():
        return jsonify({"reply": "Login required"})
    data = request.get_json()
    message = data.get("message")
    user = current_user()
    context = {
        "user_id": user["id"],
        "username": user["username"]
    }
    reply = llm_engine.generate(message, context)
    db = ConnectDatabase()
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO llm_chat_logs(user_id, role, message, response)
        VALUES(%s,%s,%s,%s)
    """,(user["id"],session["role"],message,reply))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({
        "reply": reply
    })

@app.route("/student/api/learning-summary")
def student_learning_summary_api():
    if not login_required():
        return jsonify({"error": "login required"})

    user = current_user()

    db = ConnectDatabase()
    conn = db.connect()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT AVG(grade) AS average_score
        FROM assignment_submissions
        WHERE student_name = %s
          AND grade IS NOT NULL
    """, (user["username"],))
    avg_result = cursor.fetchone()
    average_score = avg_result["average_score"] if avg_result and avg_result["average_score"] is not None else 0

    cursor.execute("""
        SELECT COUNT(*) AS total_records
        FROM class_memberships
        WHERE user_id = %s
    """, (user["id"],))
    record_result = cursor.fetchone()
    total_records = record_result["total_records"] if record_result else 0

    cursor.execute("""
        SELECT
            SUM(
                TIMESTAMPDIFF(
                    SECOND,
                    assignments.created_at,
                    assignment_submissions.submitted_at
                )
            ) AS total_study_time
        FROM assignment_submissions
        JOIN assignments
            ON assignments.id = assignment_submissions.assignment_id
        WHERE assignment_submissions.student_name = %s
    """, (user["username"],))
    study_result = cursor.fetchone()
    total_seconds = study_result["total_study_time"] if study_result and study_result["total_study_time"] is not None else 0

    cursor.close()
    conn.close()

    return jsonify({
        "average_score": round(float(average_score), 2),
        "total_records": total_records,
        "total_study_time": round(total_seconds / 3600, 2)
    })

def get_materials(user_id):
    db = ConnectDatabase()
    conn = db.connect()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT *
        FROM study_materials
        WHERE user_id = %s
        ORDER BY id DESC
    """, (user_id,))
    materials = cursor.fetchall()
    cursor.close()
    conn.close()
    return materials


def add_material(user_id, title, subject, link):
    db = ConnectDatabase()
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO study_materials(user_id, title, subject, link)
        VALUES(%s, %s, %s, %s)
    """, (user_id, title, subject, link))
    conn.commit()
    cursor.close()
    conn.close()


def delete_material(material_id):
    db = ConnectDatabase()
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM study_materials WHERE id=%s", (material_id,))
    conn.commit()
    cursor.close()
    conn.close()


def get_tasks(user_id):
    db = ConnectDatabase()
    conn = db.connect()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT *
        FROM tasks
        WHERE user_id = %s
        ORDER BY
            CASE
                WHEN status = 'pending' THEN 0
                ELSE 1
            END,
            id DESC
    """, (user_id,))
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    return tasks


def add_task(user_id, task):
    db = ConnectDatabase()
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tasks(user_id, task, status)
        VALUES(%s, %s, 'pending')
    """, (user_id, task))
    conn.commit()
    cursor.close()
    conn.close()


def delete_task(task_id):
    db = ConnectDatabase()
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=%s", (task_id,))
    conn.commit()
    cursor.close()
    conn.close()


def complete_task(task_id):
    db = ConnectDatabase()
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET status='completed' WHERE id=%s", (task_id,))
    conn.commit()
    cursor.close()
    conn.close()


def add_class_request(user_id, class_name, teacher_name):
    db = ConnectDatabase()
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO class_requests(user_id, class_name, teacher_name, status)
        VALUES(%s, %s, %s, 'pending')
    """, (user_id, class_name, teacher_name))
    conn.commit()
    cursor.close()
    conn.close()


def get_class_requests_by_user(user_id):
    db = ConnectDatabase()
    conn = db.connect()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT *
        FROM class_requests
        WHERE user_id = %s
        ORDER BY id DESC
    """, (user_id,))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


def get_all_class_requests():
    db = ConnectDatabase()
    conn = db.connect()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT class_requests.*, users.username
        FROM class_requests
        JOIN users
            ON users.id = class_requests.user_id
        ORDER BY class_requests.id DESC
    """)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


def get_teacher_class_requests(teacher_name):
    db = ConnectDatabase()
    conn = db.connect()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT class_requests.*, users.username
        FROM class_requests
        JOIN users
            ON users.id = class_requests.user_id
        WHERE class_requests.teacher_name = %s
        ORDER BY class_requests.id DESC
    """, (teacher_name,))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


def update_class_request(request_id, status):
    db = ConnectDatabase()
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE class_requests
        SET status = %s
        WHERE id = %s
    """, (status, request_id))
    conn.commit()
    cursor.close()
    conn.close()


def current_user():
    if "user_id" not in session:
        return None

    db = ConnectDatabase()
    conn = db.connect()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id=%s", (session["user_id"],))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user


def login_required():
    return "user_id" in session


def role_redirect(role):
    if role == "student":
        return redirect(url_for("student"))
    if role == "teacher":
        return redirect(url_for("teacher"))
    if role == "schooladministrator":
        return redirect(url_for("schooladministrator"))
    if role == "systemadministrator":
        return redirect(url_for("systemadministrator"))
    return redirect(url_for("dashboard"))


def get_support_messages_by_user(user_id):
    db = ConnectDatabase()
    conn = db.connect()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT id, user_id, teacher_name, message, sender, created_at
        FROM teaching_support
        WHERE user_id = %s
        ORDER BY created_at ASC, id ASC
    """, (user_id,))

    messages = cursor.fetchall()

    cursor.close()
    conn.close()

    return messages


def get_teacher_students_with_chat(teacher_name):
    db = ConnectDatabase()
    conn = db.connect()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT DISTINCT
            users.id AS user_id,
            users.username,
            class_memberships.class_name,
            (
                SELECT ts.message
                FROM teaching_support ts
                WHERE ts.user_id = users.id
                  AND ts.teacher_name = class_memberships.teacher_name
                ORDER BY ts.created_at DESC, ts.id DESC
                LIMIT 1
            ) AS last_message,
            (
                SELECT ts.sender
                FROM teaching_support ts
                WHERE ts.user_id = users.id
                  AND ts.teacher_name = class_memberships.teacher_name
                ORDER BY ts.created_at DESC, ts.id DESC
                LIMIT 1
            ) AS last_sender,
            (
                SELECT ts.created_at
                FROM teaching_support ts
                WHERE ts.user_id = users.id
                  AND ts.teacher_name = class_memberships.teacher_name
                ORDER BY ts.created_at DESC, ts.id DESC
                LIMIT 1
            ) AS last_created_at
        FROM class_memberships
        JOIN users
            ON users.id = class_memberships.user_id
        WHERE class_memberships.teacher_name = %s
        ORDER BY users.username ASC, class_memberships.class_name ASC
    """, (teacher_name,))

    students = cursor.fetchall()

    cursor.close()
    conn.close()

    return students
def build_student_dashboard_context(user, selected_teacher_name=None, topic_id=None):

    learner = InputLearningInformation()

    db = ConnectDatabase()
    conn = db.connect()
    cursor = conn.cursor(dictionary=True)

    records = learner.get_learning_data_by_user(user["id"])

    graph_service = MakeLearningDataGraph()
    graph = graph_service.create_graph(records)

    report_service = MakeLearningReport()
    report = report_service.generate_report(user, records)

    learning_summary = report_service.learning_summary(user, records)

    if records:
        avg = report.get("average_score", 0)
        study = report.get("total_study_time", 0)
    else:
        avg = 0
        study = 0

    recommendation_service = RecommendLearningPlan(learning_model)
    recommendation = recommendation_service.recommend(avg, study)

    tasks = get_tasks(user["id"])
    materials = get_materials(user["id"])
    class_requests = get_class_requests_by_user(user["id"])

    cursor.execute("""
        SELECT teacher_name, class_name
        FROM class_memberships
        WHERE user_id = %s
        ORDER BY class_name ASC, teacher_name ASC
    """, (user["id"],))
    teachers = cursor.fetchall()

    student_teachers = []

    for t in teachers:

        cursor.execute("""
            SELECT message, sender
            FROM teaching_support
            WHERE user_id = %s
              AND teacher_name = %s
            ORDER BY created_at DESC, id DESC
            LIMIT 1
        """, (user["id"], t["teacher_name"]))

        last = cursor.fetchone()

        student_teachers.append({
            "teacher_name": t["teacher_name"],
            "class_name": t["class_name"],
            "last_message": last["message"] if last else None,
            "last_sender": last["sender"] if last else None
        })

    cursor.execute("""
        SELECT
            assignments.id,
            assignments.teacher_name,
            assignments.class_name,
            assignments.title,
            assignments.description,
            assignments.url,
            assignments.file_path,
            assignments.due_date,
            assignments.created_at,
            CASE
                WHEN assignment_submissions.student_name IS NOT NULL THEN 1
                ELSE 0
            END AS submitted
        FROM class_memberships
        JOIN assignments
            ON assignments.class_name = class_memberships.class_name
           AND assignments.teacher_name = class_memberships.teacher_name
        LEFT JOIN assignment_submissions
            ON assignments.id = assignment_submissions.assignment_id
           AND assignment_submissions.student_name = %s
        WHERE class_memberships.user_id = %s
        ORDER BY assignments.created_at DESC
    """, (user["username"], user["id"]))

    assignments = cursor.fetchall()

    cursor.execute("""
        SELECT
            assignment_submissions.id,
            assignment_submissions.student_name,
            COALESCE(assignment_submissions.class_name, assignments.class_name) AS class_name,
            assignment_submissions.comment,
            assignment_submissions.file_path,
            assignment_submissions.submitted_at,
            assignment_submissions.grade,
            assignments.title
        FROM assignment_submissions
        JOIN assignments
            ON assignments.id = assignment_submissions.assignment_id
        WHERE assignment_submissions.student_name = %s
        ORDER BY assignment_submissions.submitted_at DESC
    """, (user["username"],))

    submissions = cursor.fetchall()

    # ================================
    # 追加統計
    # ================================

    cursor.execute("""
        SELECT AVG(grade) AS average_score
        FROM assignment_submissions
        WHERE student_name = %s
          AND grade IS NOT NULL
    """,(user["username"],))

    avg_result = cursor.fetchone()
    average_score = avg_result["average_score"] if avg_result["average_score"] else 0


    cursor.execute("""
        SELECT COUNT(*) AS total_records
        FROM class_memberships
        WHERE user_id = %s
    """,(user["id"],))

    rec_result = cursor.fetchone()
    total_records = rec_result["total_records"]


    cursor.execute("""
        SELECT
            SUM(
                TIMESTAMPDIFF(
                    SECOND,
                    assignments.created_at,
                    assignment_submissions.submitted_at
                )
            ) AS total_study_time
        FROM assignment_submissions
        JOIN assignments
            ON assignments.id = assignment_submissions.assignment_id
        WHERE assignment_submissions.student_name = %s
    """,(user["username"],))

    study_result = cursor.fetchone()

    total_seconds = study_result["total_study_time"] if study_result["total_study_time"] else 0
    total_study_time = round(total_seconds / 3600,2)

    report["average_score"] = round(average_score,2)
    report["total_records"] = total_records
    report["total_study_time"] = total_study_time

    learning_summary["average_score"] = report["average_score"]
    learning_summary["total_records"] = report["total_records"]
    learning_summary["total_study_time"] = report["total_study_time"]

    # ================================
    # Discussion
    # ================================

    cursor.execute("""
        SELECT id, title, created_by, created_at
        FROM discussion_topics
        ORDER BY created_at DESC, id DESC
    """)

    topics = cursor.fetchall()

    selected_topic = None
    messages = []

    if topic_id:

        cursor.execute("""
            SELECT *
            FROM discussion_topics
            WHERE id = %s
        """, (topic_id,))

        selected_topic = cursor.fetchone()

        if selected_topic:

            cursor.execute("""
                SELECT sender, message, created_at
                FROM discussion_messages
                WHERE topic_id = %s
                ORDER BY created_at ASC, id ASC
            """, (selected_topic["id"],))

            messages = cursor.fetchall()

    support_messages = []
    selected_teacher = None

    if selected_teacher_name:

        selected_teacher = {"teacher_name": selected_teacher_name}

        cursor.execute("""
            SELECT id, user_id, teacher_name, message, sender, created_at
            FROM teaching_support
            WHERE user_id = %s
              AND teacher_name = %s
            ORDER BY created_at ASC, id ASC
        """, (user["id"], selected_teacher_name))

        support_messages = cursor.fetchall()

    cursor.close()
    conn.close()

    return {
        "user": user,
        "records": records,
        "graph": graph,
        "report": report,
        "learning_summary": learning_summary,
        "recommendation": recommendation,
        "tasks": tasks,
        "materials": materials,
        "class_requests": class_requests,
        "assignments": assignments,
        "submissions": submissions,
        "student_teachers": student_teachers,
        "selected_teacher": selected_teacher,
        "support_messages": support_messages,
        "topics": topics,
        "selected_topic": selected_topic,
        "messages": messages,
        "role": session["role"]
    }

def build_teacher_dashboard_context(user, selected_student_id=None, topic_id=None):
    db = ConnectDatabase()
    conn = db.connect()
    cursor = conn.cursor(dictionary=True, buffered=True)

    cursor.execute("""
        SELECT
            users.username,
            class_memberships.class_name,
            SUM(learning_information.study_time) AS study_time,
            AVG(assignment_submissions.grade) AS grade,
            class_memberships.created_at AS approved_date
        FROM class_memberships
        JOIN users
            ON users.id = class_memberships.user_id
        LEFT JOIN learning_information
            ON learning_information.user_id = users.id
           AND learning_information.class_name = class_memberships.class_name
        LEFT JOIN assignment_submissions
            ON assignment_submissions.student_name = users.username
           AND assignment_submissions.class_name = class_memberships.class_name
        WHERE class_memberships.teacher_name = %s
        GROUP BY users.username, class_memberships.class_name, class_memberships.created_at
        ORDER BY class_memberships.created_at DESC, users.username ASC
    """, (user["username"],))
    data = cursor.fetchall()

    cursor.execute("""
        SELECT
            id,
            title,
            description,
            url,
            file_path,
            due_date,
            created_at,
            class_name
        FROM assignments
        WHERE teacher_name = %s
        ORDER BY created_at DESC
    """, (user["username"],))
    assignments = cursor.fetchall()

    cursor.execute("""
        SELECT
            assignment_submissions.id,
            assignment_submissions.student_name,
            assignment_submissions.comment,
            assignment_submissions.file_path,
            assignment_submissions.submitted_at,
            assignment_submissions.grade,
            assignments.title,
            assignments.class_name
        FROM assignment_submissions
        JOIN assignments
            ON assignments.id = assignment_submissions.assignment_id
        WHERE assignments.teacher_name = %s
        ORDER BY assignment_submissions.submitted_at DESC, assignment_submissions.id DESC
    """, (user["username"],))
    submissions = cursor.fetchall()

    cursor.execute("""
        SELECT
            id,
            title,
            created_by,
            created_at
        FROM discussion_topics
        ORDER BY created_at DESC, id DESC
    """)
    topics = cursor.fetchall()

    selected_topic = None
    messages = []

    if topic_id:
        cursor.execute("""
            SELECT *
            FROM discussion_topics
            WHERE id = %s
        """, (topic_id,))
        selected_topic = cursor.fetchone()

        if selected_topic:
            cursor.execute("""
                SELECT sender, message, created_at
                FROM discussion_messages
                WHERE topic_id = %s
                ORDER BY created_at ASC, id ASC
            """, (selected_topic["id"],))
            messages = cursor.fetchall()

    selected_student = None
    support_messages = []

    if selected_student_id:
        cursor.execute("""
            SELECT
                users.id AS user_id,
                users.username,
                class_memberships.class_name
            FROM class_memberships
            JOIN users
                ON users.id = class_memberships.user_id
            WHERE class_memberships.user_id = %s
              AND class_memberships.teacher_name = %s
            LIMIT 1
        """, (selected_student_id, user["username"]))
        selected_student = cursor.fetchone()

        if selected_student:
            cursor.execute("""
                SELECT id, user_id, teacher_name, message, sender, created_at
                FROM teaching_support
                WHERE user_id = %s
                  AND teacher_name = %s
                ORDER BY created_at ASC, id ASC
            """, (selected_student_id, user["username"]))
            support_messages = cursor.fetchall()

    cursor.close()
    conn.close()

    requests = get_teacher_class_requests(user["username"])
    teacher_students = get_teacher_students_with_chat(user["username"])

    return {
        "user": user,
        "data": data,
        "requests": requests,
        "assignments": assignments,
        "submissions": submissions,
        "teacher_students": teacher_students,
        "selected_student": selected_student,
        "support_messages": support_messages,
        "topics": topics,
        "selected_topic": selected_topic,
        "messages": messages,
        "role": session["role"]
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        db = ConnectDatabase()
        conn = db.connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if not user:
            flash("Invalid username")
            return redirect(url_for("login"))

        maker = MakeAccount()
        hashed = maker.hash_password(password)

        if hashed != user["password"]:
            flash("Invalid password")
            return redirect(url_for("login"))

        session["user_id"] = user["id"]
        session["role"] = user["role"]
        return role_redirect(user["role"])

    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm = request.form.get("confirm_password")
        role = request.form.get("role")

        if password != confirm:
            flash("Passwords do not match")
            return redirect(url_for("signup"))

        maker = MakeAccount()
        result = maker.create_account(username, password, email, role)

        if not result["success"]:
            flash(result["message"])
            return redirect(url_for("signup"))

        flash("Account created")
        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/dashboard")
def dashboard():
    if not login_required():
        return redirect(url_for("login"))

    user = current_user()
    return render_template("dashboard.html", user=user, role=session["role"])


@app.route("/student", methods=["GET", "POST"])
def student():
    if not login_required():
        return redirect(url_for("login"))
    if session["role"] != "student":
        return redirect(url_for("dashboard"))

    user = current_user()
    topic_id = request.args.get("topic_id")

    if request.method == "POST":
        form_type = request.form.get("form_type")

        if form_type == "task":
            task = request.form.get("task", "").strip()
            if task:
                add_task(user["id"], task)
            return redirect(url_for("student"))

        if form_type == "material":
            title = request.form.get("material_title", "").strip()
            subject = request.form.get("material_subject", "").strip()
            link = request.form.get("material_link", "").strip()

            if title:
                add_material(user["id"], title, subject, link)
            return redirect(url_for("student"))

        if form_type == "class_request":
            class_name = request.form.get("class_name", "").strip()
            teacher_name = request.form.get("teacher_name", "").strip()

            if class_name and teacher_name:
                add_class_request(user["id"], class_name, teacher_name)
            return redirect(url_for("student"))

        if form_type == "create_topic":
            title = request.form.get("topic_title", "").strip()
            class_name = "default"

            if title:
                db = ConnectDatabase()
                conn = db.connect()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO discussion_topics(class_name, title, created_by)
                    VALUES(%s, %s, %s)
                """, (class_name, title, user["username"]))
                conn.commit()
                cursor.close()
                conn.close()

            return redirect(url_for("student"))

        if form_type == "discussion_message":
            topic_id = request.form.get("topic_id")
            message = request.form.get("discussion_message", "").strip()

            if topic_id and message:
                db = ConnectDatabase()
                conn = db.connect()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO discussion_messages(topic_id, sender, message)
                    VALUES(%s, %s, %s)
                """, (topic_id, user["username"], message))
                conn.commit()
                cursor.close()
                conn.close()

            return redirect(url_for("student", topic_id=topic_id))

        return redirect(url_for("student"))

    context = build_student_dashboard_context(user, selected_teacher_name=None, topic_id=topic_id)
    return render_template("student.html", **context)


@app.route("/student/delete-material/<int:material_id>", methods=["POST"])
def student_delete_material(material_id):
    if not login_required():
        return redirect(url_for("login"))
    if session["role"] != "student":
        return redirect(url_for("dashboard"))

    delete_material(material_id)
    return redirect(url_for("student"))


@app.route("/student/delete-task/<int:task_id>", methods=["POST"])
def student_delete_task(task_id):
    if not login_required():
        return redirect(url_for("login"))
    if session["role"] != "student":
        return redirect(url_for("dashboard"))

    delete_task(task_id)
    return redirect(url_for("student"))


@app.route("/student/complete-task/<int:task_id>", methods=["POST"])
def student_complete_task(task_id):
    if not login_required():
        return redirect(url_for("login"))
    if session["role"] != "student":
        return redirect(url_for("dashboard"))

    complete_task(task_id)
    return redirect(url_for("student"))


@app.route("/student/delete-class-request/<int:request_id>", methods=["POST"])
def student_delete_class_request(request_id):
    if not login_required():
        return redirect(url_for("login"))
    if session["role"] != "student":
        return redirect(url_for("dashboard"))

    db = ConnectDatabase()
    conn = db.connect()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT user_id, class_name
        FROM class_requests
        WHERE id = %s
    """, (request_id,))
    req = cursor.fetchone()

    if req:
        cursor.execute("""
            DELETE FROM class_memberships
            WHERE user_id = %s
              AND class_name = %s
        """, (req["user_id"], req["class_name"]))

        cursor.execute("""
            DELETE FROM class_requests
            WHERE id = %s
        """, (request_id,))
        conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("student"))


@app.route("/student/chat/<teacher_name>")
def student_chat(teacher_name):
    if not login_required():
        return redirect(url_for("login"))
    if session["role"] != "student":
        return redirect(url_for("dashboard"))

    user = current_user()
    topic_id = request.args.get("topic_id")

    context = build_student_dashboard_context(
        user=user,
        selected_teacher_name=teacher_name,
        topic_id=topic_id
    )
    return render_template("student.html", **context)


@app.route("/student/send_message/<teacher_name>", methods=["POST"])
def student_send_message(teacher_name):
    if not login_required():
        return redirect(url_for("login"))
    if session["role"] != "student":
        return redirect(url_for("dashboard"))

    user = current_user()
    message = request.form.get("message", "").strip()

    if message == "":
        return redirect(url_for("student_chat", teacher_name=teacher_name))

    db = ConnectDatabase()
    conn = db.connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO teaching_support(user_id, teacher_name, message, sender)
        VALUES(%s, %s, %s, 'student')
    """, (user["id"], teacher_name, message))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("student_chat", teacher_name=teacher_name))


@app.route("/student/submit_assignment/<int:assignment_id>", methods=["POST"])
def submit_assignment(assignment_id):
    if not login_required():
        return redirect(url_for("login"))
    if session["role"] != "student":
        return redirect(url_for("dashboard"))

    user = current_user()
    file = request.files.get("file")
    comment = request.form.get("comment")

    if not file or file.filename == "":
        flash("Please select a file.")
        return redirect(url_for("student"))

    upload_folder = app.config["UPLOAD_FOLDER"]
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    filename = secure_filename(file.filename)
    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)

    db = ConnectDatabase()
    conn = db.connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT class_name
        FROM assignments
        WHERE id = %s
    """, (assignment_id,))
    assignment_row = cursor.fetchone()
    class_name = assignment_row[0] if assignment_row else None

    cursor.execute("""
        SELECT id
        FROM assignment_submissions
        WHERE assignment_id = %s
          AND student_name = %s
    """, (assignment_id, user["username"]))
    existing = cursor.fetchone()

    if existing:
        cursor.execute("""
            UPDATE assignment_submissions
            SET comment = %s,
                file_path = %s,
                class_name = %s,
                submitted_at = NOW()
            WHERE assignment_id = %s
              AND student_name = %s
        """, (comment, filepath, class_name, assignment_id, user["username"]))
    else:
        cursor.execute("""
            INSERT INTO assignment_submissions
            (assignment_id, student_name, class_name, comment, file_path, submitted_at)
            VALUES(%s, %s, %s, %s, %s, NOW())
        """, (assignment_id, user["username"], class_name, comment, filepath))

    conn.commit()

    cursor.close()
    conn.close()

    flash("Assignment submitted successfully.")
    return redirect(url_for("student"))


@app.route("/teacher", methods=["GET", "POST"])
def teacher():
    if not login_required():
        return redirect(url_for("login"))
    if session["role"] != "teacher":
        return redirect(url_for("dashboard"))

    user = current_user()
    topic_id = request.args.get("topic_id")

    if request.method == "POST":
        form_type = request.form.get("form_type")

        if form_type == "create_topic":
            title = request.form.get("topic_title", "").strip()
            class_name = "default"

            if title:
                db = ConnectDatabase()
                conn = db.connect()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO discussion_topics(class_name, title, created_by)
                    VALUES(%s, %s, %s)
                """, (class_name, title, user["username"]))
                conn.commit()
                cursor.close()
                conn.close()

            return redirect(url_for("teacher"))

        if form_type == "discussion_message":
            topic_id = request.form.get("topic_id")
            message = request.form.get("discussion_message", "").strip()

            if topic_id and message:
                db = ConnectDatabase()
                conn = db.connect()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO discussion_messages(topic_id, sender, message)
                    VALUES(%s, %s, %s)
                """, (topic_id, user["username"], message))
                conn.commit()
                cursor.close()
                conn.close()

            return redirect(url_for("teacher", topic_id=topic_id))

        return redirect(url_for("teacher"))

    db = ConnectDatabase()
    conn = db.connect()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
                   SELECT users.username,
                          class_memberships.class_name,
                          COALESCE(SUM(learning_information.study_time), 0) AS study_time,
                          COALESCE(AVG(learning_information.score), 0)      AS score,
                          class_memberships.created_at                      AS approved_date
                   FROM class_memberships
                            JOIN users
                                 ON users.id = class_memberships.user_id
                            LEFT JOIN learning_information
                                      ON learning_information.user_id = users.id
                                          AND learning_information.class_name = class_memberships.class_name
                   WHERE class_memberships.teacher_name = %s
                   GROUP BY users.username, class_memberships.class_name, class_memberships.created_at
                   ORDER BY class_memberships.created_at DESC, users.username ASC
                   """, (user["username"],))
    student_records = cursor.fetchall()

    cursor.execute("""
        SELECT
            users.username,
            COALESCE(AVG(learning_information.score),0) AS avg_grade,
            COALESCE(SUM(learning_information.study_time),0) AS total_study_time
        FROM class_memberships
        JOIN users
            ON users.id = class_memberships.user_id
        LEFT JOIN learning_information
            ON learning_information.user_id = users.id
           AND learning_information.class_name = class_memberships.class_name
        WHERE class_memberships.teacher_name=%s
        GROUP BY users.username
    """,(user["username"],))
    students = cursor.fetchall()

    student_count = len(students)

    total_score = 0
    total_time = 0

    for s in students:
        total_score += s["avg_grade"]
        total_time += s["total_study_time"]

    class_average_score = 0
    class_average_study_time = 0

    if student_count > 0:
        class_average_score = round(total_score / student_count, 2)
        class_average_study_time = round(total_time / student_count, 2)

    cursor.close()
    conn.close()

    context = build_teacher_dashboard_context(user, selected_student_id=None, topic_id=topic_id)

    context["student_records"] = student_records
    context["class_overview"] = {
        "student_count": student_count,
        "average_score": class_average_score,
        "average_study_time": class_average_study_time
    }

    return render_template("teacher.html", **context)


@app.route("/teacher/approve/<int:req_id>", methods=["POST"])
def teacher_approve(req_id):
    if not login_required():
        return redirect(url_for("login"))
    if session["role"] != "teacher":
        return redirect(url_for("dashboard"))

    db = ConnectDatabase()
    conn = db.connect()
    cursor = conn.cursor(dictionary=True, buffered=True)

    cursor.execute("SELECT * FROM class_requests WHERE id=%s", (req_id,))
    req = cursor.fetchone()

    if req:
        cursor.execute("""
            SELECT *
            FROM class_memberships
            WHERE user_id = %s
              AND class_name = %s
              AND teacher_name = %s
        """, (req["user_id"], req["class_name"], req["teacher_name"]))
        exist = cursor.fetchone()

        if not exist:
            cursor.execute("""
                INSERT INTO class_memberships(user_id, class_name, teacher_name, created_at)
                VALUES(%s, %s, %s, NOW())
            """, (req["user_id"], req["class_name"], req["teacher_name"]))

        cursor.execute("""
            UPDATE class_requests
            SET status = 'approved'
            WHERE id = %s
        """, (req_id,))
        conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("teacher"))


@app.route("/teacher/reject/<int:req_id>", methods=["POST"])
def teacher_reject(req_id):
    if not login_required():
        return redirect(url_for("login"))
    if session["role"] != "teacher":
        return redirect(url_for("dashboard"))

    update_class_request(req_id, "rejected")
    return redirect(url_for("teacher"))


@app.route("/teacher/send-message/<int:user_id>", methods=["POST"])
def teacher_send_message(user_id):
    if not login_required():
        return redirect(url_for("login"))
    if session["role"] != "teacher":
        return redirect(url_for("dashboard"))

    user = current_user()
    message = request.form.get("message", "").strip()

    if message == "":
        return redirect(url_for("teacher_chat", user_id=user_id))

    db = ConnectDatabase()
    conn = db.connect()
    cursor = conn.cursor(dictionary=True, buffered=True)

    cursor.execute("""
        SELECT *
        FROM class_memberships
        WHERE user_id = %s
          AND teacher_name = %s
        LIMIT 1
    """, (user_id, user["username"]))
    membership = cursor.fetchone()

    if membership:
        cursor.execute("""
            INSERT INTO teaching_support(user_id, teacher_name, message, sender)
            VALUES(%s, %s, %s, 'teacher')
        """, (user_id, user["username"], message))
        conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("teacher_chat", user_id=user_id))


@app.route("/teacher/chat/<int:user_id>")
def teacher_chat(user_id):
    if not login_required():
        return redirect(url_for("login"))
    if session["role"] != "teacher":
        return redirect(url_for("dashboard"))

    user = current_user()
    topic_id = request.args.get("topic_id")

    context = build_teacher_dashboard_context(
        user=user,
        selected_student_id=user_id,
        topic_id=topic_id
    )
    return render_template("teacher.html", **context)


@app.route("/teacher/add_assignment", methods=["POST"])
def add_assignment():
    if not login_required():
        return redirect(url_for("login"))
    if session["role"] != "teacher":
        return redirect(url_for("dashboard"))

    user = current_user()

    class_name = request.form.get("class_name")
    title = request.form.get("title")
    description = request.form.get("description")
    url = request.form.get("url")
    due_date = request.form.get("due_date")
    file = request.files.get("file")

    file_path = None

    if file and file.filename != "":
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)

    db = ConnectDatabase()
    conn = db.connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO assignments(teacher_name, class_name, title, description, url, file_path, due_date)
        VALUES(%s, %s, %s, %s, %s, %s, %s)
    """, (user["username"], class_name, title, description, url, file_path, due_date))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("teacher"))


@app.route("/teacher/delete_assignment/<int:id>", methods=["POST"])
def delete_assignment(id):
    if not login_required():
        return redirect(url_for("login"))
    if session["role"] != "teacher":
        return redirect(url_for("dashboard"))

    db = ConnectDatabase()
    conn = db.connect()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM assignments WHERE id=%s", (id,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("teacher"))


@app.route("/teacher/edit_assignment/<int:id>", methods=["POST"])
def edit_assignment(id):
    if not login_required():
        return redirect(url_for("login"))
    if session["role"] != "teacher":
        return redirect(url_for("dashboard"))

    class_name = request.form.get("class_name")
    title = request.form.get("title")
    description = request.form.get("description")
    url = request.form.get("url")
    due_date = request.form.get("due_date")

    db = ConnectDatabase()
    conn = db.connect()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE assignments
        SET class_name = %s,
            title = %s,
            description = %s,
            url = %s,
            due_date = %s
        WHERE id = %s
    """, (class_name, title, description, url, due_date, id))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("teacher"))


@app.route("/student/get_assignments")
def get_assignments():
    if not login_required():
        return {"data": []}

    if session["role"] != "student":
        return {"data": []}

    user = current_user()

    db = ConnectDatabase()
    conn = db.connect()
    cursor = conn.cursor(dictionary=True, buffered=True)

    cursor.execute("""
        SELECT
            assignments.id,
            assignments.class_name,
            assignments.title,
            assignments.description,
            assignments.url,
            assignments.file_path,
            assignments.due_date,
            assignments.teacher_name,
            CASE
                WHEN assignment_submissions.id IS NOT NULL THEN 1
                ELSE 0
            END AS submitted
        FROM class_memberships
        JOIN assignments
            ON assignments.class_name = class_memberships.class_name
           AND assignments.teacher_name = class_memberships.teacher_name
        LEFT JOIN assignment_submissions
            ON assignment_submissions.assignment_id = assignments.id
           AND assignment_submissions.student_name = %s
        WHERE class_memberships.user_id = %s
        ORDER BY assignments.created_at DESC
    """, (user["username"], user["id"]))

    assignments = cursor.fetchall()

    cursor.close()
    conn.close()

    return {"data": assignments}


@app.route("/teacher/grade/<int:submission_id>", methods=["POST"])
def grade_submission(submission_id):
    if not login_required():
        return redirect(url_for("login"))
    if session["role"] != "teacher":
        return redirect(url_for("dashboard"))

    grade = request.form.get("grade")

    db = ConnectDatabase()
    conn = db.connect()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE assignment_submissions
        SET grade = %s
        WHERE id = %s
    """, (grade, submission_id))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("teacher"))

@app.route("/teacher/class-overview-data")
def teacher_class_overview_data():

    user = current_user()

    db = ConnectDatabase()
    conn = db.connect()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT
        users.username,
        COALESCE(AVG(assignment_submissions.grade),0) AS avg_grade,
        COALESCE(SUM(li.study_time),0) AS total_study_time
    FROM class_memberships cm
    JOIN users
        ON users.id = cm.user_id
    LEFT JOIN assignment_submissions
        ON assignment_submissions.student_name = users.username
    LEFT JOIN learning_information li
        ON li.user_id = users.id
    WHERE cm.teacher_name = %s
    GROUP BY users.username
    """, (user["username"],))

    students = cursor.fetchall()

    student_count = len(students)

    total_score = 0
    total_time = 0

    for s in students:
        total_score += float(s["avg_grade"])
        total_time += float(s["total_study_time"])

    class_average_score = 0
    class_average_study_time = 0

    if student_count > 0:
        class_average_score = round(total_score / student_count, 2)
        class_average_study_time = round(total_time / student_count, 2)

    cursor.close()
    conn.close()

    return {
        "student_count": student_count,
        "class_average_score": class_average_score,
        "class_average_study_time": class_average_study_time,
        "students": students
    }

@app.route("/schooladministrator")
def schooladministrator():
    if not login_required():
        return redirect(url_for("login"))
    if session["role"] != "schooladministrator":
        return redirect(url_for("dashboard"))

    db = ConnectDatabase()
    conn = db.connect()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("schooladministrator.html", users=users, role=session["role"])


@app.route("/api/school_performance")
def api_school_performance():
    if not login_required():
        return {"error": "login required"}
    if session["role"] != "schooladministrator":
        return {"error": "permission denied"}

    db = ConnectDatabase()
    conn = db.connect()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT
            AVG(score) AS avg_score,
            SUM(study_time) AS total_study_time,
            COUNT(*) AS records
        FROM learning_information
    """)
    data = cursor.fetchone()
    cursor.close()
    conn.close()

    if not data:
        data = {"avg_score": 0, "total_study_time": 0, "records": 0}

    if data["avg_score"] is None:
        data["avg_score"] = 0
    if data["total_study_time"] is None:
        data["total_study_time"] = 0
    if data["records"] is None:
        data["records"] = 0

    return data


@app.route("/api/teacher_monitoring")
def api_teacher_monitoring():
    if not login_required():
        return {"error": "login required"}
    if session["role"] != "schooladministrator":
        return {"error": "permission denied"}

    db = ConnectDatabase()
    conn = db.connect()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT
            users.id,
            users.username,
            COUNT(class_requests.id) AS total_requests,
            SUM(CASE WHEN class_requests.status = 'approved' THEN 1 ELSE 0 END) AS approved_requests,
            SUM(CASE WHEN class_requests.status = 'pending' THEN 1 ELSE 0 END) AS pending_requests
        FROM users
        LEFT JOIN class_requests
            ON users.username = class_requests.teacher_name
        WHERE users.role = 'teacher'
        GROUP BY users.id, users.username
    """)
    teachers = cursor.fetchall()
    cursor.close()
    conn.close()

    for teacher in teachers:
        if teacher["total_requests"] is None:
            teacher["total_requests"] = 0
        if teacher["approved_requests"] is None:
            teacher["approved_requests"] = 0
        if teacher["pending_requests"] is None:
            teacher["pending_requests"] = 0

    return teachers


@app.route("/api/admin_report")
def api_admin_report():
    if not login_required():
        return {"error": "login required"}
    if session["role"] != "schooladministrator":
        return {"error": "permission denied"}

    db = ConnectDatabase()
    conn = db.connect()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS total_users FROM users")
    users = cursor.fetchone()

    cursor.execute("SELECT COUNT(*) AS total_students FROM users WHERE role='student'")
    students = cursor.fetchone()

    cursor.execute("SELECT COUNT(*) AS total_teachers FROM users WHERE role='teacher'")
    teachers = cursor.fetchone()

    cursor.execute("SELECT COUNT(*) AS total_school_admins FROM users WHERE role='schooladministrator'")
    school_admins = cursor.fetchone()

    cursor.execute("""
        SELECT
            AVG(score) AS average_score,
            SUM(study_time) AS total_study_time,
            COUNT(*) AS total_learning_records
        FROM learning_information
    """)
    learning = cursor.fetchone()

    cursor.execute("SELECT COUNT(*) AS pending_requests FROM class_requests WHERE status='pending'")
    pending = cursor.fetchone()

    cursor.execute("SELECT COUNT(*) AS approved_requests FROM class_requests WHERE status='approved'")
    approved = cursor.fetchone()

    cursor.close()
    conn.close()

    report = {
        "total_users": users["total_users"],
        "total_students": students["total_students"],
        "total_teachers": teachers["total_teachers"],
        "total_school_admins": school_admins["total_school_admins"],
        "average_score": learning["average_score"] if learning["average_score"] is not None else 0,
        "total_study_time": learning["total_study_time"] if learning["total_study_time"] is not None else 0,
        "total_learning_records": learning["total_learning_records"],
        "pending_requests": pending["pending_requests"],
        "approved_requests": approved["approved_requests"]
    }

    return report


@app.route("/systemadministrator")
def systemadministrator():
    if not login_required():
        return redirect(url_for("login"))
    if session["role"] != "systemadministrator":
        return redirect(url_for("dashboard"))

    db = ConnectDatabase()
    conn = db.connect()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("systemadministrator.html", users=users, role=session["role"])


@app.route("/api/users")
def api_users():
    if not login_required():
        return {"error": "login required"}
    if session["role"] != "systemadministrator":
        return {"error": "permission denied"}

    db = ConnectDatabase()
    conn = db.connect()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, username, email, role FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()

    return users


@app.route("/api/create_user", methods=["POST"])
def api_create_user():
    if not login_required():
        return {"error": "login required"}
    if session["role"] != "systemadministrator":
        return {"error": "permission denied"}

    data = request.get_json()

    if not data:
        return {"success": False, "message": "No data received"}

    maker = MakeAccount()
    result = maker.create_account(data["username"], data["password"], data["email"], data["role"])
    return result


@app.route("/api/delete_user/<int:user_id>", methods=["DELETE"])
def api_delete_user(user_id):
    if not login_required():
        return {"error": "login required"}
    if session["role"] != "systemadministrator":
        return {"error": "permission denied"}

    if session["user_id"] == user_id:
        return {"success": False, "message": "You cannot delete your own account"}

    db = ConnectDatabase()
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()

    return {"success": True}


@app.route("/api/database_status")
def api_database_status():
    if not login_required():
        return {"error": "login required"}
    if session["role"] != "systemadministrator":
        return {"error": "permission denied"}

    db = ConnectDatabase()
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = len(cursor.fetchall())
    cursor.close()
    conn.close()

    return {"status": "connected", "tables": tables}


@app.route("/api/security_logs")
def api_security_logs():
    if not login_required():
        return {"error": "login required"}
    if session["role"] != "systemadministrator":
        return {"error": "permission denied"}

    db = ConnectDatabase()
    conn = db.connect()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT action, target, created_at
            FROM security_logs
            ORDER BY created_at DESC
            LIMIT 10
        """)
        logs = cursor.fetchall()
    except Exception:
        logs = [{"action": "system", "target": "no logs table", "created_at": "-"}]

    cursor.close()
    conn.close()

    return logs


@app.route("/setting", methods=["GET", "POST"])
def setting():
    if not login_required():
        return redirect(url_for("login"))

    user = current_user()
    setting_service = Setting()

    if request.method == "POST":
        theme = request.form.get("theme")
        language = request.form.get("language")
        setting_service.save_setting(user["id"], theme, language)
        return redirect(url_for("setting"))

    setting_data = setting_service.get_setting(user["id"])
    return render_template("setting.html", setting=setting_data, role=session["role"])


if __name__ == "__main__":
    app.run(debug=True)
