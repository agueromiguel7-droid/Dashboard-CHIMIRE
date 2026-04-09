"""
ui_components.py  –  CHIMIRE Dashboard
Fidelidad visual al reporte Power BI (carpeta Imagens Chimire)
Paleta: Deep Navy #0B1426 | Electric Cyan #00E5FF | Orange-highlight #FF5722 | Blue-mid #1565C0
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import data_processing as dp
from translations import TRANSLATIONS
from plotly.subplots import make_subplots

# ──────────────────────────────────────────────
#  DESIGN SYSTEM
# ──────────────────────────────────────────────
C = {
    'navy':    '#0B1426',
    'cyan':    '#00E5FF',
    'blue1':   '#1565C0',
    'blue2':   '#1E88E5',
    'blue3':   '#64B5F6',
    'orange':  '#FF5722',
    'green':   '#00897B',
    'grid':    '#E8ECF0',
    'bg':      '#F7F9FC',
    'white':   '#FFFFFF',
    'text':    '#1A2340',
    'muted':   '#5F6B7A',
}

_SCENARIO_COLORS = {
    'Caso Base': C['navy'],
    'Esc 1':     C['blue2'],
    'Esc 2':     C['blue1'],
}

PROD_COLORS = {
    'P10':   C['navy'],
    'P50':   C['blue2'],
    'P90':   C['orange'],
    'Media': C['cyan'],
    '1P':    C['navy'],
    '2P':    C['blue2'],
    '3P':    C['blue3'],
}

def _base_layout(fig, title='', height=340):
    fig.update_layout(
        title=dict(text=title, font=dict(size=12, color=C['text']), x=0),
        plot_bgcolor=C['white'],
        paper_bgcolor=C['bg'],
        font=dict(family='Inter, sans-serif', size=9, color=C['text']),
        margin=dict(l=10, r=10, t=35, b=70),   # generous bottom for legend
        height=height,
        legend=dict(
            orientation='h',
            yanchor='top', y=-0.22,      # well below x-axis label
            xanchor='center', x=0.5,
            font=dict(size=8),
            traceorder='normal',
            entrywidth=90,               # wider entries so they spread horizontally
        ),
    )
    fig.update_xaxes(
        showgrid=True, gridwidth=1, gridcolor=C['grid'],
        zeroline=False, linecolor=C['grid'],
        tickfont=dict(size=8),           # smaller axis ticks
    )
    fig.update_yaxes(
        showgrid=True, gridwidth=1, gridcolor=C['grid'],
        zeroline=False, linecolor=C['grid'],
        tickfont=dict(size=8),
    )
    return fig


def _card(col, label, value, unit=''):
    col.markdown(f"""
    <div style="background:{C['white']};border-left:5px solid {C['cyan']};
                border-radius:8px;padding:14px 18px;box-shadow:0 1px 4px rgba(0,0,0,.08)">
      <p style="margin:0;font-size:11px;color:{C['muted']};font-weight:600;
                text-transform:uppercase;letter-spacing:.5px">{label}</p>
      <p style="margin:4px 0 0;font-size:28px;font-weight:700;color:{C['navy']}">{value}
        <span style="font-size:13px;color:{C['muted']}">{unit}</span></p>
    </div>""", unsafe_allow_html=True)



# ──────────────────────────────────────────────
#  TAB 1 – VALORACIÓN Y RESUMEN
# ──────────────────────────────────────────────
def render_tab_valoracion(datos, escenario, texts):
    agrupacion_opts = dp.get_agrupacion_options(datos)

    # ── Título + selector de precio (Diseño Ultra-Compacto) ──
    st.markdown("<div style='margin-top:-25px'></div>", unsafe_allow_html=True)
    h_col1, h_col2 = st.columns([1.8, 1])
    with h_col1:
        st.markdown(f"<h2 style='margin:0; padding:0; font-size:1.5rem; color:{C['navy']}'>💰 {texts['metrica']} de Valoración</h2>" if texts['metrica'] == 'Métrica' else f"<h2 style='margin:0; padding:0; font-size:1.5rem; color:{C['navy']}'>💰 Valuation {texts['metrica']}s</h2>", unsafe_allow_html=True)
    with h_col2:
        agrupacion = st.selectbox(
            "Precio Ref.", agrupacion_opts, index=0,
            key="val_agrupacion", label_visibility="collapsed"
        ) if agrupacion_opts else None

    df = dp.get_kpi_df_agrupacion(datos, escenario, agrupacion)

    def _lookup(keyword):
        # Determine current column names (Indicator/Media vs Indicador/Media)
        col_ind = 'Indicator' if 'Indicator' in df.columns else 'Indicador'
        col_val = 'Mean'      if 'Mean'      in df.columns else 'Media'

        if col_ind not in df.columns or col_val not in df.columns:
            return 0.0
        
        # Translate keyword if in English
        search_term = keyword
        if col_ind == 'Indicator':
            # Use English keyword mapping from translations.py if available
            search_term = TRANSLATIONS['English']['keywords'].get(keyword, keyword)
            
        mask = df[col_ind].astype(str).str.contains(search_term, case=False, na=False)
        return round(float(df.loc[mask, col_val].iloc[0]), 2) if mask.any() else 0.0

    vpn = _lookup('neto 15')
    vpi = _lookup('inversión')
    vpc = _lookup('costos')
    rec = _lookup('Recuperación')
    ei  = _lookup('Eficiencia')
    rbc = _lookup('beneficio')

    # Costos por tipo (desde PBI MPP)
    costs = dp.get_costs_summary(datos, escenario)

    # ── Layout: KPIs (izq, borde cyan) | Panel costos (der, borde azul oscuro) ──
    left_col, right_col = st.columns([3, 2])

    with left_col:
        r1 = st.columns(3)
        _card(r1[0], 'VPN (MMUSD)', f"{vpn:.2f}")
        _card(r1[1], 'VPI (MMUSD)', f"{vpi:.2f}")
        _card(r1[2], 'VPC (MMUSD)', f"{vpc:.2f}")
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        r2 = st.columns(3)
        _card(r2[0], texts['rec_period'] if 'rec_period' in texts else 'Período Rec.', f"{rec:.2f}")
        _card(r2[1], 'EI',           f"{ei:.2f}")
        _card(r2[2], 'RBC',          f"{rbc:.2f}")

    with right_col:
        cost_labels = list(costs.keys())
        n = len(cost_labels)
        for row_i in range(0, n, 3):
            row_items = cost_labels[row_i:row_i+3]
            sub_cols  = st.columns(len(row_items))
            for ci, lbl in enumerate(row_items):
                val      = costs.get(lbl, 0.0)
                disp_lbl = lbl.replace('\n', ' ')
                sub_cols[ci].markdown(
                    f"<div style='background:{C['white']};border-left:5px solid {C['blue1']};"
                    f"border-radius:6px;padding:10px 12px;"
                    f"box-shadow:0 1px 4px rgba(0,0,0,.07);margin-bottom:8px;text-align:left'>"
                    f"<p style='margin:0;font-size:9px;color:{C['muted']};font-weight:600;"
                    f"text-transform:uppercase;letter-spacing:.3px'>{disp_lbl}</p>"
                    f"<p style='margin:2px 0 0;font-size:20px;font-weight:700;color:{C['blue1']}'>"
                    f"{val:.2f}</p></div>",
                    unsafe_allow_html=True
                )

    st.divider()

    # ── Tabla Pozos + Gráfico CAPEX/OPEX ──────────────────────
    tbl_col, chart_col = st.columns([3, 2])

    with tbl_col:
        # Título con acento cyan
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px;margin-top:10px">
          <div style="width:4px;height:22px;background:{C['cyan']};border-radius:2px"></div>
          <p style="margin:0;font-size:14px;font-weight:700;color:{C['navy']}">Technical Production Metrics</p>
        </div>""", unsafe_allow_html=True)

        pozos_df = dp.get_pozos_df(datos, escenario)
        if not pozos_df.empty:
            show_map = {
                'Well Type': 'WELL TYPE',
                'Pozo Tipo': 'POZO TIPO',
                'Count':     'COUNT',
                'Cantidad':  'CANT.',
                'Cost_MP':   'COST (MMUSD)',
                'Costo_MP':  'COSTO (MUSD)',
                'Qo_Mean':   'QO EXP.',
                'Qo_50':     'QO ESP.',
                'Qg_Mean':   'QG EXP.',
                'Qg_50':     'QG ESP.',
            }
            avail = [c for c in show_map if c in pozos_df.columns]
            tbl = pozos_df[avail].dropna(subset=[avail[0]]).rename(columns=show_map).copy()

            p2 = dp.get_pozos2_df(datos, escenario)
            np_map = {}; gp_map = {}
            col_pt = 'Well Type' if 'Well Type' in p2.columns else 'Pozo Tipo'
            if not p2.empty and col_pt in p2.columns:
                for _, r in p2.dropna(subset=[col_pt]).iterrows():
                    pt  = r[col_pt]
                    npc = [c for c in p2.columns if 'Np' in str(c)]
                    gpc = [c for c in p2.columns if 'Gp' in str(c)]
                    if npc: np_map[pt] = round(float(r[npc[0]]), 1)
                    if gpc: gp_map[pt] = round(float(r[gpc[0]]), 1)
            
            p_label = 'WELL TYPE' if 'WELL TYPE' in tbl.columns else 'POZO TIPO'
            tbl['NP'] = tbl[p_label].map(np_map).fillna(0.0)
            tbl['GP'] = tbl[p_label].map(gp_map).fillna(0.0)

            # Estilo de tabla "Premium"
            st.markdown(f"""
            <style>
                .stDataFrame [data-testid="stTable"] {{
                    font-size: 11px;
                }}
                [data-testid="stMetricValue"] {{
                    font-size: 24px;
                }}
            </style>
            """, unsafe_allow_html=True)

            st.dataframe(
                tbl.style.format(
                    {c: '{:,.1f}' for c in tbl.columns if c != p_label}, na_rep='–'
                ).set_properties(subset=[p_label], **{'font-weight': 'bold', 'color': C['navy']})
                .set_table_styles([
                    {'selector': 'th', 'props': [('background-color', '#F0F2F6'), ('color', '#5F6B7A'), ('font-weight', '700'), ('text-transform', 'uppercase'), ('font-size', '10px'), ('letter-spacing', '0.5px')]},
                    {'selector': 'td', 'props': [('padding', '10px')]}
                ]),
                use_container_width=True, hide_index=True, height=260
            )
        else:
            st.info("Sin datos de pozos disponibles." if texts['metrica'] == 'Métrica' else "No well data available.")

    with chart_col:
        mpp = dp.get_mpp_df(datos, escenario)
        if not mpp.empty:
            ts_c = [c for c in mpp.columns if str(c).startswith('2')]
            dates_all = pd.to_datetime(ts_c, errors='coerce')

            # --- Control del Rango de Fechas ---
            valid_dates = dates_all.dropna()
            if not valid_dates.empty:
                date_min = valid_dates.min().to_pydatetime()
                date_max = valid_dates.max().to_pydatetime()

                st.markdown(f"<p style='font-size:10px;color:{C['muted']};font-weight:700;text-transform:uppercase;margin-bottom:0'>{texts['rango_fechas'] if 'rango_fechas' in texts else 'Rango de Fechas'}</p>", unsafe_allow_html=True)
                fecha_inicio, fecha_fin = st.slider(
                    "range_val_chart",
                    min_value=date_min, max_value=date_max, value=(date_min, date_max),
                    format="DD/MM/YYYY", label_visibility="collapsed", key="val_date_slider"
                )
                
                mask = (dates_all >= pd.Timestamp(fecha_inicio)) & (dates_all <= pd.Timestamp(fecha_fin))
                ts_filtered = [ts_c[i] for i, m in enumerate(mask) if m]
                dates_plt = dates_all[mask]
            else:
                ts_filtered = ts_c
                dates_plt = dates_all

            capex_vars = [v for v in mpp['Variable'].dropna().unique() if 'CAPEX' in str(v).upper()]
            opex_vars  = [v for v in mpp['Variable'].dropna().unique() if 'OPEX'  in str(v).upper()]

            def _sv(vlist, cat='Media'):
                # Handle categories and variable column names
                target_cat = TRANSLATIONS['English']['values'].get(cat, cat) if 'Category' in mpp.columns else cat
                col_var = 'Variable'
                col_cat = 'Category' if 'Category' in mpp.columns else 'Categoría'

                s = pd.Series(0.0, index=ts_filtered)
                for vn in vlist:
                    # Translate vn for English mode
                    search_vn = TRANSLATIONS['English']['values'].get(vn, vn) if 'Category' in mpp.columns else vn
                    r = mpp[(mpp[col_var] == search_vn) & (mpp[col_cat] == target_cat)]
                    if not r.empty:
                        s += pd.to_numeric(r.iloc[0][ts_filtered], errors='coerce').fillna(0)
                return s

            capex_s = _sv(capex_vars)
            opex_s  = _sv(opex_vars)
            # Acumulado se calcula sobre el rango completo para ser correcto, pero filtrado para el plot
            total_perf_s = (pd.to_numeric(mpp[mpp['Variable'].isin(capex_vars + opex_vars)][ts_c].sum(), errors='coerce')).fillna(0)
            acum_s_full = total_perf_s.cumsum()
            acum_s = acum_s_full[mask]

            fig_co = go.Figure()
            fig_co.add_trace(go.Bar(
                x=dates_plt, y=capex_s.values, name='CAPEX',
                marker_color=C['blue2'], yaxis='y'
            ))
            fig_co.add_trace(go.Bar(
                x=dates_plt, y=opex_s.values, name='OPEX',
                marker_color=C['orange'], yaxis='y'
            ))
            fig_co.add_trace(go.Scatter(
                x=dates_plt, y=acum_s.values, name=texts['accum'] if 'accum' in texts else 'Acumulado',
                line=dict(color=C['navy'], width=2), mode='lines', yaxis='y2'
            ))
            fig_co.update_layout(
                barmode='stack',
                title=dict(text=texts['chart_costs'] if 'chart_costs' in texts else 'Perfiles de Egresos CAPEX y OPEX', font=dict(size=12, weight='bold'), x=0),
                height=380, margin=dict(l=10, r=10, t=40, b=65),
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=9),
                legend=dict(orientation='h', yanchor='top', y=-0.2,
                            xanchor='center', x=0.5, font=dict(size=9)),
                yaxis=dict(title='MMUSD', tickfont=dict(size=8), showgrid=True, gridcolor='#eee'),
                yaxis2=dict(title=texts['accum'] if 'accum' in texts else 'Acum.', overlaying='y', side='right',
                            tickfont=dict(size=8), showgrid=False),
                xaxis=dict(tickfont=dict(size=8), showgrid=False)
            )
            st.plotly_chart(fig_co, use_container_width=True)
        else:
            st.info("Sin datos de CAPEX/OPEX para este escenario." if texts['metrica'] == 'Métrica' else "No CAPEX/OPEX data for this scenario.")









# ──────────────────────────────────────────────
#  TAB 2 – PRODUCCIÓN Y COSTOS
# ──────────────────────────────────────────────
def _get_timeseries(mpp_df, variable, categories):
    """Extrae una dict {cat: pd.Series of dates→values} para la variable dada."""
    ts_cols = [c for c in mpp_df.columns if str(c).startswith('2')]
    result = {}
    col_var = 'Variable'
    col_cat = 'Category' if 'Category' in mpp_df.columns else 'Categoría'
    is_en = (col_cat == 'Category')
    
    for cat in categories:
        target_cat = TRANSLATIONS['English']['values'].get(cat, cat) if is_en else cat
        search_vn = TRANSLATIONS['English']['values'].get(variable, variable) if is_en else variable
        
        row = mpp_df[(mpp_df[col_var] == search_vn) & (mpp_df[col_cat] == target_cat)]
        if not row.empty:
            series = row.iloc[0][ts_cols]
            # Convertir fechas string a datetime
            dates = pd.to_datetime(ts_cols, errors='coerce')
            s = pd.Series(series.values, index=dates).dropna()
            result[cat] = s
    return result, ts_cols


def render_tab_produccion(datos, escenario, texts):
    mpp    = dp.get_mpp_df(datos, escenario)
    pozos2 = dp.get_pozos2_df(datos, escenario)

    if mpp.empty:
        st.info("Sin datos de producción para este escenario." if texts['metrica'] == 'Métrica' else "No production data for this scenario.")
        return

    ts_cols = [c for c in mpp.columns if str(c).startswith('2')]
    dates   = pd.to_datetime(ts_cols, errors='coerce')

    st.markdown(f"#### 📉 {texts['chart_prod'] if 'chart_prod' in texts else 'Perfiles de Producción'}")

    # Compute valid date range from time-series columns
    valid_dates = dates.dropna()
    date_min    = valid_dates.min().to_pydatetime()
    date_max    = valid_dates.max().to_pydatetime()

    # ── Fila de controles: Fluido | Rango de Fechas en la misma línea ──
    # CSS trick: push slider content down to vertically align with radio
    st.markdown(
        "<style>.prod-ctrl-row .stSlider{padding-top:18px}</style>",
        unsafe_allow_html=True
    )
    ctrl_a, ctrl_b = st.columns([2, 5])

    with ctrl_a:
        fluido = st.radio(
            "Fluido" if texts['metrica'] == 'Métrica' else "Fluid", [texts['oil'], texts['gas']],
            horizontal=True, key="fluido_toggle"
        )
        # Map back to internal storage names
        internal_fluido = "Aceite" if fluido == texts['oil'] else "Gas"

    with ctrl_b:
        st.markdown(
            f"<p style='font-size:10px;color:#5F6B7A;margin:0 0 0 0;"
            f"text-transform:uppercase;letter-spacing:.5px;line-height:1'>"
            f"{texts['rango_fechas'] if 'rango_fechas' in texts else 'Rango de Fechas'}</p>",
            unsafe_allow_html=True
        )
        fecha_inicio, fecha_fin = st.slider(
            label            = "rango_fechas",
            min_value        = date_min,
            max_value        = date_max,
            value            = (date_min, date_max),
            format           = "DD/MM/YYYY",
            label_visibility = "collapsed",
            key              = "prod_date_range"
        )

    # Build a boolean mask over the dates array using the selected range
    date_mask = (dates >= pd.Timestamp(fecha_inicio)) & (dates <= pd.Timestamp(fecha_fin))
    ts_filtered = [ts_cols[i] for i, m in enumerate(date_mask) if m]
    dates_f     = dates[date_mask]

    # x-axis range for Plotly (slightly padded)
    xrange = [fecha_inicio, fecha_fin]

    if internal_fluido == "Aceite":
        var_diaria   = "Qo"
        var_acum     = "NP"
        label_diaria = f"Qo (bd) – {texts['chart_prod']} {texts['daily']} {texts['oil']}" if texts['metrica'] != 'Métrica' else "Qo (bd) – Producción Diaria de Aceite"
        label_acum   = f"Np (MMb) – {texts['chart_prod']} {texts['accum']} {texts['oil']}" if texts['metrica'] != 'Métrica' else "Np (MMb) – Producción Acumulada de Aceite"
        unit_d, unit_a = "bd", "MMb"
    else:
        var_diaria   = "Qg"
        var_acum     = "GP"
        label_diaria = f"Qg (Mpcd) – {texts['chart_prod']} {texts['daily']} {texts['gas']}" if texts['metrica'] != 'Métrica' else "Qg (Mpcd) – Producción Diaria de Gas"
        label_acum   = f"Gp (MMpc) – {texts['chart_prod']} {texts['accum']} {texts['gas']}" if texts['metrica'] != 'Métrica' else "Gp (MMpc) – Producción Acumulada de Gas"
        unit_d, unit_a = "Mpcd", "MMpc"

    # ── Gráficos de Producción y Reservas ──────────────────
    col_reservas, col_prod = st.columns([1, 1.3])

    with col_reservas:
        reservas_var = "Reservas Aceite" if internal_fluido == "Aceite" else "Reservas Gas"
        col_var = 'Variable'
        col_cat = 'Category' if 'Category' in mpp.columns else 'Categoría'
        is_en = (col_cat == 'Category')
        search_res = TRANSLATIONS['English']['values'].get(reservas_var, reservas_var) if is_en else reservas_var
        
        fig_res = go.Figure()
        cats_res = ['1P', '2P', '3P']
        colors_res = [C['navy'], C['blue2'], C['blue3']]
        
        for i, cat in enumerate(cats_res):
            row_res = mpp[(mpp[col_var] == search_res) & (mpp[col_cat] == cat)]
            if not row_res.empty:
                val = 0.0
                if ts_cols:
                    try:
                        val = float(row_res.iloc[0][ts_cols[0]])
                    except:
                        val = 0.0
                
                txt_val = f"{val:,.1f}" if val > 0 else ""
                fig_res.add_trace(go.Bar(
                    x=[cat], y=[val], name=cat,
                    marker_color=colors_res[i],
                    text=[txt_val], textposition='outside',
                    textfont=dict(size=11, color=C['navy'])
                ))
        
        lbl_res = f"Reservas de {texts['oil'] if internal_fluido=='Aceite' else texts['gas']} ({unit_a})" if texts['metrica'] == 'Métrica' else f"{texts['oil'] if internal_fluido=='Aceite' else texts['gas']} Reserves ({unit_a})"
        _base_layout(fig_res, lbl_res, height=330)
        fig_res.update_layout(
            showlegend=False,
            margin=dict(l=10, r=10, t=35, b=40),
            yaxis=dict(autorange=True, rangemode='tozero')
        )
        st.plotly_chart(fig_res, use_container_width=True)

    with col_prod:
        fig_prod = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Plot Diaria (left axis)
        for cat, color in [('P10', C['navy']), ('Media', C['blue2']), ('P90', C['orange'])]:
            target_cat = ('Mean' if cat == 'Media' else cat) if is_en else cat
            search_vn = TRANSLATIONS['English']['values'].get(var_diaria, var_diaria) if is_en else var_diaria
            
            row_d = mpp[(mpp[col_var] == search_vn) & (mpp[col_cat] == target_cat)]
            if not row_d.empty and ts_filtered:
                y = row_d.iloc[0][ts_filtered].values
                fig_prod.add_trace(go.Scatter(
                    x=dates_f, y=y, name=f"{cat} ({texts['daily']})",
                    line=dict(color=color, width=2.5), mode='lines'
                ), secondary_y=False)
                
        # Plot Acumulada (right axis)
        for cat, color in [('P10', C['navy']), ('Media', C['blue1']), ('P90', '#FF8A65')]:
            target_cat = ('Mean' if cat == 'Media' else cat) if is_en else cat
            search_vn = TRANSLATIONS['English']['values'].get(var_acum, var_acum) if is_en else var_acum
            
            row_a = mpp[(mpp[col_var] == search_vn) & (mpp[col_cat] == target_cat)]
            if not row_a.empty and ts_filtered:
                y = row_a.iloc[0][ts_filtered].values
                fig_prod.add_trace(go.Scatter(
                    x=dates_f, y=y, name=f"{cat} ({texts['accum']})",
                    line=dict(color=color, width=2, dash='dot'), mode='lines'
                ), secondary_y=True)

        combined_label = f"{var_diaria} y {var_acum} – {texts['chart_prod']}"
        _base_layout(fig_prod, combined_label, height=330)
        fig_prod.update_layout(
            legend=dict(
                orientation='h',
                yanchor='top', y=-0.15,
                xanchor='center', x=0.5,
                font=dict(size=9),
                traceorder='normal',
            ),
        )
        fig_prod.update_xaxes(title_text='Fecha' if texts['metrica'] == 'Métrica' else 'Date', range=xrange)
        fig_prod.update_yaxes(title_text=unit_d, secondary_y=False, showgrid=True, gridcolor=C['grid'])
        fig_prod.update_yaxes(title_text=unit_a, secondary_y=True, showgrid=False)
        st.plotly_chart(fig_prod, use_container_width=True)

    # ── Fila inferior: CAPEX | OPEX | Cantidad de Pozos Tipo ─
    st.divider()
    c1, c2, c3 = st.columns(3)

    year_start = fecha_inicio.year
    year_end   = fecha_fin.year

    # ─── helper: build annual stacked series filtered to date range ──────
    def _annual_series(var_name, cat='Media'):
        col_var = 'Variable'
        col_cat = 'Category' if 'Category' in mpp.columns else 'Categoría'
        is_en = (col_cat == 'Category')
        
        target_cat = ('Mean' if cat == 'Media' else cat) if is_en else cat
        search_vn = TRANSLATIONS['English']['values'].get(var_name, var_name) if is_en else var_name
        
        rows = mpp[(mpp[col_var] == search_vn) & (mpp[col_cat] == target_cat)]
        if rows.empty or not ts_filtered:
            return pd.Series(dtype=float)
        y = rows.iloc[0][ts_filtered].values
        s = pd.Series(y.astype(float), index=dates_f)
        annual = s.groupby(s.index.year).sum()
        return annual[(annual.index >= year_start) & (annual.index <= year_end)]

    def _chart_style(fig, title, color_map=None):
        """Apply DESIGN.md aesthetics: no harsh borders, tonal depth, Electric Cyan accent."""
        _base_layout(fig, title, height=340)
        fig.update_layout(
            plot_bgcolor='#FFFFFF',
            paper_bgcolor='#F7F9FB',
            bargap=0.25,
            yaxis=dict(
                autorange=True,          # let plotly auto-scale properly
                rangemode='tozero',
                tickformat='.1f',
            ),
        )
        fig.update_xaxes(
            range=[year_start - 0.5, year_end + 0.5],
            tickmode='linear', dtick=1,
            tickangle=-45,
            title_text='Año',
        )
        return fig

    # ─── CAPEX section ───────────────────────────────────────────────────
    with c1:
        all_capex = sorted(set(str(v).strip() for v in mpp['Variable'].dropna().unique()
                               if 'CAPEX' in str(v).upper() or 'Capex' in str(v)))

        # Use language-specific keys to avoid Streamlit value/options mismatch on switch
        capex_key = "capex_sel_en" if texts['metrica'] != 'Métrica' else "capex_sel_es"
        
        # Initialize session state default (first run only)
        if capex_key not in st.session_state:
            st.session_state[capex_key] = all_capex[:] if all_capex else []

        # Read current selection (updated after user interacts with expander)
        capex_sel = st.session_state.get(capex_key, all_capex[:])
        
        # Fallback: ensure no stale invalid selection ruins the widget
        valid_capex_sel = [x for x in capex_sel if x in all_capex]
        if len(valid_capex_sel) == 0 and len(all_capex) > 0:
            valid_capex_sel = all_capex[:]
            st.session_state[capex_key] = valid_capex_sel
            
        capex_sel = valid_capex_sel

        # ── Título del bloque ──
        st.markdown(
            "<p style='font-size:11px;font-weight:600;color:#012743;"
            "text-transform:uppercase;letter-spacing:.5px;margin:0 0 2px 0'>"
            "CAPEX (MMUSD)</p>", unsafe_allow_html=True
        )

        # ── Gráfico (usa selección actual) ──
        if capex_sel:
            palette_capex = [C['navy'], C['blue2'], C['blue3'], C['cyan'], '#0D47A1', '#29B6F6']
            fig3 = go.Figure()
            for i, var in enumerate(capex_sel):
                annual = _annual_series(var)
                if not annual.empty:
                    col_bar = palette_capex[i % len(palette_capex)]
                    txt = [f"{v:.1f}" if v > 0.01 else "" for v in annual.values]
                    fig3.add_trace(go.Bar(
                        x=annual.index, y=annual.values,
                        name=var.replace('CAPEX ', ''),
                        marker_color=col_bar,
                        text=txt, textposition='outside',
                        textfont=dict(size=9),
                    ))
            fig3.update_layout(barmode='stack')
            _chart_style(fig3, '')
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.info("Selecciona al menos un tipo de CAPEX.")

        # ── Selector desplegable DEBAJO del gráfico ──
        with st.expander("▾ Filtrar tipos de CAPEX", expanded=False):
            st.multiselect(
                "Tipos de CAPEX" if texts['metrica'] == 'Métrica' else "CAPEX Types", all_capex,
                default=capex_sel,
                key=capex_key,
                label_visibility="collapsed"
            )

    # ─── OPEX section ────────────────────────────────────────────────────
    with c2:
        all_opex = sorted(set(str(v).strip() for v in mpp['Variable'].dropna().unique()
                              if 'OPEX' in str(v).upper() or 'Opex' in str(v)))

        opex_key = "opex_sel_en" if texts['metrica'] != 'Métrica' else "opex_sel_es"

        # Initialize session state default (first run only)
        if opex_key not in st.session_state:
            st.session_state[opex_key] = all_opex[:] if all_opex else []

        # Read current selection
        opex_sel = st.session_state.get(opex_key, all_opex[:])
        
        # Fallback: ensure no stale invalid selection ruins the widget
        valid_opex_sel = [x for x in opex_sel if x in all_opex]
        if len(valid_opex_sel) == 0 and len(all_opex) > 0:
            valid_opex_sel = all_opex[:]
            st.session_state[opex_key] = valid_opex_sel
            
        opex_sel = valid_opex_sel

        # ── Título del bloque ──
        st.markdown(
            "<p style='font-size:11px;font-weight:600;color:#012743;"
            "text-transform:uppercase;letter-spacing:.5px;margin:0 0 2px 0'>"
            "OPEX (MMUSD)</p>", unsafe_allow_html=True
        )

        # ── Gráfico (usa selección actual) ──
        if opex_sel:
            palette_opex = [C['orange'], '#E53935', '#FB8C00', '#FF7043', '#D84315', '#BF360C']
            fig4 = go.Figure()
            for i, var in enumerate(opex_sel):
                annual = _annual_series(var)
                if not annual.empty:
                    col_bar = palette_opex[i % len(palette_opex)]
                    txt = [f"{v:.1f}" if v > 0.01 else "" for v in annual.values]
                    fig4.add_trace(go.Bar(
                        x=annual.index, y=annual.values,
                        name=var.replace('OPEX ', ''),
                        marker_color=col_bar,
                        text=txt, textposition='outside',
                        textfont=dict(size=9),
                    ))
            fig4.update_layout(barmode='stack')
            _chart_style(fig4, '')
            st.plotly_chart(fig4, use_container_width=True)
        else:
            st.info("Selecciona al menos un tipo de OPEX.")

        # ── Selector desplegable DEBAJO del gráfico ──
        with st.expander("▾ Filtrar tipos de OPEX", expanded=False):
            st.multiselect(
                "Tipos de OPEX" if texts['metrica'] == 'Métrica' else "OPEX Types", all_opex,
                default=opex_sel,
                key=opex_key,
                label_visibility="collapsed"
            )


    # ─── Cantidad de Actividad por Pozo Tipo ─────────────────────────────
    with c3:
        st.markdown(
            f"<p style='font-size:11px;font-weight:600;color:#012743;"
            f"text-transform:uppercase;letter-spacing:.5px;margin:0 0 4px 0'>"
            f"Cantidad de Actividad</p>", unsafe_allow_html=True
        )
        col_pt  = 'Well Type' if 'Well Type' in pozos2.columns else 'Pozo Tipo'
        col_qty = 'Count'     if 'Count'     in pozos2.columns else 'Cantidad'
        
        if not pozos2.empty and col_pt in pozos2.columns and col_qty in pozos2.columns:
            total = int(pozos2[col_qty].sum())
            txt5 = [str(int(v)) if v > 0 else "" for v in pozos2[col_qty]]
            fig5 = go.Figure(go.Bar(
                x=pozos2[col_pt],
                y=pozos2[col_qty],
                marker_color=C['blue2'],
                text=txt5,
                textposition='outside',
                textfont=dict(size=10, color=C['navy']),
            ))
            _base_layout(fig5, f'Total: {total}', height=340)
            fig5.update_layout(
                yaxis=dict(autorange=True, rangemode='tozero'),
                bargap=0.3,
            )
            fig5.update_xaxes(tickangle=-35)
            fig5.update_yaxes(title_text='# Intervenciones')
            st.plotly_chart(fig5, use_container_width=True)
        else:
            st.info("Sin datos de intervenciones por Pozo Tipo.")


# ──────────────────────────────────────────────
#  TAB 3 – GESTIÓN DE POZOS
# ──────────────────────────────────────────────
def render_tab_pozos(datos, escenario_active, texts):
    # ── Pestaña de Resumen y Comparación de Pozos Tipo ──
    st.markdown(f"### {texts['well_mgmt']}")

    # 1. Filtro Discreto de Escenarios (Popover)
    pop_title = "⚙️ Comparar Escenarios" if texts['metrica'] == 'Métrica' else "⚙️ Compare Scenarios"
    pop_label = "Seleccionar Escenarios" if texts['metrica'] == 'Métrica' else "Select Scenarios"

    # Prepare Scenario Options
    is_en = (texts['metrica'] != 'Métrica')
    trans_vals = TRANSLATIONS['English']['values']
    esc_opts = ["Caso Base", "Esc 1", "Esc 2"]
    if is_en:
        esc_opts = [trans_vals.get(e, e) for e in esc_opts]

    # Robust selection: detect language switch or empty state and reset session state manually
    if "pozos_esc_sel" not in st.session_state or not st.session_state["pozos_esc_sel"] or not all(e in esc_opts for e in st.session_state["pozos_esc_sel"]):
        st.session_state["pozos_esc_sel"] = esc_opts
        
    with st.popover(pop_title):
        esc_sel = st.multiselect(pop_label, esc_opts, key="pozos_esc_sel")

    if not esc_sel:
        st.warning("Seleccione al menos un escenario para visualizar las gráficas." if texts['metrica'] == 'Métrica' else "Select at least one scenario to view the charts.")
        return

    # 2. Recolección y Procesamiento de Datos
    all_p2 = []
    for esc in esc_sel:
        df = dp.get_pozos2_df(datos, esc)
        if not df.empty:
            df = df.copy()
            df['Escenario_Source'] = esc
            all_p2.append(df)

    if not all_p2:
        st.info("No hay datos de pozos disponibles para los escenarios seleccionados." if texts['metrica'] == 'Métrica' else "No well data available for selected scenarios.")
        return

    full_p2 = pd.concat(all_p2)
    col_pt = 'Well Type' if 'Well Type' in full_p2.columns else 'Pozo Tipo'
    pozo_tipos = sorted(full_p2[col_pt].dropna().unique())

    # Función auxiliar para formatear leyendas a la izquierda
    def _style_left_legend(fig, title):
        fig.update_layout(
            title=dict(text=title, font=dict(size=13, weight='bold'), x=0.05),
            height=340,
            margin=dict(l=150, r=20, t=50, b=40), # Espacio a la izquierda para la leyenda
            legend=dict(
                orientation='v',
                yanchor='middle', y=0.5,
                xanchor='right', x=-0.1, # Posición a la izquierda del gráfico
                font=dict(size=10)
            ),
            barmode='group',
            bargap=0.2,
            bargroupgap=0.1,
            hovermode='x unified',
            plot_bgcolor='rgba(0,0,0,0)',
        )
        fig.update_xaxes(showgrid=False, linecolor=C['grid'])
        fig.update_yaxes(showgrid=True, gridcolor=C['grid'], zeroline=False)
        return fig

    def _get_avg_metrics(df_full, var_cols):
        # Promedia las métricas por Pozo Tipo entre los escenarios seleccionados
        col_pt = 'Well Type' if 'Well Type' in df_full.columns else 'Pozo Tipo'
        sub = df_full[[col_pt] + var_cols].groupby(col_pt).mean().reindex(pozo_tipos).fillna(0)
        return sub

    # ── GRÁFICO 1: Cantidad de Actividad por Escenario ──
    fig_act = go.Figure()
    for esc in esc_sel:
        col_pt = 'Well Type' if 'Well Type' in full_p2.columns else 'Pozo Tipo'
        col_qty = 'Count'     if 'Count'     in full_p2.columns else 'Cantidad'
        sub = full_p2[full_p2['Escenario_Source'] == esc].set_index(col_pt).reindex(pozo_tipos).fillna(0)
        fig_act.add_trace(go.Bar(
            x=pozo_tipos, y=sub[col_qty], name=esc,
            # Handle translated scenario names for colors
            marker_color=_SCENARIO_COLORS.get(esc, _SCENARIO_COLORS.get(next((k for k, v in trans_vals.items() if v == esc), esc), C['blue2'])),
            text=sub[col_qty].astype(int).replace(0, ''),
            textposition='outside',
        ))
    _style_left_legend(fig_act, "Cantidad de Actividad por Escenario" if texts['metrica'] == 'Métrica' else "Activity Count per Scenario")
    st.plotly_chart(fig_act, use_container_width=True)

    # ── GRÁFICO 2: Pozos_Qo (bd) ──
    qo_vars = ['Qo_10', 'Qo Esperado (bd)', 'Qo_90']
    
    is_en_mode_b = (texts['metrica'] != 'Métrica')
    trans_headers = TRANSLATIONS['English']['headers']
    qo_vars_search = [trans_headers.get(v, v) if is_en_mode_b else v for v in qo_vars]
    
    avg_qo = _get_avg_metrics(full_p2, [v for v in qo_vars_search if v in full_p2.columns])
    fig_qo = go.Figure()
    colors_qo = [C['blue1'], C['blue2'], C['orange']]
    names_qo = [texts['val_p10'], texts['val_exp'], texts['val_p90']]
    for i, col in enumerate(avg_qo.columns):
        fig_qo.add_trace(go.Bar(
            x=pozo_tipos, y=avg_qo[col], name=names_qo[i],
            marker_color=colors_qo[i],
            text=avg_qo[col].round(0).replace(0, ''),
            textposition='outside',
        ))
    _style_left_legend(fig_qo, f"Pozos_Qo (bd)" if texts['metrica'] == 'Métrica' else f"Wells_Qo (bd)")
    st.plotly_chart(fig_qo, use_container_width=True)

    # ── GRÁFICO 3: Pozos_Qg (Mpcd) ──
    qg_vars = ['Qg_10', 'Qg Esperado (Mpcd)', 'Qg_90']
    
    qg_vars_search = [trans_headers.get(v, v) if is_en_mode_b else v for v in qg_vars]
    avg_qg = _get_avg_metrics(full_p2, [v for v in qg_vars_search if v in full_p2.columns])
    fig_qg = go.Figure()
    colors_qg = [C['navy'], C['blue1'], C['blue3']]
    names_qg = ['Qg_10', 'Qg_50', 'Qg_90']
    for i, col in enumerate(avg_qg.columns):
        fig_qg.add_trace(go.Bar(
            x=pozo_tipos, y=avg_qg[col], name=names_qg[i],
            marker_color=colors_qg[i],
            text=avg_qg[col].round(0).replace(0, ''),
            textposition='outside',
        ))
    _style_left_legend(fig_qg, f"Pozos_Qg (Mpcd)" if texts['metrica'] == 'Métrica' else f"Wells_Qg (Mscfd)")
    st.plotly_chart(fig_qg, use_container_width=True)

    # ── GRÁFICO 4: Pozos_Costo (MMUSD) ──
    cost_vars = ['Costo_Mín', 'Costo Más Probable (MMUSD)', 'Costo_Máx']
    avg_cost = _get_avg_metrics(full_p2, [v for v in cost_vars if v in full_p2.columns])
    fig_cost = go.Figure()
    colors_cost = ['#1A237E', '#3949AB', C['orange']]
    names_cost = ['Costo_Mín', 'Costo_MP', 'Costo_Máx']
    for i, col in enumerate(avg_cost.columns):
        fig_cost.add_trace(go.Bar(
            x=pozo_tipos, y=avg_cost[col], name=names_cost[i],
            marker_color=colors_cost[i],
            text=avg_cost[col].round(2).replace(0, ''),
            textposition='outside',
        ))
    _style_left_legend(fig_cost, f"Pozos_Costo (MMUSD)" if texts['metrica'] == 'Métrica' else f"Wells_Cost (MMUSD)")
    st.plotly_chart(fig_cost, use_container_width=True)

    # ── GRÁFICO 5: Pozos_Abandono (MMUSD) ──
    aban_vars = ['Abandono_Mín', 'Abandono_MP', 'Abandono_Máx']
    avg_aban = _get_avg_metrics(full_p2, [v for v in aban_vars if v in full_p2.columns])
    # Filtrar Pozo Tipos que tengan algún valor de abandono > 0
    pozo_tipos_aban = avg_aban[avg_aban.sum(axis=1) > 0].index.tolist()
    if pozo_tipos_aban:
        fig_aban = go.Figure()
        colors_aban = [C['orange'], C['blue3'], C['navy']]
        names_aban = ['Abandono_Mín', 'Abandono_MP', 'Abandono_Máx']
        for i, col in enumerate(avg_aban.columns):
            fig_aban.add_trace(go.Bar(
                x=pozo_tipos_aban, y=avg_aban.loc[pozo_tipos_aban, col], name=names_aban[i],
                marker_color=colors_aban[i],
                text=avg_aban.loc[pozo_tipos_aban, col].round(2).replace(0, ''),
                textposition='outside',
            ))
        _style_left_legend(fig_aban, f"Pozos_Abandono (MMUSD)" if texts['metrica'] == 'Métrica' else f"Wells_Abandonment (MMUSD)")
        st.plotly_chart(fig_aban, use_container_width=True)
    else:
        st.info("Sin datos de costos de abandono para graficar.")


# ──────────────────────────────────────────────
#  TAB 4 – ANÁLISIS CORNER
# ──────────────────────────────────────────────
def render_tab_corner(datos, escenario, texts):
    df = dp.get_corner_df(datos, escenario)

    st.markdown(f"### 🏁 {texts['corner_title']}")

    col_ind = 'Indicator' if 'Indicator' in df.columns else 'Indicador'
    col_act = 'Asset'     if 'Asset'     in df.columns else 'Activo'

    if df.empty:
        st.warning("Sin datos de Corner para el escenario seleccionado." if texts['metrica'] == 'Métrica' else "No Corner data for this scenario.")
        return

    # Columnas de valor: formato '$PRECIO/TASA%'
    val_cols = [c for c in df.columns if str(c).startswith('$')]

    if not val_cols:
        st.warning("No se encontraron columnas de sensibilidad ($X/Y%)." if texts['metrica'] == 'Métrica' else "No sensitivity columns ($X/Y%) found.")
        return

    # Selector de Indicador
    if col_ind in df.columns:
        indicadores = df[col_ind].dropna().unique().tolist()
        
        # Orden de prioridad para mostrar estos indicadores en la cima de la lista
        is_en = (texts['metrica'] != 'Métrica')
        pri_es = [
            "Valor presente neto 15 (Contratista)",
            "TIR Nominal Modificada (Contratista)",
            "VPN15/bpce (Contratista)"
        ]
        pri_en = [
            "Net Present Value 15 (Contractor)",
            "Modified Nominal IRR (Contractor)",
            "NPV15/boe (Contractor)"
        ]
        priority = pri_en if is_en else pri_es
        
        top_inds = [x for x in priority if x in indicadores]
        rest_inds = [x for x in indicadores if x not in priority]
        indicadores = top_inds + rest_inds

        # Find default indicator ("presente neto" or translated "net present")
        search_key = TRANSLATIONS['English']['keywords'].get('neto 15', 'neto 15') if is_en else 'presente neto'
        
        ind_sel = st.selectbox("Indicador" if texts['metrica'] == 'Métrica' else "Indicator", indicadores,
                               index=next((i for i,v in enumerate(indicadores)
                                           if search_key.lower() in str(v).lower()), 0))
        row = df[df[col_ind] == ind_sel]
    else:
        row = df
        ind_sel = "Indicador"

    if row.empty:
        st.info("Sin datos para este indicador." if texts['metrica'] == 'Métrica' else "No data for this indicator.")
        return

    # Parsear precio y tasa de los nombres de columna
    # Formato: '$40/12.50%' → precio=40, tasa=12.5
    parsed = []
    for c in val_cols:
        try:
            parts = c.replace('$','').replace('%','').split('/')
            price = float(parts[0])
            rate  = float(parts[1])
            val   = float(row.iloc[0][c])
            parsed.append({'Precio (USD/bl)': price, 'Tasa (%)': rate, 'Valor': val, 'col': c})
        except Exception:
            continue

    if not parsed:
        st.warning("No se pudieron parsear las columnas de sensibilidad." if texts['metrica'] == 'Métrica' else "Sensitivity columns could not be parsed.")
        return

    # ── Grid para las dos tablas lado a lado ──
    col1, col2 = st.columns(2)
    
    # Obtener los valores únicos de Activo
    activos = sorted(df[col_act].dropna().unique().tolist())
    
    for i, active_type in enumerate(activos):
        # Seleccionar la columna para mostrar (col1 o col2)
        target_col = col1 if i % 2 == 0 else col2
        
        with target_col:
            # Filtrar por Indicador y por el Activo específico
            sub_df = df[(df[col_ind] == ind_sel) & (df[col_act] == active_type)]
            
            if sub_df.empty:
                st.info(f"Sin datos para {active_type}" if texts['metrica'] == 'Métrica' else f"No data for {active_type}")
                continue

            # Parsear datos para el heatmap
            parsed_sub = []
            for c in val_cols:
                try:
                    parts = c.replace('$','').replace('%','').split('/')
                    price = float(parts[0])
                    rate  = float(parts[1])
                    val   = float(sub_df.iloc[0][c])
                    parsed_sub.append({'Precio': price, 'Tasa': rate, 'Valor': val})
                except Exception:
                    continue

            if not parsed_sub:
                continue

            # Crear el pivot para el gráfico
            piv_df = pd.DataFrame(parsed_sub)
            pivot  = piv_df.pivot(index='Precio', columns='Tasa', values='Valor').sort_index(ascending=False)

            # Título de la tabla
            st.markdown(f"<p style='font-size:14px; font-weight:800; color:{C['navy']}; margin:10px 0 0 0; border-bottom: 2px solid {C['blue2']}; width: fit-content;'>{active_type}</p>", unsafe_allow_html=True)
            
            # Generar Tabla HTML
            # -----------------
            # 1. Cabecera (Esquina + Tasas)
            html = '<table class="corner-table">'
            html += '<tr class="header-row">'
            html += '<th class="corner-label" style="line-height:1.2;">Precio<br>(USD/b)</th>'
            for c in pivot.columns:
                html += f'<th>{c:.1f}</th>'
            html += '</tr>'
            
            # 2. Filas (Precio + Valores)
            max_val = pivot.max().max()
            min_val = pivot.min().min()
            
            for pr, row_vals in pivot.iterrows():
                html += '<tr>'
                html += f'<td class="price-col">{pr:.0f}</td>'
                for val in row_vals:
                    # Normalizar para el color (Blues)
                    norm = (val - min_val) / (max_val - min_val) if max_val > min_val else 0.5
                    alpha = 0.05 + (norm * 0.8) # Entre 5% y 85% de intensidad
                    bg_color = f"rgba(11, 36, 64, {alpha})"
                    txt_color = "#FFFFFF" if alpha > 0.5 else "#101828"
                    
                    html += f'<td style="background-color: {bg_color}; color: {txt_color};" class="cell-val">{val:.2f}</td>'
                html += '</tr>'
            html += '</table>'
            
            st.markdown(html, unsafe_allow_html=True)



# ──────────────────────────────────────────────
#  TAB 5 – COMPARACIÓN DE ESCENARIOS
# ──────────────────────────────────────────────
def render_tab_comparacion(datos, texts):
    all_mpp = dp.get_all_mpp(datos)
    if all_mpp.empty:
        st.info("Sin datos para comparar." if texts['metrica'] == 'Métrica' else "No data to compare.")
        return

    # Scenario options and multi-select (all by default)
    col_esc = 'Scenario' if 'Scenario' in all_mpp.columns else 'Escenario'
    esc_opts = sorted(all_mpp[col_esc].unique().tolist())
    
    # ── Header & Global Controls ──────────────────────────────
    st.markdown(f"#### 📊 {texts['comp_scen']}")
    
    # Date baseline
    ts_cols = [c for c in all_mpp.columns if str(c).startswith('2')]
    dates_all = pd.to_datetime(ts_cols, errors='coerce')
    valid_dates = dates_all.dropna()
    d_min, d_max = valid_dates.min().to_pydatetime(), valid_dates.max().to_pydatetime()
    
    # Robust selection: detect language switch or empty state and reset session state manually
    # MOVE OUTSIDE POPOVER to ensure it runs even if popover remains closed
    if "comp_esc_sel" not in st.session_state or not st.session_state["comp_esc_sel"] or not all(e in esc_opts for e in st.session_state["comp_esc_sel"]):
        st.session_state["comp_esc_sel"] = esc_opts
        
    # Top Control Bar
    ctrl_a, ctrl_b, ctrl_c = st.columns([3, 1.5, 4.5])
    with ctrl_a:
        pop_esc = "⚙️ Escenarios" if texts['metrica'] == 'Métrica' else "⚙️ Scenarios"
        with st.popover(pop_esc, use_container_width=True):
            sel_label = "Seleccionar Escenarios" if texts['metrica'] == 'Métrica' else "Select Scenarios"
            esc_sel = st.multiselect(sel_label, esc_opts, key="comp_esc_sel")
    
    with ctrl_b:
        fluido = st.radio("Fluido" if texts['metrica'] == 'Métrica' else "Fluid", [texts['oil'], texts['gas']], horizontal=True, key="comp_flu_sel")
        internal_fluido = "Aceite" if fluido == texts['oil'] else "Gas"

    with ctrl_c:
        st.markdown(f"<p style='font-size:10px;color:{C['muted']};font-weight:700;text-transform:uppercase;margin-bottom:0'>{texts['rango_fechas'] if 'rango_fechas' in texts else 'Rango de Fechas'}</p>", unsafe_allow_html=True)
        fecha_inicio, fecha_fin = st.slider(
            "range_comp",
            min_value=d_min, max_value=d_max, value=(d_min, d_max),
            format="DD/MM/YYYY", label_visibility="collapsed", key="comp_date_slider"
        )

    if not esc_sel:
        st.warning("Seleccione al menos un escenario." if texts['metrica'] == 'Métrica' else "Please select at least one scenario.")
        return

    # Filter variables by fluid for production
    if internal_fluido == "Aceite":
        var_d, var_a = "Qo", "NP"
        title_d = f"{texts['daily']} {texts['oil']}"
        title_a = f"{texts['accum']} {texts['oil']}"
        u_d, u_a = "bd", "MMb"
    else:
        var_d, var_a = "Qg", "GP"
        title_d = f"{texts['daily']} {texts['gas']}"
        title_a = f"{texts['accum']} {texts['gas']}"
        u_d, u_a = "Mpcd", "MMpc"

    ts_f = [ts_cols[i] for i, d in enumerate(dates_all) if pd.Timestamp(fecha_inicio) <= d <= pd.Timestamp(fecha_fin)]
    dates_f = dates_all[(dates_all >= pd.Timestamp(fecha_inicio)) & (dates_all <= pd.Timestamp(fecha_fin))]
    current_mpp = all_mpp[all_mpp[col_esc].isin(esc_sel)]

    # --- 2x2 Grid Layout ---
    row1_l, row1_r = st.columns(2)
    row2_l, row2_r = st.columns(2)

    # Translate internal search variables if in English
    trans_vals = TRANSLATIONS['English']['values']
    is_en_mode = (texts['metrica'] != 'Métrica')
    search_vd = trans_vals.get(var_d, var_d) if is_en_mode else var_d
    search_va = trans_vals.get(var_a, var_a) if is_en_mode else var_a

    # 1. TOP LEFT: Daily Production
    with row1_l:
        fig_d = go.Figure()
        col_cat = 'Category' if 'Category' in current_mpp.columns else 'Categoría'
        is_en = (col_cat == 'Category')
        target_cat = 'Mean' if is_en else 'Media'

        for esc in esc_sel:
            sub = current_mpp[current_mpp[col_esc] == esc]
            row = sub[(sub['Variable'] == search_vd) & (sub[col_cat] == target_cat)]
            
            if not row.empty:
                y = pd.to_numeric(row.iloc[0][ts_f], errors='coerce').fillna(0).values
                c_color = _SCENARIO_COLORS.get(esc, _SCENARIO_COLORS.get(next((k for k, v in trans_vals.items() if v == esc), esc), C['navy']))
                fig_d.add_trace(go.Scatter(x=dates_f, y=y, name=esc, line=dict(color=c_color, width=2)))
        _base_layout(fig_d, title_d, height=320)
        fig_d.update_xaxes(title_text='Fecha' if texts['metrica'] == 'Métrica' else 'Date')
        fig_d.update_yaxes(title_text=u_d)
        st.plotly_chart(fig_d, use_container_width=True)

    # 2. TOP RIGHT: Accumulated Production
    with row1_r:
        fig_a = go.Figure()
        for esc in esc_sel:
            sub = current_mpp[current_mpp[col_esc] == esc]
            row = sub[(sub['Variable'] == search_va) & (sub[col_cat] == target_cat)]
            if not row.empty:
                y = pd.to_numeric(row.iloc[0][ts_f], errors='coerce').fillna(0).values
                c_color = _SCENARIO_COLORS.get(esc, _SCENARIO_COLORS.get(next((k for k, v in trans_vals.items() if v == esc), esc), C['navy']))
                fig_a.add_trace(go.Scatter(x=dates_f, y=y, name=esc, line=dict(color=c_color, width=2)))
        _base_layout(fig_a, title_a, height=320)
        fig_a.update_xaxes(title_text='Fecha' if texts['metrica'] == 'Métrica' else 'Date')
        fig_a.update_yaxes(title_text=u_a)
        st.plotly_chart(fig_a, use_container_width=True)

    # 3. BOTTOM LEFT: Annualized CAPEX
    with row2_l:
        pop_label = "Categorías CAPEX" if texts['metrica'] == 'Métrica' else "CAPEX Categories"
        capex_all = sorted([v for v in current_mpp['Variable'].unique() if 'CAPEX' in str(v).upper()])
        
        # Robust selection: if options changed due to lang toggle, reset
        if "comp_capex_sel" not in st.session_state or not st.session_state["comp_capex_sel"] or not all(e in capex_all for e in st.session_state["comp_capex_sel"]):
            st.session_state["comp_capex_sel"] = capex_all
            
        with st.popover(pop_label, use_container_width=True):
            capex_sel = st.multiselect("Filtrar" if texts['metrica'] == 'Métrica' else "Filter", capex_all, key="comp_capex_sel")
        
        fig4 = go.Figure()
        for esc in esc_sel:
            sub = current_mpp[current_mpp[col_esc] == esc]
            rows = sub[sub['Variable'].isin(capex_sel) & (sub[col_cat] == target_cat)]
            if not rows.empty:
                y_annual = rows[ts_f].astype(float).sum().groupby(dates_f.year).sum()
                c_color = _SCENARIO_COLORS.get(esc, _SCENARIO_COLORS.get(next((k for k, v in trans_vals.items() if v == esc), esc), C['navy']))
                fig4.add_trace(go.Bar(x=y_annual.index, y=y_annual.values, name=esc, marker_color=c_color))
        _base_layout(fig4, 'CAPEX Anual' if texts['metrica'] == 'Métrica' else 'Annual CAPEX', height=320)
        fig4.update_yaxes(title_text='MMUSD')
        fig4.update_layout(barmode='group')
        st.plotly_chart(fig4, use_container_width=True)

    # 4. BOTTOM RIGHT: Annualized OPEX
    with row2_r:
        pop_label = "Categorías OPEX" if texts['metrica'] == 'Métrica' else "OPEX Categories"
        opex_all = sorted([v for v in current_mpp['Variable'].unique() if 'OPEX' in str(v).upper()])
        
        # Robust selection: if options changed due to lang toggle, reset
        if "comp_opex_sel" not in st.session_state or not st.session_state["comp_opex_sel"] or not all(e in opex_all for e in st.session_state["comp_opex_sel"]):
            st.session_state["comp_opex_sel"] = opex_all
            
        with st.popover(pop_label, use_container_width=True):
            opex_sel = st.multiselect("Filtrar" if texts['metrica'] == 'Métrica' else "Filter", opex_all, key="comp_opex_sel")
        
        fig5 = go.Figure()
        for esc in esc_sel:
            sub = current_mpp[current_mpp[col_esc] == esc]
            rows = sub[sub['Variable'].isin(opex_sel) & (sub[col_cat] == target_cat)]
            if not rows.empty:
                y_annual = rows[ts_f].astype(float).sum().groupby(dates_f.year).sum()
                c_color = _SCENARIO_COLORS.get(esc, _SCENARIO_COLORS.get(next((k for k, v in trans_vals.items() if v == esc), esc), C['navy']))
                fig5.add_trace(go.Bar(x=y_annual.index, y=y_annual.values, name=esc, marker_color=c_color))
        _base_layout(fig5, 'OPEX Anual' if texts['metrica'] == 'Métrica' else 'Annual OPEX', height=320)
        fig5.update_layout(barmode='group')
        fig5.update_yaxes(title_text='MMUSD')
        st.plotly_chart(fig5, use_container_width=True)



def render_tab_kpi_intervenciones(datos, texts, lang):
    is_en = (lang == 'English')
    
    # Textos locales
    t_num_int = "No de Intervenciones" if not is_en else "Number of Interventions"
    t_part = "Porcentaje de Participación" if not is_en else "Participation Percentage"
    t_price = "Precio del Barril" if not is_en else "Barrel Price"
    t_kpi_title = "KPI, Intervenciones y Np" if not is_en else "KPI, Interventions, and Np"
    t_bubble_desc = "<b>Valor</b> = No Intervenciones, <b>Media</b> = KPI Promedio, <b>Máx Acumulado</b> = Np" if not is_en else "<b>Value</b> = Number of Interventions, <b>Mean</b> = Average KPI, <b>Max Cumulative</b> = Np"
    t_ind_boe_36 = "Indicadores por Barril (36 USD/boe)" if not is_en else "Indicators per Barrel (36 USD/boe)"
    t_ind_boe_50 = "Indicadores por Barril (50 USD/boe)" if not is_en else "Indicators per Barrel (50 USD/boe)"
    t_total = "Total" if not is_en else "Total"
    
    pbi3 = datos.get('pbi3', pd.DataFrame())
    pozos2 = datos.get('pozos2', pd.DataFrame())
    mpp = datos.get('mpp', pd.DataFrame())
    desc_df = datos.get('escenarios', pd.DataFrame())
    
    if pbi3.empty or pozos2.empty or mpp.empty:
        st.warning("Faltan datos necesarios para mostrar esta pestaña.")
        return

    col_esc_pbi3 = 'Scenario' if 'Scenario' in pbi3.columns else 'Escenario'
    escs_available = pbi3[col_esc_pbi3].dropna().unique().tolist()
    
    col_ind = 'Indicator' if 'Indicator' in pbi3.columns else 'Indicador'
    kpis_all = sorted(pbi3[col_ind].dropna().unique().tolist())
    
    col_act = 'Asset' if 'Asset' in pbi3.columns else 'Activo'
    activos_all = pbi3[col_act].dropna().unique().tolist()
    
    col_grp = 'Grouping' if 'Grouping' in pbi3.columns else 'Agrupación'
    precios_all = sorted(pbi3[col_grp].dropna().unique().tolist())
    
    col_f, col_g = st.columns([1, 3])
    
    with col_f:
        # Fila 1: Participación y Precio
        f_c1, f_c2 = st.columns(2)
        with f_c1:
            st.markdown(f"<p style='font-size:12px;font-weight:600;color:{C['navy']}'>{t_part}</p>", unsafe_allow_html=True)
            sel_activo = st.radio("Participación", options=activos_all, index=0, label_visibility="collapsed", key="kpi_act_radio")
        with f_c2:
            st.markdown(f"<p style='font-size:12px;font-weight:600;color:{C['navy']}'>{t_price}</p>", unsafe_allow_html=True)
            sel_precio = st.radio("Precio", options=precios_all, index=0, label_visibility="collapsed", key="kpi_price_radio")
        
        st.markdown(f"<div style='margin-top:20px'></div>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size:12px;font-weight:600;color:{C['navy']}'>KPI</p>", unsafe_allow_html=True)
        sel_kpi = st.selectbox("KPI a graficar", options=kpis_all, index=1 if len(kpis_all) > 1 else 0, label_visibility="collapsed")
        
    with col_g:
        col_esc_p2 = 'Scenario' if 'Scenario' in pozos2.columns else 'Escenario'
        col_cant_p2 = next((c for c in ['Cantidad', 'Quantity', 'Count'] if c in pozos2.columns), None)
        if col_cant_p2 and col_esc_p2 in pozos2.columns:
            intervenciones = pozos2.groupby(col_esc_p2)[col_cant_p2].sum().to_dict()
        else:
            intervenciones = {}
            
        col_esc_mpp = 'Scenario' if 'Scenario' in mpp.columns else 'Escenario'
        col_var_mpp = 'Variable' if 'Variable' in mpp.columns else 'Variable'
        col_cat_mpp = 'Category' if 'Category' in mpp.columns else 'Categoría'
        
        np_sizes = {}
        for esc in escs_available:
            sub_mpp = mpp[(mpp[col_esc_mpp] == esc) & (mpp[col_var_mpp] == 'Np') & (mpp[col_cat_mpp].isin(['Media', 'P50', 'Mean', 'Expected']))]
            val = 0
            if not sub_mpp.empty:
                numeric_vals = pd.to_numeric(sub_mpp.iloc[0], errors='coerce').dropna()
                val = numeric_vals.max() if not numeric_vals.empty else 100
            np_sizes[esc] = val if val > 0 else 100

        col_val_pbi3 = 'Mean' if 'Mean' in pbi3.columns else 'Media'
        kpi_y = {}
        for esc in escs_available:
            # Filtrar por Escenario, Activo (Participación), KPI Y PRECIO
            sub_pbi = pbi3[(pbi3[col_esc_pbi3] == esc) & (pbi3[col_act] == sel_activo) & (pbi3[col_ind] == sel_kpi) & (pbi3[col_grp] == sel_precio)]
            val = sub_pbi[col_val_pbi3].mean() if not sub_pbi.empty else 0
            kpi_y[esc] = val

        fig_scatter = go.Figure()
        for esc in escs_available:
            c_color = _SCENARIO_COLORS.get(esc, _SCENARIO_COLORS.get(next((k for k, v in TRANSLATIONS.get('English', {}).get('values', {}).items() if v == esc), esc), C['navy']))
            fig_scatter.add_trace(go.Scatter(
                x=[intervenciones.get(esc, 0)], y=[kpi_y.get(esc, 0)],
                mode='markers+text', name=esc, text=[esc],
                textposition="top center",
                marker=dict(
                    size=[np_sizes.get(esc, 100)], sizemode='area',
                    sizeref=2.*max(list(np_sizes.values()) + [1])/(40.**2),
                    sizemin=4, color=c_color
                )
            ))
            
        _base_layout(fig_scatter, t_kpi_title, height=350)
        fig_scatter.update_xaxes(title_text=t_num_int)
        fig_scatter.update_yaxes(title_text='Indicador_Media')
        
        fig_scatter.add_annotation(
            text=t_bubble_desc, xref="paper", yref="paper",
            x=1.0, y=1.0, showarrow=False,
            font=dict(size=9, color=C['muted']), align="right"
        )
            
        st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
    
    sel_esc = st.radio("Escenario Inferior", options=escs_available, horizontal=True, label_visibility="collapsed")
    
    st.markdown("<div style='margin-top:15px'></div>", unsafe_allow_html=True)
    col_desc, col_w1, col_w2 = st.columns([1.5, 2.25, 2.25])
    
    with col_desc:
        desc_text = "Detailed assessment for " + sel_esc
        if is_en:
            fallback_descs = {
                "Base Case": "Approved development plan considering: 211 activities and the purchase of 3 compressors.",
                "Scenario 1": "Considers 304 activities, 50 new wells starting drilling in 2025, and the purchase of 2 compressors.",
                "Scenario 2": "Considers 397 activities, 100 new wells starting drilling in 2025, and the purchase of 3 compressors."
            }
            en_descs = TRANSLATIONS.get("English", {}).get("descriptions", fallback_descs)
            desc_text = en_descs.get(sel_esc.strip(), fallback_descs.get(sel_esc.strip(), "Detailed assessment for " + sel_esc))
        else:
            col_desc_df = 'Description' if 'Description' in desc_df.columns else 'Descripcion'
            col_esc_df = 'Scenario' if 'Scenario' in desc_df.columns else 'Escenario'
            if col_esc_df in desc_df.columns and col_desc_df in desc_df.columns:
                row_desc = desc_df[desc_df[col_esc_df] == sel_esc]
                if not row_desc.empty:
                    desc_text = row_desc.iloc[0][col_desc_df]
                    
        st.markdown(f"""
            <div style='background-color:#F7F9FC; border:1px solid #D0D7DE; padding:15px; border-radius:6px; height:100%; display:flex; align-items:center; justify-content:center; box-shadow: 2px 2px 5px rgba(0,0,0,0.05);'>
                <p style='font-size:12px; color:#24292F; text-align:center; margin:0;'>{desc_text}</p>
            </div>
        """, unsafe_allow_html=True)

    def draw_waterfall(agrupacion_precio, title):
        sub = pbi3[(pbi3[col_esc_pbi3] == sel_esc) & (pbi3[col_act] == sel_activo) & (pbi3['Grouping' if is_en else 'Agrupación'] == agrupacion_precio)]
        
        waterfall_inds = {
            "Take PDVSA/bpce (Contratista)": "PDVSA Take/boe<br>(Contractor)",
            "Regalías (Contratista)": "Royalties<br>(Contractor)",
            "Opex/bpce (Contratista)": "OPEX/boe<br>(Contractor)",
            "Capex/bpce (Contratista)": "CAPEX/boe<br>(Contractor)",
            "Ganancia/bpce (Contratista)": "Profit/boe<br>(Contractor)",
            "ISLR/bpce (Contratista)": "Income Tax/boe<br>(Contractor)"
        }
        
        search_inds = {}
        for k, v in waterfall_inds.items():
            mapped_k = TRANSLATIONS.get('English', {}).get('values', {}).get(k, k) if is_en else k
            display_name = v if is_en else k.replace(' (', '<br>(')
            search_inds[mapped_k] = display_name
            
        data_points = []
        for ind_key, display_name in search_inds.items():
            row = sub[sub[col_ind] == ind_key]
            if not row.empty:
                val = row.iloc[0][col_val_pbi3]
                data_points.append({'name': display_name, 'value': float(val)})
                
        data_points.sort(key=lambda x: x['value'], reverse=True)
        
        x_vals = [d['name'] for d in data_points] + [t_total]
        y_vals = [d['value'] for d in data_points] + [sum(d['value'] for d in data_points)]
        measure_vals = ["relative"] * len(data_points) + ["total"]
        
        fig = go.Figure(go.Waterfall(
            name="20", orientation="v", measure=measure_vals,
            x=x_vals, textposition="outside", text=[f"{v:.2f}" for v in y_vals], y=y_vals,
            connector={"line":{"color":"rgb(63, 63, 63)"}},
            decreasing={"marker":{"color": C['orange']}},
            increasing={"marker":{"color": "#E5A024"}}, 
            totals={"marker":{"color": C['navy']}},    
        ))
        
        _base_layout(fig, title, height=220)
        fig.update_layout(margin=dict(l=10, r=10, t=30, b=40), showlegend=False, waterfallgap=0.3)
        fig.update_xaxes(tickfont=dict(size=8), tickangle=0)
        return fig

    with col_w1:
        fig_w1 = draw_waterfall('36 USD/bl', t_ind_boe_36)
        st.plotly_chart(fig_w1, use_container_width=True)
        
    with col_w2:
        fig_w2 = draw_waterfall('50 USD/bl', t_ind_boe_50)
        st.plotly_chart(fig_w2, use_container_width=True)


# ──────────────────────────────────────────────
#  MAIN RENDER (orchestrator with Tabs)
# ──────────────────────────────────────────────
def render_dashboard(datos, escenario, texts):
    lang = 'Español' if texts.get('metrica') == 'Métrica' else 'English'
    tabs = st.tabs(texts['tabs'])

    with tabs[0]:
        try:
            render_tab_produccion(datos, escenario, texts)
        except Exception as e:
            st.error(f"Error en Producción: {e}")

    with tabs[1]:
        try:
            render_tab_valoracion(datos, escenario, texts)
        except Exception as e:
            st.error(f"Error en Valoración: {e}")

    with tabs[2]:
        try:
            render_tab_comparacion(datos, texts)
        except Exception as e:
            st.error(f"Error en Comparación: {e}")

    with tabs[3]:
        try:
            render_tab_pozos(datos, escenario, texts)
        except Exception as e:
            st.error(f"Error en Pozos: {e}")

    with tabs[4]:
        try:
            render_tab_kpi_intervenciones(datos, texts, lang)
        except Exception as e:
            st.error(f"Error en KPI vs Intervenciones: {e}")

    with tabs[5]:
        try:
            render_tab_corner(datos, escenario, texts)
        except Exception as e:
            st.error(f"Error en Corner: {e}")
