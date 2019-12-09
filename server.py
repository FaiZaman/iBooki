from flask import Flask, render_template, request, redirect, Response
import pandas as pd

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/validate", methods = ['POST'])
def validate():

    books = pd.read_csv("dataset/books.csv")
    ratings = pd.read_csv("dataset/ratings.csv")
    users = pd.read_csv("dataset/users.csv")

    userID = request.form['userID']
    for index, row in users.iterrows():
        if userID == row['userID']:
            return userID
    return "No"


if __name__ == "__main__":
    app.run()