import data_processing as dp
import pandas as pd

try:
    _, d = dp.load_and_process_data()
    df = d.get('pbi3', pd.DataFrame())
    print(f"COLUMNS: {df.columns.tolist()}")
    col_grp = next((c for c in df.columns if 'Agrupaci' in c or 'Grouping' in c), None)
    print(f"FOUND COL: {col_grp}")
    if col_grp:
        print(f"UNIQUE VALS: {df[col_grp].unique().tolist()}")
    else:
        print("COL NOT FOUND")
except Exception as e:
    print(f"ERROR: {e}")
