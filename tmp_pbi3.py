import pandas as pd
xl = pd.ExcelFile('2021.04.26 Datos PBI CapexAjustCompres.xlsx')
p = xl.parse('Pozos')
p.columns = [str(c).strip() for c in p.columns]
p2 = xl.parse('Pozos (2)')
p2.columns = [str(c).strip() for c in p2.columns]

print("=== Pozos cols:", list(p.columns))
print()
cb = p[p['Escenario']=='Caso Base']
print("Pozos Caso Base sample:")
print(cb[['Pozo Tipo','Cantidad','Qo_50','Qg_50','Costo_MP']].head(8).to_string())
print()
print("=== Pozos(2) cols:", list(p2.columns))
cb2 = p2[p2['Escenario']=='Caso Base']
print("Pozos2 Caso Base all cols:")
print(cb2.head(8).to_string(max_colwidth=15))
