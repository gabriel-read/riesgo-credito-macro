"""Pure presentation adapters for approved CSVs; never estimate or change sources."""

import csv
import hashlib
import io
import re

from src.tables import fmt_es


LABELS = {
    "series": "Serie", "download_date": "Fecha de descarga", "source": "Fuente", "file": "Archivo",
    "n_rows": "Filas", "first_obs": "Primera observación", "last_obs": "Última observación",
    "clave": "Clave", "estudio": "Estudio", "dependiente": "Dependiente", "regresores": "Regresores",
    "metodo": "Método", "signo": "Signo y contexto", "seccion_principal": "Sección",
    "": "Índice CSV", "variable": "Variable", "termino": "Término", "etiqueta": "Etiqueta",
    "coef": "Coef.", "ee_hac": "EE HAC", "z": "z", "p": "p",
    "ic_inf": "IC inf.", "ic_sup": "IC sup.", "signo_esperado": "Signo previsto",
    "coincide": "Coincide", "nota": "Nota", "decision": "Decisión", "referencia": "Referencia",
    "motivo": "Motivo", "prueba": "Prueba", "estadístico": "Estadístico",
    "estadistico": "Estadístico", "p_valor": "p", "veredicto": "Veredicto",
    "efecto": "Efecto", "escala": "Escala", "de": "DE", "estimacion": "Estimación",
    "ee": "EE", "estado": "Estado", "unidad": "Unidad", "limitacion": "Limitación",
    "detalle": "Detalle", "origen": "Origen", "pronostico": "Pronóstico",
    "n_trimestres": "Trimestres", "rmse_modelo": "RMSE modelo", "rmse_ingenuo": "RMSE ingenuo",
    "mae_modelo": "MAE modelo", "mae_ingenuo": "MAE ingenuo", "cociente_rmse": "Razón RMSE",
    "dm_estadistico": "Estad. DM", "dm_p": "p DM", "significancia": "Significancia",
    "variante": "Variante", "dependiente": "Dependiente", "forma_y": "Forma de Y",
    "terminos_diferencia": "Diferencias", "inicio": "Inicio", "fin": "Fin", "n_obs": "Obs.",
    "rezagos_hac": "Rezagos HAC", "k": "k", "n": "n", "robustez": "Robustez",
    "columna_panel": "Columna panel", "forma": "Forma", "adf_stat": "Estad. ADF",
    "adf_p": "p ADF", "kpss_stat": "Estad. KPSS", "kpss_p": "p KPSS",
    "orden": "Orden", "no_i0": "No I(0)", "h": "h", "R": "R", "beta": "β",
    "phi": "φ", "mismo_signo": "Mismo signo", "banda_excluye_cero": "Banda sin cero",
    "descripcion": "Descripción", "est": "Estimación", "chi2": "χ²", "h1_signo": "Signo H1",
    "h1_respaldada": "Respalda H1", "modelo": "Modelo", "muestra": "Muestra", "controles": "Controles",
    "ic90_inf": "IC90 inf.", "ic90_sup": "IC90 sup.", "phi_ee": "EE φ",
    "phi_ic90_inf": "IC90 φ inf.", "phi_ic90_sup": "IC90 φ sup.", "phi_nota": "Nota φ",
    "elemento": "Elemento", "gl": "GL", "resultado": "Resultado", "K": "K",
    "S": "S", "ee_S": "EE S", "p_S": "p S", "S_rez": "S rez.", "ee_S_rez": "EE S rez.",
    "p_S_rez": "p S rez.", "h_estrella": "h estrella", "h1": "H1", "p_principal": "p principal",
    "n_params": "Parámetros", "nobs": "Obs.", "aic": "AIC", "bic": "BIC", "marca": "Marca",
    "psi": "ψ", "media": "Media", "desv_est": "DE", "min": "Mín.", "mediana": "Mediana",
    "max": "Máx.", "adf_lags": "Rezagos ADF", "kpss_p_truncado": "p KPSS acotado",
    "escenario": "Escenario", "trimestre": "Trimestre", "delta": "Δ", "p05": "P05",
    "p95": "P95", "prop_pos": "Prop. positiva", "delta_final": "Δ final", "delta_pico": "Δ pico",
    "pico_trimestre": "Trimestre pico", "delta_min": "Δ mín.", "sin_aumento": "Sin aumento",
    "prop_pos_final": "Prop. final +", "prop_pos_pico": "Prop. pico +", "nivel_pico": "Nivel pico",
    "nivel_pico_trimestre": "Trimestre nivel pico", "dr": "Morosidad",
    "n_fuera_rango": "N fuera rango", "prop_fuera_rango": "Prop. fuera rango",
    "n_explosivas": "N explosivas", "prop_explosivas": "Prop. explosivas",
    "n_trimestres_fuera": "Trimestres fuera", "n_replicas_fuera_rango": "Réplicas fuera",
    "prop_replicas_fuera_rango": "Prop. réplicas fuera", "nivel_min": "Nivel mín.",
    "nivel_max": "Nivel máx.", "prop_trimestres_fuera": "Prop. trimestres fuera",
    "n_replicas_fuera_rango_modelo": "Réplicas fuera / modelo",
    "prop_replicas_fuera_rango_modelo": "Prop. fuera / modelo",
    "nivel_min_modelo": "Nivel mín. / modelo", "nivel_max_modelo": "Nivel máx. / modelo",
    "tipo": "Tipo", "delta_modelo1": "Δ Modelo I", "delta_modelo2": "Δ Modelo II",
    "diferencia_I_II": "Diferencia I−II", "trimestre_adaptado": "Trim. adaptado",
    "trimestre_original": "Trim. original", "dr_adaptado": "Nivel adaptado",
    "dr_original": "Nivel original", "delta_adaptado": "Δ adaptado", "delta_original": "Δ original",
    "DR_observado": "Nivel observado", "trimestre_fed": "Trimestre Fed", "PIB": "PIB",
    "ΔU": "ΔU", "π": "Inflación", "ΔFFR": "ΔFFR", "CRED": "Crédito",
    "credito_observado": "Crédito observado", "U_implicito": "U implícito",
    "tasa_proxy_implicita": "Tasa implícita", "tasa_proxy_negativa": "Tasa negativa",
    "c": "Cambio", "c_final": "Cambio final", "c_final_p05": "P05 final",
    "c_final_p95": "P95 final", "c_pico": "Cambio pico", "prop_c_pos_final": "Prop. final +",
    "prop_c_pos_pico": "Prop. pico +", "rotulo": "Rótulo", "sensibilidad": "Sensibilidad",
    "regla": "Regla", "nivel_final": "Nivel final", "delta_principal_2029t1": "Δ principal 2029T1",
    "n_alcanzados": "Alcanzados",
    "R3_drclacbs": "R3: tarjetas", "R3_drblacbs": "R3: empresas", "R3_drsreacbs": "R3: inmuebles",
}

SELECTED = {
    "fred_manifest": ["series", "source", "download_date"],
    "lit_estudios": ["estudio", "dependiente", "regresores", "metodo", "signo"],
    "model1_coefficients": ["termino", "coef", "ee_hac", "p", "ic_inf", "ic_sup"],
    "model2_coefficients": ["termino", "coef", "ee_hac", "p", "ic_inf", "ic_sup"],
    "descriptives": ["variable", "media", "desv_est", "min", "max"],
    "stationarity": ["variable", "forma", "adf_p", "kpss_p", "decision"],
    "model1_stationarity": ["termino", "forma", "adf_p", "kpss_p", "decision"],
    "model2_stationarity": ["termino", "forma", "adf_p", "kpss_p", "decision"],
    "model1_effects": ["termino", "efecto", "estimacion", "ee", "p"],
    "model1_robustness_estimates": ["variante", "termino", "coef", "p", "estado"],
    "model1_robustness_summary": ["termino", "k", "n", "robustez"],
    "model1_oos": ["pronostico", "rmse_modelo", "rmse_ingenuo", "dm_p", "veredicto"],
    "model2_effects": ["efecto", "est", "ee_hac", "p", "h1_respaldada"],
    "model2_inputs63": ["modelo", "termino", "coef", "p", "n_obs"],
    "model2_lp": ["h", "beta", "ic90_inf", "ic90_sup", "phi"],
    "model2_robustness_estimates": ["variante", "K", "S", "p_S", "estado"],
    "model2_robustness_summary": ["termino", "k", "n", "robustez"],
    "stress_delta": ["modelo", "escenario", "trimestre", "delta", "p05", "p95"],
    "stress_levels": ["modelo", "escenario", "trimestre", "dr", "p05", "p95"],
    "stress_origin": ["modelo", "escenario", "trimestre_adaptado", "dr_adaptado", "dr_original"],
    "stress_paths": ["modelo", "escenario", "trimestre", "PIB", "ΔU", "ΔFFR"],
    "stress_rate_sensitivity": ["modelo", "escenario", "trimestre", "c", "p05", "p95"],
    "stress_sensitivity": ["modelo", "escenario", "sensibilidad", "nivel_final", "delta_final"],
}

TITLES = {
    "fred_manifest": "Manifiesto de fuentes congeladas",
    "lit_estudios": "Estudios verificados: variables, métodos y signos",
    "descriptives": "Estadísticos descriptivos", "stationarity": "Estacionariedad de las series",
    "model1_coefficients": "Modelo I — coeficientes", "model1_effects": "Modelo I — efectos",
    "model1_deviations": "Modelo I — desviaciones", "model1_diagnostics": "Modelo I — diagnósticos",
    "model1_limitations": "Modelo I — limitaciones", "model1_oos": "Modelo I — evaluación fuera de muestra",
    "model1_robustness_estimates": "Modelo I — estimaciones de robustez",
    "model1_robustness_summary": "Modelo I — resumen de robustez",
    "model1_stationarity": "Modelo I — estacionariedad",
    "model2_coefficients": "Modelo II — coeficientes", "model2_comparison": "Modelo II — comparación dinámica",
    "model2_deviations": "Modelo II — desviaciones", "model2_diagnostics": "Modelo II — diagnósticos",
    "model2_effects": "Modelo II — efectos", "model2_inputs63": "Insumos de comparación de modelos",
    "model2_limitations": "Modelo II — limitaciones", "model2_lp": "Modelo II — proyecciones locales",
    "model2_reading": "Modelo II — lectura de resultados",
    "model2_robustness_estimates": "Modelo II — estimaciones de robustez",
    "model2_robustness_summary": "Modelo II — resumen de robustez",
    "model2_selection": "Modelo II — selección de rezagos", "model2_stationarity": "Modelo II — estacionariedad",
    "model2_trajectory": "Modelo II — trayectoria", "stress_delta": "Estrés — cambios adverso menos base",
    "stress_levels": "Estrés — niveles de morosidad", "stress_limitations": "Estrés — limitaciones",
    "stress_models": "Estrés — comparación entre modelos", "stress_origin": "Estrés — variante de origen",
    "stress_paths": "Estrés — trayectorias de regresores", "stress_rate_sensitivity": "Estrés — sensibilidad de tasa",
    "stress_sensitivity": "Estrés — otras sensibilidades",
}

VALUE_LABELS = {
    'gdp_growth': 'PIB (crecimiento)', 'd_unemp': 'Cambio del desempleo', 'inflation': 'Inflación',
    'd_ffr': 'Cambio de la tasa', 'credit_growth': 'Crédito rezagado', 'y_lag': 'Dependiente rezagada',
    'd_dr': 'Cambio de morosidad', 'd_dr_l1': 'Cambio de morosidad rezagado',
    'gdp_l1': 'PIB real rezagado', 'd_unemp_l1': 'Cambio del desempleo rezagado',
    'inflation_l1': 'Inflación rezagada', 'credit_l4': 'Crédito rezagado',
    'const': 'Constante', 'modelo1': 'Modelo I', 'modelo2': 'Modelo II',
    'base': 'Base', 'severo': 'Adverso Fed', 'propio': 'Escenario D',
    'dralacbs': 'Morosidad', 'dralacbs_logit': 'Logit de morosidad',
    'gdpc1_yoy': 'PIB real interanual', 'gdp_yoy': 'PIB nominal interanual',
    'unrate': 'Desempleo', 'cpiaucsl_yoy': 'Inflación interanual',
    'fedfunds': 'Tasa de fondos federales', 'loans_yoy': 'Crédito interanual',
    'dralacbn': 'Morosidad sin ajuste estacional', 'drclacbs': 'Morosidad de tarjetas',
    'drblacbs': 'Morosidad empresarial', 'drsreacbs': 'Morosidad inmobiliaria',
    'coralacbs': 'Castigos netos de préstamos',
}


def display_cell(value: str, column: str = '') -> str:
    """Readable labels, with raw identifiers retained in the separate trace."""
    value = value.replace('no detallados en el resumen leído', 'no especificados en la fuente consultada')
    value = value.replace('no detallado en resumen leído', 'no especificado en la fuente consultada')
    if column == 'metodo':
        value = value.replace('mínimos cuadrados generalizables factibles', 'mínimos cuadrados generalizados factibles')
    if column == 'modelo':
        value = re.sub(r'\s*\(spec\s*00[1-6]\)', '', value)
    if column == 'prueba' and value.startswith('VIF'):
        value = readable_vif(value)
        for key, label in VALUE_LABELS.items():
            value = re.sub(r'\b' + re.escape(key) + r'\b', lambda _: label, value)
    if column == 'estudio':
        year = re.search(r'\b(\d{4})\b', value)
        names = re.findall(r'(?:^|;|\by\b)\s*([^,;]+),', value)
        if year and names:
            author = names[0] + ' et al.' if len(names) > 2 else ' y '.join(names)
            value = author.strip() + ' (' + year[1] + ')'
    if column in {'regresores', 'metodo'}:
        value = value.replace('tipo de interés de lending', 'tasa de préstamo')
    if column == 'signo':
        value = re.sub(r'\s*\(texto completo,[^)]*\)', '', value)
    if column in {'nota', 'origen', 'motivo', 'referencia', 'detalle', 'limitacion', 'regla', 'rotulo'}:
        value = presentation_note(value)
    if column in {'termino', 'variable', 'modelo', 'escenario', 'columna_panel'}:
        rate_lag = re.fullmatch(r'd_ffr_l(\d+)', value)
        impulse = re.fullmatch(r'covid_(\d{4})q([1-4])', value)
        if rate_lag:
            value = 'Cambio de tasa contemporáneo' if rate_lag[1] == '0' else 'Cambio de tasa, rezago ' + rate_lag[1]
        elif impulse:
            value = 'Impulso ' + impulse[1] + 'T' + impulse[2]
        elif value.endswith('_d'):
            value = 'Cambio de ' + VALUE_LABELS.get(value[:-2], value[:-2])
        elif value.endswith('_logit'):
            value = 'Logit de ' + VALUE_LABELS.get(value[:-6], value[:-6])
        value = VALUE_LABELS.get(value, value)
    return format_report_cell(value, column)


def readable_vif(text: str) -> str:
    def label(match):
        key = match[1]
        lag = re.fullmatch(r'd_ffr_l(\d+)', key)
        name = ('Cambio de tasa contemporáneo' if lag[1] == '0' else 'Cambio de tasa, rezago ' + lag[1]) if lag else VALUE_LABELS.get(key, key)
        return 'VIF (' + name + ')'
    return re.sub(r'VIF \(([^)]+)\)', label, text)


def presentation_note(note: str) -> str:
    """Remove operational labels without changing approved scientific qualifications."""
    note = note.replace('Pre-registro de la spec 003', 'Pre-registro del Modelo I')
    note = note.replace('Pre-registro de la spec 004', 'Pre-registro del Modelo II')
    note = note.replace('el coeficiente del Modelo I se lee de las salidas de la spec 003',
                        'los coeficientes de ambos modelos provienen de sus estimaciones principales')
    note = note.replace('; la redacción de la comparación corresponde a la spec 006.', '.')
    note = re.sub(r'(?i)\bspec\s*00[1-6]\b', 'especificación pre-registrada', note)
    note = note.replace('Signo no reutilizado: observaciones opcionales de 002 pendientes; consultar matriz y auditoría.',
                        'Lectura de signo no presentada; consultar la fuente citada.')
    note = re.sub(r'`?(?:outputs|specs|report)/[^\s`;]+`?', 'la fuente original', note)
    note = note.replace('por la regla heredada', 'mientras la lectura del Modelo II no sea de evidencia fuerte')
    note = note.replace('regla heredada', 'regla de tasa en cero')
    note = note.replace('no detallado en resumen leído', 'no especificado en la fuente consultada')
    note = note.replace('pendiente-lectura', 'lectura no disponible')
    note = note.replace('consultar la matriz', 'consultar la fuente citada')
    note = re.sub(r'\bmodelo1\b', 'Modelo I', note)
    note = re.sub(r'\bmodelo2\b', 'Modelo II', note)
    return readable_vif(note)


def format_report_cell(value: str, column: str = "") -> str:
    """Spanish three-decimal display; source CSV retains full precision."""
    if column in ('kpss_p', 'kpss_p_truncado'):
        compact = value.replace(' ', '').replace(',', '.')
        bound = re.fullmatch(r'([<>≥≤])([0-9.]+)', compact)
        if bound:
            # A common non-strict bound is supported by both strict and non-strict
            # source limits. Numeric endpoints without documented limits stay exact.
            operator = {'>': '≥', '<': '≤'}.get(bound[1], bound[1])
            value = operator + ' ' + fmt_es(float(bound[2]), 2)
        elif re.fullmatch(r"[+-]?\d+(?:\.\d*)?(?:[eE][+-]?\d+)?", value):
            value = fmt_es(float(value), 3)
    elif column in {'p', 'p_valor', 'adf_p', 'p_S', 'p_S_rez', 'dm_p', 'p_principal'} and re.fullmatch(r"\d+(?:\.\d*)?(?:[eE][+-]?\d+)?", value):
        value = '< 0,001' if float(value) < .001 else fmt_es(float(value), 3)
    elif column == "seccion_principal":
        pass
    elif re.fullmatch(r"[+-]?\d+(?:\.\d*)?(?:[eE][+-]?\d+)?", value):
        value = value if re.fullmatch(r"[+-]?\d+", value) else fmt_es(float(value), 3)
    elif re.fullmatch(r"\d{4}Q[1-4]", value):
        value = value.replace("Q", "T")
    elif value in ("True", "False"):
        value = "sí" if value == "True" else "no"
    return value.replace("\\", "\\\\").replace("|", "\\|").replace("\r", " ").replace("\n", " ")


def _label(column: str) -> str:
    if column in LABELS:
        return LABELS[column]
    if re.fullmatch(r"R\d(?:_\w+)?", column):
        return column.replace("_", " ")
    return column.replace("_", " ")


def _markdown(headers: list[str], rows: list[list[str]], source: str) -> str:
    lines = ["| " + " | ".join(format_report_cell(_label(c)) for c in headers) + " |",
             "| " + " | ".join("---" for _ in headers) + " |"]
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    caption = ('Fuente: matriz de literatura verificada; elaboración propia.' if 'lit_estudios' in source or 'matriz-literatura' in source
               else 'Fuente: FRED y Reserva Federal; adaptación propia.' if 'stress_' in source
               else 'Fuente: FRED; elaboración propia.')
    lines.extend(['', caption])
    has_numeric = any(re.fullmatch(r'[<>≥≤]?\s*[+-]?\d+(?:[,.]\d+)?', cell) for row in rows for cell in row)
    if not ('lit_estudios' in source or 'matriz-literatura' in source) and has_numeric:
        lines.append('Cifras redondeadas a tres decimales. La fuente original conserva la precisión completa.')
        if any(c in {'p', 'p_valor', 'adf_p', 'p_S', 'p_S_rez', 'dm_p', 'p_principal'} for c in headers):
            lines.append('Los p-valores inferiores a 0,001 se muestran como < 0,001.')
        if any(c.startswith('kpss_') for c in headers):
            lines.append('KPSS conserva sus límites de censura: ≥ y ≤ unifican los límites documentados; no indican valores exactos.')
    lines.append('')
    return "\n".join(lines)


def build_report_tables(sources: dict[str, str], source_notes: dict[str, str] | None = None,
                        source_markdown: dict[str, str] | None = None) -> dict:
    """Build selected-column tables and complete narrow-panel annexes from CSV text."""
    files, trace = {}, {}
    annex = ["# Anexos completos de tablas", "",
             "Los paneles conservan todas las filas y columnas de los CSV originales. "
             "La primera columna se repite para facilitar la lectura; los paneles se leen en el mismo orden.", ""]
    for name, text in sorted(sources.items()):
        if not re.fullmatch(r"[a-z0-9_]+", name):
            raise ValueError(f"Tabla: nombre inválido {name!r}")
        parsed = list(csv.reader(io.StringIO(text)))
        if not parsed or not parsed[0] or len(set(parsed[0])) != len(parsed[0]):
            raise ValueError(f"{name}: cabecera CSV vacía o duplicada")
        headers, raw_rows = parsed[0], parsed[1:]
        if any(len(row) != len(headers) for row in raw_rows):
            raise ValueError(f"{name}: fila CSV con distinto número de celdas")
        source = "data/raw/manifest.csv" if name == 'fred_manifest' else f"outputs/tables/{name}.csv"
        bounds = {}
        approved_md = (source_markdown or {}).get(name, '')
        if 'kpss_p' in headers and approved_md and name in {'model1_stationarity', 'model2_stationarity'}:
            md_rows = [[cell.strip() for cell in line.strip().strip('|').split('|')]
                       for line in approved_md.splitlines() if line.startswith('|')]
            if not md_rows or 'kpss_p' not in md_rows[0] or len(md_rows[2:]) != len(raw_rows):
                raise ValueError(f'{name}: fuente KPSS incompatible')
            md_headers = md_rows[0]
            for index, (row, md_row) in enumerate(zip(raw_rows, md_rows[2:])):
                if len(md_row) != len(md_headers) or any(
                    md_row[md_headers.index(key)] != row[headers.index(key)]
                    for key in ('termino', 'forma') if key in headers):
                    raise ValueError(f'{name}: identidad KPSS incompatible')
                value = md_row[md_headers.index('kpss_p')]
                if re.fullmatch(r'[<>≥≤]\s*\d+[,.]\d+', value):
                    endpoint = float(re.sub(r'^[<>≥≤]\s*', '', value).replace(',', '.'))
                    if endpoint != float(row[headers.index('kpss_p')]):
                        raise ValueError(f'{name}: límite KPSS incompatible')
                    bounds[index] = value

        def contextual_markdown(columns, rows):
            notes = []
            approved_note = presentation_note((source_notes or {}).get(name, ""))
            if name == "model2_lp" and any(c == "phi" or c.startswith("phi_") for c in columns) and approved_note:
                notes.append(approved_note)
            if name == "model1_robustness_estimates" and "motivo" in columns:
                notes.append("Las celdas vacías de Motivo indican que no se proporciona una explicación adicional. "
                             "En las filas con estado «estimada» no se informa una causa de no estimación; "
                             "las filas «no estimada» conservan su motivo original.")
            if name == 'stationarity' and '' in columns:
                notes.append('Índice CSV identifica la fila original; no representa una variable económica.')
            if name in {'model1_diagnostics', 'model2_diagnostics'}:
                if 'veredicto' in columns:
                    notes.append('VIF no es una prueba con p-valor. En CUSUM, la salida del modelo no exporta un estadístico ni p-valor; se informa el veredicto. Los vacíos o guiones no representan ceros.')
                if 'nota' in columns:
                    notes.append('Las celdas vacías indican que no se proporciona información adicional para esa prueba. Los resultados se presentan en el panel de estadísticos y veredictos anterior.')
            prefix = "\n\n".join(notes)
            return (prefix + "\n\n" if prefix else "") + _markdown(columns, rows, source)

        def panel(columns):
            indices = [headers.index(c) for c in columns]
            def value(row, index, column):
                if headers[column] == 'kpss_p':
                    explicit = row[headers.index('kpss_p_truncado')] if 'kpss_p_truncado' in headers else ''
                    return explicit or bounds.get(index, row[column])
                return row[column]
            return [[display_cell(value(row, index, i), headers[i]) for i in indices]
                    for index, row in enumerate(raw_rows)]

        chosen = [c for c in SELECTED.get(name, headers[:5]) if c in headers] or headers[:5]
        display_rows = panel(chosen)
        files[f"{name}.md"] = contextual_markdown(chosen, display_rows)
        panels = []
        note_columns = ['phi_nota'] if name == 'model2_lp' and 'phi_nota' in headers else []
        identity = ([c for c in ('termino', 'efecto', 'escala') if c in headers] if name == 'model1_effects' else
                    [c for c in ('modelo', 'termino') if c in headers] if name == 'model2_inputs63' else
                    [c for c in ('modelo', 'escenario', 'sensibilidad') if c in headers] if name == 'stress_sensitivity' else
                    [c for c in ('modelo', 'escenario', 'trimestre', 'trimestre_adaptado') if c in headers]
                    if name.startswith('stress_') else
                    [c for c in ('variante', 'termino') if c in headers] if name.endswith('robustness_estimates') else
                    [c for c in ('variable', 'termino', 'forma') if c in headers] if 'stationarity' in name else [])
        identity = identity or [headers[0]]
        remaining = [c for c in headers if c not in identity + note_columns]
        width = max(1, min(3, 5 - len(identity)))
        groups = [identity + remaining[i:i + width] for i in range(0, len(remaining), width)] or [identity]
        annex.extend([f"## {TITLES.get(name, name.replace('_', ' '))}", "", f"CSV completo: `{source}`.", ""])
        for index, columns in enumerate(groups, 1):
            filename = f"{name}_anexo_{index}.md"
            rows = panel(columns)
            files[filename] = contextual_markdown(columns, rows)
            if note_columns and any(c == 'phi' or c.startswith('phi_') for c in columns):
                note_lines = [f"Nota φ, h = {row[0]}: {row[headers.index('phi_nota')]}"
                              for row in raw_rows if row[headers.index('phi_nota')]]
                if note_lines:
                    files[filename] = '\n\n'.join(note_lines) + '\n\n' + files[filename]
            panels.append({"file": filename, "columns": columns, "rows": rows})
            annex.extend([f"### Panel {index}", "",
                          "Columnas originales: " + "; ".join(f"`{c or '(índice CSV)'}`" for c in columns) + ".", "",
                          f"{{{{< include ../outputs/informe/{filename} >}}}}", ""])
        trace[name] = {"source": source, "source_sha256": hashlib.sha256(text.encode()).hexdigest(),
                       "rows": len(raw_rows), "columns": headers,
                       "presentation": {"file": f"{name}.md", "columns": chosen, "rows": display_rows},
                       "annex_panels": panels}
        trace[name]['note_columns'] = note_columns
        if bounds:
            trace[name]['censoring_source'] = {'file': f'outputs/tables/{name}.md',
                                             'sha256': hashlib.sha256(approved_md.encode()).hexdigest(),
                                             'rows': bounds}
        trace[name]['field_notes'] = [{'h': row[0], 'phi_nota': row[headers.index('phi_nota')]}
                                     for row in raw_rows] if note_columns else []
        if (source_notes or {}).get(name):
            trace[name]["source_note"] = source_notes[name]
            trace[name]["source_note_file"] = f"outputs/tables/{name}.md"
            files[name + '_nota.md'] = presentation_note(source_notes[name]) + '\n'
    return {"files": files, "trace": trace, "annex": "\n".join(annex)}


def literature_report_table(matrix_text: str):
    """Copy verified studies; never reuse the five questioned sign readings."""
    import pandas as pd

    from src.references import parse_matrix

    _, rows = parse_matrix(matrix_text)
    questioned = {"koju2018", "tanaskovic2015", "nkusu2011", "jimenez2014a", "obradovic2026"}
    records = []
    for row in rows:
        cells = row.cells
        if cells["Estado"] != "verificado" or cells["Tipo"] != "estudio":
            continue
        key = cells["Clave"]
        finding = cells["Hallazgo o aporte"]
        explicit_sign = any(word in finding.lower() for word in ("positivo", "negativo", "no significativo"))
        provenance = re.search(r'\((texto completo,[^)]*)\)', finding)
        consulted = 'Base consultada: ' + provenance[1] + '. ' if provenance else 'Base consultada: resumen del estudio, según la verificación de literatura. '
        if key == 'obradovic2026' and re.search(r'tipos de interés de lending[^;]*\bpositivo\b', finding, re.I):
            reader_note = ('El resumen informa una asociación positiva de la tasa de préstamo con la morosidad; '
                           'esa tasa no es la tasa de política. El guion remite al signo descrito en la sección 2.5.')
            if 'el efecto del tipo de cambio oficial no es consistente' in finding and 'el efecto del desempleo es negativo' in finding:
                remainder = finding[finding.index('el efecto del tipo de cambio oficial'):]
                reader_note += ' ' + remainder[0].upper() + remainder[1:]
        elif key in questioned:
            reader_note = 'El signo no se sintetiza en esta tabla; debe leerse en el contexto de la fuente citada.'
        elif explicit_sign:
            reader_note = 'El signo se presenta con su contexto; no debe interpretarse como un efecto único de todos los regresores.'
        else:
            reader_note = 'La información consultada no permite asignar un signo a cada regresor.'
        records.append({"clave": key, "estudio": cells["Autor(es) y año"],
                        "dependiente": cells["Variable dependiente"], "regresores": cells["Regresores"],
                        "metodo": cells["Método"], "signo": "—" if key in questioned or not explicit_sign else finding,
                        "seccion_principal": cells["Sección principal"],
                        "nota": consulted + reader_note})
    return pd.DataFrame(records, columns=["clave", "estudio", "dependiente", "regresores", "metodo", "signo", "seccion_principal", "nota"])
