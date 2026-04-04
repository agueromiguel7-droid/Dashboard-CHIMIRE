import pandas as pd
import streamlit as st

@st.cache_data
def load_and_process_data():
    """
    Carga el Excel completo y normaliza los nombres de columnas (strip de espacios).
    """
    file_path = "2021.04.26 Datos PBI CapexAjustCompres.xlsx"
    xl = pd.ExcelFile(file_path)

    def parse_clean(sheet_name):
        df = xl.parse(sheet_name)
        df.columns = [str(c).strip() for c in df.columns]
        return df

    datos = {
        'escenarios': parse_clean("DescEscenarios"),
        'pbi3':       parse_clean("PBI 3"),          # KPIs probabilísticos
        'pbi4':       parse_clean("PBI 4"),          # Tablas de sensibilidad financiera
        'mpp':        parse_clean("PBI MPP"),        # Prod + Capex/Opex (series de tiempo)
        'pozos2':     parse_clean("Pozos (2)"),      # Tabla resumen de pozos tipo
        'pozos':      parse_clean("Pozos"),          # Intervenciones detalle
        'corner':     parse_clean("DatosCorner"),    # Matriz Corner $ vs Tasa
    }

    # Lista de escenarios disponibles
    if 'Escenario' in datos['escenarios'].columns:
        escenarios_disp = datos['escenarios']['Escenario'].dropna().unique().tolist()
    else:
        escenarios_disp = datos['pbi3']['Escenario'].dropna().unique().tolist()

    return escenarios_disp, datos


def _filter(df, escenario):
    if 'Escenario' in df.columns:
        return df[df['Escenario'] == escenario].copy()
    return df.copy()


def get_kpi_df(datos, escenario):
    return _filter(datos['pbi3'], escenario)


def get_kpi_df_agrupacion(datos, escenario, agrupacion=None):
    """Retorna KPIs de PBI 3 filtrando por escenario y agrupación de precio."""
    df = _filter(datos['pbi3'], escenario)
    if agrupacion and 'Agrupación' in df.columns:
        df = df[df['Agrupación'] == agrupacion]
    return df


def get_agrupacion_options(datos):
    """Lista de valores únicos de Agrupación en PBI 3."""
    df = datos['pbi3']
    if 'Agrupación' in df.columns:
        return sorted(df['Agrupación'].dropna().unique().tolist())
    return []


def get_costs_summary(datos, escenario):
    """
    Calcula los totales acumulados (suma de serie temporal, categoría Media)
    para los tipos de CAPEX y OPEX desde la hoja PBI MPP.
    Retorna un dict {label: value_MMUSD}.
    """
    mpp = _filter(datos['mpp'], escenario)
    if mpp.empty:
        return {}

    ts_cols = [c for c in mpp.columns if str(c).startswith('2')]

    # Mapeo: etiqueta → [nombres candidatos en columna Variable]
    cost_map = {
        'Capex Infra.\n(MMUSD)':    ['CAPEX Infraestructura'],
        'Capex Pozos\n(MMUSD)':     ['CAPEX Pozo+Desarrollo', 'CAPEX Pozo + Desarrollo'],
        'Abandono Pozos\n(MMUSD)':  ['CAPEX Abandono Pozos', 'OPEX Abandono Pozos',
                                      'OPEX Abandono Infraestructura'],
        'Opex RMA\n(MMUSD)':        ['OPEX RMA'],
        'Opex RMR\n(MMUSD)':        ['OPEX RME'],
        'Opex Variable\n(MMUSD)':   ['OPEX Variable'],
        'Opex Fijo\n(MMUSD)':       ['OPEX Fijo', 'OPEX mano de obra'],
    }

    result = {}
    for label, var_names in cost_map.items():
        total = 0.0
        for vn in var_names:
            rows = mpp[
                (mpp['Variable'].str.strip() == vn.strip()) &
                (mpp['Categoría'] == 'Media')
            ]
            if not rows.empty:
                vals = pd.to_numeric(rows.iloc[0][ts_cols], errors='coerce').fillna(0)
                total += float(vals.sum())
                break
        result[label] = round(total, 2)
    return result


def get_mpp_df(datos, escenario):
    return _filter(datos['mpp'], escenario)

def get_pozos2_df(datos, escenario):
    return _filter(datos['pozos2'], escenario)

def get_pozos_df(datos, escenario):
    return _filter(datos['pozos'], escenario)

def get_corner_df(datos, escenario):
    return _filter(datos['corner'], escenario)

def get_all_mpp(datos):
    """Retorna MPP completo (todos los escenarios) para comparación."""
    return datos['mpp'].copy()
