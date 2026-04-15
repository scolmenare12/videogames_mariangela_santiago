import streamlit as st

from shared import load_tables

st.set_page_config(
    page_title="Ventas globales — Nintendo, Sony, Microsoft",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title(
    "Análisis comparativo de ventas globales de videojuegos: "
    "Nintendo, Sony y Microsoft"
)

st.divider()

try:
    df_videogame_sales, _, _ = load_tables()
except FileNotFoundError:
    st.error(
        "No se encontraron los CSV generados. Ejecuta primero `dataset_limpio.py` "
        "para crear `videogame_sales.csv`, `top_publishers.csv` y "
        "`top_publishers_sales.csv`."
    )
    st.stop()

st.subheader("Tabla de ventas globales de videojuegos")
st.dataframe(df_videogame_sales, width="stretch", hide_index=True)

st.markdown(
    """
### Introducción a la aplicación

Esta aplicación interactiva complementa el informe de investigación del curso **Computación I**
(Facultad de Ciencias Económicas y Sociales, Escuela de Estadística y Ciencias Actuariales,
Universidad Central de Venezuela). En la barra lateral, la primera página es el **dashboard de
estadísticas descriptivas** (tabla 4.1 del informe); el resto son las **visualizaciones** (barras,
circular, serie temporal y ranking por empresa).

Los gráficos usan los mismos criterios que el estudio en PDF: solo se consideran como editoras
**Nintendo**, **Sony Computer Entertainment** y **Microsoft Game Studios**; las ventas se expresan
en **millones de unidades** vendidas a nivel global; el periodo cubierto en el dataset llega
hasta **2016** (según los años válidos del archivo fuente).

---

### Contexto de la investigación

La industria de los videojuegos es un sector económico de gran envergadura y **alta volatilidad**:
la tecnología, las tendencias, la competencia y la economía global condicionan rápidamente qué
productos destacan o pierden relevancia. **Nintendo**, **Sony** y **Microsoft** se han consolidado
como tres de las corporaciones más influyentes: no solo compiten en el mercado, sino que muchas
veces marcan tendencias de consumo y de plataforma a escala mundial.

Sin **comparaciones basadas en datos** sobre ventas netas o globales, las estrategias comerciales
corren el riesgo de apoyarse solo en intuiciones. Un análisis estadístico descriptivo permite
**visualizar el desempeño** de cada empresa, identificar **patrones y picos** en el tiempo y
reconocer **títulos destacados**, lo que interesa a analistas, desarrolladores y editores que
buscan entender la dinámica competitiva del sector.

---

### Preguntas de investigación

1. ¿Qué empresa tiene la **mayor cantidad de ventas globales**?
2. ¿Cuál empresa ha tenido el **pico más alto** de ventas globales (en el tiempo)?
3. ¿Cuáles son los **diez juegos más vendidos** en el contexto del estudio (por empresa y en conjunto)?

**Objetivo general:** analizar de forma comparativa el desempeño en ventas de videojuegos de
Nintendo, Sony y Microsoft, para identificar patrones, tendencias y productos relevantes.

**Objetivos específicos:** cuantificar ventas totales por empresa; comparar ventas anuales en el
tiempo; determinar el top 10 de juegos más vendidos por empresa.

---

### Sobre los datos

La tabla siguiente muestra el detalle por título (nombre, plataforma, año, género, editorial y
ventas globales en millones de unidades). El resumen descriptivo está en la página **0**; las
gráficas, en las páginas siguientes.

**Autores del proyecto:** Mariangela Laya (30849318) y Santiago Colmenares (32270162)
"""
)