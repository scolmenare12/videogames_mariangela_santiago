import altair as alt
import pandas as pd
import streamlit as st

from shared import PUBLISHER_ORDER, load_tables

DISPLAY_NAME = {
    "Nintendo": "Nintendo",
    "Sony Computer Entertainment": "Sony",
    "Microsoft Game Studios": "Microsoft",
}

st.set_page_config(
    page_title="Estadísticas descriptivas — Ventas videojuegos",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded",
)


def _tabla_descriptiva(df_ventas: pd.DataFrame) -> pd.DataFrame:
    filas = []
    for pub in PUBLISHER_ORDER:
        s = df_ventas.loc[df_ventas["Publisher"] == pub, "Global_Sales_Millions"]
        std = float(s.std(ddof=1))
        mean = float(s.mean())
        cv_pearson = (mean / std) * 100 if std else float("nan")
        filas.append(
            {
                "Empresa": DISPLAY_NAME[pub],
                "Publicaciones": int(s.shape[0]),
                "Total": float(s.sum()),
                "Media": mean,
                "Mediana": float(s.median()),
                "Varianza": float(s.var(ddof=1)),
                "Desv. tip.": std,
                "CV (%)": cv_pearson,
            }
        )
    return pd.DataFrame(filas)


st.title("Dashboard — Análisis descriptivo")
st.caption(
    "Resumen de la variable **ventas globales** (millones de unidades) por editorial. "
    "Las definiciones coinciden con la sección 4.3 del informe: varianza y desviación típica "
    "muestrales (n−1); el **coeficiente de variación de Pearson** se calcula como "
    "(media / desv. típica) × 100."
)

try:
    df_videogame_sales, _, _ = load_tables()
except FileNotFoundError:
    st.error(
        "No se encontraron los CSV generados. Ejecuta primero `dataset_limpio.py` "
        "para crear los archivos de datos."
    )
    st.stop()

tabla = _tabla_descriptiva(df_videogame_sales)

st.subheader("Tabla Resultados descriptivos")
st.dataframe(
    tabla,
    width="stretch",
    hide_index=True,
    column_config={
        "Empresa": st.column_config.TextColumn("Empresa"),
        "Publicaciones": st.column_config.NumberColumn("Publicaciones", format="%d"),
        "Total": st.column_config.NumberColumn("Total (M)", format="%.2f"),
        "Media": st.column_config.NumberColumn("Media", format="%.2f"),
        "Mediana": st.column_config.NumberColumn("Mediana", format="%.2f"),
        "Varianza": st.column_config.NumberColumn("Varianza", format="%.2f"),
        "Desv. tip.": st.column_config.NumberColumn("Desv. tip.", format="%.2f"),
        "CV (%)": st.column_config.NumberColumn("CV", format="%.2f %%"),
    },
)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader("Total de ventas por empresa (M)")
    ch_total = (
        alt.Chart(tabla)
        .mark_bar()
        .encode(
            x=alt.X("Empresa:N", title="Empresa", sort=list(tabla["Empresa"])),
            y=alt.Y("Total:Q", title="Millones de unidades"),
            color=alt.Color(
                "Empresa:N",
                legend=None,
                scale=alt.Scale(
                    domain=["Nintendo", "Sony", "Microsoft"],
                    range=["#E60012", "#1E6BD6", "#107C10"],
                ),
            ),
            tooltip=[
                "Empresa",
                alt.Tooltip("Total:Q", title="Total (M)", format=".2f"),
            ],
        )
    )
    st.altair_chart(ch_total, width="stretch", theme="streamlit")

with col2:
    st.subheader("Coeficiente de variación de Pearson (%)")
    ch_cv = (
        alt.Chart(tabla)
        .mark_bar()
        .encode(
            x=alt.X("Empresa:N", title="Empresa", sort=list(tabla["Empresa"])),
            y=alt.Y("CV (%):Q", title="CV (media / desv. típ.) × 100"),
            color=alt.Color(
                "Empresa:N",
                legend=None,
                scale=alt.Scale(
                    domain=["Nintendo", "Sony", "Microsoft"],
                    range=["#E60012", "#1E6BD6", "#107C10"],
                ),
            ),
            tooltip=[
                "Empresa",
                alt.Tooltip("CV (%):Q", title="CV (%)", format=".2f"),
            ],
        )
    )
    st.altair_chart(ch_cv, width="stretch", theme="streamlit")