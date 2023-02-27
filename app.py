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
    return render_template("index.html", title="Welcome Home")

# create new user page
@app.route("/create_user", methods=["GET", "POST"])
@app.route("/create_account", methods=["GET", "POST"])
def create_account():
    if request.method == "POST":
        try:
            insert_user(request.form["username"], request.form["email"], request.form["password"])
            print("SUCCESS")
        except:
            print("ERROR")
    return render_template("create_account.html", title="Create Account")

@app.route("/edit_user", methods=["GET", "POST"])
@app.route("/edit_account", methods=["GET", "POST"])
def edit_account():
    if request.method == "POST":
        try:
            insert_user(request.form["username"], request.form["email"], request.form["password"])
            print("SUCCESS")
        except:
            print("ERROR")
    return render_template("edit_user.html", title="Edit Account")

# route to data page showing users
@app.route("/data")
def data():
    details = select_users()
    return render_template("data.html", title="View Data", users = details)

#Sign In
@app.route("/sign_in")
def sign_in():
    return render_template("sign_in.html", title="Sign In")

#landing
@app.route("/landing")
def landing():
    return render_template("landing.html", title="Landing")

#to be deleted one day
@app.route("/playground")
def playground():
    return render_template("playground.html", title="Playground")




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
