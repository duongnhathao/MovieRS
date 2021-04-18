import pandas as pd 
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse 
from scipy.sparse.linalg import svds
from sklearn.metrics import mean_squared_error
from math import sqrt
import json
import pickle5 as pickle

# Reading ratings file
#ratings = pd.read_csv("/content/drive/MyDrive/nam 4/hk2/BI/final/demo/dataset/ml-1m/ml-1m/ratings.dat", sep='::', encoding='latin-1', names=['user_id', 'movie_id', 'rating', 'timestamp'])
# movies = pd.read_csv('../model/movies.dat', sep='::', names=['movie_id', 'title', 'genres'])
# ratings = pd.read_csv('../model/ratings.dat', sep='::', encoding='latin-1', names=['user_id', 'movie_id', 'rating', 'timestamp'])

class SVD(object):
    
    #Hàm khởi tạo đầu vào
    def __init__(self, data_ratings, data_movies, K, user_based = 1):
        self.data = data_ratings
        self.movies = data_movies
        self.K = K
        self.user_based = user_based
    def setData(self, data_ratings, data_movie,K):
        self.data = data_ratings
        self.movies = data_movie
        self.K = K

    #Hàm tạo ma trận Utility 
    def create_matrixUtility(self):
        Ratings_df = self.data.pivot(index = 'user_id', columns ='movie_id', values = 'rating').fillna(0)
        return Ratings_df
    
    #Hàm tính trung bình ratings
    def ratings_mean(self):
        R = self.create_matrixUtility()
        
        if self.user_based: #Theo UserID
            users_ratings_mean = pd.DataFrame(self.data.groupby('user_id')['rating'].mean())
            return users_ratings_mean.values
        else: #Theo movie_id
            items_ratings_mean = pd.DataFrame(self.data.groupby('movie_id')['rating'].mean())
            return items_ratings_mean.values
    
    #Hàm chuẩn hóa ma trận (Normalized utility matrix)
    #Ma trận Utility - Mean ratings; Các vị trí chưa rating thay bằng 0.0
    def normalize_matrix(self):
        R = self.create_matrixUtility()
        R = R.values #Chuyển dataframe sang array để tính toán
        ratings_mean = self.ratings_mean()
        
        #Lấy ra kích thước của mảng index là userID, col là movieID
        index, col = R.shape  
        if self.user_based: #Theo user based 
            for i in range(0, index):
              for j in range(0, col):
                if (R[i][j] != 0):
                  R[i][j] = R[i][j] - ratings_mean[i][0]
            return R
        else: #Theo item based
            for i in range(0, col):
                for j in range(0, index):
                    if (R[j][i] != 0):
                      R[j][i] = R[j][i] - ratings_mean[i][0]
            return R
    
    #Hàm fit model
    def fit(self):
        Ratings_demeaned = self.normalize_matrix() #Ma trận normalized
        U, sigma, Vt = svds(Ratings_demeaned, self.K)  #Sử dụng sdvs của Scipy
        S = sorted(sigma, reverse=True) #sắp xếp lại giá trị trong Sigmal theo thứ tự giảm dần
        sigma = np.diag(S)
        all_predicted_ratings = np.dot(np.dot(U, sigma), Vt)
        
        ratings_mean = self.ratings_mean()  #Ratings mean  
        if self.user_based: #Theo user based 
            self.preds = all_predicted_ratings + ratings_mean.reshape(-1, 1)
        else: ##Theo item based 
            pred = all_predicted_ratings.transpose() + ratings_mean.reshape(-1, 1)
            self.preds = pred.transpose()
        
    #Hàm predict của 1 cặp user - movie
    def predict(self, user_id, movie_id):
        ratings_df = self.create_matrixUtility()
        preds = pd.DataFrame(self.preds, columns = ratings_df.columns, index = ratings_df.index)
        return {'userid':user_id, 'movie_id' :movie_id, 
                'actual' :ratings_df[movie_id][user_id],
                'pred' :round(preds[movie_id][user_id],3)}
  

    #Hàm recommend movie cho user
    #Truyền vào userID, file data movie và số lượng phim cầm recommend
    def recommend_movies(self, userID, num_recommendations):
        Ratings = self.create_matrixUtility()
        preds = pd.DataFrame(self.preds, columns = Ratings.columns) #chuyển self.preds về dataframe để recommend

        # Lấy và sắp xếp lại dự đoán ratings của user
        user_row_number = userID -1 # Do mảng dự đoán self.preds là mảng nên bắt đầu từ 0 cho nên cần -1 để theo đung vị trí
        sorted_user_predictions = preds.iloc[user_row_number].sort_values(ascending=False) # User ID bắt đầu từ 1

        #Lấy data của user và merge với thông tin của file data movie
        user_data = self.data[self.data.user_id == (userID)]
        user_full = (user_data.merge(self.movies, how = 'left', left_on = 'movie_id', right_on = 'movie_id').
                         sort_values(['rating'], ascending=False)
                     )

        #Recommend các bộ phim có dự đoán ratings cao nhất mà user đó chưa xem
        recommendations = (self.movies[~self.movies['movie_id'].isin(user_full['movie_id'])].
             merge(pd.DataFrame(sorted_user_predictions).reset_index(), how = 'left',
                   left_on = 'movie_id',
                   right_on = 'movie_id').
             rename(columns = {user_row_number: 'Predictions'}).
             sort_values('Predictions', ascending = False).
                           iloc[:num_recommendations, :-1]
                          )
        #Merge lại để lấy cột ratings dự đoán
        recommendations = pd.merge(recommendations, pd.DataFrame(sorted_user_predictions).reset_index(), on='movie_id')
        recommendations.rename(columns={userID-1:'Pre_ratings'}, inplace=True)
        return user_full,  recommendations
    
    def conver_json(self, data):
      return json.loads(data.to_json(orient='index'))

    #Hàm tính độ lỗi RMSE
    def RMSE(self):
      ratings_df = self.create_matrixUtility()
      ratings = ratings_df.values       
      y_actuals = ratings[ratings.nonzero()].flatten() #Lấy ra ratings thực tế
      y_preds = self.preds[ratings.nonzero()].flatten() #Lấy ra ratings dự đoán theo y_actual
    
      return mean_squared_error(y_preds, y_actuals, squared=False)

def save_model(model, filename):
    pickle.dump(model, open(filename, 'wb'))
    print("Done!")

def load_model(filename):
    return pickle.load(open(filename, 'rb'))



