"""Pure text rendering and report variables for spec 005."""
from __future__ import annotations

import numpy as np
import pandas as pd

from src.design import ModelDataError
from src.tables import fmt_es, quarter_label, to_markdown

STRESS_TABLES = ('stress_paths', 'stress_levels', 'stress_delta', 'stress_rate_sensitivity',
                 'stress_models', 'stress_sensitivity', 'stress_origin', 'stress_limitations')

PRINCIPAL_NOTE = (
    'Nota: en el ejercicio principal los coeficientes de ΔFFR se fijan en cero por la regla heredada. '
    'Son proyecciones condicionales asociadas a las trayectorias, con incertidumbre de parámetros; '
    'las bandas de niveles no son intervalos de predicción. '
    'Fuente: FRED, Reserva Federal (escenarios 2026), adaptación propia.'
)


def stress_variables(values: dict) -> dict:
    """Format computed leaves, preserving all approved nested dimensions."""
    def convert(value):
        if isinstance(value, dict):
            return {key: convert(item) for key, item in value.items()}
        if isinstance(value, pd.Period):
            return quarter_label(value)
        if isinstance(value, (bool, np.bool_)):
            return 'sí' if value else 'no'
        if isinstance(value, (int, np.integer)):
            return str(value)
        if isinstance(value, (float, np.floating)):
            if not np.isfinite(value):
                raise ModelDataError('variable del estrés: valor no finito')
            return fmt_es(float(value), 3)
        if isinstance(value, str):
            return value
        raise ModelDataError(f'variable del estrés: tipo no admitido {type(value)}')
    return convert(values)


def render_stress_tables(tables: dict[str, pd.DataFrame]) -> dict[str, tuple[str, str]]:
    if set(tables) != set(STRESS_TABLES):
        raise ModelDataError('estrés: faltan tablas del contrato')
    rendered = {}
    for name in STRESS_TABLES:
        frame = tables[name].copy()
        numeric = frame.select_dtypes(include=np.number)
        if not np.isfinite(numeric.to_numpy()).all():
            raise ModelDataError(f'{name}: valor no finito')
        for column in frame:
            if isinstance(frame[column].dtype, pd.PeriodDtype):
                frame[column] = frame[column].map(quarter_label)
        csv_text = frame.to_csv(index=False, lineterminator='\n')
        # Mixed counterfactual columns contain numbers and "no aplica"; format per cell.
        display = frame.copy()
        def display_value(value):
            if isinstance(value, (bool, np.bool_)):
                return 'sí' if value else 'no'
            if isinstance(value, (float, np.floating)):
                if not np.isfinite(value):
                    raise ModelDataError(f'{name}: valor no finito')
                return fmt_es(float(value), 3)
            if isinstance(value, (int, np.integer)):
                return str(value)
            return str(value)
        for column in display:
            display[column] = display[column].map(display_value)
        # Escape only the stress presentation; preserve literal strings in CSV.
        def markdown_cell(value):
            return (str(value).replace('\\', '\\\\').replace('|', '\\|')
                    .replace('\r\n', '<br>').replace('\n', '<br>').replace('\r', '<br>'))
        for column in display:
            display[column] = display[column].map(markdown_cell)
        display.columns = [markdown_cell(column) for column in display.columns]
        md = to_markdown(display, decimals=3)
        note = PRINCIPAL_NOTE
        if name in ('stress_levels', 'stress_delta'):
            levels = tables['stress_levels']
            if 'n_replicas_fuera_rango_modelo' in levels:
                for model, group in levels.groupby('modelo', sort=False):
                    summary = group.iloc[0]
                    if summary.n_replicas_fuera_rango_modelo > 0:
                        note += (f' Advertencia: niveles fuera de [0, 100] en {model}, sin truncar: '
                                 f'{int(summary.n_replicas_fuera_rango_modelo)} réplicas '
                                 f'(proporción {fmt_es(float(summary.prop_replicas_fuera_rango_modelo), 3)}), '
                                 f'mínimo {fmt_es(float(summary.nivel_min_modelo), 3)}, '
                                 f'máximo {fmt_es(float(summary.nivel_max_modelo), 3)}.')
        if name == 'stress_rate_sensitivity':
            note += ' Sensibilidad, no efecto estimado; usa los coeficientes de tasa sin fijarlos en cero.'
            # Required label is deliberately lower case in every output.
            note = note.replace('Sensibilidad, no efecto estimado', 'sensibilidad, no efecto estimado')
        if name == 'stress_models':
            note += ' Diferencia puntual entre modelos, sin banda: no hay una distribución conjunta.'
        if name == 'stress_origin':
            note += ' Los primeros trimestres del calendario original son contrafactuales; comparación por paso k.'
        rendered[name] = (csv_text, md + '\n\n' + note + '\n')
    return rendered
