import pickle
import streamlit as st
import requests

st.set_page_config(layout="wide")
print('***************HELLO***********')
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:4]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters


st.header('Finally, the answer to "What should we watch tonight?"')
movies = pickle.load(open('/app/moderndatenight/movie_list.pkl','rb'))
similarity = pickle.load(open('/app/moderndatenight/similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie1 = st.selectbox(
    "Your Movie",
    movie_list
)

movie_list = movies['title'].values
selected_movie2 = st.selectbox(
    "Their Movie",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie1)
    recommended_movie_names1,recommended_movie_posters1 = recommend(selected_movie2)
    for i in enumerate(st.columns(len(recommended_movie_names))):
        i[1].text(recommended_movie_names[i[0]])
        i[1].image(recommended_movie_posters[i[0]])
    if selected_movie1!=selected_movie2:
        for i in enumerate(st.columns(len(recommended_movie_names1))):
            i[1].text(recommended_movie_names1[i[0]])
            i[1].image(recommended_movie_posters1[i[0]])
