from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import pymysql

app = Flask(__name__)

# create connection to mysql
load_dotenv()
conn = pymysql.connect(
    host="database-2.ceckcclbqkdy.us-east-1.rds.amazonaws.com",
    port=3306,
    user=os.getenv("db_user"),
    password=os.getenv("db_pw"),
    db='database_2'
)

# HOME
@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html", title="Welcome to BrandName")

# create new user
@app.route("/create_user", methods=["GET", "POST"])
def create_user():
    if request.method == "POST":
        try:
            insert_user(request.form["username"], request.form["email"], request.form["password"])
            print("SUCCESS")
        except:
            print("ERROR")
    return render_template("create_user.html", title="Create User")

#Sign In
@app.route("/sign_in")
def sign_in():
    return render_template("sign_in.html", title="Sign In")

@app.route("/manage_users", methods=["GET", "POST"])
def manage_users():
    details = select_users()
    # print(request.form.items)
    if request.method == "POST":
        print("manage_users_POST: " + str(request.form.items))
        return render_template("manage_user.html", title="Manage User", username=request.form["username"], email=request.form["email"], pw=request.form["pw"])
    elif request.method == "GET":
        print("GET: " + str(request.form.items))
    return render_template("manage_users.html", title="Manage Users", users=details)

@app.route("/manage_user", methods=["GET", "POST"])
def manage_user():
    if request.method == "POST":
        # insert_user(request.form["username"], request.form["email"], request.form["password"])
        # print("SUCCESS AT MANAGER_USER()")
        print("manage_user_POST: " + str(request.form.items))
    elif request.method == "GET":
        print("GET: " + str(request.form.items))
    return render_template("manage_user.html", title="Manage User")




# AWS DATABASE FUNCTIONS BELOW

# get all users from mysql
def select_users():
    cur=conn.cursor()
    cur.execute("SELECT username,email,password,create_time FROM user")
    details = cur.fetchall()
    return details

# insert new user into mysql
def insert_user(name,email,password):
    cur=conn.cursor()
    cur.execute("INSERT INTO user (username,email,password) VALUES (%s,%s,%s)", (name,email,password))
    conn.commit()





# Parking Lot
# @app.route("/create_account", methods=["GET", "POST"])
# def create_account():
#     if request.method == "POST":
#         try:
#             insert_user(request.form["username"], request.form["email"], request.form["password"])
#             print("SUCCESS")
#         except:
#             print("ERROR")
#     return render_template("create_account.html", title="Create Account")

# @app.route("/edit_user", methods=["GET", "POST"])
# @app.route("/edit_account", methods=["GET", "POST"])
# def edit_account():
#     if request.method == "POST":
#         try:
#             insert_user(request.form["username"], request.form["email"], request.form["password"])
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
