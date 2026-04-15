from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent
SOURCE_CSV = BASE / "12. Videogame Sales.csv"

PUBLISHERS_FILTER = (
    "Nintendo",
    "Sony Computer Entertainment",
    "Microsoft Game Studios",
)


def build_dataframes() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Lee el CSV fuente y devuelve:
    - df_limpio: ventas por título (columnas sin ventas regionales, tres editoriales).
    - top_publishers: ID, Publisher, Total_Games.
    - top_publishers_sales: ID, Publisher, Total_Sales_Millions.
    """
    df = pd.read_csv(SOURCE_CSV)

    columnas_a_eliminar = ["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"]
    columnas_existentes = [col for col in columnas_a_eliminar if col in df.columns]
    df_limpio = df.drop(columns=columnas_existentes)

    df_limpio = df_limpio.rename(columns={"Global_Sales": "Global_Sales_Millions"})
    df_limpio = df_limpio.drop_duplicates()

    df_limpio = df_limpio[df_limpio["Publisher"].isin(PUBLISHERS_FILTER)].copy()
    df_limpio = df_limpio[df_limpio["Year"].astype(str) != "N/A"].copy()

    publisher_df = (
        df_limpio.groupby("Publisher")
        .agg(
            {
                "Name": "count",
                "Global_Sales_Millions": "sum",
            }
        )
        .rename(
            columns={
                "Name": "Total_Games",
                "Global_Sales_Millions": "Total_Sales_Millions",
            }
        )
        .reset_index()
    )

    top_publisher_df = publisher_df.sort_values(
        by="Total_Games", ascending=False
    ).reset_index(drop=True)
    top_publisher_df.insert(0, "ID", range(1, len(top_publisher_df) + 1))
    top_publishers = top_publisher_df[["ID", "Publisher", "Total_Games"]].copy()

    top_publishers_sales_df = publisher_df.sort_values(
        by="Total_Sales_Millions", ascending=False
    ).reset_index(drop=True)
    top_publishers_sales_df.insert(0, "ID", range(1, len(top_publishers_sales_df) + 1))
    top_publishers_sales = top_publishers_sales_df[
        ["ID", "Publisher", "Total_Sales_Millions"]
    ].copy()

    return df_limpio, top_publishers, top_publishers_sales


if __name__ == "__main__":
    df_limpio, top_publishers, top_publishers_sales = build_dataframes()
    print(df_limpio.columns.tolist())
    print(f"Registros en df_limpio: {len(df_limpio)}")
    df_limpio.to_csv(BASE / "videogame_sales.csv", index=False)
    top_publishers.to_csv(BASE / "top_publishers.csv", index=False)
    top_publishers_sales.to_csv(BASE / "top_publishers_sales.csv", index=False)
    print("CSV exportados en la carpeta del proyecto (opcional).")
