from flask import Flask, render_template, request, redirect, url_for, flash, session
from LearnInsight_ver_01.Backend.Account.MakeAccount import MakeAccount
from LearnInsight_ver_01.Backend.Account.EditAccount import EditAccount
from LearnInsight_ver_01.Backend.Database.CreateDatabase import CreateDatabase
from LearnInsight_ver_01.Backend.Database.ConnectDatabase import ConnectDatabase
from LearnInsight_ver_01.Backend.Information.InputLearningInformation import InputLearningInformation
from LearnInsight_ver_01.Backend.Information.InputUserInformation import InputUserInformation
from LearnInsight_ver_01.Backend.Information.EditLearningInformation import EditLearningInformation
from LearnInsight_ver_01.Backend.Information.EditUserInformation import EditUserInformation
from LearnInsight_ver_01.Backend.System.MakeLearningDataGraph import MakeLearningDataGraph
from LearnInsight_ver_01.Backend.System.MakeLearningReport import MakeLearningReport
from LearnInsight_ver_01.Backend.System.RecommendLearningPlan import RecommendLearningPlan
from LearnInsight_ver_01.Backend.System.Setting import Setting
from LearnInsight_ver_01.Backend.MachineLearning.trainData import TrainData
from LearnInsight_ver_01.Backend.MachineLearning.predict import Predict
from LearnInsight_ver_01.Backend.MachineLearning.evaluate import Evaluate

app = Flask(__name__,template_folder="FrontEnd/templates",static_folder="FrontEnd/static")
app.secret_key = "learninsight_secret_key"
CreateDatabase().create_database()

def create_material_table():
    db=ConnectDatabase()
    conn=db.connect()
    cursor=conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS study_materials(
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        title VARCHAR(255),
        subject VARCHAR(255),
        link TEXT
    )""")
    conn.commit()
    cursor.close()
    conn.close()

def create_tasks_table():
    db=ConnectDatabase()
    conn=db.connect()
    cursor=conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS tasks(
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        task TEXT,
        status VARCHAR(50),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    conn.commit()
    cursor.close()
    conn.close()

def create_class_requests_table():
    db=ConnectDatabase()
    conn=db.connect()
    cursor=conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS class_requests(
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        class_name VARCHAR(255),
        teacher_name VARCHAR(255),
        status VARCHAR(50) DEFAULT 'pending'
    )""")
    conn.commit()
    cursor.close()
    conn.close()

create_material_table()
create_tasks_table()
create_class_requests_table()

def get_materials(user_id):
    db=ConnectDatabase()
    conn=db.connect()
    cursor=conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM study_materials WHERE user_id=%s",(user_id,))
    materials=cursor.fetchall()
    cursor.close()
    conn.close()
    return materials

def add_material(user_id,title,subject,link):
    db=ConnectDatabase()
    conn=db.connect()
    cursor=conn.cursor()
    cursor.execute("INSERT INTO study_materials(user_id,title,subject,link) VALUES(%s,%s,%s,%s)",(user_id,title,subject,link))
    conn.commit()
    cursor.close()
    conn.close()

def delete_material(material_id):
    db=ConnectDatabase()
    conn=db.connect()
    cursor=conn.cursor()
    cursor.execute("DELETE FROM study_materials WHERE id=%s",(material_id,))
    conn.commit()
    cursor.close()
    conn.close()

def get_tasks(user_id):
    db=ConnectDatabase()
    conn=db.connect()
    cursor=conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks WHERE user_id=%s",(user_id,))
    tasks=cursor.fetchall()
    cursor.close()
    conn.close()
    return tasks

def add_task(user_id,task):
    db=ConnectDatabase()
    conn=db.connect()
    cursor=conn.cursor()
    cursor.execute("INSERT INTO tasks(user_id,task,status) VALUES(%s,%s,'pending')",(user_id,task))
    conn.commit()
    cursor.close()
    conn.close()

def delete_task(task_id):
    db=ConnectDatabase()
    conn=db.connect()
    cursor=conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=%s",(task_id,))
    conn.commit()
    cursor.close()
    conn.close()

def complete_task(task_id):
    db=ConnectDatabase()
    conn=db.connect()
    cursor=conn.cursor()
    cursor.execute("UPDATE tasks SET status='completed' WHERE id=%s",(task_id,))
    conn.commit()
    cursor.close()
    conn.close()

def add_class_request(user_id,class_name,teacher_name):
    db=ConnectDatabase()
    conn=db.connect()
    cursor=conn.cursor()
    cursor.execute("INSERT INTO class_requests(user_id,class_name,teacher_name,status) VALUES(%s,%s,%s,'pending')",(user_id,class_name,teacher_name))
    conn.commit()
    cursor.close()
    conn.close()

def get_class_requests_by_user(user_id):
    db=ConnectDatabase()
    conn=db.connect()
    cursor=conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM class_requests WHERE user_id=%s",(user_id,))
    data=cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def get_all_class_requests():
    db=ConnectDatabase()
    conn=db.connect()
    cursor=conn.cursor(dictionary=True)
    cursor.execute("""SELECT class_requests.*,users.username
    FROM class_requests
    JOIN users ON users.id=class_requests.user_id""")
    data=cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def update_class_request(request_id,status):
    db=ConnectDatabase()
    conn=db.connect()
    cursor=conn.cursor()
    cursor.execute("UPDATE class_requests SET status=%s WHERE id=%s",(status,request_id))
    conn.commit()
    cursor.close()
    conn.close()

def current_user():
    if "user_id" not in session:
        return None
    db=ConnectDatabase()
    conn=db.connect()
    cursor=conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id=%s",(session["user_id"],))
    user=cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def login_required():
    return "user_id" in session

def role_redirect(role):
    if role=="student":
        return redirect(url_for("student"))
    if role=="teacher":
        return redirect(url_for("teacher"))
    if role=="schooladministrator":
        return redirect(url_for("schooladministrator"))
    if role=="systemadministrator":
        return redirect(url_for("systemadministrator"))
    return redirect(url_for("dashboard"))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")
        db=ConnectDatabase()
        conn=db.connect()
        cursor=conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username=%s",(username,))
        user=cursor.fetchone()
        cursor.close()
        conn.close()
        if not user:
            flash("Invalid username")
            return redirect(url_for("login"))
        maker=MakeAccount()
        hashed=maker.hash_password(password)
        if hashed!=user["password"]:
            flash("Invalid password")
            return redirect(url_for("login"))
        session["user_id"]=user["id"]
        session["role"]=user["role"]
        return role_redirect(user["role"])
    return render_template("login.html")

@app.route("/signup",methods=["GET","POST"])
def signup():
    if request.method=="POST":
        username=request.form.get("username")
        email=request.form.get("email")
        password=request.form.get("password")
        confirm=request.form.get("confirm_password")
        role=request.form.get("role")
        if password!=confirm:
            flash("Passwords do not match")
            return redirect(url_for("signup"))
        maker=MakeAccount()
        result=maker.create_account(username,password,email,role)
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
    user=current_user()
    return render_template("dashboard.html",user=user)

@app.route("/student",methods=["GET","POST"])
def student():
    if not login_required():
        return redirect(url_for("login"))
    if session["role"]!="student":
        return redirect(url_for("dashboard"))
    user=current_user()
    learner=InputLearningInformation()
    if request.method=="POST":
        form_type=request.form.get("form_type")
        if form_type=="task":
            task=request.form.get("task")
            add_task(user["id"],task)
        if form_type=="material":
            title=request.form.get("material_title")
            subject=request.form.get("material_subject")
            link=request.form.get("material_link")
            add_material(user["id"],title,subject,link)
        if form_type=="class_request":
            class_name=request.form.get("class_name")
            teacher_name=request.form.get("teacher_name")
            add_class_request(user["id"],class_name,teacher_name)
        return redirect(url_for("student"))
    records=learner.get_learning_data_by_user(user["id"])
    graph=MakeLearningDataGraph().create_graph(records)
    report=MakeLearningReport().generate_report(user,records)
    if records:
        avg=report["average_score"]
        study=report["total_study_time"]
    else:
        avg=0
        study=0
    recommendation=RecommendLearningPlan().recommend(avg,study)
    tasks=get_tasks(user["id"])
    materials=get_materials(user["id"])
    class_requests=get_class_requests_by_user(user["id"])
    return render_template("student.html",records=records,graph=graph,report=report,recommendation=recommendation,tasks=tasks,materials=materials,class_requests=class_requests)

@app.route("/student/delete-task/<int:task_id>",methods=["POST"])
def student_delete_task(task_id):
    delete_task(task_id)
    return redirect(url_for("student"))

@app.route("/student/complete-task/<int:task_id>",methods=["POST"])
def student_complete_task(task_id):
    complete_task(task_id)
    return redirect(url_for("student"))

@app.route("/student/delete-material/<int:material_id>",methods=["POST"])
def student_delete_material(material_id):
    delete_material(material_id)
    return redirect(url_for("student"))

@app.route("/teacher")
def teacher():
    if not login_required():
        return redirect(url_for("login"))
    if session["role"]!="teacher":
        return redirect(url_for("dashboard"))
    db=ConnectDatabase()
    conn=db.connect()
    cursor=conn.cursor(dictionary=True)
    cursor.execute("""SELECT users.username,learning_information.*
    FROM learning_information
    JOIN users ON users.id=learning_information.user_id""")
    data=cursor.fetchall()
    cursor.close()
    conn.close()
    requests=get_all_class_requests()
    return render_template("teacher.html",data=data,requests=requests)

@app.route("/teacher/approve/<int:req_id>",methods=["POST"])
def teacher_approve(req_id):
    update_class_request(req_id,"approved")
    return redirect(url_for("teacher"))

@app.route("/teacher/reject/<int:req_id>",methods=["POST"])
def teacher_reject(req_id):
    update_class_request(req_id,"rejected")
    return redirect(url_for("teacher"))

@app.route("/schooladministrator")
def schooladministrator():
    if not login_required():
        return redirect(url_for("login"))
    if session["role"]!="schooladministrator":
        return redirect(url_for("dashboard"))
    db=ConnectDatabase()
    conn=db.connect()
    cursor=conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users=cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("schooladministrator.html",users=users)

@app.route("/systemadministrator")
def systemadministrator():
    if not login_required():
        return redirect(url_for("login"))
    if session["role"]!="systemadministrator":
        return redirect(url_for("dashboard"))
    db=ConnectDatabase()
    conn=db.connect()
    cursor=conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users=cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("systemadministrator.html",users=users)

@app.route("/setting",methods=["GET","POST"])
def setting():
    if not login_required():
        return redirect(url_for("login"))
    user=current_user()
    setting_service=Setting()
    if request.method=="POST":
        theme=request.form.get("theme")
        language=request.form.get("language")
        setting_service.save_setting(user["id"],theme,language)
        return redirect(url_for("setting"))
    setting_data=setting_service.get_setting(user["id"])
    return render_template("setting.html",setting=setting_data)

@app.route("/train-model")
def train_model():
    if not login_required():
        return redirect(url_for("login"))
    user=current_user()
    learner=InputLearningInformation()
    records=learner.get_learning_data_by_user(user["id"])
    if len(records)<2:
        flash("Not enough data")
        return redirect(url_for("student"))
    X=[r["study_time"] for r in records]
    y=[r["score"] for r in records]
    trainer=TrainData()
    model=trainer.train(X,y)
    predictor=Predict()
    predictions=predictor.predict(model,X)
    evaluator=Evaluate()
    metrics=evaluator.evaluate_model(y,predictions)
    return render_template("system.html",metrics=metrics)

if __name__=="__main__":
    app.run(debug=True)