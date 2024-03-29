from flask import Flask, url_for, render_template, request, redirect, make_response, session
import pandas as pd
import recommender

# create app and read in users
app = Flask(__name__)
app.secret_key = "thisisasecretkeyyoullneverguessit"

@app.route("/")
def home():
    session.pop('userID', None)
    return render_template("index.html")


@app.route("/ratings/<userID>")
def ratings(userID):

    userID = session['userID']
    user_ratings = get_user_ratings(int(userID))

    # if empty then return message saying none rated, otherwise return and display table
    if user_ratings.empty:
        empty_message = "<h2>You haven't rated anything yet!</h2>"
        return render_template("ratings.html", id=userID, ratings=empty_message)

    user_ratings = user_ratings[['bookID', 'Title', 'Genre', 'Rating']]

    return render_template("ratings.html", id=userID, ratings=user_ratings.to_html(index=False\
        ,classes=["table-bordered", "table-dark", "table-striped", "table-hover", "table-sm"]))


@app.route("/recommendations/<userID>")
def recommendations(userID):

    userID = session['userID']
    user_ratings = get_user_ratings(int(userID))

    # if empty then return message saying that at least one must be rated for recommendations, otherwise display table
    if user_ratings.empty:
        empty_message = "<h2>You must rate at least one book to receive a recommendation!</h2>"
        return render_template("recommendations.html", id=userID, recommendations=empty_message)

    predictions, books, ratings = recommender.read_and_predict()
    user_data, user_recommendations = recommender.recommend_books(predictions, int(userID), books, ratings, num_recommendations=5)
    return render_template("recommendations.html", id=userID, recommendations=user_recommendations.to_html(index=False\
        ,classes=["table-bordered", "table-dark", "table-striped", "table-hover", "table-sm"]))


@app.route("/search", methods = ['POST'])
def search():

    search_query = request.form['search_query']
    search_query = search_query.title()
    userID = session['userID']

    # merge and group the dataframes, then search for keyword
    books = pd.read_csv("dataset/books.csv")
    ratings = pd.read_csv("dataset/ratings.csv")
    merged_data = (ratings.merge(books, how='left', left_on='bookID', right_on='bookID'))
    capitilised = merged_data['Title'].str.title()
    capitilised = capitilised.to_frame()
    merged_data['Title'] = capitilised

    # if no results return empty message otherwise return results
    search_results = merged_data[merged_data['Title'].str.contains(search_query, na=False)]
    if search_results.empty:
        empty_message = "<h2>No books found!</h2>"
        return render_template("update.html", id=userID, search_results=empty_message)

    search_results.groupby(['bookID', 'Title', 'Genre'])
    search_results = search_results.drop_duplicates(['bookID'])
    modified_search_results = search_results.drop(columns=['userID', 'Rating']).sort_values(by=['bookID'])
        
    return render_template("update.html", id=userID, search_results=modified_search_results.to_html(index=False\
        ,classes=["table-bordered", "table-dark", "table-striped", "table-hover", "table-sm"]))


@app.route("/getBooks", methods = ['GET'])
def getBooks():

    userID = session['userID']
    books = pd.read_csv("dataset/books.csv")

    return render_template("update.html", id=userID, search_results=books.to_html(index=False\
        ,classes=["table-bordered", "table-dark", "table-striped", "table-hover", "table-sm"]))


@app.route("/update/<userID>")
def update(userID):

    search_results = ""
    userID = session['userID']

    # search functionality goes here

    return render_template("update.html", id=userID, search_results=search_results)


@app.route("/validateUser", methods = ['POST'])
def validateUser():

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

    session.pop('userID', None)
    users = pd.read_csv("dataset/users.csv")
    userID = request.form['userID']

    exists = False
    for index, row in users.iterrows():
        if int(userID) == int(row['userID']):
            exists = True
            break
    if exists:
        return "oops", 400
    
    # if ID does not exist append to DF and csv and set in session
    session['userID'] = int(userID)
    users = users.append({'userID': userID}, ignore_index=True)
    users_csv = users.to_csv(r'dataset/users.csv', index=False)
    return "works", 200


@app.route("/getUserID", methods = ['GET'])
def getUserID():

    userID = session['userID']
    return userID, 200


@app.route("/updateRating", methods = ['POST'])
def updateRating():

    bookID = int(request.form['book-id'])
    new_rating = int(request.form['new-rating'])
    userID = session['userID']
    
    verified = validateBook(bookID)
    if not verified or new_rating > 5:
        error_message = "<h2>Invalid book ID or rating. Please try again.</h2>"
        return render_template("update.html", id=userID, search_results=error_message)

    ratings = pd.read_csv("dataset/ratings.csv")

    # update the rating or add if it doesn't exist
    matches = ratings.loc[(ratings.userID == userID) & (ratings['bookID'] == bookID)]
    if matches.empty:
        ratings = ratings.append({'userID': userID, 'bookID': bookID, 'Rating': new_rating}, ignore_index=True)

    ratings.loc[(ratings.userID == userID) & (ratings['bookID'] == bookID)] = [[userID, bookID, new_rating]]
    ratings_csv = ratings.to_csv(r'dataset/ratings.csv', index=False)
    user_ratings = get_user_ratings(userID)

    return render_template("ratings.html", id=userID, ratings=user_ratings.to_html(index=False\
        ,classes=["table-bordered", "table-dark", "table-striped", "table-hover", "table-sm"]))


@app.route("/deleteRating", methods = ['POST'])
def deleteRating():
    
    bookID = int(request.form['book-id'])
    verified = validateBook(bookID)
    userID = session['userID']

    if not verified:
        error_message = "<h2>Invalid book ID. Please try again.</h2>"
        return render_template("update.html", id=userID, search_results=error_message)

    ratings = pd.read_csv("dataset/ratings.csv")

    matches = ratings.loc[(ratings.userID == userID) & (ratings['bookID'] == bookID)]
    if matches.empty:
        print("is empty")
        return "nope", 400

    index = ratings.loc[(ratings.userID == userID) & (ratings['bookID'] == bookID)].index[0]
    ratings = ratings.drop([index])
    ratings_csv = ratings.to_csv(r'dataset/ratings.csv', index=False)
    user_ratings = get_user_ratings(userID)

    return render_template("ratings.html", id=userID, ratings=user_ratings.to_html(index=False\
        ,classes=["table-bordered", "table-dark", "table-striped", "table-hover", "table-sm"]))



def validateBook(bookID):

    books = pd.read_csv("dataset/books.csv")

    for index, row in books.iterrows():
        if int(bookID) == int(row['bookID']):
            return True
    return False


def get_user_ratings(userID):

    # read in ratings and take only the ones rated by current user
    ratings = pd.read_csv("dataset/ratings.csv")
    user_ratings = ratings.loc[ratings['userID'] == userID]

    # remove user ID column and sory by bookID
    user_ratings = user_ratings.drop(['userID'], axis=1)
    user_ratings = user_ratings.sort_values(by=['bookID'])

    # Add book title and genre
    books = pd.read_csv("dataset/books.csv")
    user_ratings = (user_ratings.merge(books, how='left', left_on='bookID', right_on='bookID'))

    return user_ratings


if __name__ == "__main__":
    app.run(debug=True)