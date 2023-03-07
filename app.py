from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
import os
import pymysql

app = Flask(__name__)

# HOME
@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html", title="Welcome to BrandName")

@app.route("/sign_in")
def sign_in():
    return render_template("sign_in.html", title="Sign In")

@app.route("/modal")
def modal():
    return render_template("modal.html", title="Modal Test")

@app.route("/settings")
def user_settings():
    return render_template("settings.html", title="Settings")

# create new user
@app.route("/create_user", methods=["GET", "POST"])
def create_user():
    if request.method == "POST":
        user_exists = False
        username = request.form["username"]
        results = select_user(username)

        # check if user exists already
        for result in results:
            if result[0] == username:
                user_exists = True
            else:
                user_exists = False
                print("no match in db")
        # if user does not exist, create it
        if user_exists == False:
            try:
                insert_user(request.form["username"], request.form["email"], request.form["pw"])
                print("SUCCESS")
            except:
                print("ERROR on INSERT")
    return render_template("create_user.html", title="Create User")

@app.route("/manage_users", methods=["GET", "POST"])
def manage_users():
    details = select_users()
    if request.method == "POST":
            return redirect(url_for("manage_user", username=request.form["username"]), 302)
    elif request.method == "GET":
        print("GET: " + str(request.form.items))

    return render_template("manage_users.html", title="Manage Users", users=details)

@app.route("/manage_user", methods=["GET", "POST"])
def manage_user():
    if request.method == "POST":
        print("manage_user() :_: POST")
        #TODO : UPDATE user
        # insert_user(request.form["username"], request.form["email"], request.form["pw"])
        # print("SUCCESS AT MANAGER_USER()")
        username = request.args.get('username', default = None, type = str)
        details = select_user(username)

    # called if coming from manage_users page
    if request.method == "GET":
        username = request.args.get('username', default = None, type = str)
        details = select_user(username)
        email = details[0][1]
        pw = details[0][2]
        created_time = details[0][3]
        return render_template("manage_user.html",
                               title=email,
                               username=username,
                               email=email,
                               pw=pw,
                               created_time=created_time)
    return render_template("manage_user.html", title="Manage User")



# AWS DATABASE FUNCTIONS
# get all users from mysql
def select_users():
    conn = mysql_conn()
    cur=conn.cursor()
    cur.execute("SELECT username,email,password,create_time FROM user")
    details = cur.fetchall()
    return details
# insert new user into mysql
def insert_user(name,email,pw):
    conn = mysql_conn()
    cur=conn.cursor()
    cur.execute("INSERT INTO user (username,email,password) VALUES (%s,%s,%s)", (name,email,pw))
    conn.commit()
# get a user from mysql
def select_user(username):
    conn = mysql_conn()
    cur=conn.cursor()
    cur.execute("SELECT * FROM user WHERE username=%s", username)
    details = cur.fetchall()
    return details
# connect to mysql
def mysql_conn():
    conn = pymysql.connect(
        host=os.getenv("db_host"),
        port=3306,
        user=os.getenv("db_user"),
        password=os.getenv("db_pw"),
        db=os.getenv("db")
    )
    return conn

# MAIN function
if __name__ == "__main__":
    app.run()
    load_dotenv()
    mysql_conn()








# PARKING LOT
# @app.route("/create_account", methods=["GET", "POST"])
# def create_account():
#     if request.method == "POST":
#         try:
#             insert_user(request.form["username"], request.form["email"], request.form["pw"])
#             print("SUCCESS")
#         except:
#             print("ERROR")
#     return render_template("create_account.html", title="Create Account")

# @app.route("/edit_user", methods=["GET", "POST"])
# @app.route("/edit_account", methods=["GET", "POST"])
# def edit_account():
#     if request.method == "POST":
#         try:
#             insert_user(request.form["username"], request.form["email"], request.form["pw"])
#             print("SUCCESS")
#         except:
#             print("ERROR")
#     return render_template("edit_user.html", title="Edit Account")

# route to data page showing users
# @app.route("/data")
# def data():
#     details = select_users()
#     return render_template("data.html", title="View Data", users = details)

# @app.route("/landing")
# def landing():
#     return render_template("landing.html", title="Landing")
