import pandas as pd
xl = pd.ExcelFile("2021.04.26 Datos PBI CapexAjustCompres.xlsx")
df = xl.parse("PBI MPP")
df.columns = [str(c).strip() for c in df.columns]
capex = sorted([v for v in df['Variable'].dropna().unique() if 'CAPEX' in str(v).upper() or 'Capex' in str(v)])
opex  = sorted([v for v in df['Variable'].dropna().unique() if 'OPEX'  in str(v).upper() or 'Opex'  in str(v)])
print("FULL CAPEX LIST:", capex)
print("FULL OPEX LIST:", opex)
