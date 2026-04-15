import altair as alt
import streamlit as st

from shared import PUBLISHER_COLORS, PUBLISHER_ORDER, load_tables

st.set_page_config(
    page_title="Top 10 por empresa — Ventas videojuegos",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Top 10 de ventas por empresa")
st.markdown(
    """
Selecciona una **empresa** para ver los **diez títulos** con mayores ventas globales (millones
de unidades) dentro del dataset del estudio. Las barras usan el color asignado a esa editorial.
"""
)

try:
    df_videogame_sales, _, _ = load_tables()
except FileNotFoundError:
    st.error(
        "No se encontraron los CSV generados. Ejecuta primero `dataset_limpio.py` "
        "para crear los archivos de datos."
    )
    st.stop()

empresa_top = st.selectbox("Empresa", options=list(PUBLISHER_ORDER))
color_emp = PUBLISHER_COLORS[empresa_top]
df_top10 = (
    df_videogame_sales.loc[
        df_videogame_sales["Publisher"] == empresa_top,
        ["Name", "Platform", "Year", "Genre", "Global_Sales_Millions"],
    ]
    .nlargest(10, "Global_Sales_Millions")
    .assign(Rank=lambda d: range(1, len(d) + 1))
)
graf_top10 = (
    alt.Chart(df_top10)
    .mark_bar()
    .encode(
        y=alt.Y(
            "Name:N",
            title="Videojuego",
            sort=alt.EncodingSortField(
                field="Global_Sales_Millions",
                order="descending",
            ),
        ),
        x=alt.X(
            "Global_Sales_Millions:Q",
            title="Ventas globales (millones de unidades)",
        ),
        color=alt.value(color_emp),
        tooltip=[
            alt.Tooltip("Rank:Q", title="Puesto"),
            alt.Tooltip("Name:N", title="Título"),
            alt.Tooltip("Platform:N", title="Plataforma"),
            alt.Tooltip("Year:Q", title="Año", format=".0f"),
            alt.Tooltip("Genre:N", title="Género"),
            alt.Tooltip(
                "Global_Sales_Millions:Q",
                title="Ventas (M)",
                format=".2f",
            ),
        ],
    )
    .properties(height=420)
)
st.altair_chart(graf_top10, width="stretch", theme="streamlit")
