from flask import Flask, url_for, render_template, request, redirect, make_response, session
import pandas as pd
import recommender

# create app and read in users
app = Flask(__name__)
app.secret_key = "thisisasecretkeyyoullneverguessit"

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ratings/<userID>")
def ratings(userID):

    user_ratings = get_user_ratings(int(userID))

    # if empty then return message saying none rated, otherwise return and display table
    if user_ratings.empty:
        empty_message = "<h2>You haven't rated anything yet!</h2>"
        return render_template("ratings.html", id=userID, ratings=empty_message)

    user_ratings = user_ratings[['Book ID', 'Title', 'Genre', 'Rating']]

    return render_template("ratings.html", id=userID, ratings=user_ratings.to_html(index=False\
        ,classes=["table-bordered", "table-dark", "table-striped", "table-hover", "table-sm", "display-table"]))


@app.route("/recommendations/<userID>")
def recommendations(userID):

    user_ratings = get_user_ratings(int(userID))
    if user_ratings.empty:
        empty_message = "<h2>You must rate at least one book to receive a recommendation!</h2>"
        return render_template("recommendations.html", id=userID, recommendations=empty_message)

    predictions, books, ratings = recommender.read_and_predict()
    user_data, user_recommendations = recommender.recommend_books(predictions, int(userID), books, ratings, num_recommendations=5)
    return render_template("recommendations.html", id=userID, recommendations=user_recommendations.to_html(index=False\
        ,classes=["table-bordered", "table-dark", "table-striped", "table-hover", "table-sm"]))


@app.route("/validate", methods = ['POST'])
def validate():

    # validates if user ID is actual user
    users = pd.read_csv("dataset/users.csv")
    userID = request.form['userID']
    
    for index, row in users.iterrows():
        if int(userID) == int(row['userID']):
            session['userID'] = int(userID)
            return "works", 200
    session.pop('userID', None)
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


def get_user_ratings(userID):

    # read in ratings and take only the ones rated by current user
    ratings = pd.read_csv("dataset/ratings.csv")
    user_ratings = ratings.loc[ratings['userID'] == userID]

    # remove user ID column and sory by book ID
    user_ratings = user_ratings.drop(['userID'], axis=1)
    user_ratings = user_ratings.sort_values(by=['Book ID'])

    # Add book title and genre
    books = pd.read_csv("dataset/books.csv")
    user_ratings = (user_ratings.merge(books, how='left', left_on='Book ID', right_on='Book ID'))

    return user_ratings


if __name__ == "__main__":
    app.run()