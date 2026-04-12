import altair as alt
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


st.set_page_config(
    page_title="Ventas globales — Nintendo, Sony, Microsoft",
    layout="wide",
)

st.title(
    "Análisis comparativo de ventas globales  de las empresas de videojuegos "
    "Nintendo, Sony y Microsoft"
)

@st.cache_data
def load_tables():
    df_videogame_sales = pd.read_csv(BASE / "videogame_sales.csv")
    top_pub = pd.read_csv(BASE / "top_publishers.csv")
    top_pub_sales = pd.read_csv(BASE / "top_publishers_sales.csv")
    return df_videogame_sales, top_pub, top_pub_sales

st.divider()

try:
    df_videogame_sales, top_publishers, top_publishers_sales = load_tables()
except FileNotFoundError as e:
    st.error(
        "No se encontraron los CSV generados. Ejecuta primero `dataset_limpio.py` "
        "para crear `videogame_sales.csv`, `top_publishers.csv` y "
        "`top_publishers_sales.csv`."
    )
    st.stop()

vista = st.selectbox(
    "Cambiar vista",
    options=[
        "videogame_sales",
        "top_publishers",
        "top_publishers_sales",
    ],
    format_func=lambda x: {
        "videogame_sales": "Ventas globales de videojuegos",
        "top_publishers": "Total de juegos publicados por las empresas",
        "top_publishers_sales": "Total de juegos vendidos por las empresas",
    }[x],
)

if vista == "videogame_sales":
    st.dataframe(df_videogame_sales, width="stretch", hide_index=True)
elif vista == "top_publishers":
    st.markdown("### Total de juegos publicados por las empresas")
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
elif vista == "top_publishers_sales":
    st.markdown("### Total de juegos vendidos por las empresas")
    st.caption(
        "Cada sector es proporcional a las ventas globales acumuladas. En el centro se muestran "
        "esas ventas en millones de unidades (M). Pasa el cursor para ver participación y títulos en catálogo."
    )
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
