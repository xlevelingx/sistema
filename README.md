# 🎬 CineBot - Sistema de Recomendación de Películas

CineBot es una aplicación web desarrollada con **Python** y **Streamlit**, que recomienda películas en `.TIEMPO REAL` utilizando técnicas de Machine Learning basadas en similitud de contenido.  
Con una interfaz amigable y visual, permite al usuario seleccionar una película y recibir recomendaciones personalizadas acompañadas de sus respectivos pósters.

--------------------------------------------------


## Tecnologías utilizadas

- **Python 3**
- **Streamlit**
- **Pandas / NumPy**
- **scikit-learn (opcional para cálculo de similitud)**
- **TMDb API** para obtener pósters de películas

--------------------------------------------------


## Ejecutar la app

streamlit run recomendacion.py

--------------------------------------------------


## Desarrollado por

Max:
📍 Lima, Perú 🇵🇪
📧 maxwinchez@gmail.com


--------------------------------------------------

## 📦 Instalación
Clona el repositorio:

--------------------------------------------------


### Crea un archivo .env en la raíz del proyecto y añade tu API Key de TMDb:

- **TMDB_API_KEY=tu_api_key_aqui**

--------------------------------------------------


### 🔑 Configurar tu propia TMDb API Key

Para obtener una API Key personalizada, debes crear una cuenta gratuita en [The Movie Database (TMDb)](https://www.themoviedb.org/settings/api) y generar tu propia clave.

Esta clave es necesaria para que el sistema pueda acceder a los pósters de las películas desde la API oficial de TMDb.

Una vez que la tengas, crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```env
TMDB_API_KEY=TU_API_KEY_AQUI

--------------------------------------------------



