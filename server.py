from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/receiver")
def validate():

    books = pd.read_csv("dataset/books.csv")
    ratings = pd.read_csv("dataset/ratings.csv")
    users = pd.read_csv("dataset/users.csv")


if __name__ == "__main__":
    app.run()