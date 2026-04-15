import altair as alt
import streamlit as st

from shared import PUBLISHER_COLORS, PUBLISHER_ORDER, load_tables

st.set_page_config(
    page_title="Ventas por año — Ventas videojuegos",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Ventas por año (serie temporal)")
st.markdown(
    """
Para cada **año** se suman las ventas globales (millones de unidades) de todos los títulos de
cada empresa. Cada **línea** corresponde a una editorial y usa su **color** corporativo.
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

df_ano = (
    df_videogame_sales.dropna(subset=["Year"])
    .assign(Year=lambda d: d["Year"].astype(int))
    .groupby(["Publisher", "Year"], as_index=False)["Global_Sales_Millions"]
    .sum()
)
escala_lineas = alt.Scale(
    domain=list(PUBLISHER_ORDER),
    range=[PUBLISHER_COLORS[p] for p in PUBLISHER_ORDER],
)
base_lineas = (
    alt.Chart(df_ano)
    .encode(
        x=alt.X("Year:O", title="Año", sort="ascending"),
        y=alt.Y(
            "Global_Sales_Millions:Q",
            title="Ventas (millones de unidades)",
        ),
        color=alt.Color(
            "Publisher:N",
            sort=list(PUBLISHER_ORDER),
            scale=escala_lineas,
            legend=alt.Legend(title="Empresa"),
        ),
        tooltip=[
            alt.Tooltip("Publisher:N", title="Empresa"),
            alt.Tooltip("Year:O", title="Año"),
            alt.Tooltip(
                "Global_Sales_Millions:Q",
                title="Ventas (M)",
                format=".2f",
            ),
        ],
    )
)
grafico_lineas = base_lineas.mark_line(
    point=True,
    strokeWidth=2.5,
    interpolate="monotone",
).properties(height=420)
st.altair_chart(grafico_lineas, width="stretch", theme="streamlit")
