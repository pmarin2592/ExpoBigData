import sys

import streamlit as st
import os
from PIL import Image

from visualizacion.Visualizador import Visualizador

# Añadir la raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Calcula la ruta absoluta de main.py
BASE_DIR = os.path.dirname(__file__)

# Abre la imagen desde la misma carpeta que main.py
logo_path = os.path.join(BASE_DIR, "logo-cuc.png")
logo = Image.open(logo_path)
visualizador = Visualizador()

st.set_page_config(page_title="Informe Ejecutivo", layout="wide", page_icon="📊")
# Cachear modelo para no reentrenar cada vez

# Menú lateral
st.sidebar.image(logo, width=120)
#st.sidebar.title("Menú")
opcion = st.sidebar.radio("Seleccione una opción", ["Estadisticas","Formulario de Predicción"])

if opcion == "Estadisticas":
  visualizador.cargar_estadisticas()
else:
  visualizador.cargar_formulario()


