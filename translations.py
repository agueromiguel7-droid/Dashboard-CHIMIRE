
# translations.py – CHIMIRE Dashboard Internationalization Mapping

TRANSLATIONS = {
    "English": {
        "headers": {
            "Activo": "Asset",
            "Activo ": "Asset",
            "Region Fiscal": "Fiscal Region",
            "Region Fiscal ": "Fiscal Region",
            "Escenario": "Scenario",
            "Forma": "Form",
            "Año de evaluación": "Eval Year",
            "Tipo de Contrato": "Contract Type",
            "Agrupación": "Grouping",
            "Campo": "Field",
            "Análisis": "Analysis",
            "Assumptions": "Assumptions",
            "Contribución a la Varianza": "Variance Contribution",
            "Indicador": "Indicator",
            "Indicador ": "Indicator",
            "Unidad": "Unit",
            "Media": "Mean",
            "SD": "StdDev",
            "Tamaño muestra": "Sample Size",
            "Prob VPN<0": "Prob NPV<0",
            "Variable": "Variable",
            "Categoría": "Category",
            "Suma Total": "Total",
            "Pozo Tipo": "Well Type",
            "Cantidad": "Count",
            "Costo_MP": "Cost (MP)",
            "Qo_50": "Qo Mean",
            "Qg_50": "Qg Mean",
            "Descripción Escenario": "Scenario Description",
            "Información": "Information",
            "Valor": "Value",
            "Qo_10": "Qo P10",
            "Qo Esperado (bd)": "Qo Mean (bd)",
            "Qo_90": "Qo P90",
            "Qg_10": "Qg P10",
            "Qg Esperado (Mpcd)": "Qg Mean (Mpcd)",
            "Qg_90": "Qg P90"
        },
        "values": {
            # Scenarios
            "Caso Base": "Base Case",
            "Esc 1": "Scenario 1",
            "Esc 2": "Scenario 2",
            "VPN": "NPV",
            "VPI": "PVI",
            "TIR": "IRR",
            
            # Categories
            "Media": "Mean",
            "P10": "P10",
            "P50": "P50",
            "P90": "P90",
            "Mínimo": "Minimum",
            "Máximo": "Maximum",
            
            # Assets & Regions
            "PDVSA 70% - Contratista 30%": "PDVSA 70% - Contractor 30%",
            "PDVSA 30% - Contratista 70%": "PDVSA 30% - Contractor 70%",
            "Aceite - Terrestre": "Oil - Onshore",
            "Asignación": "Assignment",
            
            # Indicators (PBI 3)
            "Crudo Equivalente": "Oil Equivalent",
            "Praticipación (PDVSA)": "PDVSA Share",
            "Participación (Contratista)": "Contractor Share",
            "Flujo de efectivo libre (Activo)": "Free Cash Flow (Asset)",
            "Flujo de efectivo libre (Estado)": "Free Cash Flow (State)",
            "Flujo de efectivo libre (PDVA)": "Free Cash Flow (PDVSA)",
            "Flujo de efectivo libre (Contratista)": "Free Cash Flow (Contractor)",
            "Valor presente neto 15 (Contratista)": "Net Present Value 15 (Contractor)",
            "Valor presente de la inversión (Contratista)": "Investment Present Value (Contractor)",
            "Valor presente de los costos (Contratista)": "Costs Present Value (Contractor)",
            "Valor presente de inversión y costos (Contratista)": "Total Costs Present Value (Contractor)",
            "Eficiencia de la inversión (Contratista)": "Investment Efficiency (Contractor)",
            "Relación beneficio costo (Contratista)": "Benefit Cost Ratio (Contractor)",
            "TIR Nominal Anualizada (Contratista)": "Nominal Annualized IRR (Contractor)",
            "TIR Nominal Flujo Anual (Contratista)": "Nominal Annual Flow IRR (Contractor)",
            "TIR Nominal Modificada (Contratista)": "Modified Nominal IRR (Contractor)",
            "Periodo de Recuperación (Contratista)": "Payback Period (Contractor)",
            "Máximo requerimiento de financiamiento (Contratista)": "Max Financing Requirement (Contractor)",
            "Precio bruto (Contratista)": "Gross Price (Contractor)",
            "Regalías (Contratista)": "Royalties (Contractor)",
            "Capex/bpce (Contratista)": "Capex/boe (Contractor)",
            "Opex/bpce (Contratista)": "Opex/boe (Contractor)",
            "ISLR/bpce (Contratista)": "Income Tax/boe (Contractor)",
            "Take PDVSA/bpce (Contratista)": "PDVSA Take/boe (Contractor)",
            "Ganancia/bpce (Contratista)": "Profit/boe (Contractor)",
            "VPN15/bpce (Contratista)": "NPV15/boe (Contractor)",
            
            # Variables (PBI MPP)
            "CAPEX Infraestructura": "Infrastructure CAPEX",
            "CAPEX Pozo+Desarrollo": "Well+Development CAPEX",
            "CAPEX Abandono Pozos": "Well Abandonment CAPEX",
            "OPEX Abandono Pozos": "Well Abandonment OPEX",
            "OPEX Abandono Infraestructura": "Infra Abandonment OPEX",
            "OPEX RMA": "RMA OPEX",
            "OPEX RME": "RME OPEX",
            "OPEX Variable": "Variable OPEX",
            "OPEX Fijo": "Fixed OPEX",
            "OPEX mano de obra": "Labor OPEX",
            "Qo": "Oil Prod",
            "Qg": "Gas Prod",
            "NP": "Cum Oil",
            "GP": "Cum Gas",
            
            # Variables (Pozos (2))
            "Reactivación": "Reactivation",
            "Limpieza y Estimulación": "Cleansing and Stimulation",
            "Cambio de Zona": "Change of Zone",
            "RaRc": "Workover-Well Service",
            "Sensillo Selectivo Baja Productividad": "Selective Sensor Low Productivity",
            "Sencillo Selectivo Media Productividad": "Simple Selective Medium Productivity",
            "Sensillo Selectivo Alta Productividad": "High Productivity Selective Sensor",
            "Comingle Baja Productividad": "Comingle Low Productivity",
            "Comingle Media Productividad": "Comingle Media Productivity",
            "Comingle Alta Productividad": "Comingle High Productivity",

            # Well Types
            "Pozo Vertical": "Vertical Well",
            "Pozo Horizontal": "Horizontal Well",
            "Pozo Inyector": "Injector Well",
            
            # Misc
            "Analista": "Analyst",
            "nan": "N/A"
        },
        "keywords": {
            # Search keywords used in code for lookups
            "neto 15": "net present value 15",
            "inversión": "investment",
            "costos": "costs",
            "Recuperación": "Payback",
            "Eficiencia": "Efficiency",
            "beneficio": "benefit",
            "Aceite": "Oil",
            "Gas": "Gas"
        }
    }
}
