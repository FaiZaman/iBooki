import pandas as pd
import numpy as np
from scipy.sparse.linalg import svds

def read_and_predict():

    # read in dataframes
    books = pd.read_csv("dataset/books.csv")
    ratings = pd.read_csv("dataset/ratings.csv")

    # convert to numeric and combine ratings per user
    books['Book ID'] = books['Book ID'].apply(pd.to_numeric)
    ratings_combined = ratings.pivot(index = "userID", columns="Book ID", values="Rating").fillna(0)

    # demean the ratings
    ratings_demeaned = ratings_combined.as_matrix()
    mean_rating = np.mean(ratings_demeaned, 1)
    ratings_demeaned = ratings_demeaned - mean_rating.reshape(-1, 1)

    # singular value decomposition
    U, sigma, Vt = svds(ratings_demeaned, k=8)
    sigma = np.diag(sigma)

    # get predicted ratings for all users
    all_predicted_ratings = np.dot(np.dot(U, sigma), Vt) + mean_rating.reshape(-1, 1)
    predictions = pd.DataFrame(all_predicted_ratings, columns=ratings_combined.columns)
    return predictions, books, ratings

def recommend_books(predictions, userID, books, ratings, num_recommendations=5):

    # get and sort user predictions
    user_index_ID = userID - 1    
    user_predictions = predictions.iloc[user_index_ID].sort_values(ascending=False)

    # get the user data and merge with book data
    user_data = ratings[ratings['userID'] == (userID)]
    user_rated = (user_data.merge(books, how = 'left', left_on = 'Book ID', right_on = "Book ID").sort_values(['Rating'], ascending=False))

    # recommend the highest rated books that the user has not seen yet
    recommendations = (books[~books['Book ID'].isin(user_rated['Book ID'])].merge\
        (pd.DataFrame(user_predictions).reset_index(), how='left', left_on='Book ID', right_on="Book ID").rename\
        (columns = {user_index_ID: 'Predictions'}).sort_values('Predictions', ascending=False).iloc[:num_recommendations, :-1])

    return user_data, recommendations

#predictions, books, ratings = read_and_predict()
#recommend_books(predictions, userID=, books=books, ratings=ratings, num_recommendations=5)
