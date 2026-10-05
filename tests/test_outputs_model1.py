"""Tests de las salidas del Modelo I: figuras y variables del informe (spec 003, tarea 8).

Cubre RF-11, RF-14, RF-19, RF-22 y RNF-8. Todo sobre datos sintéticos (fixture de sesión
`model1_result`); ningún test lee datos reales. Las figuras se cierran al terminar.
"""

from __future__ import annotations

import ast
import dataclasses
import io
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest

from src.figures import plot_model1_coefficients, plot_model1_cusum, plot_model1_oos
from src.model1 import effects_table, fmt_p
from src.model1_config import COVID_QUARTERS, MACRO_TERMS, VARIANTS
from src.report_vars import model1_variables
from src.tables import fmt_es

FOOTER = "Fuente: FRED; elaboración propia"
SHORT = ["ΔPIB", "ΔU", "π", "ΔFFR", "CRED(t−4)"]  # orden de MACRO_TERMS


@pytest.fixture
def figs():
    """Registra las figuras creadas y las cierra al terminar el test."""
    created: list = []
    yield created
    for f in created:
        plt.close(f)


def _png(fig) -> bytes:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    return buf.getvalue()


def _check_common(fig) -> None:
    """8×4,5 pulgadas, 200 dpi, sin título y con el pie de fuente (RF-11, RF-14, RF-19)."""
    assert tuple(fig.get_size_inches()) == (8.0, 4.5)
    assert fig.dpi == 200
    assert all(ax.get_title() == "" for ax in fig.axes)
    assert fig._suptitle is None
    assert FOOTER in [t.get_text() for t in fig.texts]


# --- Figura de coeficientes (RF-11) ---


def test_coefficients_figure_plots_impact_per_sd_with_95_ci_and_zero_line(model1_result, figs):
    fig = plot_model1_coefficients(model1_result.effects)
    figs.append(fig)
    _check_common(fig)
    ax = fig.axes[0]
    eff = model1_result.effects
    sel = eff[(eff["efecto"] == "impacto") & (eff["escala"] == "por 1 DE")].reset_index(drop=True)
    assert len(sel) == 5

    points, _, barlines = ax.containers[0].lines
    np.testing.assert_allclose(points.get_xdata(), sel["estimacion"])
    segs = barlines[0].get_segments()
    np.testing.assert_allclose([s[0][0] for s in segs], sel["ic_inf"])
    np.testing.assert_allclose([s[1][0] for s in segs], sel["ic_sup"])

    zero = [ln for ln in ax.lines if list(ln.get_xdata()) == [0, 0]]
    assert len(zero) == 1  # línea vertical en cero
    assert [t.get_text() for t in ax.get_yticklabels()] == SHORT


def test_coefficients_figure_uses_the_impact_per_sd_and_not_other_effects(model1_result, figs):
    fig = plot_model1_coefficients(model1_result.effects)
    figs.append(fig)
    xs = fig.axes[0].containers[0].lines[0].get_xdata()
    eff = model1_result.effects
    per_pp = eff[(eff["efecto"] == "impacto") & (eff["escala"] == "por 1 pp")]["estimacion"].to_numpy()
    long_de = eff[(eff["efecto"] == "largo plazo") & (eff["escala"] == "por 1 DE")]["estimacion"].to_numpy()
    assert not np.allclose(xs, per_pp)
    assert not np.allclose(xs, long_de)


def test_coefficients_figure_has_spanish_axis_with_the_unit(model1_result, figs):
    fig = plot_model1_coefficients(model1_result.effects)
    figs.append(fig)
    assert "pp de morosidad por 1 DE" in fig.axes[0].get_xlabel()


def test_coefficients_figure_skips_and_notes_a_regressor_without_defined_sd(model1_result, figs):
    design = model1_result.fit.design
    X = design.X.copy()
    X["d_ffr"] = 0.5  # DE = 0 → «no definido»
    fit = dataclasses.replace(model1_result.fit, design=dataclasses.replace(design, X=X))
    fig = plot_model1_coefficients(effects_table(fit))
    figs.append(fig)
    assert [t.get_text() for t in fig.axes[0].get_yticklabels()] == [s for s in SHORT if s != "ΔFFR"]
    note = " ".join(t.get_text() for t in fig.texts)
    assert "No definido" in note and "ΔFFR" in note


def test_coefficients_figure_without_plottable_effects_raises(model1_result):
    eff = model1_result.effects.copy()
    eff["estado"] = "no definido"
    with pytest.raises(ValueError, match="efectos por 1 DE"):
        plot_model1_coefficients(eff)


# --- Figura CUSUM (RF-14) ---


def test_cusum_figure_has_statistic_and_two_5_percent_bands(model1_result, figs):
    fig = plot_model1_cusum(model1_result.cusum)
    figs.append(fig)
    _check_common(fig)
    ax = fig.axes[0]
    assert len(ax.lines) == 3
    c = model1_result.cusum
    np.testing.assert_allclose(ax.lines[0].get_ydata(), c["cusum"].to_numpy())
    np.testing.assert_allclose(ax.lines[1].get_ydata(), c["lower"].to_numpy())
    np.testing.assert_allclose(ax.lines[2].get_ydata(), c["upper"].to_numpy())
    labels = [t.get_text() for t in ax.get_legend().get_texts()]
    assert labels == ["CUSUM", "Bandas al 5 %"]
    assert ax.get_xlabel() == "Trimestre"
    assert "residuos recursivos" in ax.get_ylabel()


def test_cusum_figure_labels_quarters_in_spanish(model1_result, figs):
    fig = plot_model1_cusum(model1_result.cusum)
    figs.append(fig)
    labels = [t.get_text() for t in fig.axes[0].get_xticklabels() if t.get_text()]
    assert labels and all("T" in lab and lab[:4].isdigit() for lab in labels)


# --- Figura fuera de muestra (RF-19): exactamente 4 series ---


def test_oos_figure_draws_exactly_four_series(model1_result, figs):
    fig = plot_model1_oos(model1_result.oos)
    figs.append(fig)
    _check_common(fig)
    ax = fig.axes[0]
    assert len(ax.lines) == 4
    s = model1_result.oos.series
    for line, col in zip(ax.lines, ["observado", "un_paso", "dinamico", "ingenuo_un_paso"]):
        np.testing.assert_allclose(line.get_ydata(), s[col].to_numpy())
    labels = [t.get_text() for t in ax.get_legend().get_texts()]
    assert labels == [
        "Observada", "Modelo a un paso", "Modelo dinámico", "Ingenuo a un paso (paseo aleatorio)",
    ]


def test_oos_figure_does_not_draw_the_constant_naive_but_the_series_keeps_it(model1_result, figs):
    fig = plot_model1_oos(model1_result.oos)
    figs.append(fig)
    const = model1_result.oos.series["ingenuo_dinamico"].to_numpy()
    for line in fig.axes[0].lines:
        assert not np.allclose(line.get_ydata(), const)
    assert "ingenuo_dinamico" in model1_result.oos.series.columns  # auditoría numérica
    assert (model1_result.oos.table["rmse_ingenuo"] > 0).all()  # y en la tabla de métricas


def test_oos_figure_axis_is_in_spanish_with_the_unit(model1_result, figs):
    fig = plot_model1_oos(model1_result.oos)
    figs.append(fig)
    ax = fig.axes[0]
    assert "morosidad" in ax.get_ylabel() and "%" in ax.get_ylabel()
    assert ax.get_xlabel() == "Trimestre"


# --- Las figuras no escriben a disco y son deterministas ---


def test_figures_are_deterministic_png_bytes(model1_result, figs):
    makers = [
        lambda: plot_model1_coefficients(model1_result.effects),
        lambda: plot_model1_cusum(model1_result.cusum),
        lambda: plot_model1_oos(model1_result.oos),
    ]
    for make in makers:
        a, b = make(), make()
        figs.extend([a, b])
        assert _png(a) == _png(b)


def test_plot_functions_never_save_to_disk():
    tree = ast.parse(Path("src/figures.py").read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name.startswith("plot_model1_"):
            for sub in ast.walk(node):
                if isinstance(sub, ast.Attribute):
                    assert sub.attr != "savefig", node.name
                if isinstance(sub, ast.Call) and getattr(sub.func, "id", "") == "open":
                    pytest.fail(f"{node.name}: contiene open()")


# =====================================================================================
# Variables del informe: bloque `modelo1:` (RF-22)
# =====================================================================================

TOP_KEYS = [
    "estimador", "forma_y", "muestra_inicio", "muestra_fin", "n_obs", "n_parametros",
    "rezagos_hac", "dummies_covid", "truncamiento_espectral", "r2", "r2_ajustado",
    "ee_regresion", "variantes", "coef", "efectos", "signo", "diag", "robustez",
    "variantes_muestra", "oos", "no_i0", "limitaciones", "desviaciones",
]


@pytest.fixture(scope="module")
def mv(model1_result) -> dict:
    return model1_variables(model1_result)


def _leaves(obj):
    if isinstance(obj, dict):
        for v in obj.values():
            yield from _leaves(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _leaves(v)
    else:
        yield obj


def test_model1_variables_has_all_the_documented_keys_in_order(mv):
    assert list(mv) == TOP_KEYS


def test_model1_variables_are_all_preformatted_text(mv):
    """Todo es texto ya formateado: ningún float, int, bool ni NaN llega a `_variables.yml`."""
    leaves = list(_leaves(mv))
    assert leaves and all(isinstance(v, str) for v in leaves)
    assert not any(v.lower() == "nan" for v in leaves)


def test_model1_variables_inventory_comes_from_the_fit(mv, model1_result):
    f = model1_result.coef_footer
    assert mv["estimador"] == "MCO con errores Newey-West (HAC, kernel de Bartlett)"
    assert mv["forma_y"] == f["forma_y"] == "primera diferencia"
    assert (mv["muestra_inicio"], mv["muestra_fin"]) == ("2000T1", "2026T2")
    assert mv["n_obs"] == str(f["n_obs"]) == "106"
    assert mv["n_parametros"] == str(f["n_parametros"]) == "11"
    assert mv["rezagos_hac"] == str(f["rezagos_hac"]) == "4"
    assert mv["dummies_covid"] == "2020T2, 2020T3, 2020T4 y 2021T1"
    assert mv["truncamiento_espectral"] == "no"
    assert mv["r2"] == fmt_es(f["r2"], 3) and mv["r2_ajustado"] == fmt_es(f["r2_ajustado"], 3)
    assert mv["ee_regresion"] == fmt_es(f["ee_regresion"], 3)


def test_model1_variables_variants_list_names_and_samples(mv, model1_result):
    ids = [v.id for v in VARIANTS]
    assert list(mv["variantes"]) == ids and len(ids) == 10
    assert mv["variantes"]["R4"] == "PIB nominal"
    assert list(mv["variantes_muestra"]) == ids
    r1 = mv["variantes_muestra"]["R1"]
    assert r1 == {"estado": "estimada", "motivo": "", "inicio": "2000T1", "fin": "2026T2", "n_obs": "98"}
    r8 = mv["variantes_muestra"]["R8"]
    assert r8["estado"] == "no estimada" and r8["motivo"] == "sin historia anterior a 2000T1"
    assert r8["inicio"] == r8["fin"] == r8["n_obs"] == "—"
    assert mv["variantes_muestra"]["R6"]["inicio"] == "2001T1"


def test_model1_variables_coefficients_for_every_term(mv, model1_result):
    terms = list(model1_result.fit.params.index)
    assert list(mv["coef"]) == terms and len(terms) == 11
    tab = model1_result.coefficients.set_index("termino")
    for t in terms:
        assert list(mv["coef"][t]) == ["coef", "ee", "p", "ic_inf", "ic_sup"]
        assert mv["coef"][t]["coef"] == fmt_es(tab.loc[t, "coef"], 3)
        assert mv["coef"][t]["ee"] == fmt_es(tab.loc[t, "ee_hac"], 3)
        assert mv["coef"][t]["p"] == fmt_p(tab.loc[t, "p"])
        assert mv["coef"][t]["ic_inf"] == fmt_es(tab.loc[t, "ic_inf"], 3)
        assert mv["coef"][t]["ic_sup"] == fmt_es(tab.loc[t, "ic_sup"], 3)
    assert "< 0,001" in {mv["coef"][t]["p"] for t in terms}  # p-valores pequeños como texto


def test_model1_variables_effects_in_pp_for_one_pp_and_one_sd(mv, model1_result):
    assert list(mv["efectos"]) == list(MACRO_TERMS)
    eff = model1_result.effects
    for term in MACRO_TERMS:
        e = mv["efectos"][term]
        assert len(e) == 20
        for efecto, ek in (("impacto", "impacto"), ("largo plazo", "largo")):
            for escala, sk in (("por 1 pp", "pp"), ("por 1 DE", "de")):
                row = eff[(eff["termino"] == term) & (eff["efecto"] == efecto) & (eff["escala"] == escala)].iloc[0]
                base = f"{ek}_{sk}"
                assert e[base] == fmt_es(row["estimacion"], 3)
                assert e[f"{base}_ee"] == fmt_es(row["ee"], 3)
                assert e[f"{base}_p"] == fmt_p(row["p"])
                assert e[f"{base}_ic_inf"] == fmt_es(row["ic_inf"], 3)
                assert e[f"{base}_ic_sup"] == fmt_es(row["ic_sup"], 3)


def test_model1_variables_unreported_effects_are_text_never_numbers(model1_result):
    params = model1_result.fit.params.copy()
    params["y_lag"] = 0.97  # 1 − ρ ≤ 0,05
    eff = effects_table(dataclasses.replace(model1_result.fit, params=params))
    out = model1_variables(dataclasses.replace(model1_result, effects=eff))
    for term in MACRO_TERMS:
        e = out["efectos"][term]
        for key in [k for k in e if k.startswith("largo_")]:
            assert e[key] == "no reportado (1 − ρ ≤ 0,05)", key
        assert e["impacto_pp"] != "no reportado (1 − ρ ≤ 0,05)"


def test_model1_variables_undefined_sd_effect_is_text(model1_result):
    design = model1_result.fit.design
    X = design.X.copy()
    X["d_ffr"] = 0.5
    fit = dataclasses.replace(model1_result.fit, design=dataclasses.replace(design, X=X))
    out = model1_variables(dataclasses.replace(model1_result, effects=effects_table(fit)))
    e = out["efectos"]["d_ffr"]
    assert e["impacto_de"] == e["impacto_de_ee"] == e["largo_de"] == "no definido"
    assert e["impacto_pp"] != "no definido"


def test_model1_variables_sign_robustness_and_non_i0(mv, model1_result):
    assert list(mv["signo"]) == list(MACRO_TERMS)
    assert mv["signo"]["gdp_growth"] == "sí" and mv["signo"]["inflation"] == "sin contraste"
    assert list(mv["robustez"]) == list(MACRO_TERMS)
    summary = model1_result.robustness_summary.set_index("termino")
    for t in MACRO_TERMS:
        assert mv["robustez"][t] == summary.loc[t, "robustez"]
    assert mv["no_i0"] == "π y CRED(t−4)"


def test_model1_variables_diagnostics_have_statistic_p_and_verdict(mv, model1_result):
    d = mv["diag"]
    assert list(d) == ["bg", "bp", "white", "jb", "reset", "chow_2008t3", "chow_2020t2", "cusum", "vif"]
    tab = model1_result.diagnostics.set_index("prueba")
    for key, name in [("bg", "Breusch-Godfrey"), ("bp", "Breusch-Pagan"), ("white", "White"),
                      ("jb", "Jarque-Bera"), ("reset", "RESET"), ("chow_2008t3", "Chow 2008Q3"),
                      ("chow_2020t2", "Chow 2020Q2")]:
        assert list(d[key]) == ["estadistico", "p", "veredicto"]
        assert d[key]["estadistico"] == fmt_es(tab.loc[name, "estadístico"], 3)
        assert d[key]["p"] == fmt_p(tab.loc[name, "p_valor"])
        assert d[key]["veredicto"] == tab.loc[name, "veredicto"]
    assert list(d["cusum"]) == ["veredicto"] and d["cusum"]["veredicto"] == tab.loc["CUSUM", "veredicto"]
    assert list(d["vif"]) == ["y_lag", *MACRO_TERMS]
    assert list(d["vif"]["gdp_growth"]) == ["valor", "veredicto"]
    assert d["vif"]["gdp_growth"]["valor"] == fmt_es(tab.loc["VIF (gdp_growth)", "estadístico"], 3)


def test_model1_variables_out_of_sample_block(mv, model1_result):
    o, t = mv["oos"], model1_result.oos.table.set_index("pronostico")
    assert list(o) == [
        "n_trimestres", "rmse_modelo_un_paso", "rmse_ingenuo_un_paso", "mae_modelo_un_paso",
        "mae_ingenuo_un_paso", "cociente_un_paso", "rmse_modelo_dinamico", "rmse_ingenuo_dinamico",
        "mae_modelo_dinamico", "mae_ingenuo_dinamico", "cociente_dinamico", "dm_estadistico",
        "dm_p", "veredicto_un_paso", "veredicto_dinamico", "significancia_un_paso",
    ]
    assert o["n_trimestres"] == "18"
    assert o["rmse_modelo_un_paso"] == fmt_es(t.loc["a un paso", "rmse_modelo"], 2)
    assert o["rmse_ingenuo_dinamico"] == fmt_es(t.loc["dinámico", "rmse_ingenuo"], 2)  # se conserva
    assert o["cociente_dinamico"] == fmt_es(t.loc["dinámico", "cociente_rmse"], 2)
    assert o["dm_estadistico"] == fmt_es(t.loc["a un paso", "dm_estadistico"], 2)
    assert o["dm_p"] == fmt_p(t.loc["a un paso", "dm_p"])
    assert o["veredicto_un_paso"] == t.loc["a un paso", "veredicto"]
    assert o["significancia_un_paso"] == t.loc["a un paso", "significancia"]


def test_model1_variables_limitations_and_deviations_are_lists_from_the_tables(mv, model1_result):
    lim, dev = model1_result.limitations, model1_result.deviations
    assert len(mv["limitaciones"]) == len(lim) and len(mv["desviaciones"]) == len(dev)
    assert mv["limitaciones"][0] == f"{lim.iloc[0]['limitacion']}: {lim.iloc[0]['detalle']}"
    assert any("Endogeneidad" in x for x in mv["limitaciones"])
    r = dev.iloc[-1]
    assert mv["desviaciones"][-1] == f"{r['decision']} ({r['referencia']}): {r['motivo']}"
    assert any("2026-10-05 · C1" in x for x in mv["desviaciones"])


# --- Ninguna cifra a mano (principio 5) ---


def test_model1_variables_react_to_the_data_so_nothing_is_hardcoded(model1_result):
    from src.model1 import run_model1
    from tests.synthetic_model1 import END, make_full, make_stationarity

    other = run_model1(make_full(seed_x=777, seed_e=778), make_stationarity(), END)
    a, b = model1_variables(model1_result), model1_variables(other)
    assert list(a) == list(b)
    numeric_diff = [
        k for k in ("r2", "r2_ajustado", "ee_regresion") if a[k] != b[k]
    ] + [t for t in a["coef"] if a["coef"][t]["coef"] != b["coef"][t]["coef"]]
    assert len(numeric_diff) >= 8  # los números salen de la estimación, no del código
    assert a["oos"]["rmse_modelo_un_paso"] != b["oos"]["rmse_modelo_un_paso"]


def test_model1_variables_source_has_no_numeric_literals_beyond_decimals_and_indexes():
    """En las funciones del bloque `modelo1:` no hay floats ni enteros fuera de {0, 1, 2, 3}."""
    tree = ast.parse(Path("src/report_vars.py").read_text(encoding="utf-8"))
    checked = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and (node.name == "model1_variables" or node.name.startswith("_m1_")):
            checked += 1
            for sub in ast.walk(node):
                if isinstance(sub, ast.Constant) and isinstance(sub.value, (int, float)) and not isinstance(sub.value, bool):
                    assert isinstance(sub.value, int) and sub.value in {0, 1, 2, 3}, (
                        f"{node.name}: cifra a mano {sub.value!r}"
                    )
    assert checked >= 2


def test_covid_quarters_in_the_variables_come_from_the_config(mv):
    labels = [f"{q[:4]}T{q[-1]}" for q in COVID_QUARTERS]
    assert all(lab in mv["dummies_covid"] for lab in labels)


def test_quarter_axis_labels_always_fall_on_the_same_quarter(model1_result, figs):
    for fig in (plot_model1_oos(model1_result.oos), plot_model1_cusum(model1_result.cusum)):
        figs.append(fig)
        labels = [t.get_text() for t in fig.axes[0].get_xticklabels() if t.get_text()]
        assert len(labels) >= 3
        assert len({lab[-2:] for lab in labels}) == 1, labels  # mismo «T#» en todos
