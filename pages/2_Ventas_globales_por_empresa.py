import altair as alt
import streamlit as st

from shared import PUBLISHER_COLORS, PUBLISHER_ORDER, load_tables

st.set_page_config(
    page_title="Ventas por empresa — Ventas videojuegos",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Ventas globales acumuladas por empresa")
st.markdown(
    """
Gráfico **circular**: cada sector es proporcional a las **ventas globales acumuladas** (millones
de unidades) de cada editorial. En el centro se muestran esas ventas en **M**. Pasa el cursor
para ver participación y cantidad de juegos en catálogo.
"""
)

try:
    _, top_publishers, top_publishers_sales = load_tables()
except FileNotFoundError:
    st.error(
        "No se encontraron los CSV generados. Ejecuta primero `dataset_limpio.py` "
        "para crear los archivos de datos."
    )
    st.stop()

total_ventas = top_publishers_sales["Total_Sales_Millions"].sum()
df_pie = (
    top_publishers_sales.merge(
        top_publishers[["Publisher", "Total_Games"]],
        on="Publisher",
        how="left",
    )
    .assign(
        Porcentaje=lambda d: (d["Total_Sales_Millions"] / total_ventas * 100).round(1),
        Etiqueta_centro=lambda d: d["Total_Sales_Millions"].map(lambda x: f"{x:.1f} M"),
    )
)
df_pie = df_pie.set_index("Publisher").loc[list(PUBLISHER_ORDER)].reset_index()

escala_editorial = alt.Scale(
    domain=list(PUBLISHER_ORDER),
    range=[PUBLISHER_COLORS[p] for p in PUBLISHER_ORDER],
)
escala_blanco = alt.Scale(
    domain=list(PUBLISHER_ORDER),
    range=["#ffffff", "#ffffff", "#ffffff"],
)
theta_ventas = alt.Theta(
    field="Total_Sales_Millions",
    type="quantitative",
    stack=True,
    title="Ventas (millones de unidades)",
)
color_arc = alt.Color(
    "Publisher:N",
    sort=list(PUBLISHER_ORDER),
    scale=escala_editorial,
    legend=alt.Legend(title="Empresa"),
)
color_etiqueta = alt.Color(
    "Publisher:N",
    sort=list(PUBLISHER_ORDER),
    scale=escala_blanco,
    legend=None,
)

capa_arc = (
    alt.Chart(df_pie)
    .encode(theta=theta_ventas, color=color_arc)
    .mark_arc(
        outerRadius=160,
        innerRadius=0,
        stroke="#ffffff",
        strokeWidth=1.5,
    )
    .encode(
        tooltip=[
            alt.Tooltip("Publisher:N", title="Empresa"),
            alt.Tooltip("Total_Sales_Millions:Q", title="Ventas (M)", format=".2f"),
            alt.Tooltip("Total_Games:Q", title="Juegos en catálogo"),
            alt.Tooltip("Porcentaje:Q", title="Participación", format=".1f"),
        ],
    )
)
capa_etiquetas = (
    alt.Chart(df_pie)
    .encode(theta=theta_ventas, color=color_etiqueta)
    .mark_text(
        radius=100,
        size=13,
        fontWeight="lighter",
        fill="white",
        lineHeight=18,
        stroke="white",
        strokeWidth=0.35,
    )
    .encode(text=alt.Text("Etiqueta_centro:N"))
)
capas_pie = (capa_arc + capa_etiquetas).properties(height=420)
st.altair_chart(capas_pie, width="stretch", theme="streamlit")

st.markdown(
    """
### Liderazgo de mercado de Nintendo: Domina ampliamente la grafica representadno más del 67% del total combinado de estas 3 empresas. Sus ventas triplican a las de Sony en esta estudio.

### Competencia directa de Sony: Mantiene una posición sólida en el segundo lugar mientras que Microsoft ocupa una porción significativamente menor, representando menos del 10% del total. Esto refleja una brecha considerable entre Sony y Microsoft en términos de ventas globales acumuladas dentro del dataset.
    """
)