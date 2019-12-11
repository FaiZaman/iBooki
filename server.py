from flask import Flask, url_for, render_template, request, redirect, make_response
import pandas as pd

# create app and read in users
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/profile/<userID>")
def profile(userID):
    return render_template("profile.html", id=userID)


@app.route("/validate", methods = ['POST'])
def validate():

    # validates if user ID is actual user
    users = pd.read_csv("dataset/users.csv")
    userID = request.form['userID']
    
    for index, row in users.iterrows():
        if int(userID) == int(row['userID']):
            return "works", 200
    return "oops", 400


@app.route("/addNewUser", methods = ['POST'])
def addNewUser():

    users = pd.read_csv("dataset/users.csv")
    userID = request.form['userID']

    exists = False
    for index, row in users.iterrows():
        if int(userID) == int(row['userID']):
            exists = True
            break
    if exists:
        return "oops", 400
    
    # if ID does not exist append to DF and csv
    users = users.append({'userID': userID}, ignore_index=True)
    users_csv = users.to_csv(r'dataset/users.csv', index=False)
    return "works", 200

if __name__ == "__main__":
    app.run()