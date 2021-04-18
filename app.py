import flask
import difflib
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import omdb
import math    
import RS.rs as rs
import os.path

from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="geoapiExercises")

app = flask.Flask(__name__, template_folder='templates')

df2 = pd.read_csv('./model/tmdb.csv')

# if using the module level client
omdb.set_default('apikey', '101ed70')

ratings = pd.read_csv('./model/ratings.dat', sep='::', encoding='latin-1', names=['user_id', 'movie_id', 'rating', 'timestamp'])
users = pd.read_csv('./model/users.dat', sep='::', encoding='latin-1', names=['user_id','gender','age','occupation', 'Zip-code'])
movies = pd.read_csv('./model/movies.dat', sep='::', encoding='latin-1', names=['movie_id', 'title', 'genres'])


list_user = users.to_json(orient='index')
list_movie = movies.to_json(orient='index')
dataset = pd.merge(pd.merge(movies, ratings),users)
# Break up the big genre string into a string array
movies['genres'] = movies['genres'].str.split('|')
# Convert genres to string value
movies['genres'] = movies['genres'].fillna("").astype('str')
from sklearn.feature_extraction.text import TfidfVectorizer
tf = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
tfidf_matrix = tf.fit_transform(movies['genres'])
from sklearn.metrics.pairwise import linear_kernel
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
# Build a 1-dimensional array with movie titles
titles = movies['title']
indices = pd.Series(movies.index, index=movies['title'])
 
if os.path.isfile('./model/item_based_model.sav'):
        filename = './model/item_based_model.sav'
        svd_model = rs.load_model(filename)
        print("\n\nModel load with RMSE : ", svd_model.RMSE(),'\n\n\n')
else:
    svd = rs.SVD(ratings, movies, K = 50, user_based = 0)
    #Fit model tập dữ liệu
    svd.fit()
    #Save model
    filename = './model/item_based_model.sav'
    rs.save_model(svd, filename)
    svd_model = rs.load_model(filename)
    print("\n\nModel load with RMSE : ", svd_model.RMSE(),'\n\n')

# count = CountVectorizer(stop_words='english')
# count_matrix = count.fit_transform(df2['soup'])

# cosine_sim2 = cosine_similarity(count_matrix, count_matrix)

# df2 = df2.reset_index()
# indices = pd.Series(df2.index, index=df2['title'])
# all_titles = [df2['title'][i] for i in range(len(df2['title']))]

def get_name_and_year(title):
    word_list = title.split(' ') 
    year = word_list[-1]
    year = year.replace('(','')
    year = year.replace(')','')
    name = title.rsplit(' ', 1)[0]
    while name.find("(")>0:
        name = name.rsplit(' ', 1)[0]
    name = name.rsplit(',', 1)[0]
    return name,year  

def search_movie_with_title(title,year =None):
    if pd.isna(year)==False :
        movie =omdb.get(title=title, year=year, fullplot=True, tomatoes=True)
    else:
        movie =omdb.get(title=title, fullplot=True, tomatoes=True)
    if movie:
        return movie
    else: 
        return {}


def genre_recommendations(title):
    idx = indices[str(title)]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:21]
    movie_indices = [i[0] for i in sim_scores]
    return titles.iloc[movie_indices]



# Set up the main route
@app.route('/')
@app.route('/index')
def index():
    return flask.render_template('index.html')

@app.route('/content-base')
def content_base():
    return flask.render_template('content-base.html')

@app.route('/search-movie',methods=['GET','POST'])
def search_movie():
    if flask.request.method == 'GET':
        return flask.render_template('search-movie.html')
    elif flask.request.method == 'POST':
        m_name = flask.request.form['movie_name']
        headers = {
            't': m_name,
            'plot':'full',
           'apikey':'101ed70'
            }
        response = requests.get("https://www.omdbapi.com/", params=headers)
        if(response.status_code==200):
            movie_info = response.json()
            return flask.render_template('movie-info.html',movie_info=movie_info )
        else:
            return flask.render_template('index.html')

@app.route('/recommendation',methods=['GET'])
def recommendation():
    return flask.render_template('select-recommend-page.html')

@app.route('/recommend-for-userid',methods=['GET','POST'])
def recommenforuser():
    if flask.request.method == 'GET':
        return flask.render_template('recommendforuser.html')
    if flask.request.method == 'POST':
        user_id = flask.request.form['user_id']
        user_id = int(user_id.title())
        exists_user = user_id in users.user_id
        if exists_user:
            list_movie,list_recommend = svd_model.recommend_movies(user_id,20)
            # return flask.render_template('recommendforuser.html')
            arr=[]

            for i in list_recommend.values.tolist():
                     
                    word_list = i[1].split(' ') 

                    year = word_list[-1]
                    year = year.replace('(','')
                    year = year.replace(')','')
                    text = i[1].rsplit(' ', 1)[0]
                    while text.find("(")>0:
                        text = text.rsplit(' ', 1)[0]
                    text = text.rsplit(',', 1)[0]
                    movie_search = {}
                    
                    movie_search = search_movie_with_title(text,year)
                    print('\n\n',text,'\n',year)
                    print(movie_search)
                    if movie_search:
                        arr.append(movie_search)
                    else:
                        temp ={'title':text,'year':year}
                        arr.append(temp)
            return flask.render_template('list-recommend.html',list_item=arr)
            



@app.route('/predict-rating-movie-for-userid',methods=['GET','POST'])
def recommend_for_user():
    if flask.request.method == 'GET':
        return flask.render_template('select_user_id_and_movie_id.html')
    if flask.request.method == 'POST':
        user_id = flask.request.form['user_id']
        movie_id = flask.request.form['movie_id']
        user_id = int(user_id.title())
        movie_id = int(movie_id.title())
        exists = movie_id in movies.movie_id
        exists_user = user_id in users.user_id
        if exists and exists_user:
            movie_json = movies[movies['movie_id'] == movie_id]
            user_json = users[users['user_id'] == user_id]
            movie_json = movie_json.iloc[0]["title"]
            name,year = get_name_and_year(movie_json)
            movie = search_movie_with_title(name,year)
            predict = svd_model.predict(user_id,movie_id)
            age = user_json.iloc[0]["age"]
            male = user_json.iloc[0]["gender"]
            location = geolocator.geocode(user_json.iloc[0]["Zip-code"])
            
            return flask.render_template('predict_movie_with_id.html',movie=movie,predict=predict,age=age,male=male,location=location)
        else:
            return flask.render_template('predict_movie_with_id_error.html')

@app.route('/predict-top-movie-for-user-id',methods=['POST'])
def redict_top_movie_for_user():
    ab,c=svd_model.recommend_movies(1,20)
    print(c)

 

@app.route('/search-movie-for-recommend',methods=['GET','POST'])


def demo():
    if flask.request.method == 'GET':
        return flask.render_template('search-movie.html')
    if flask.request.method == 'POST':
        m_name = flask.request.form['movie_name']
        m_name = m_name.title()
        movie = search_movie_with_title(m_name)
        if movie:
            print(movie)
            replace_name = str(movie['title'])+" ("+str(movie['year'])+")"
            arr = []

            if replace_name in titles.tolist():
                print("Recommend Movie Name",genre_recommendations(replace_name))
                for i in genre_recommendations(replace_name).head(20):
                    word_list = i.split(' ') 

                    year = word_list[-1]
                    year = year.replace('(','')
                    year = year.replace(')','')
                    text = i.rsplit(' ', 1)[0]
                    while text.find("(")>0:
                        text = text.rsplit(' ', 1)[0]
                    text = text.rsplit(',', 1)[0]
                    movie_search = {}
                    
                    movie_search = search_movie_with_title(text,year)
                    print('\n\n',text,'\n',year)
                    print(movie_search)
                    if movie_search:
                        arr.append(movie_search)
                    else:
                        temp ={'title':text,'year':year}
                        arr.append(temp)
                for i in arr:
                    print(i,'\n')
                print(arr)
                # return json.dumps(arr)
                return flask.render_template('list-recommend.html',list_item=arr)
            else:
                return(flask.render_template('negative.html',name=replace_name,list_name=titles.tolist()))
        else:
                return(flask.render_template('negative.html',name=m_name,list_name=titles.tolist()))

if __name__ == '__main__':
    app.config['ENV'] = 'development'
    app.config['DEBUG'] = True
    app.config['TESTING'] = True
    app.run(debug=True, use_debugger=False, use_reloader=False)