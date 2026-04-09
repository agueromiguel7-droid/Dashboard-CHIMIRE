import pandas as pd
import streamlit as st
from translations import TRANSLATIONS

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


def apply_translations(datos, escenarios_disp, lang):
    """
    Traduce los DataFrames y la lista de escenarios si el idioma es English.
    """
    if lang != "English":
        return escenarios_disp, datos

    trans = TRANSLATIONS.get("English", {})
    header_map = trans.get("headers", {})
    value_map = trans.get("values", {})

    new_datos = {}
    for sheet_name, df in datos.items():
        df_copy = df.copy()
        
        # 1. Traducir Nombres de Columnas
        df_copy.columns = [header_map.get(str(c).strip(), str(c).strip()) for c in df_copy.columns]
        
        # 2. Traducir Valores en columnas clave (si existen)
        cat_cols = ['Scenario', 'Variable', 'Category', 'Indicator', 'Asset', 'Grouping', 'Well Type']
        for col in df_copy.columns:
            if col in cat_cols:
                df_copy[col] = df_copy[col].astype(str).map(lambda x: value_map.get(x.strip(), x.strip()))
        
        new_datos[sheet_name] = df_copy

    # 3. Traducir la lista de escenarios
    new_escenarios = [value_map.get(str(e).strip(), str(e).strip()) for e in escenarios_disp]

    return new_escenarios, new_datos


def _filter(df, escenario):
    # Support both "Escenario" (ES) and "Scenario" (EN)
    col = 'Scenario' if 'Scenario' in df.columns else 'Escenario'
    if col in df.columns:
        return df[df[col] == escenario].copy()
    return df.copy()


def get_kpi_df(datos, escenario):
    return _filter(datos['pbi3'], escenario)


def get_kpi_df_agrupacion(datos, escenario, agrupacion=None, activo=None):
    """Retorna KPIs de PBI 3 filtrando por escenario, agrupación de precio y activo."""
    df = _filter(datos['pbi3'], escenario)
    # Support both "Agrupación" (ES) and "Grouping" (EN)
    col_ag = 'Grouping' if 'Grouping' in df.columns else 'Agrupación'
    col_act = 'Asset' if 'Asset' in df.columns else 'Activo'
    
    if agrupacion and col_ag in df.columns:
        df = df[df[col_ag] == agrupacion]
    if activo and col_act in df.columns:
        df = df[df[col_act] == activo]
    return df


def get_agrupacion_options(datos):
    """Lista de valores únicos de Agrupación en PBI 3."""
    df = datos['pbi3']
    col_ag = 'Grouping' if 'Grouping' in df.columns else 'Agrupación'
    if col_ag in df.columns:
        return sorted(df[col_ag].dropna().unique().tolist())
    return []

def get_activo_options(datos):
    """Lista de valores únicos de Activo en PBI 3."""
    df = datos['pbi3']
    col_act = 'Asset' if 'Asset' in df.columns else 'Activo'
    if col_act in df.columns:
        return sorted(df[col_act].dropna().unique().tolist())
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
    trans = TRANSLATIONS.get("English", {})
    val_map = trans.get("values", {})
    
    for label, var_names in cost_map.items():
        total = 0.0
        col_var = 'Variable'
        col_cat = 'Category' if 'Category' in mpp.columns else 'Categoría'
        is_en = (col_cat == 'Category')

        for vn in var_names:
            # Search for the translated name if in English, otherwise Spanish
            search_vn = val_map.get(vn.strip(), vn.strip()) if is_en else vn.strip()
            
            rows = mpp[
                (mpp[col_var].str.strip() == search_vn) &
                (mpp[col_cat] == ('Mean' if is_en else 'Media'))
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
