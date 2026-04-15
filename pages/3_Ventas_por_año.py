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

st.markdown(
    """
### Interpretación de resultados

**1. El Dominio y los Picos de Nintendo (Línea Roja)**

Años 80 y 90: Se observa su dominio inicial con fluctuaciones que corresponden a las eras de la NES y SNES.

El "Megapico" (2006-2009): Es el punto más alto de toda la gráfica, superando los 200 millones de unidades en un solo año (alrededor de 2006). Esto coincide perfectamente con el lanzamiento y fenómeno global de la Wii y la Nintendo DS.

Segundo Pico (2009-2010): Se ve un rebote importante antes de una caída sostenida hacia 2016.

**2. La Consistencia de Sony (Línea Azul)**

Entrada al Mercado (1994): La línea azul comienza a mediados de los 90 con el lanzamiento de la PlayStation original.

Estabilidad: A diferencia de Nintendo, Sony muestra una línea mucho más estable, manteniéndose mayormente entre los 20 y 50 millones de unidades anuales. No tiene picos tan extremos, pero su presencia es constante a través de las eras de PS1, PS2 y PS3.

**3. La Trayectoria de Microsoft (Línea Verde)**

Inicio Tardío (2001): Es la última en aparecer, coincidiendo con la primera Xbox.

Crecimiento: Logra su mejor desempeño entre 2010 y 2011, donde llega a superar los 50 millones de unidades, acercándose e incluso cruzándose brevemente con las ventas de Sony en ese periodo (era dorada de la Xbox 360 y Kinect).

**4. Tendencia Final (Hacia 2016)**

Se observa que las tres líneas convergen hacia la baja al final de la serie (2015-2016). Esto suele ocurrir en los datasets de videojuegos porque los datos de los años más recientes a veces están incompletos o reflejan el final de un ciclo de consolas antes del despegue total de la siguiente generación.
    """
)