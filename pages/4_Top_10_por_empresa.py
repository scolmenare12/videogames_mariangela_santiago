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

st.markdown(f"### Empresa seleccionada: {empresa_top}")

if empresa_top == "Nintendo":
    st.markdown(
        """
El fenómeno de Wii Sports: Existe una brecha enorme entre el primer y el segundo lugar. Wii Sports vendió más del doble que Super Mario Bros., en gran parte porque se incluía en el paquete inicial de la consola Wii en la mayoría de los mercados.

Franquicias Dominantes: La marca Mario aparece en 4 de los 10 puestos (contando Mario Kart y las versiones New), consolidándose como el pilar comercial de la empresa.

Legado Histórico: Títulos clásicos como Tetris y Duck Hunt se mantienen en el Top 10 histórico, lo que demuestra el impacto de las primeras consolas (NES y Game Boy) en las cifras totales.

Consistencia: El rango entre el puesto 5 y el 10 es muy estrecho (apenas 3.5 millones de diferencia), lo que indica un nivel de éxito muy similar para sus grandes éxitos de portátiles y consolas de sobremesa.
        """
    )
elif empresa_top == "Sony Computer Entertainment":
    st.markdown(
        """
El Imperio de Gran Turismo: La saga ocupa 5 de los 10 puestos más altos. Es, por mucho, la marca más valiosa para Sony según este dataset, logrando ventas consistentes a través de diferentes generaciones de consolas (PS1, PS2 y PS3).

Alianzas Estratégicas: Se observa la importancia de los RPGs de Square Enix, con dos títulos de Final Fantasy en la lista. Esto subraya cómo los juegos de terceros (aunque publicados o asociados fuertemente con Sony en su momento) fueron vitales para su éxito.

Variedad de Géneros: A diferencia de Nintendo, que se apoya mucho en plataformas y juegos familiares, el Top de Sony es más variado, incluyendo simulación de carreras, RPGs épicos, lucha (Tekken) y plataformas (Crash Bandicoot).

Escala de Ventas: Es interesante notar que el juego más vendido de Sony (~15 M) está muy por debajo de los niveles de los líderes de Nintendo (~82 M o ~40 M). Esto sugiere que el éxito de Sony tiende a repartirse entre una biblioteca más amplia de juegos medianamente masivos, en lugar de concentrarse en un solo fenómeno global.
        """
    )
elif empresa_top == "Microsoft Game Studios":
    st.markdown(
        """
El Efecto "Bundle": Al igual que ocurrió con Wii Sports en Nintendo, Kinect Adventures! ocupa el primer lugar con una ventaja considerable (~22 M). Esto se debe a que se vendía incluido con el sensor Kinect, convirtiéndose en el título más distribuido de la marca.

"La Casa de Halo": El impacto de esta franquicia es impresionante: ocupa 6 de los 10 puestos. Esto demuestra que la identidad de Xbox durante años dependió directamente de la saga del Jefe Maestro.

Diversificación con Minecraft: Es notable ver a Minecraft en el 5° puesto. Aunque es un fenómeno global multiplataforma, su presencia aquí refleja su enorme peso dentro del ecosistema de Microsoft tras la adquisición de Mojang.
        """
    )