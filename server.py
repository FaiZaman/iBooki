from flask import Flask, url_for, render_template, request, redirect, Response
import pandas as pd

app = Flask(__name__)

books = pd.read_csv("dataset/books.csv")
ratings = pd.read_csv("dataset/ratings.csv")
users = pd.read_csv("dataset/users.csv")

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/profile")
def profile():
    return render_template("profile.html")


@app.route("/validate", methods = ['POST'])
def validate():

    userID = request.form['userID']
    for index, row in users.iterrows():
        if int(userID) == int(row['userID']):
            return redirect(url_for("profile", id=userID))
    return "No"


@app.route("/userID", methods = ['POST'])
def addNewUser():

    userID = request.form['userID']
    users.append(userID)
    return users


if __name__ == "__main__":
    app.run()