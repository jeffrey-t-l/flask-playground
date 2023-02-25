from flask import Flask, render_template, request


app = Flask(__name__)

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
        print(request.form["firstname"])
        print(request.form["lastname"])
    return render_template("create.html", title="Create")

@app.route("/data")
def data():
    return render_template("data.html", title="View Data")
