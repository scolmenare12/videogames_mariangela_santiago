import streamlit as st
import pandas as pd
from pathlib import Path

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


@st.cache_data
def load_tables():
    df_videogame_sales = pd.read_csv(BASE / "videogame_sales.csv")
    top_pub = pd.read_csv(BASE / "top_publishers.csv")
    top_pub_sales = pd.read_csv(BASE / "top_publishers_sales.csv")
    return df_videogame_sales, top_pub, top_pub_sales
