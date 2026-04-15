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

st.markdown(
    """
### Interpretación de resultados

Empate técnico en el catálogo: Existe una diferencia mínima entre Nintendo y Sony en cuanto al número de títulos publicados. Ambas compañías han mantenido una estrategia de producción masiva para alimentar sus múltiples generaciones de consolas.

Relación Volumen vs. Ventas: Si recordamos el primer gráfico de "Ventas Globales", Nintendo tenía casi el triple de ventas que Sony, pero aquí vemos que tienen casi la misma cantidad de juegos. Esto confirma que Nintendo logra muchas más ventas por cada título individual que lanza (mayor eficiencia por juego).

La posición de Microsoft: Con aproximadamente 200 juegos, el catálogo de Microsoft es significativamente más pequeño (menos de un tercio de los otros dos). Esto se explica por su entrada más tardía al mercado (2001) y un enfoque históricamente más concentrado en franquicias clave como Halo o Gears of War.

Densidad del Dataset: Este gráfico ayuda a validar que el estudio es equilibrado para Nintendo y Sony, dándoles el mismo "peso" en cuanto a presencia de títulos, mientras que Microsoft actúa como un competidor con una librería más selecta.
    """
)