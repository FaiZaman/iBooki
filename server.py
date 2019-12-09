from flask import Flask, render_template
import csv

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/receiver")
def validate():
    books = {}
    ratings = {}

if __name__ == "__main__":
    app.run()