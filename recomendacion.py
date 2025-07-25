import streamlit as st
import pandas as pd
import numpy as np
import requests
import os
from dotenv import load_dotenv
import datetime
import time 
import pytz 

load_dotenv()


st.set_page_config(
    page_title="CineBot - Recomendador",
    page_icon="🎬",
    layout="wide"
)

st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    /* para el sidebar*/
    [data-testid="stSidebar"] {
        background-color: rgba(30, 30, 30, 0.95);
        color: white;
        padding: 1rem;
    }
    .sidebar-text {
        font-family: 'Segoe UI', sans-serif;
        font-size: 16px;
        color: #f1f1f1;
    }
    .blink {
        animation: blink-animation 1.5s steps(5, start) infinite;
        color: #FF9800;
        font-weight: bold;
    }
    @keyframes blink-animation {
        to { visibility: hidden; }
    }
    .slide-in {
        animation: slideIn 1s ease-in-out;
    }
    @keyframes slideIn {
        from { transform: translateX(-100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    .fade-in {
        animation: fadeIn 1s ease-in-out;
    }
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    .movie-title {
        font-family: 'Poppins', sans-serif;
        font-weight: 300;
        color: #ffffff;
        text-align: center;
        margin-top: 0.5rem;
        font-size: 16px;
        letter-spacing: 0.5px;
    }
    .stButton>button {
        background-color: #9c1204;
        color: white;
        border-radius: 8px;
        padding: 10px 16px;
        font-size: 16px;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: black;
    }
    

    /* para las redes sociales*/
        .social-icon {
            font-size: 25px;
            margin: 0 20px;
            transition: transform 1s ease, background-color 0.3s, box-shadow 0.3s;
            padding: 12px;
            border-radius: 50%;
            display: inline-block;
        }
        .social-icon:hover,
        .social-icon:active {  
            transform: rotate(360deg) scale(1.2); 
            box-shadow: 0 0 20px rgba(255, 87, 34, 0.7);  
        }
        .social-icon i {
            color: white;
        }
        
    
    /* para el titulo Sistema de Películas en Tiempo Real*/
        @keyframes slideInFromLeft {
            0% { transform: translateX(-100%); opacity: 0; }
            50% { transform: translateX(20px); opacity: 0.7; }
            100% { transform: translateX(0); opacity: 1; }
        }
        @keyframes color-shift {
            0% { 
                color: #FF5722; 
                box-shadow: 0 0 10px 6px #FF5722; 
            }
            10% { 
                color: #3F51B5; 
                box-shadow: 0 0 10px 6px #3F51B5; 
            }
            20% { 
                color: #4CAF50; 
                box-shadow: 0 0 10px 6px #4CAF50; 
            }
            30% { 
                color: #FFC107; 
                box-shadow: 0 0 10px 6px #FFC107; 
            }
            40% { 
                color: #9C27B0; 
                box-shadow: 0 0 10px 6px #9C27B0; 
            }
            50% { 
                color: #FF9800; 
                box-shadow: 0 0 10px 6px #FF9800; 
            }
            60% { 
                color: #00BCD4; 
                box-shadow: 0 0 10px 6px #00BCD4; 
            }
            70% { 
                color: #8BC34A; 
                box-shadow: 0 0 10px 6px #8BC34A; 
            }
            80% { 
                color: #673AB7; 
                box-shadow: 0 0 10px 6px #673AB7; 
            }
            90% { 
                color: #E91E63; 
                box-shadow: 0 0 10px 6px #E91E63; 
            }
            100% { 
                color: #FF5722; 
                box-shadow: 0 0 10px 6px #FF5722; 
            }
        }
        .animated-title {
            font-family: 'Poppins', sans-serif;
            font-size: 36px;
            font-weight: 700;
            text-align: center;
            animation: 
                slideInFromLeft 1.1s ease-out, 
                color-shift 1.1s ease-in-out infinite; 
            transition: transform 0.5s ease;
            cursor: pointer;
        }
        .animated-title:hover {
            transform: scale(1.1); 
        }
    </style>
""", unsafe_allow_html=True)


def fetch_poster(movie_id):
    try:
        api_key = os.getenv("TMDB_API_KEY")
        if not api_key:
            st.error("⚠️ API Key no encontrada. Verifica tu archivo .env.")
            return 'https://via.placeholder.com/500x750?text=Sin+API+Key'

        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if 'poster_path' in data and data['poster_path']:
            return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"
        else:
            return 'https://via.placeholder.com/500x750?text=Poster+no+disponible'
    except requests.exceptions.RequestException as e:
        st.error(f"Error al obtener el póster: {e}")
        return 'https://via.placeholder.com/500x750?text=Error+de+conexión'

def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
    except IndexError:
        st.error(f"Película '{movie}' no encontrada.")
        return [], []

    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movie_names, recommended_movie_posters

with st.sidebar:
    st.markdown('<h2 class="slide-in">🎬 CineBot</h2>', unsafe_allow_html=True)
    st.markdown('<h4 class="sidebar-text">Tu Guía Instantánea de Películas 🎥</h4>', unsafe_allow_html=True)
    st.image('images/sololeveling.gif', use_container_width=True)
    st.markdown('<hr>', unsafe_allow_html=True)
    st.image('images/goku.gif', use_container_width=True)
    st.markdown('<hr>', unsafe_allow_html=True)
    st.image('images/gojo.gif', use_container_width=True)
    st.markdown('<hr>', unsafe_allow_html=True)
    st.image('images/shipudeen.gif', use_container_width=True)
    st.markdown('<hr>', unsafe_allow_html=True)

    st.markdown('<p class="sidebar-text">✨ Recomendaciones de películas en tiempo real con <strong>CineBot</strong>.</p>', unsafe_allow_html=True)
    st.markdown(""" 
        <div style='font-family: "Segoe UI", sans-serif; font-size: 13px; color: #aaa; margin-top: 20px;'>
            <p style="margin-bottom: 2px;">📌 <span style="font-weight: 300;">Autor</span></p>
            <hr style="border: none; border-top: 0.3px solid #ccc; margin: 4px 0;">
            <p style="margin-bottom: 2px;">👤 <span style="font-weight: 300;">Max Winchez</span></p>
            <p style="margin-top: 0;">📧 <span style="font-weight: 300;">maxwinchez@gmail.com</span></p>
        </div>
    """, unsafe_allow_html=True)

try:
    movies = pd.read_pickle('movies.pkl')
    similarity = np.array(pd.read_pickle('similarity.pkl'))
except Exception as e:
    st.error(f"Error al cargar los datos: {e}")


st.markdown("""
    <div class="animated-title">
        🎥 Sistema de Películas en Tiempo Real
    </div>
    <br>
""", unsafe_allow_html=True)
selected_movie = st.selectbox("🎞️ Selecciona una película", movies['title'].values)

if st.button('🎯 Mostrar Recomendaciones'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    if recommended_movie_names:
        cols = st.columns(5)
        for i, col in enumerate(cols):
            if i < len(recommended_movie_names):
                col.markdown(
                    f"<div class='fade-in'><img src='{recommended_movie_posters[i]}' width='100%'><p class='movie-title'>{recommended_movie_names[i]}</p></div>",
                    unsafe_allow_html=True
                )
    else:
        st.warning("No se encontraron recomendaciones.")
        
        
st.markdown("""
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" rel="stylesheet">
    <div style="text-align: center;">
        <br><br>
        <h4 style="font-size: 18px; color: #888; margin-bottom: 10px;">Encuentrame en</h4>
        <a href="https://www.facebook.com/wr.max.404270" target="_blank" class="social-icon">
            <i class="fab fa-facebook-f"></i>
        </a>
        <a href="https://github.com/" target="_blank" class="social-icon">
            <i class="fab fa-github"></i>
        </a>
        <a href="https://www.linkedin.com/in/max-winchez-rivera-3719a4237/" target="_blank" class="social-icon">
            <i class="fab fa-linkedin"></i>
        </a>
    </div>
""", unsafe_allow_html=True)


footer_placeholder = st.empty()
peru_tz = pytz.timezone('America/Lima')

while True:
    current_year = datetime.datetime.now(peru_tz).year
    current_time = datetime.datetime.now(peru_tz).strftime("%H:%M:%S")

    footer_placeholder.markdown(f"""
        <hr style='margin-top: 3rem;'>
        <div style='text-align: center; font-size: 14px; color: #888;'>
            © {current_year} CineBot Max | Lima, Perú. Todos los derechos reservados. {current_time}
        </div>
    """, unsafe_allow_html=True)

    time.sleep(1)
    

