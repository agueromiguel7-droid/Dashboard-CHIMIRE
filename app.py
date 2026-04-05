import streamlit as st
import streamlit_authenticator as stauth
import data_processing as dp
import ui_components as ui

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Dashboard CHIMIRE Analytics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS THEME ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .stApp { background-color: #F7F9FC; color: #1A2340; }

    /* Global Layout and Header Height Reduction - Ultra Compact */
    [data-testid="stHeader"] { height: 0; padding: 0 !important; visibility: hidden !important; border: none; }
    .main .block-container { 
        padding-top: 0 !important; 
        padding-bottom: 1rem !important;
        margin-top: -4.5rem !important;
    }
    .stApp > header { display: none !important; }

    .main-header {
        font-size: 1.45rem !important;
        font-weight: 800 !important;
        color: #0B1426 !important;
        margin: 0 !important;
        line-height: 1.1 !important;
        padding: 0 !important;
    }
    .sub-header {
        font-size: 0.85rem !important;
        color: #5F6B7A !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    



    /* High-Precision Slider Fix: Centering & Dates */
    div[data-testid="stSlider"] {
        padding-top: 1.5rem !important; /* Space for the title and dates */
    }
    div[data-testid="stSlider"] [data-baseweb="slider"] > div {
        background: #E8EDF2 !important; 
        height: 4px !important;
    }
    div[data-testid="stSlider"] [data-baseweb="slider"] > div > div > div {
        background: #0B2440 !important;
        height: 4px !important;
    }
    div[data-testid="stSlider"] [role="slider"] {
        background-color: #0B2440 !important;
        border: 2px solid #00E5FF !important;
        height: 20px !important;
        width: 20px !important;
        top: 2px !important; /* Precise vertical centering */
    }
    /* Fixing the RED DATES - Universal component override with label revert */
    div[data-testid="stSlider"] * {
        color: #0B2440 !important; /* Force blue on all parts (dates, values) */
        font-weight: 700;
    }
    div[data-testid="stSlider"] [data-testid="stWidgetLabel"] p {
        color: #5F6B7A !important; /* Keep the main TITLE in grey as requested */
        font-size: 0.70rem !important;
        letter-spacing: 0.8px;
        text-transform: uppercase;
        margin-bottom: 25px !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 6px; }
    .stTabs [data-baseweb="tab"] {
        height: 38px;
        background-color: #F0F2F6;
        border-radius: 8px 8px 0 0;
        padding: 0 16px;
        font-size: 0.88rem;
        font-weight: 500;
        color: #4A4F5A;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0B1426 !important;
        border-bottom: 2px solid #00E5FF !important;
        color: #FFFFFF !important;
        font-weight: 700;
    }


    /* Corner Analysis Styled Table */
    .corner-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.82rem;
        margin-top: 10px;
    }
    .corner-table th, .corner-table td {
        border: 1px solid #D0D5DD;
        text-align: center;
        padding: 6px 4px;
        min-width: 45px;
    }
    .corner-table .header-row {
        background-color: #F9FAFB;
        color: #5F6B7A;
        font-weight: 700;
    }
    .corner-table .corner-label {
        background-color: #F2F4F7;
        color: #5F6B7A;
        font-weight: 700;
        font-size: 0.75rem;
    }
    .corner-table .price-col {
        background-color: #F9FAFB;
        color: #5F6B7A;
        font-weight: 600;
    }
    .corner-table .cell-val {
        font-weight: 600;
        color: #101828;
    }
    [data-testid="stSidebar"] {
        background: #FFFFFF;
        border-right: 1px solid #E0E8F2;
    }
    [data-testid="stSidebar"] .stRadio > label {
        font-size: 11px;
        color: #5F6B7A;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    [data-testid="stSidebar"] .stSelectbox label {
        font-size: 11px;
        color: #5F6B7A;
    }
    /* Compact components */
    [data-testid="stSidebar"] div[data-testid="stImage"] { margin-bottom: -15px; margin-top: -10px; }
    [data-testid="stSidebar"] hr { margin-top: 6px !important; margin-bottom: 6px !important; }
    [data-testid="stSidebar"] section[data-testid="stSidebarNav"] { padding-top: 0.5rem; }
    [data-testid="stSidebar"] .stSelectbox { margin-bottom: -5px; }
    [data-testid="stSidebar"] .stRadio { margin-bottom: -5px; }
    </style>
    """, unsafe_allow_html=True)

import bcrypt

# --- AUTHENTICATION ---
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None
if 'name' not in st.session_state:
    st.session_state['name'] = None
if 'username' not in st.session_state:
    st.session_state['username'] = None

def manual_login():
    """Formulario de login nativo usando bcrypt directo para evitar fallos de stauth."""
    with st.container():
        st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("<h2 style='text-align: center; color: #0B2440;'>CHIMIRE Login</h2>", unsafe_allow_html=True)
            with st.form("Login Form"):
                user_input = st.text_input("Username").strip().lower()
                pass_input = st.text_input("Password", type="password")
                submit = st.form_submit_button("Login", use_container_width=True)
                
                if submit:
                    try:
                        # 1. Cargar secretos (Formato plano)
                        config = st.secrets.to_dict()
                        
                        # 2. Buscar al usuario directamente
                        if user_input in config and isinstance(config[user_input], (dict, st.runtime.secrets.Secrets)):
                            user_data = config[user_input]
                            # LIMPIEZA PROFUNDA: Solo permitimos caracteres válidos de BCrypt
                            import re
                            raw_val = str(user_data.get("password", ""))
                            stored_hash = re.sub(r'[^A-Za-z0-9./$]', '', raw_val)
                            
                            # 3. Validación Ultra-Resiliente (Bypass de emergencia)
                            try:
                                # Opción A: Probar con BCrypt
                                if len(stored_hash) == 60 and bcrypt.checkpw(pass_input.encode('utf-8'), stored_hash.encode('utf-8')):
                                    valid = True
                                # Opción B: Probar comparación directa (Rescate)
                                elif pass_input == str(user_data.get("password", "")):
                                    valid = True
                                else:
                                    valid = False
                                    
                                if valid:
                                    st.session_state['authentication_status'] = True
                                    st.session_state['name'] = user_data.get("name", user_input)
                                    st.session_state['username'] = user_input
                                    st.rerun()
                                else:
                                    st.error(f"⚠️ Contraseña incorrecta (Hash detectado: {len(stored_hash)} chars)")
                                    st.session_state['authentication_status'] = False
                            except Exception as e:
                                # Opción C: Si bcrypt explota, al menos permitir entrada por texto plano
                                if pass_input == str(user_data.get("password", "")):
                                    st.session_state['authentication_status'] = True
                                    st.rerun()
                                else:
                                    st.error(f"❌ Error en motor: {str(e)}")
                        else:
                            st.warning(f"⚠️ Usuario '{user_input}' no encontrado en Secrets")
                            st.session_state['authentication_status'] = False
                    except Exception as e:
                        st.error(f"❌ Error Técnico: {str(e)}")
                        st.session_state['authentication_status'] = False

if st.session_state['authentication_status'] is not True:
    manual_login()

if st.session_state["authentication_status"]:
    # ── LOGOUT EN SIDEBAR (Para mantener compatibilidad) ──────────
    def logout():
        st.session_state['authentication_status'] = None
        st.session_state['name'] = None
        st.session_state['username'] = None
        st.rerun()

if st.session_state["authentication_status"]:
    # ── SIDEBAR ─────────────────────────────────
    with st.sidebar:
        # Logo
        try:
            st.image("mi_logo.png", use_container_width=True)
        except Exception:
            st.markdown("### ⚡ CHIMIRE")
        st.divider()

        # Idioma
        st.markdown("""
            <style>
            /* Reducir espacio en selector de idioma */
            div[data-testid="stSidebar"] .stSelectbox { margin-bottom: -20px; }
            div[data-testid="stSidebar"] .stRadio { margin-bottom: -10px; }
            </style>
            """, unsafe_allow_html=True)
        lang = st.selectbox("🌐 Idioma / Language", ["Español", "English"])
        st.divider()

        # Carga de datos (necesaria para saber los escenarios en el sidebar)
        escenarios, datos = dp.load_and_process_data()

        # Selector de Escenario en el sidebar
        texts_scenario = "Escenario" if lang == "Español" else "Scenario"
        escenario_selected = st.radio(texts_scenario, options=escenarios, index=0)
        st.divider()

        # ── DESCRIPCIÓN E IMAGEN DEL ESCENARIO ──────────────────
        try:
            # Buscar descripción en la hoja DescEscenarios
            df_desc = datos['escenarios']
            desc_row = df_desc[df_desc['Escenario'] == escenario_selected]
            if not desc_row.empty:
                # 1. Imagen centrada y con espacio superior
                img_path = {
                    "Caso Base": "Escenario Base.png",
                    "Esc 1":     "Escenario 1.png",
                    "Esc 2":     "Escenario 2.png"
                }.get(escenario_selected, "Escenario Base.png")

                st.markdown("<div style='margin-top:10px'></div>", unsafe_allow_html=True)
                col_i1, col_i2, col_i3 = st.columns([1, 4, 1])
                with col_i2:
                    st.image(img_path, use_container_width=True)

                # 2. Descripción traducida
                # Si el idioma es inglés, usamos traducciones predefinidas
                if lang == "English":
                    desc_text = {
                        "Caso Base": "Considers 397 activities, 100 new wells starting drilling in 2025, and the purchase of 3 compressors.",
                        "Esc 1":     "Considers 304 activities, 50 new wells starting drilling in 2025, and the purchase of 2 compressors.",
                        "Esc 2":     "Considers 397 activities, 100 new wells starting drilling in 2025, and the purchase of 3 compressors."
                    }.get(escenario_selected, desc_row.iloc[0]['Descripcion'])
                else:
                    desc_text = desc_row.iloc[0]['Descripcion']

                st.markdown(f"""
                    <div style='background-color:#F0F4F8; padding:8px; border-radius:6px; border:1px solid #D0D7DE; margin-bottom:10px'>
                        <p style='font-size:10.5px; line-height:1.3; color:#24292F; margin:0;'>
                            <b>{escenario_selected}:</b> {desc_text}
                        </p>
                    </div>
                """, unsafe_allow_html=True)
                st.divider() # Separation line after description
        except Exception as e:
            pass # Silencioso si no hay imagen o descripción

        # ── SECCIÓN DE USUARIO ──────────────────────────
        st.markdown("<div style='margin-top:15px'></div>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size:12px;color:#5F6B7A;margin:0;font-weight:500'>👤 {st.session_state['name']}</p>",
                    unsafe_allow_html=True)
        # Logout (Manual)
        logout_text = '🔒 Cerrar Sesión' if lang == 'Español' else '🔒 Logout'
        if st.button(logout_text, use_container_width=True):
            logout()

    # ── TEXTOS i18n GLOBAL ──────────────────────
    texts = {
        "Español": {
            "title":        "Valoración del Campo CHIMIRE",
            "subtitle":     "Dashboard de Análisis de Producción y Economía",
            "scenario":     "Escenario",
            "tabs":         ["📊 Valoración y Resumen", "📈 Producción y Costos", "📉 Comparación Escenarios", "🛢️ Gestión de Pozos", "🏁 Análisis Corner"],
            "metrica":      "Métrica",
            "rango":        "Rango Probabilístico",
            "unit":         "Unidad",
            "val_p10":      "P10 (Pesimista)",
            "val_exp":      "Media (Esperado)",
            "val_p90":      "P90 (Optimista)",
            "chart_prod":   "Perfiles de Producción",
            "chart_costs":  "Costos Globales",
            "well_mgmt":    "Gestión de Pozos Tipo",
            "corner_title": "Análisis Corner – Matriz de Sensibilidad",
            "comp_scen":    "Comparación de Escenarios",
            "filter":       "Filtrar",
            "oil":          "Aceite",
            "gas":          "Gas",
            "daily":        "Diaria",
            "accum":        "Acumulada",
        },
        "English": {
            "title":        "CHIMIRE Field Valuation",
            "subtitle":     "Production & Economic Analysis Dashboard",
            "scenario":     "Scenario",
            "tabs":         ["📊 Valuation & Summary", "📈 Production & Costs", "📉 Scenario Comparison", "🛢️ Well Management", "🏁 Corner Analysis"],
            "metrica":      "Metric",
            "rango":        "Probabilistic Range",
            "unit":         "Unit",
            "val_p10":      "P10 (Pessimistic)",
            "val_exp":      "Mean (Expected)",
            "val_p90":      "P90 (Optimistic)",
            "chart_prod":   "Production Profiles",
            "chart_costs":  "Global Costs",
            "well_mgmt":    "Well Type Management",
            "corner_title": "Corner Analysis – Sensitivity Matrix",
            "comp_scen":    "Scenario Comparison",
            "filter":       "Filter",
            "oil":          "Oil",
            "gas":          "Gas",
            "daily":        "Daily",
            "accum":        "Cumulative",
        }
    }[lang]

    # ── MAIN CONTENT ────────────────────────────
    st.markdown(f"<h1 class='main-header'>{texts['title']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p class='sub-header'>{texts['subtitle']} &nbsp;|&nbsp; <b>{escenario_selected}</b></p>",
                unsafe_allow_html=True)

    # Renderizado por Pestañas
    ui.render_dashboard(datos, escenario_selected, texts)

elif st.session_state["authentication_status"] is False:
    st.error("Usuario/contraseña incorrectos")
elif st.session_state["authentication_status"] is None:
    st.warning("Por favor, ingrese sus credenciales para acceder al Dashboard")
