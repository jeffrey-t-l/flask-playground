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
    user="admin",
    password=os.getenv("db_pw"),
    db='database_2'
)

# HOME
@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html", title="FatFish")

# @app.route("/if_statement")
# def if_statement():
#     if True == True:
#         data = "this is all the data"
#     return data

@app.route("/playground")
def playground():
    return render_template("playground.html", title="FatFish | Playground")

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        # print(type(request.form["firstname"]))
        select_user()
        insert_user("jeff", "jeff@test.com", "j_pw")
    return render_template("create.html", title="Create")

@app.route("/data")
def data():
    details = select_users()
    # print(str(users))
    # for user in users:
    #     print(str(user))
    return render_template("data.html", title="View Data", users = details)

def select_users():
    cur=conn.cursor()
    cur.execute("SELECT * FROM user")
    details = cur.fetchall()
    # print(str(details))
    return details

def insert_user(name,email,password):
    cur=conn.cursor()
    cur.execute("INSERT INTO user (username,email,password) VALUES (%s,%s,%s)", (name,email,password))
    # INSERT INTO user (username,email,password,create_time) VALUES ("test_username", "test@email.com", "test_pw")
    conn.commit()
