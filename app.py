import streamlit as st
import pickle
import requests
import pandas as pd

movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))

def fetch_poster(movie_id):
    response = requests.get("https://imdb.iamidiotareyoutoo.com/photo/{movie_id}?api_key=dlaa405518bcd86047c245cdc2bfe4e5&language=en-US")
    data = response.json()
    # tmdb it is database which consist of all the details of the movies
    return "https://image.tmdb.org/t/p/w500/"+data["poster_path"]


def recommed_movies(movie):

    movie_id = movies[movies["title"]== movie].index[0]
    distance = similarity[movie_id]
    movies_list = sorted(list(enumerate(distance)),reverse=True,key=lambda x : x[1])[1:6]
    # reason why indexing starting from [1:6] because every vector has high similarity to itself

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)

        recommended_movies_posters.append(fetch_poster(movie_id))
        
        
    return recommended_movies,recommended_movies_posters

# code for interface designing

st.title("Movie Recommendation System")

user_input = st.selectbox( "Enter movie name?", movies["title"].values)

if st.button("Recommend"):
    names , posters = recommed_movies (user_input)

    col1, col2, col3, col4, col5 = st.columns(5)

    columns = [col1, col2, col3, col4, col5]

    for i,col in enumerate(columns):

        with col:
            st.text(names[i])
            st.image(posters[i])



    
