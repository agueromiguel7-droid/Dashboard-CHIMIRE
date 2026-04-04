import pandas as pd
import os

file_path = "2021.04.26 Datos PBI CapexAjustCompres.xlsx"
if os.path.exists(file_path):
    try:
        xl = pd.ExcelFile(file_path)
        print(f"File found: {file_path}")
        for s in xl.sheet_names:
            df = xl.parse(s, nrows=20)
            print(f"Sheet: {s}")
            # print(f"Columns: {df.columns.tolist()}")
            # List unique rows in columns if they exist
            found_cols = []
            for col in ['Indicador', 'Variable', 'Categoría', 'Activo', 'Agrupación']:
                if col in df.columns:
                    found_cols.append(col)
                    print(f"  Values in {col}: {df[col].dropna().unique().tolist()}")
            if not found_cols:
                # print("  No standard columns found.")
                pass
            print("-" * 15)
    except Exception as e:
        print(f"Error reading Excel: {e}")
else:
    print(f"File {file_path} not found.")

def get_unique_from_col(sheet_name, col_name):
    if sheet_name in xl.sheet_names:
        df = xl.parse(sheet_name)
        if col_name in df.columns:
            return df[col_name].dropna().unique().tolist()
    return []

# Deep scan for translation mapping
print("\n--- DEEP SCAN FOR DATA MAPPING ---")
xl = pd.ExcelFile(file_path)
print("PBI 3 Indicators:", get_unique_from_col("PBI 3", "Indicador"))
print("PBI MPP Variables:", get_unique_from_col("PBI MPP", "Variable"))
print("PBI MPP Categories:", get_unique_from_col("PBI MPP", "Categoría"))
print("DatosCorner Activo:", get_unique_from_col("DatosCorner", "Activo"))
print("Pozos (2) Pozo Tipo:", get_unique_from_col("Pozos (2)", "Pozo Tipo"))
print("Pozos (2) Agrupación:", get_unique_from_col("Pozos (2)", "Agrupación"))
