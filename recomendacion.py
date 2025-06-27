import streamlit as st
import pandas as pd
import numpy as np
import requests

# 📄 Configuración general de la página
st.set_page_config(
    page_title="CineBot - Recomendador",
    page_icon="🎬",
    layout="wide"
)

# 🎨 Estilos CSS personalizados
st.markdown("""
    <style>
    /* Sidebar animado */
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
        to {
            visibility: hidden;
        }
    }

    .slide-in {
        animation: slideIn 1s ease-in-out;
    }

    @keyframes slideIn {
        from {
            transform: translateX(-100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    .fade-in {
        animation: fadeIn 1s ease-in-out;
    }

    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    .movie-title {
        font-weight: bold;
        text-align: center;
        margin-top: 0.5rem;
        color: #333333;
    }

    .stButton>button {
        background-color: #FF5722;
        color: white;
        border-radius: 8px;
        padding: 10px 16px;
        font-size: 16px;
        transition: background-color 0.3s ease;
    }

    .stButton>button:hover {
        background-color: #e64a19;
    }
    </style>
""", unsafe_allow_html=True)

# 🧠 Función para obtener póster
def fetch_poster(movie_id):
    try:
        api_key = 'dddf41ab7ba39b964d38b377d61f4042'
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

# 🔍 Recomendación de películas
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

# 📌 Sidebar con diseño elegante
with st.sidebar:
    st.markdown('<h2 class="slide-in">🎬 CineBot</h2>', unsafe_allow_html=True)
    st.markdown('<h4 class="sidebar-text">Tu Guía Instantánea de Películas 🎥</h4>', unsafe_allow_html=True)
    st.image('https://img.blogs.es/iahuawei/wp-content/uploads/2018/12/mitos-1080x675.jpg', use_column_width=True)
    st.markdown('<hr>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-text">✨ Recomendaciones de películas en tiempo real con <strong>CineBot</strong>.</p>', unsafe_allow_html=True)
    st.markdown('<hr>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-text">👤 <span class="blink">Max</span></p>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-text">📧 <span class="blink">maxwinchez@gmail.com</span></p>', unsafe_allow_html=True)

# 🧠 Cargar los datos
try:
    movies = pd.read_pickle('movies.pkl')
    similarity = np.array(pd.read_pickle('similarity.pkl'))
except Exception as e:
    st.error(f"Error al cargar los datos: {e}")

# 🖼️ Interfaz principal
st.title('🎥 Sistema de Recomendación de Películas')
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

# 🧾 Footer
st.markdown("""
    <hr style='margin-top: 3rem;'>
    <div style='text-align: center; font-size: 14px; color: #888;'>
        © 2025 CineBot | Desarrollado por Max | Lima - Perú 🇵🇪
    </div>
""", unsafe_allow_html=True)

