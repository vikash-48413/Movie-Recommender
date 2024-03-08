#
# import streamlit as st
# import pandas as pd
# import pickle
# import requests
#
# def fetch_poster(movie_id):
#     response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=53a2d777efe008fac676de2a3713c751'.format(movie_id))
#     data = response.json()
#     poster_path = data.get('poster_path')
#     if poster_path:
#         return "https://image.tmdb.org/t/p/w500/" + poster_path
#     else:
#         return None
#
# def recommend(movie):
#     movie_index = movies[movies['title'] == movie].index[0]
#     distances = similarity[movie_index]
#     movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
#
#     recommended_movies = []
#     recommended_movies_posters = []
#     for i in movies_list:
#         movie_id = movies.iloc[i[0]].movie_id
#
#         recommended_movies.append(movies.iloc[i[0]].title)
#
#         # fetch poster from API
#         poster_url = fetch_poster(movie_id)
#         if poster_url:
#             recommended_movies_posters.append(poster_url)
#
#     return recommended_movies, recommended_movies_posters
#
# movies_dict = pickle.load(open('movie_dict.pkl','rb'))
# movies = pd.DataFrame(movies_dict)
#
# similarity = pickle.load(open('similarity.pkl','rb'))
#
# st.title('Movie Recommender System')
#
# selected_movie_name = st.selectbox(
#     'Select a movie:',
#     movies['title'].values)
#
# if st.button('Recommend'):
#     names, posters = recommend(selected_movie_name)
#
#     col1, col2, col3, col4, col5 = st.columns(5)
#
#     with col1:
#         st.image(posters[0], use_column_width=True)
#         st.caption(names[0])
#
#     with col2:
#         st.image(posters[1], use_column_width=True)
#         st.caption(names[1])
#
#     with col3:
#         st.image(posters[2], use_column_width=True)
#         st.caption(names[2])
#
#     with col4:
#         st.image(posters[3], use_column_width=True)
#         st.caption(names[3])
#
#     with col5:
#         st.image(posters[4], use_column_width=True)
#         st.caption(names[4])



import streamlit as st
import pandas as pd
import pickle
import requests

API_KEY = '53a2d777efe008fac676de2a3713c751'
BASE_URL = 'https://api.themoviedb.org/3/movie/'
POSTER_URL = 'https://image.tmdb.org/t/p/w500/'

def fetch_poster(movie_id):
    response = requests.get(f'{BASE_URL}{movie_id}?api_key={API_KEY}')
    data = response.json()
    return f"{POSTER_URL}{data['poster_path']}" if data.get('poster_path') else None

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:6]

    recommended_movies = [movies.iloc[i[0]].title for i in movies_list]
    recommended_movies_posters = [fetch_poster(movies.iloc[i[0]].movie_id) for i in movies_list]

    return recommended_movies, recommended_movies_posters

movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox('Select a movie:', movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(5)

    for col, name, poster in zip(cols, names, posters):
        with col:
            st.image(poster, use_column_width=True)
            st.caption(name)

