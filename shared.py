import streamlit as st
from pathlib import Path

from dataset_limpio import build_dataframes

BASE = Path(__file__).resolve().parent

PUBLISHER_ORDER = (
    "Nintendo",
    "Sony Computer Entertainment",
    "Microsoft Game Studios",
)
PUBLISHER_COLORS = {
    "Nintendo": "#E60012",
    "Sony Computer Entertainment": "#1E6BD6",
    "Microsoft Game Studios": "#107C10",
}

ERROR_DATOS_FUENTE = (
    "No se encontró el archivo `12. Videogame Sales.csv` en la carpeta del proyecto. "
    "Colócalo junto a `app.py` y reinicia la aplicación."
)

@st.cache_data
def load_tables():
    """Dataframes derivados en memoria desde `dataset_limpio.build_dataframes()` (sin CSV intermedios)."""
    return build_dataframes()
