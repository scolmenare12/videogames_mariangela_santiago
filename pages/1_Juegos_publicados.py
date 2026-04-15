import altair as alt
import streamlit as st

from shared import PUBLISHER_COLORS, PUBLISHER_ORDER, load_tables

st.set_page_config(
    page_title="Juegos publicados — Ventas videojuegos",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Juegos publicados por empresa")
st.markdown(
    """
Cada barra representa el **número de títulos** en el dataset asociados a cada editorial
(Nintendo, Sony Computer Entertainment, Microsoft Game Studios), tras el filtrado del estudio.
"""
)

try:
    _, top_publishers, _ = load_tables()
except FileNotFoundError:
    st.error(
        "No se encontraron los CSV generados. Ejecuta primero `dataset_limpio.py` "
        "para crear los archivos de datos."
    )
    st.stop()

grafico_barras = (
    alt.Chart(top_publishers)
    .mark_bar()
    .encode(
        x=alt.X("Publisher:N", title="Empresa", sort=list(PUBLISHER_ORDER)),
        y=alt.Y("Total_Games:Q", title="Juegos publicados"),
        color=alt.Color(
            "Publisher:N",
            scale=alt.Scale(
                domain=list(PUBLISHER_ORDER),
                range=[PUBLISHER_COLORS[p] for p in PUBLISHER_ORDER],
            ),
            legend=None,
        ),
        tooltip=["Publisher", "Total_Games"],
    )
)
st.altair_chart(grafico_barras, width="stretch", theme="streamlit")
