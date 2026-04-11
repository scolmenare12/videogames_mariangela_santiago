import pandas as pd

# Cargar el csv
df = pd.read_csv('12. Videogame Sales.csv')

# Mostrar información básica del df
print(df.columns.tolist())
print(df.head(10))

# Eliminar columnas de ventas regionales ya que vamos a trabajar con las globales
columnas_a_eliminar = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']
columnas_existentes = [col for col in columnas_a_eliminar if col in df.columns]
df_limpio = df.drop(columns=columnas_existentes)

# Renombrar Global Sales para denotar medida (Millones)
df_limpio = df_limpio.rename(columns={'Global_Sales': 'Global_Sales_Millions'})

# Eliminar filas duplicadas
filas_antes = len(df_limpio)
df_limpio = df_limpio.drop_duplicates()
filas_despues = filas_antes - len(df_limpio)

print(f"Filas duplicadas eliminadas: {filas_despues}")

# En este caso hay 0 filas duplicadas

# Mismo criterio que script_limpieza.R: solo estos tres publishers (coincidencia exacta)
publishers_r = [
    'Nintendo',
    'Sony Computer Entertainment',
    'Microsoft Game Studios',
]
df_limpio = df_limpio[df_limpio['Publisher'].isin(publishers_r)].copy()

# Excluir filas con año desconocido (valor literal "N/A" en el CSV)
filas_antes_year = len(df_limpio)
df_limpio = df_limpio[df_limpio['Year'].astype(str) != 'N/A'].copy()
print(f"Filas eliminadas por Year = N/A: {filas_antes_year - len(df_limpio)}")

print(df_limpio.columns.tolist())

publisher_df = (
    df_limpio.groupby('Publisher')
    .agg({
        'Name': 'count',  # Contar número de juegos
        'Global_Sales_Millions': 'sum'  # Suma de total de ventas
    })
)

# Renombrar columnas y devolver Publisher como columna normal
publisher_df = (
    publisher_df
    .rename(columns={
        'Name': 'Total_Games',
        'Global_Sales_Millions': 'Total_Sales_Millions'
    })
    .reset_index()
)

# Ordenar por Total_Games de mayor a menor
top_publisher_df = publisher_df.sort_values(by='Total_Games', ascending=False).reset_index(drop=True)

# Crear columna de ID
top_publisher_df.insert(0, 'ID', range(1, len(top_publisher_df) + 1))

# Seleccion de las columnas para el DF top_publishers
top_publishers = top_publisher_df[['ID', 'Publisher', 'Total_Games']].copy()

# Ordenar por Total_Sales_Millions de mayor a menor
top_publishers_sales_df = publisher_df.sort_values(by='Total_Sales_Millions', ascending=False).reset_index(drop=True)

# Crear columna de ID
top_publishers_sales_df.insert(0, 'ID', range(1, len(top_publishers_sales_df) + 1))

# Seleccion de las columnas para el DF top_publishers_sales
top_publishers_sales = top_publishers_sales_df[['ID', 'Publisher', 'Total_Sales_Millions']].copy()


