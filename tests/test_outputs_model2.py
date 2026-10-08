"""Tests de las figuras y de las variables del informe del Modelo II (spec 004, tarea 7).

Cubre RF-9, RF-18, RF-28, RNF-8 (bytes deterministas) y RNF-11 (etiquetas en español). Datos
sintéticos; sin red ni datos reales.
"""

from __future__ import annotations

import ast
import dataclasses
import io

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest
import yaml

from src.figures import plot_model2_profile, plot_model2_response
from src.model2 import VariantOutcome2, robustness_summary2
from src.model2_config import ROBUST2
from src.report_vars import model2_variables
from src.tables import fmt_es
from tests.test_language import find_causal_language


@pytest.fixture(scope="module")
def result(model2_result):
    return model2_result


@pytest.fixture(scope="module")
def figs(result):
    detection = result.comparison_counts["horizonte_deteccion"]
    return {
        "profile": plot_model2_profile(result.coefficients, result.peak),
        "response": plot_model2_response(result.lp, result.trajectory, detection),
    }


def _png(fig) -> bytes:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    return buf.getvalue()


def fig_texts(fig) -> list[str]:
    out = [t.get_text() for t in fig.texts]
    for ax in fig.axes:
        out += [ax.get_xlabel(), ax.get_ylabel(), ax.get_title()]
        legend = ax.get_legend()
        if legend:
            out += [t.get_text() for t in legend.get_texts()]
    return out


# --- Formato común (RF-9, RF-18) ---


def test_figure_format(figs):
    for name, fig in figs.items():
        assert tuple(fig.get_size_inches()) == (8.0, 4.5) and fig.dpi == 200, name
        assert all(ax.get_title() == "" for ax in fig.axes), name              # sin título
        assert any("Fuente: FRED; elaboración propia" in t.get_text() for t in fig.texts), name


def test_figures_are_deterministic_png_bytes(result):
    detection = result.comparison_counts["horizonte_deteccion"]
    a = _png(plot_model2_profile(result.coefficients, result.peak))
    b = _png(plot_model2_profile(result.coefficients, result.peak))
    c = _png(plot_model2_response(result.lp, result.trajectory, detection))
    d = _png(plot_model2_response(result.lp, result.trajectory, detection))
    assert a == b and c == d and a[:8] == b"\x89PNG\r\n\x1a\n" and a != c
    plt.close("all")


def test_figure_labels_are_in_spanish_without_causal_language(figs):
    text = " ".join(t for fig in figs.values() for t in fig_texts(fig))
    assert find_causal_language(text) == []
    assert "Rezago" in text and "Horizonte" in text and "pp de morosidad" in text and "Banda al 90 %" in text


# --- Perfil de θ_j (RF-9) ---


def test_profile_has_one_point_per_lag_with_95_percent_ci_and_zero_line(result, figs):
    ax = figs["profile"].axes[0]
    K = result.K
    bars = ax.containers[0]
    xs = bars[0].get_xdata()
    assert list(xs) == list(range(K + 1))
    theta = result.coefficients.set_index("termino").loc[[f"d_ffr_l{j}" for j in range(K + 1)]]
    assert np.allclose(bars[0].get_ydata(), theta["coef"])
    low = np.array([seg[0][1] for seg in bars[2][0].get_segments()])
    high = np.array([seg[1][1] for seg in bars[2][0].get_segments()])
    assert np.allclose(low, theta["ic_inf"]) and np.allclose(high, theta["ic_sup"])        # IC 95 %
    zero = [ln for ln in ax.lines if len(set(ln.get_ydata())) == 1 and ln.get_ydata()[0] == 0]
    assert zero, "falta la línea en cero"


def test_profile_marks_the_peak_only_when_it_is_within_the_lags(result):
    inside = {"h_star": 1, "signo": "+"}
    outside = {"h_star": result.K + 3, "signo": "+"}
    fig_in = plot_model2_profile(result.coefficients, inside)
    fig_out = plot_model2_profile(result.coefficients, outside)
    labels_in = " ".join(fig_texts(fig_in))
    labels_out = " ".join(fig_texts(fig_out))
    assert "h* = 1" in labels_in and "h* =" not in labels_out
    plt.close("all")


def test_profile_without_dffr_coefficients_raises(result):
    empty = result.coefficients[~result.coefficients["termino"].str.startswith("d_ffr_l")]
    with pytest.raises(ValueError):
        plot_model2_profile(empty, result.peak)


# --- Respuesta (RF-18) ---


def test_response_has_two_panels_with_the_right_series(result, figs):
    fig = figs["response"]
    assert len(fig.axes) == 2
    ax1, ax2 = fig.axes
    lines = {ln.get_label(): ln for ln in ax1.lines}
    assert np.allclose(lines["β_h (proyección local)"].get_ydata(), result.lp["beta"].astype(float))
    assert np.allclose(lines["R(h) (rezagos distribuidos)"].get_ydata(), result.trajectory["R"])
    phi = [ln for ln in ax2.lines if ln.get_label() == "φ_h (respuesta de la tasa)"][0]
    assert np.allclose(phi.get_ydata(), result.lp["phi"].astype(float))
    assert phi.get_ydata()[0] == 1.0                                         # φ_0 = 1 por construcción
    assert len(ax1.collections) == 1 and len(ax2.collections) == 1            # una banda cada panel
    assert any("Banda al 90 %" in t.get_text() for t in ax1.get_legend().get_texts())


def test_response_phi0_has_no_band_and_band_is_the_hac_90_percent(result, figs):
    ax2 = figs["response"].axes[1]
    band = ax2.collections[0].get_paths()[0].vertices
    assert band.shape[0] > 0
    lp = result.lp
    assert lp.loc[0, "phi_ee"] is None and lp.loc[0, "phi_ic90_inf"] is None   # sin banda en h = 0


def test_response_marks_the_detection_horizon_only_when_there_is_one(result):
    with_det = plot_model2_response(result.lp, result.trajectory, "h2")
    without = plot_model2_response(result.lp, result.trajectory, "ninguno")
    assert "h = 2" in " ".join(fig_texts(with_det))
    assert "Horizonte de detección" not in " ".join(fig_texts(without))
    plt.close("all")


def test_response_leaves_gaps_for_not_estimated_horizons(result):
    lp = result.lp.copy()
    for h in (11, 12):
        lp.loc[lp["h"] == h, ["beta", "ee", "ic90_inf", "ic90_sup", "phi"]] = np.nan
        lp.loc[lp["h"] == h, "estado"] = "no estimada"
    fig = plot_model2_response(lp, result.trajectory, "ninguno")
    y = [ln for ln in fig.axes[0].lines if ln.get_label() == "β_h (proyección local)"][0].get_ydata()
    assert np.isnan(y[-2:]).all() and not np.isnan(y[:-2]).any()
    plt.close("all")


# --- Variables del informe (RF-28) ---


@pytest.fixture(scope="module")
def mv(result):
    return model2_variables(result)


def _leaves(o):
    if isinstance(o, dict):
        for v in o.values():
            yield from _leaves(v)
    elif isinstance(o, list):
        for v in o:
            yield from _leaves(v)
    else:
        yield o


def test_variables_keys_and_text_only(mv):
    assert list(mv) == ["estimador", "forma_y", "k_elegido", "criterio", "k_bic", "k_aic", "muestra_inicio",
                        "muestra_fin", "n_obs", "n_parametros", "rezagos_hac", "dummies_covid",
                        "truncamiento_espectral", "r2", "r2_ajustado", "ee_regresion", "seleccion", "coef",
                        "efectos", "trayectoria", "granger", "lectura", "lp", "lp_resumen", "diag", "robustez",
                        "robustez_resumen", "no_i0", "limitaciones", "desviaciones"]
    assert all(isinstance(v, str) for v in _leaves(mv))                    # solo texto, ninguna cifra suelta
    assert yaml.safe_load(yaml.safe_dump(mv, allow_unicode=True)) == mv


def test_variables_inventory_matches_the_result(result, mv):
    f = result.coef_footer
    assert mv["k_elegido"] == str(result.K) and mv["criterio"] == "BIC" and mv["k_aic"] == str(result.k_aic)
    assert (mv["muestra_inicio"], mv["muestra_fin"], mv["n_obs"]) == ("2000T2", "2026T2", "105")
    assert mv["n_parametros"] == str(result.K + 11) and mv["rezagos_hac"] == "4"
    assert mv["dummies_covid"] == "2020T2, 2020T3, 2020T4 y 2021T1" and mv["forma_y"] == "primera diferencia"
    assert mv["r2"] == fmt_es(f["r2"], 3) and mv["ee_regresion"] == fmt_es(f["ee_regresion"], 3)
    assert list(mv["seleccion"]) == [f"k{k}" for k in range(1, 9)]


def test_variables_have_the_same_digits_as_the_tables(result, mv):
    for r in result.coefficients.itertuples():
        c = mv["coef"][r.termino]
        assert c["coef"] == fmt_es(r.coef, 3) and c["ee"] == fmt_es(r.ee_hac, 3)
        assert c["ic_inf"] == fmt_es(r.ic_inf, 3) and c["ic_sup"] == fmt_es(r.ic_sup, 3)
    eff = result.effects.set_index("efecto")
    for key, out in (("S", "s"), ("S_rez", "s_rez")):
        assert mv["efectos"][out]["est"] == fmt_es(eff.loc[key, "est"], 3)
        assert mv["efectos"][out]["chi2"] == fmt_es(eff.loc[key, "chi2"], 3)
    assert mv["efectos"]["h1"] == {"signo": result.hyp["h1_signo"], "respaldada": result.hyp["h1_respaldada"]}
    for r in result.trajectory.itertuples():
        assert mv["trayectoria"]["psi"][f"h{r.h}"] == fmt_es(r.psi, 3)
        assert mv["trayectoria"]["r"][f"h{r.h}"] == fmt_es(r.R, 3)
    assert mv["trayectoria"]["h_estrella"] == {"h": str(result.peak["h_star"]), "signo": result.peak["signo"]}
    assert mv["trayectoria"]["h2"] == result.hyp["h2"]
    g = result.granger
    assert mv["granger"] == {"chi2": fmt_es(g["stat"], 3), "gl": str(g["df"]), "p": mv["granger"]["p"],
                             "veredicto": g["veredicto"]}
    assert mv["lectura"]["etiqueta"] == result.reading["etiqueta"]
    assert mv["lp_resumen"] == {"k_de_n": result.comparison_counts["k_de_n"],
                                "horizonte_deteccion": result.comparison_counts["horizonte_deteccion"]}


def test_variables_local_projections_per_horizon(result, mv):
    assert list(mv["lp"]) == [f"h{h}" for h in range(13)]
    h0, h5 = mv["lp"]["h0"], mv["lp"]["h5"]
    assert h0["phi"] == "1,000" and h0["phi_ee"] == "—" and h0["phi_ic90_inf"] == "—" and h0["estado"] == "estimada"
    assert h5["beta"] == fmt_es(result.lp.loc[5, "beta"], 3) and h5["rezagos_hac"] == "6"
    assert h5["n_obs"] == str(105 - 5) and h5["phi_ee"] == fmt_es(result.lp.loc[5, "phi_ee"], 3)


def test_variables_diagnostics_keys_and_not_calculable_as_text(result, mv):
    d = mv["diag"]
    for key in ("bg", "bp", "white", "jb", "reset", "chow_2008t3", "chow_2020t2", "cusum", "vif"):
        assert key in d
    assert d["white"]["veredicto"] in ("pasa", "falla", "no calculable")
    assert "d_ffr_l0" in d["vif"] and "y_lag" in d["vif"]
    full = result.diagnostics.set_index("prueba")
    assert d["bg"]["estadistico"] == fmt_es(full.loc["Breusch-Godfrey", "estadístico"], 3)


def test_variables_not_estimated_and_not_applicable_go_as_text(result):
    r1, r2, r3 = ROBUST2
    variants = [
        VariantOutcome2(r1, "no aplica", "AIC y BIC eligen el mismo K", None, None, None, None, None),
        result.variants[1],
        VariantOutcome2(r3, "no estimada", "grados de libertad insuficientes (< 30)", None, None, None, None, None),
    ]
    lp = result.lp.copy()
    lp.loc[lp["h"] == 12, ["beta", "ee", "ic90_inf", "ic90_sup", "phi"]] = np.nan
    lp.loc[lp["h"] == 12, "estado"] = "no estimada"
    lp.loc[lp["h"] == 12, "motivo"] = "grados de libertad insuficientes (< 30)"
    new = dataclasses.replace(result, variants=variants, lp=lp,
                              robustness_summary=robustness_summary2(result.effects_raw, variants))
    mv = model2_variables(new)
    assert mv["robustez"]["r1"]["estado"] == "no aplica" and mv["robustez"]["r1"]["s_rez"] == "—"
    assert mv["robustez"]["r3"]["estado"] == "no estimada" and "grados de libertad" in mv["robustez"]["r3"]["motivo"]
    assert mv["robustez"]["r2"]["estado"] == "estimada" and mv["robustez"]["r2"]["k"] == str(variants[1].K)
    assert mv["robustez_resumen"]["r1"] == "no aplica" and mv["robustez_resumen"]["r3"] == "no estimada"
    assert mv["lp"]["h12"]["beta"] == "no estimada" and mv["lp"]["h12"]["estado"] == "no estimada"
    assert all(isinstance(v, str) for v in _leaves(mv))


def test_variables_lists_and_non_i0(result, mv):
    assert mv["no_i0"] == "π(t−1) y CRED(t−4)"
    assert len(mv["limitaciones"]) == len(result.limitations) and len(mv["desviaciones"]) == len(result.deviations)
    assert mv["limitaciones"][0].startswith(result.limitations.iloc[0]["limitacion"] + ": ")
    assert mv["trayectoria"]["aviso_rho"] == ""            # ρ̂ < 0,95 en el proceso sintético


def test_variables_functions_write_no_numbers_by_hand():
    tree = ast.parse(open("src/report_vars.py", encoding="utf-8").read())
    checked = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and (node.name == "model2_variables" or node.name.startswith("_m2_")):
            checked += 1
            for sub in ast.walk(node):
                if isinstance(sub, ast.Constant) and isinstance(sub.value, (int, float)) and not isinstance(sub.value, bool):
                    assert sub.value in (0, 3), f"{node.name}: constante numérica {sub.value!r}"   # índice [0] y decimales
    assert checked >= 5
