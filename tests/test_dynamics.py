"""Tests de src/dynamics.py (spec 004, tarea 2).

Cubre RF-6, RF-7, RF-10 a RF-13, RNF-2 y RNF-3 con los procesos A, B y E del plan §7.1 (tolerancias
declaradas, no se relajan) y con formas cerradas. Datos sintéticos; sin red ni disco.
"""

from __future__ import annotations

from types import SimpleNamespace

import numpy as np
import pandas as pd
import pytest
from scipy.stats import chi2, norm

from src.design2 import build_columns, build_design2, common_window
from src.dynamics import (
    cumulative_effects,
    evidence_reading,
    granger_lags,
    hypotheses,
    multipliers,
    peak_horizon,
    select_k,
)
from src.estimation import fit_ols_hac
from src.model2_config import EXPECTED_FORM, MAIN2, SEED2
from tests.synthetic_model2 import GAMMA, RHO, THETA, make_full2

DEC = EXPECTED_FORM


def _fit(full: pd.DataFrame, K: int):
    cols = build_columns(full, DEC)
    end = full.index[-1]
    window = common_window(cols, end)
    return fit_ols_hac(build_design2(full, MAIN2, K, DEC, window, end))


def _fake_fit(params: dict, cov: np.ndarray):
    s = pd.Series(params, dtype=float)
    return SimpleNamespace(params=s, cov=pd.DataFrame(cov, index=s.index, columns=s.index))


# --- Proceso A: recuperación punta a punta (RNF-2) ---


@pytest.fixture(scope="module")
def fit_a():
    return _fit(make_full2(n=4000), 3)


def test_recovers_known_parameters_end_to_end(fit_a):
    p = fit_a.params
    for j, theta in enumerate(THETA):
        assert abs(p[f"d_ffr_l{j}"] - theta) <= 0.05, f"theta_{j}"
    assert abs(p["y_lag"] - RHO) <= 0.05
    for term, g in GAMMA.items():
        assert abs(p[term] - g) <= 0.05, term
    eff = cumulative_effects(fit_a, 3)
    assert abs(eff["S"]["est"] - sum(THETA)) <= 0.10
    assert abs(eff["S_rez"]["est"] - sum(THETA[1:])) <= 0.10


# --- Efectos acumulados (RF-10) ---


def test_cumulative_effects_closed_form():
    params = {"const": 0.1, "y_lag": 0.5, "d_ffr_l0": 1.0, "d_ffr_l1": 2.0, "d_ffr_l2": -0.5}
    cov = np.diag([1.0, 1.0, 0.04, 0.09, 0.01])
    cov[2, 3] = cov[3, 2] = 0.02                     # cov(θ0, θ1)
    fit = _fake_fit(params, cov)
    eff = cumulative_effects(fit, 2)
    s, sr = eff["S"], eff["S_rez"]
    assert s["est"] == pytest.approx(2.5) and sr["est"] == pytest.approx(1.5)
    var_s = 0.04 + 0.09 + 0.01 + 2 * 0.02
    assert s["se"] == pytest.approx(np.sqrt(var_s))
    assert s["chi2"] == pytest.approx(2.5**2 / var_s)
    assert s["p"] == pytest.approx(chi2.sf(2.5**2 / var_s, 1))
    z = norm.ppf(0.975)
    assert s["ic_inf"] == pytest.approx(2.5 - z * np.sqrt(var_s))
    assert s["ic_sup"] == pytest.approx(2.5 + z * np.sqrt(var_s))
    var_sr = 0.09 + 0.01
    assert sr["se"] == pytest.approx(np.sqrt(var_sr))
    assert sr["p"] == pytest.approx(chi2.sf(1.5**2 / var_sr, 1))


# --- Multiplicadores ψ_h y R(h) (RF-11) ---


def _impulse_response(theta: list[float], rho: float, hmax: int) -> np.ndarray:
    """Respuesta de ΔDR a un impulso unitario en ΔFFR(t), por simulación de la recursión."""
    x = np.zeros(hmax + 1)
    x[0] = 1.0
    dy = np.zeros(hmax + 1)
    for t in range(hmax + 1):
        dy[t] = (rho * dy[t - 1] if t > 0 else 0.0) + sum(
            theta[j] * x[t - j] for j in range(len(theta)) if t - j >= 0
        )
    return dy


def test_multipliers_closed_form_k1():
    params = pd.Series({"const": 0.0, "y_lag": 0.5, "d_ffr_l0": 0.4, "d_ffr_l1": 0.2})
    tr = multipliers(params, 1)
    assert list(tr.columns) == ["h", "psi", "R"] and list(tr["h"]) == list(range(13))
    assert tr["psi"].iloc[0] == pytest.approx(0.4)
    assert tr["psi"].iloc[1] == pytest.approx(0.2 + 0.5 * 0.4)
    assert tr["psi"].iloc[2] == pytest.approx(0.5 * 0.4)
    assert tr["psi"].iloc[3] == pytest.approx(0.5**2 * 0.4)
    assert np.allclose(tr["R"], tr["psi"].cumsum())


@pytest.mark.parametrize("K,rho", [(3, 0.5), (5, 0.9), (2, -0.3)])
def test_multipliers_match_a_simulated_impulse_response(K, rho):
    theta = [0.3 - 0.07 * j for j in range(K + 1)]
    params = pd.Series({"const": 0.0, "y_lag": rho, **{f"d_ffr_l{j}": theta[j] for j in range(K + 1)}})
    assert np.allclose(multipliers(params, K)["psi"], _impulse_response(theta, rho, 12))


# --- Trimestre de efecto máximo h* (RF-11) ---


def test_peak_horizon_basic_and_sign():
    pk = peak_horizon(pd.Series([0.1, 0.4, -0.6, 0.2]))
    assert pk["h_star"] == 2 and pk["signo"] == "−"
    pk = peak_horizon(pd.Series([0.1, 0.4, 0.3]))
    assert pk["h_star"] == 1 and pk["signo"] == "+"


def test_peak_horizon_tie_goes_to_smaller_h():
    assert peak_horizon(pd.Series([0.2, 0.5, -0.5, 0.5]))["h_star"] == 1
    assert peak_horizon(pd.Series([0.5, 0.5]))["h_star"] == 0
    assert peak_horizon(pd.Series([0.1, 0.5, 0.5 + 1e-13]))["h_star"] == 1   # dentro de PEAK_TIE_TOL
    assert peak_horizon(pd.Series([0.1, 0.5, 0.5 + 1e-9]))["h_star"] == 2    # fuera de la tolerancia


# --- Proceso E: Granger (RF-12) ---


def test_granger_rejects_with_nonzero_lags():
    g = granger_lags(_fit(make_full2(n=500), 3), 3)
    assert g["df"] == 3 and g["p"] < 0.05 and g["veredicto"] == "rechaza"


def test_granger_does_not_reject_with_zero_lags():
    full = make_full2(n=500, theta=(0.30, 0.0, 0.0, 0.0))
    g = granger_lags(_fit(full, 3), 3)
    assert g["df"] == 3 and g["p"] >= 0.05 and g["veredicto"] == "no rechaza"


def test_granger_excludes_theta0():
    params = {"const": 0, "y_lag": 0, "d_ffr_l0": 100.0, "d_ffr_l1": 0.0, "d_ffr_l2": 0.0}
    g = granger_lags(_fake_fit(params, np.diag([1.0, 1.0, 1.0, 1.0, 1.0])), 2)
    assert g["stat"] == pytest.approx(0.0) and g["df"] == 2 and g["p"] == pytest.approx(1.0)


# --- H1, H2 y regla de lectura (RF-13) ---


def _eff(s, p_s, sr, p_sr):
    return {"S": {"est": s, "p": p_s}, "S_rez": {"est": sr, "p": p_sr}}


def test_hypotheses():
    h = hypotheses(_eff(0.5, 0.01, 0.3, 0.2), {"h_star": 2, "signo": "+"})
    assert (h["h1_signo"], h["h1_respaldada"], h["h2"]) == ("sí", "sí", "sí")
    h = hypotheses(_eff(0.5, 0.20, 0.3, 0.2), {"h_star": 0, "signo": "+"})
    assert (h["h1_signo"], h["h1_respaldada"], h["h2"]) == ("sí", "no", "no")
    h = hypotheses(_eff(-0.5, 0.001, 0.3, 0.2), {"h_star": 1, "signo": "−"})
    assert (h["h1_signo"], h["h1_respaldada"], h["h2"]) == ("no", "no", "sí")


@pytest.mark.parametrize("p_gr,s_rez,p_sr,label,c1,c2,contrary", [
    (0.01, 0.4, 0.01, "evidencia fuerte", True, True, False),
    (0.01, 0.4, 0.30, "evidencia parcial", True, False, False),
    (0.30, 0.4, 0.01, "evidencia parcial", False, True, False),
    (0.30, 0.4, 0.30, "sin evidencia", False, False, False),
    (0.30, -0.4, 0.01, "sin evidencia", False, False, True),
    (0.01, -0.4, 0.01, "evidencia parcial", True, False, True),
])
def test_evidence_reading_three_outcomes_and_contrary_mark(p_gr, s_rez, p_sr, label, c1, c2, contrary):
    r = evidence_reading({"p": p_gr}, _eff(0.5, 0.01, s_rez, p_sr))
    assert r["etiqueta"] == label and r["c1"] is c1 and r["c2"] is c2
    assert r["signo_contrario"] is contrary


def test_evidence_reading_uses_strict_5_percent():
    assert evidence_reading({"p": 0.05}, _eff(0.5, 0.01, 0.4, 0.05))["etiqueta"] == "sin evidencia"


# --- select_k (RF-6, RF-7) y proceso B ---


def _fake_fits(aic: dict, bic: dict):
    return {k: SimpleNamespace(k=k + 10, nobs=105, sm_result=SimpleNamespace(aic=aic[k], bic=bic[k]))
            for k in aic}


def test_select_k_picks_minimums_and_resolves_ties_to_smaller_k():
    aic = {1: 10.0, 2: 8.0, 3: 8.0, 4: 9.0}
    bic = {1: 20.0, 2: 21.0, 3: 19.0, 4: 19.0}
    sel = select_k(_fake_fits(aic, bic))
    assert sel["k_aic"] == 2 and sel["k_bic"] == 3          # AIC empata 2 y 3 → 2; BIC empata 3 y 4 → 3
    t = sel["table"]
    assert list(t["K"]) == [1, 2, 3, 4] and list(t["n_params"]) == [11, 12, 13, 14]
    assert list(t["nobs"]) == [105] * 4 and list(t["aic"]) == [10.0, 8.0, 8.0, 9.0]


def test_select_k_recovers_true_k_with_bic():
    full = make_full2(n=2000, seed_x=SEED2, seed_e=SEED2 + 1)
    fits = {K: _fit(full, K) for K in range(1, 9)}
    assert len({f.nobs for f in fits.values()}) == 1         # misma muestra efectiva
    sel = select_k(fits)
    assert sel["k_bic"] == 3
    assert np.isclose(sel["table"].loc[sel["table"]["K"] == 3, "bic"].iloc[0], fits[3].sm_result.bic)
