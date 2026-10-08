"""Tests de src/localproj.py (spec 004, tarea 3).

Cubre RF-14 a RF-17 y RNF-4 con el proceso C del plan §7.1 (tolerancias declaradas, no se relajan)
y casos hechos a mano. Datos sintéticos; sin red ni disco.
"""

from __future__ import annotations

import json

import numpy as np
import pandas as pd
import pytest

from src.design2 import build_columns, build_design2, build_lp_design, common_window
from src.dynamics import multipliers
from src.estimation import check_dof, fit_ols_hac, hac_lags
from src.localproj import (
    compare_with_trajectory,
    detection_horizon,
    local_projection,
    run_local_projections,
)
from src.model2_config import EXPECTED_FORM, LP_BAND_Z, MAIN2
from tests.synthetic_model2 import make_full2

DEC = EXPECTED_FORM
P = lambda s: pd.Period(s, "Q-DEC")  # noqa: E731
K = 3


def _setup(full: pd.DataFrame, start: str | None = None):
    end = full.index[-1]
    window = common_window(build_columns(full, DEC), end)
    if start:
        window = (P(start), end)
    return end, window


@pytest.fixture(scope="module")
def small():
    full = make_full2()
    end, window = _setup(full)
    return full, end, window, run_local_projections(full, K, DEC, window, end)


@pytest.fixture(scope="module")
def big():
    full = make_full2(n=4000)
    end, window = _setup(full)
    cols = build_columns(full, DEC)
    fit = fit_ols_hac(build_design2(full, MAIN2, K, DEC, window, end))
    return full, end, window, run_local_projections(full, K, DEC, window, end), multipliers(fit.params, K)


# --- Proceso C (RNF-4) ---


def test_lp_recovers_cumulative_response_and_rate_path(big):
    _, _, _, lp, traj = big
    assert list(lp["h"]) == list(range(13)) and (lp["estado"] == "estimada").all()
    for h in range(13):
        assert abs(lp.loc[h, "beta"] - traj.loc[h, "R"]) <= 0.12, f"beta_{h}"
    for h in range(1, 13):
        assert abs(lp.loc[h, "phi"] - 1.0) <= 0.20, f"phi_{h}"


def test_phi0_is_one_by_construction(small):
    lp = small[3]
    assert lp.loc[0, "phi"] == 1.0
    assert lp.loc[0, "phi_ee"] is None and lp.loc[0, "phi_ic90_inf"] is None and lp.loc[0, "phi_ic90_sup"] is None
    assert lp.loc[0, "phi_nota"] == "por construcción (identidad)"
    assert (lp["phi_nota"].iloc[1:] == "").all()
    num = lp[["beta", "ee", "ic90_inf", "ic90_sup", "phi"]].astype(float).to_numpy()
    assert np.isfinite(num).all()
    assert all(v is not None and np.isfinite(v) for v in lp["phi_ee"].iloc[1:])


def test_lp_is_stable_between_runs(small):
    full, end, window, lp = small
    again = run_local_projections(full, K, DEC, window, end)
    assert lp.equals(again)
    assert json.dumps(lp.loc[0].to_dict(), default=str) == json.dumps(again.loc[0].to_dict(), default=str)


# --- Ventana HAC, banda y muestra (RF-14, RF-16) ---


def test_hac_window_is_max_of_formula_and_h_plus_1(small):
    lp = small[3]
    for h in range(13):
        n = int(lp.loc[h, "n_obs"])
        assert lp.loc[h, "n_obs"] == 105 - h
        assert lp.loc[h, "rezagos_hac"] == max(hac_lags(n), h + 1)
    assert lp.loc[0, "rezagos_hac"] == 4 and lp.loc[12, "rezagos_hac"] == 13


def test_band_is_estimate_plus_minus_z90_times_se(small):
    lp = small[3]
    for h in (0, 5, 12):
        r = lp.loc[h]
        assert r["ic90_inf"] == pytest.approx(r["beta"] - LP_BAND_Z * r["ee"])
        assert r["ic90_sup"] == pytest.approx(r["beta"] + LP_BAND_Z * r["ee"])
        if h > 0:
            assert r["phi_ic90_sup"] == pytest.approx(r["phi"] + LP_BAND_Z * r["phi_ee"])
    assert LP_BAND_Z == pytest.approx(1.6449, abs=1e-4)


def test_beta0_equals_theta0_with_same_se(small):
    full, end, window, lp = small
    main = fit_ols_hac(build_design2(full, MAIN2, K, DEC, window, end))
    assert lp.loc[0, "beta"] == pytest.approx(main.params["d_ffr_l0"], abs=1e-9)
    assert lp.loc[0, "ee"] == pytest.approx(float(np.sqrt(main.cov.loc["d_ffr_l0", "d_ffr_l0"])), abs=1e-9)


# --- Horizonte sin grados de libertad (RF-16) ---


def test_horizon_without_degrees_of_freedom_is_not_estimated_and_others_unaffected():
    full = make_full2()
    end, window = _setup(full, start="2014Q1")         # 50 observaciones en h = 0; k = 14
    lp = run_local_projections(full, K, DEC, window, end)
    for h in range(13):
        dof = (50 - h) - 14
        expected = "estimada" if dof >= 30 else "no estimada"
        assert lp.loc[h, "estado"] == expected, h
    off = lp[lp["estado"] == "no estimada"]
    assert len(off) == 6 and (off["motivo"].str.contains("grados de libertad")).all()
    assert off["beta"].isna().all() and off["ee"].isna().all()
    ok = lp[lp["estado"] == "estimada"]
    assert (ok["motivo"] == "").all()
    for h in (0, 3, 6):
        alone = local_projection(full, K, h, DEC, window, end, "morosidad")
        assert alone.estado == "estimada" and alone.coef == pytest.approx(lp.loc[h, "beta"])
        assert alone.ee == pytest.approx(lp.loc[h, "ee"])
    gone = local_projection(full, K, 9, DEC, window, end, "morosidad")
    assert gone.estado == "no estimada" and "grados de libertad" in gone.motivo
    assert gone.coef is None


def test_incomplete_rank_is_not_estimated(small):
    full, end, window, _ = small
    broken = full.copy()
    broken["unrate_d"] = 0.0                            # ΔU(t−1) colineal con la constante
    out = local_projection(broken, K, 2, DEC, window, end, "morosidad")
    assert out.estado == "no estimada" and "rango" in out.motivo


# --- Horizonte de detección (RF-16, RF-17) ---


def _lp_frame(rows):
    return pd.DataFrame(rows, columns=["h", "estado", "ic90_inf", "ic90_sup"])


def test_detection_horizon_first_band_excluding_zero():
    lp = _lp_frame([(0, "estimada", -0.1, 0.3), (1, "estimada", -0.2, 0.2), (2, "estimada", 0.05, 0.5),
                    (3, "estimada", 0.1, 0.6)])
    assert detection_horizon(lp) == "h2"


def test_detection_horizon_negative_band_counts_and_none():
    assert detection_horizon(_lp_frame([(0, "estimada", -0.5, -0.1)])) == "h0"
    assert detection_horizon(_lp_frame([(0, "estimada", -0.1, 0.1), (1, "estimada", -1, 1)])) == "ninguno"


def test_detection_horizon_skips_not_estimated():
    lp = _lp_frame([(0, "no estimada", np.nan, np.nan), (1, "estimada", 0.1, 0.4)])
    assert detection_horizon(lp) == "h1"


# --- Comparación descriptiva (RF-17) ---


def test_compare_with_trajectory_counts_and_signs():
    traj = pd.DataFrame({"h": range(4), "psi": [0.4, 0.2, 0.1, 0.05], "R": [0.4, 0.6, 0.7, -0.2]})
    lp = pd.DataFrame({
        "h": range(4), "estado": ["estimada", "estimada", "estimada", "no estimada"],
        "beta": [0.4, 0.5, -0.3, np.nan], "ic90_inf": [0.1, -0.2, -0.6, np.nan],
        "ic90_sup": [0.7, 1.2, -0.1, np.nan], "phi": [1.0, 0.9, 1.1, np.nan],
    })
    table, counts = compare_with_trajectory(traj, lp)
    assert list(table.columns) == ["h", "R", "beta", "phi", "mismo_signo", "banda_excluye_cero"]
    assert list(table["mismo_signo"]) == ["sí", "sí", "no", "—"]
    assert list(table["banda_excluye_cero"]) == ["sí", "no", "sí", "—"]
    assert counts["k"] == 1 and counts["n"] == 2 and counts["k_de_n"] == "1 de 2"     # h = 0 y no estimados fuera
    assert counts["horizonte_deteccion"] == "h0"


def test_compare_counts_from_real_lp_exclude_h0(small):
    full, end, window, lp = small
    cols = build_columns(full, DEC)
    main = fit_ols_hac(build_design2(full, MAIN2, K, DEC, window, end))
    table, counts = compare_with_trajectory(multipliers(main.params, K), lp)
    assert counts["n"] == 12 and 0 <= counts["k"] <= 12
    assert counts["k_de_n"] == f"{counts['k']} de 12"
    assert table.loc[0, "mismo_signo"] == "sí"
