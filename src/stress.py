"""Pure contract readers and conditional stress projections (spec 005)."""
from __future__ import annotations

from dataclasses import dataclass
import re

import numpy as np
import pandas as pd

from src.design import ModelDataError
from src.forecast import dynamic, to_level
from src.model1_config import MACRO_TERMS
from src.model2_config import CONTROLS, COVID_NAMES
from src.tables import quarter_label


def quarter_to_period(label: str) -> pd.Period:
    compact = str(label).replace(" ", "").replace("T", "Q")
    if not re.fullmatch(r"\d{4}Q[1-4]", compact):
        raise ModelDataError(f"contrato: trimestre inválido {label}")
    return pd.Period(compact, freq="Q-DEC")


@dataclass(frozen=True)
class ModelContract:
    name: str
    terms: tuple[str, ...]
    columns: dict
    params: tuple[float, ...]
    covariance: np.ndarray
    origin: pd.Period
    dependent_column: str
    zero_terms: tuple[str, ...]
    reading: str | None


def read_model_contract(d: dict, which: str) -> ModelContract:
    """Require the approved order, source columns and lag scheme of each JSON."""
    try:
        if d["dependent"] != "dralacbs" or d["form"] != "primera diferencia":
            raise ModelDataError("contrato: dependiente o forma distinta")
        if which == "modelo1":
            expected = ["const", "y_lag", *MACRO_TERMS, *COVID_NAMES]
            mappings = {"const": None, "y_lag": {"column": "dralacbs_d", "lag": 1},
                        **{term: {"column": col, "lag": 4 if term == "credit_growth" else 0}
                           for term, col in MACRO_TERMS.items()},
                        **{term: None for term in COVID_NAMES}}
            if d["spec"] != "003-modelo-i" or d["columns"] != dict(MACRO_TERMS) or d["credit_lag"] != 4:
                raise ModelDataError("contrato: mapa o rezago del Modelo I distinto")
            zero = ("d_ffr",)
            reading = None
        elif which == "modelo2":
            K = d["k"]
            if type(K) is not int or K not in range(1, 9):
                raise ModelDataError("contrato: K distinto del rango aprobado")
            rates = [f"d_ffr_l{j}" for j in range(K + 1)]
            expected = ["const", "y_lag", *rates, *CONTROLS, *COVID_NAMES]
            mappings = {"const": None, "y_lag": {"column": "dralacbs_d", "lag": 1},
                        **{term: {"column": "fedfunds_d", "lag": j} for j, term in enumerate(rates)},
                        **{term: {"column": col, "lag": lag} for term, (col, lag) in CONTROLS.items()},
                        **{term: None for term in COVID_NAMES}}
            if d["spec"] != "004-modelo-ii" or d["columns"] != mappings or d["k_criterion"] != "BIC":
                raise ModelDataError("contrato: mapa o criterio del Modelo II distinto")
            zero = tuple(rates)
            reading = d["reading"]["etiqueta"]
            if reading not in {"sin evidencia", "evidencia parcial", "evidencia fuerte"}:
                raise ModelDataError("contrato: lectura de evidencia desconocida")
        else:
            raise ModelDataError(f"contrato: modelo desconocido {which}")
        if d["terms"] != expected:
            raise ModelDataError("contrato: términos u orden distintos")
        params = np.asarray(d["params"], dtype=float)
        cov = np.asarray(d["cov_hac"], dtype=float)
        n = len(expected)
        if params.shape != (n,) or cov.shape != (n, n) or not np.isfinite(params).all() or not np.isfinite(cov).all():
            raise ModelDataError("contrato: dimensiones o valores no finitos")
        origin = quarter_to_period(d["sample_end"])
        return ModelContract(which, tuple(expected), mappings, tuple(params), cov.copy(), origin,
                             "dralacbs_d", zero, reading)
    except (KeyError, TypeError, ValueError) as exc:
        if isinstance(exc, ModelDataError):
            raise
        raise ModelDataError(f"contrato {which}: campo ausente o inválido") from exc


def columns_to_design(contract: ModelContract, level_panel: pd.DataFrame,
                      regs: pd.DataFrame) -> pd.DataFrame:
    """Reconstruct historic X exactly, or combine observed lags with scenario paths."""
    historical = level_panel.copy()
    if "dralacbs_d" not in historical:
        historical["dralacbs_d"] = historical["dralacbs"].diff()
    reg_sources = {"gdpc1_yoy": "gdp_growth", "unrate_d": "d_unemp",
                   "cpiaucsl_yoy": "inflation", "fedfunds_d": "d_ffr"}
    X = pd.DataFrame(index=regs.index)
    for term in contract.terms:
        mapping = contract.columns[term]
        if term == "const":
            X[term] = 1.0
        elif term.startswith("covid_"):
            quarter = quarter_to_period(term.removeprefix("covid_").upper())
            X[term] = (X.index == quarter).astype(float)
        else:
            column, lag = mapping["column"], mapping["lag"]
            values = []
            for q in X.index:
                source = q - lag
                if column == "loans_yoy" and "credit_growth" in regs:
                    value = regs.loc[q, "credit_growth"]  # scenario credit already lagged
                elif column in reg_sources and source in regs.index and reg_sources[column] in regs:
                    value = regs.loc[source, reg_sources[column]]
                elif source in historical.index and column in historical:
                    value = historical.loc[source, column]
                elif term == "y_lag":
                    value = 0.0  # overwritten by forecast.dynamic for future recursion
                else:
                    raise ModelDataError(f"{contract.name}: falta {column} en {source} para {q}")
                if not np.isfinite(value):
                    raise ModelDataError(f"{contract.name}: {column} no finito en {source}")
                values.append(float(value))
            X[term] = values
    return X


def project(contract: ModelContract, params: pd.Series, X: pd.DataFrame,
            dr_origin: float, ddr_origin: float, zero_terms: list[str]) -> pd.DataFrame:
    """Approved dynamic forecast, with explicit difference and level anchors."""
    if tuple(params.index) != contract.terms or X.empty:
        raise ModelDataError("contrato: orden de parámetros o horizonte inválido")
    if not X.index.equals(pd.period_range(X.index[0], X.index[-1], freq="Q-DEC")):
        raise ModelDataError("proyección: hueco trimestral")
    if not np.isfinite(params.to_numpy()).all() or not np.isfinite([dr_origin, ddr_origin]).all():
        raise ModelDataError("proyección: parámetros o anclas no finitos")
    coefficients = params.copy()
    coefficients.loc[list(zero_terms)] = 0.0
    ddr = dynamic(coefficients, X, ddr_origin)
    anchor = X.index[0] - 1
    dr = to_level(ddr, "primera diferencia", pd.Series([dr_origin], index=[anchor]), anchor, "dynamic")
    if not np.isfinite(ddr.to_numpy()).all() or not np.isfinite(dr.to_numpy()).all():
        raise ModelDataError(f"{contract.name}: proyección no finita")
    return pd.DataFrame({"ddr": ddr, "dr": dr})


def sym_block(cov: pd.DataFrame, drop: list[str]) -> np.ndarray:
    """Extract the full-rank non-dummy block and symmetrize, never repair it."""
    if list(cov.index) != list(cov.columns):
        raise ModelDataError("covarianza: etiquetas distintas")
    terms = [term for term in cov.index if term not in drop]
    block = cov.loc[terms, terms].to_numpy(dtype=float)
    if not np.isfinite(block).all():
        raise ModelDataError("covarianza: valores no finitos")
    return (block + block.T) / 2


def draw_params(mean: np.ndarray, block: np.ndarray, n: int,
                rng: np.random.Generator) -> np.ndarray:
    """Unconditional multivariate normal coefficients with approved Cholesky."""
    mean = np.asarray(mean, dtype=float)
    if n <= 0 or block.shape != (len(mean), len(mean)) or not np.isfinite(mean).all():
        raise ModelDataError("réplicas: dimensiones inválidas")
    try:
        L = np.linalg.cholesky(block)
    except np.linalg.LinAlgError as exc:
        raise ModelDataError("covarianza: bloque no definido positivo; sin corrección") from exc
    return mean + rng.standard_normal((n, len(mean))) @ L.T


def draw_model_params(contract: ModelContract, n: int = 10000,
                      seed: int = 20261011) -> tuple[np.ndarray, np.ndarray]:
    if contract.reading == "evidencia fuerte":
        raise ModelDataError("regla heredada: evidencia fuerte exige /sdd-change")
    drop = [term for term in contract.terms if term.startswith("covid_")]
    keep = [j for j, term in enumerate(contract.terms) if term not in drop]
    cov = pd.DataFrame(contract.covariance, index=contract.terms, columns=contract.terms)
    try:
        samples = draw_params(np.asarray(contract.params)[keep], sym_block(cov, drop), n,
                              np.random.default_rng(seed))
    except ModelDataError as exc:
        raise ModelDataError(f"{contract.name}: {exc}") from exc
    sensitivity = np.zeros((n, len(contract.terms)))
    sensitivity[:, keep] = samples
    principal = sensitivity.copy()
    principal[:, [contract.terms.index(term) for term in contract.zero_terms]] = 0.0
    return principal, sensitivity


def project_replicas(contract: ModelContract, draws: np.ndarray, X: pd.DataFrame,
                     dr_origin: float, ddr_origin: float) -> np.ndarray:
    """Reuse the approved dynamic function for every coefficient replica."""
    if draws.ndim != 2 or draws.shape[1] != len(contract.terms) or not np.isfinite(draws).all():
        raise ModelDataError(f"{contract.name}: réplicas de parámetros inválidas")
    projected = np.empty((len(draws), len(X)))
    for j, values in enumerate(draws):
        ddr = dynamic(pd.Series(values, index=contract.terms), X, ddr_origin)
        projected[j] = dr_origin + np.cumsum(ddr.to_numpy(dtype=float))
    bad = ~np.isfinite(projected).all(axis=1)
    if bad.any():
        raise ModelDataError(f"{contract.name}: proyección no finita en {int(bad.sum())} réplicas")
    return projected


def _check_paths(point: pd.DataFrame, draws: np.ndarray) -> None:
    if draws.ndim != 2 or draws.shape[1] != len(point) or len(draws) == 0:
        raise ModelDataError("resumen: dimensiones distintas")
    if not np.isfinite(draws).all() or not np.isfinite(point["dr"].to_numpy()).all():
        raise ModelDataError("resumen: valor no finito")


def summarize_delta(point_adv: pd.DataFrame, point_base: pd.DataFrame,
                    draws_adv: np.ndarray, draws_base: np.ndarray) -> pd.DataFrame:
    _check_paths(point_adv, draws_adv)
    _check_paths(point_base, draws_base)
    if not point_adv.index.equals(point_base.index) or draws_adv.shape != draws_base.shape:
        raise ModelDataError("cambio: escenarios o pareo distintos")
    delta = point_adv["dr"] - point_base["dr"]
    draws = draws_adv - draws_base
    percentiles = np.percentile(draws, [5, 50, 95], axis=0, method="linear")
    result = pd.DataFrame({"delta": delta, "p05": percentiles[0], "mediana": percentiles[1],
                           "p95": percentiles[2], "prop_pos": (draws > 0).mean(axis=0)}, index=delta.index)
    peak = int(np.argmax(delta.to_numpy()))
    result.attrs.update(delta_final=float(delta.iloc[-1]), delta_pico=float(delta.iloc[peak]),
                        pico_trimestre=quarter_label(delta.index[peak]), delta_min=float(delta.min()),
                        sin_aumento=bool(delta.max() <= 0), prop_pos_final=float(result.prop_pos.iloc[-1]),
                        prop_pos_pico=float(result.prop_pos.iloc[peak]), final_p05=float(percentiles[0, -1]),
                        final_p95=float(percentiles[2, -1]))
    return result


def summarize_levels(point: pd.DataFrame, draws: np.ndarray, rhos: np.ndarray) -> pd.DataFrame:
    _check_paths(point, draws)
    if len(rhos) != len(draws) or not np.isfinite(rhos).all():
        raise ModelDataError("nivel: réplicas de persistencia inválidas")
    percentiles = np.percentile(draws, [5, 50, 95], axis=0, method="linear")
    outside = (draws < 0) | (draws > 100)
    explosive = np.abs(rhos) >= 1
    result = pd.DataFrame({"dr": point.dr, "p05": percentiles[0], "mediana": percentiles[1],
                           "p95": percentiles[2], "n_fuera_rango": outside.sum(axis=0),
                           "prop_fuera_rango": outside.mean(axis=0)}, index=point.index)
    peak = int(np.argmax(point.dr.to_numpy()))
    result.attrs.update(nivel_final=float(point.dr.iloc[-1]), nivel_pico=float(point.dr.iloc[peak]),
                        nivel_pico_trimestre=quarter_label(point.index[peak]),
                        n_explosivas=int(explosive.sum()), prop_explosivas=float(explosive.mean()),
                        n_fuera_rango=int(outside.any(axis=1).sum()),
                        prop_fuera_rango=float(outside.any(axis=1).mean()),
                        n_trimestres_fuera=int(outside.any(axis=0).sum()),
                        min=float(draws.min()), max=float(draws.max()))
    return result


def rate_sensitivity(principal_delta: pd.DataFrame, sensitivity_delta: pd.DataFrame,
                     principal_draw_delta: np.ndarray, sensitivity_draw_delta: np.ndarray) -> pd.DataFrame:
    """Paired rate contribution; evaluate peak at the sensitivity's point delta."""
    summary = summarize_delta(sensitivity_delta.rename(columns={"delta": "dr"})[["dr"]],
                              principal_delta.rename(columns={"delta": "dr"})[["dr"]],
                              sensitivity_draw_delta, principal_draw_delta)
    result = summary.rename(columns={"delta": "c"})
    peak = int(np.argmax(sensitivity_delta.delta.to_numpy()))
    result.attrs = {"c_final": float(result.c.iloc[-1]), "c_final_p05": float(result.p05.iloc[-1]),
                    "c_final_p95": float(result.p95.iloc[-1]), "c_pico": float(result.c.iloc[peak]),
                    "prop_c_pos_final": float(result.prop_pos.iloc[-1]),
                    "prop_c_pos_pico": float(result.prop_pos.iloc[peak]),
                    "pico_trimestre": quarter_label(result.index[peak])}
    return result


def origin_comparison(adapted_results: dict[str, pd.DataFrame],
                       results_2025q4: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Compare the thirteen calendar steps; stop on a violated delta invariant."""
    if set(adapted_results) != {"base", "severo"} or set(results_2025q4) != {"base", "severo"}:
        raise ModelDataError("RF-12c: faltan base o adverso")
    for source in (adapted_results, results_2025q4):
        if any(len(frame) != 13 or not np.isfinite(frame.dr.to_numpy()).all() for frame in source.values()):
            raise ModelDataError("RF-12c: trece pasos finitos requeridos")
    delta_a = adapted_results["severo"].dr.to_numpy() - adapted_results["base"].dr.to_numpy()
    delta_b = results_2025q4["severo"].dr.to_numpy() - results_2025q4["base"].dr.to_numpy()
    if not np.allclose(delta_a, delta_b, atol=1e-9, rtol=0):
        raise ModelDataError("RF-12c: Δ por paso no coincide entre orígenes")
    rows = []
    for scenario in ("base", "severo"):
        a, b = adapted_results[scenario], results_2025q4[scenario]
        for j in range(13):
            rows.append({"escenario": scenario, "k": j + 1,
                         "trimestre_adaptado": quarter_label(a.index[j]),
                         "trimestre_original": quarter_label(b.index[j]),
                         "dr_adaptado": float(a.dr.iloc[j]), "dr_original": float(b.dr.iloc[j]),
                         "delta_adaptado": float(delta_a[j]) if scenario == "severo" else 0.,
                         "delta_original": float(delta_b[j]) if scenario == "severo" else 0.})
    return pd.DataFrame(rows)


def run_stress(contracts: dict[str, ModelContract], fed: dict[str, pd.DataFrame],
               history: dict, diagnostics: dict[str, pd.DataFrame], oos: pd.DataFrame) -> dict:
    """Orchestrate approved conditional projections from supplied data, no E/S."""
    from src.scenarios import adapt_calendar, to_levels, build_regressors, scenario_d
    from src.stress_tables import stress_variables

    if contracts["modelo2"].reading == "evidencia fuerte":
        raise ModelDataError("regla heredada: evidencia fuerte exige /sdd-change")
    origin = contracts["modelo1"].origin
    if origin != pd.Period("2026Q2") or contracts["modelo2"].origin != origin:
        raise ModelDataError("contrato: origen distinto de 2026Q2")
    full = history["full"]
    hist_fed = fed["historico"].loc[pd.Period("2025Q4")]
    values = {"horizonte": {"origen": origin, "inicio": origin + 1, "fin": origin + 13, "h": 13},
              "replicas": {"n": 10000, "semilla": 20261011}, "dif_modelos": {},
              "sens_tasa": {}, "sens_cal": {}, "sens_cred": {}, "sens_origen": {}}
    level_frames, delta_frames, path_rows, rate_frames, sensitivity_rows, origin_frames = [], [], [], [], [], []
    graphics, model_deltas = {}, {}
    limitation_rows = []
    fixed_limitations = [
        "Endogeneidad: la tasa responde al ciclo; estas asociaciones no identifican shocks.",
        "La regla de tasa en cero es prudencia, no evidencia de efecto nulo.",
        "La letra a tres meses aproxima cambios de FEDFUNDS en base y severo; D usa FEDFUNDS observada.",
        "Calendario Fed adaptado al último trimestre común; la base no coincide con lo observado.",
        "La tasa y la inflación bajan en el adverso; D comparte actividad y coincide con severo bajo la regla principal.",
        "Regresores no I(0): inflación y crédito, conforme al pre-registro.",
        "Bandas solo de parámetros; omiten escenario, especificación, endogeneidad e incertidumbre del estimador HAC.",
        "Los niveles omiten innovaciones; no son intervalos de predicción.",
        "Crédito supuesto común después del tramo observado; modifica niveles, no el cambio.",
        "Recursión con un solo rezago de ΔDR; Modelo II tiene cambio cero en el primer paso bajo la regla de tasa.",
    ]
    def rows(frame, model, scenario):
        copy = frame.copy()
        copy.attrs = {}
        copy.insert(0, "trimestre", [quarter_label(q) for q in copy.index])
        copy.insert(0, "escenario", scenario)
        copy.insert(0, "modelo", model)
        return copy.reset_index(drop=True)

    for model, contract in contracts.items():
        principal_draws, raw_draws = draw_model_params(contract)
        rhos = principal_draws[:, contract.terms.index("y_lag")]
        params = pd.Series(contract.params, index=contract.terms)

        def build(mode="adapted", credit="last", include_d=False):
            anchor = pd.Period("2025Q4") if mode == "from_2025q4" else origin
            observed = full.loc[:anchor]
            level_anchor = float(full.loc[anchor, "dralacbs"])
            diff_anchor = float(full.loc[anchor, "dralacbs_d"])
            points, designs, regs_by_scenario, levels_by_scenario = {}, {}, {}, {}
            for scenario in ("base", "severo"):
                adapted = adapt_calendar(fed[scenario], hist_fed, anchor, mode)
                # FEDFUNDS anchors its implicit proxy level; only scenario changes enter models.
                levels = to_levels(adapted, history["gdpc1"], history["cpiaucsl"],
                                   float(full.loc[anchor, "unrate"]), float(full.loc[anchor, "fedfunds"]))
                regs = build_regressors(levels, full, credit_rule=credit)
                levels["fed_quarter"] = adapted["fed_quarter"]
                regs_by_scenario[scenario], levels_by_scenario[scenario] = regs, levels
            if include_d:
                regs_by_scenario["propio"] = scenario_d(regs_by_scenario["severo"], full)
                levels = levels_by_scenario["severo"].copy()
                levels["d_ffr"] = regs_by_scenario["propio"].d_ffr
                levels["fedfunds"] = float(full.loc[anchor, "fedfunds"]) + levels.d_ffr.cumsum()
                levels_by_scenario["propio"] = levels
            for scenario, regs in regs_by_scenario.items():
                design = columns_to_design(contract, observed, regs)
                designs[scenario] = design
                points[scenario] = project(contract, params, design, level_anchor, diff_anchor,
                                           list(contract.zero_terms))
            return points, designs, regs_by_scenario, levels_by_scenario, level_anchor, diff_anchor

        points, designs, regs, linked, dr_anchor, ddr_anchor = build(include_d=True)
        draws = {s: project_replicas(contract, principal_draws, X, dr_anchor, ddr_anchor)
                 for s, X in designs.items()}
        level_summaries = {s: summarize_levels(points[s], draws[s], rhos) for s in points}
        delta_summaries = {s: summarize_delta(points[s], points["base"], draws[s], draws["base"])
                           for s in ("severo", "propio")}
        model_deltas[model] = delta_summaries
        graphics[model] = (level_summaries, delta_summaries)
        observed_credit = int(regs["base"].credit_observed.sum())
        values[model] = {"credito": {"n_observados": observed_credit, "n_supuestos": len(regs["base"]) - observed_credit}}
        for scenario, summary in level_summaries.items():
            values[model][scenario] = {k: summary.attrs[k] for k in ("nivel_final", "nivel_pico", "nivel_pico_trimestre")}
            level_frame = rows(summary, model, scenario)
            for key in ("n_explosivas", "prop_explosivas", "n_trimestres_fuera"):
                level_frame[key] = summary.attrs[key]
            for column, attr in (("n_replicas_fuera_rango", "n_fuera_rango"),
                                 ("prop_replicas_fuera_rango", "prop_fuera_rango"),
                                 ("nivel_min", "min"), ("nivel_max", "max")):
                level_frame[column] = summary.attrs[attr]
            level_frame["prop_trimestres_fuera"] = summary.attrs["n_trimestres_fuera"] / len(summary)
            level_frames.append(level_frame)
            if scenario != "base":
                delta = delta_summaries[scenario]
                values[model][scenario].update({
                    "delta_final": delta.attrs["delta_final"], "delta_final_p05": delta.attrs["final_p05"],
                    "delta_final_p95": delta.attrs["final_p95"], "delta_pico": delta.attrs["delta_pico"],
                    "delta_pico_trimestre": delta.attrs["pico_trimestre"], "delta_min": delta.attrs["delta_min"],
                    "delta_sin_aumento": delta.attrs["sin_aumento"], "delta_prop_pos_final": delta.attrs["prop_pos_final"],
                    "delta_prop_pos_pico": delta.attrs["prop_pos_pico"]})
                delta_frame = rows(delta, model, scenario)
                for key in ("delta_final", "delta_pico", "pico_trimestre", "delta_min", "sin_aumento", "prop_pos_final", "prop_pos_pico"):
                    delta_frame[key] = delta.attrs[key]
                delta_frame["nivel_pico"] = summary.attrs["nivel_pico"]
                delta_frame["nivel_pico_trimestre"] = summary.attrs["nivel_pico_trimestre"]
                delta_frames.append(delta_frame)
            X = designs[scenario]
            for q in X.index:
                terms = X.loc[q]
                path_rows.append({"modelo": model, "escenario": scenario, "trimestre": quarter_label(q),
                                  "trimestre_fed": linked[scenario].loc[q, "fed_quarter"],
                                  "PIB": float(terms["gdp_growth" if model == "modelo1" else "gdp_l1"]),
                                  "ΔU": float(terms["d_unemp" if model == "modelo1" else "d_unemp_l1"]),
                                  "π": float(terms["inflation" if model == "modelo1" else "inflation_l1"]),
                                  "ΔFFR": float(terms[contract.zero_terms[0]]),
                                  "CRED": float(terms["credit_growth" if model == "modelo1" else "credit_l4"]),
                                  "credito_observado": bool(regs[scenario].loc[q, "credit_observed"]),
                                  "U_implicito": float(linked[scenario].loc[q, "unrate"]),
                                  "tasa_proxy_implicita": float(linked[scenario].loc[q, "fedfunds"]),
                                  "tasa_proxy_negativa": bool(linked[scenario].loc[q, "fedfunds"] < 0)})
        all_levels = np.stack(list(draws.values()), axis=2)
        outside = (all_levels < 0) | (all_levels > 100)
        values[model]["fuera_rango"] = {"n": int(outside.any(axis=(1, 2)).sum()),
                                        "prop": float(outside.any(axis=(1, 2)).mean()),
                                        "min": float(all_levels.min()), "max": float(all_levels.max())}
        values[model]["explosivas"] = {"n": int((np.abs(rhos) >= 1).sum()), "prop": float((np.abs(rhos) >= 1).mean())}
        # Union of replica identities over all three scenarios, not a sum of counts.
        for level_frame in level_frames[-len(level_summaries):]:
            for column, leaf in (("n_replicas_fuera_rango_modelo", "n"),
                                 ("prop_replicas_fuera_rango_modelo", "prop"),
                                 ("nivel_min_modelo", "min"), ("nivel_max_modelo", "max")):
                level_frame[column] = values[model]["fuera_rango"][leaf]
        sensitivity_points = {s: project(contract, params, X, dr_anchor, ddr_anchor, []) for s, X in designs.items()}
        sensitivity_draws = {s: project_replicas(contract, raw_draws, X, dr_anchor, ddr_anchor) for s, X in designs.items()}
        values["sens_tasa"][model] = {}
        for scenario in ("severo", "propio"):
            sensitive_delta = summarize_delta(sensitivity_points[scenario], sensitivity_points["base"],
                                               sensitivity_draws[scenario], sensitivity_draws["base"])
            contribution = rate_sensitivity(delta_summaries[scenario], sensitive_delta,
                                            draws[scenario] - draws["base"],
                                            sensitivity_draws[scenario] - sensitivity_draws["base"])
            values["sens_tasa"][model][scenario] = {key: contribution.attrs[key] for key in
                ("c_final", "c_final_p05", "c_final_p95", "c_pico", "prop_c_pos_final", "prop_c_pos_pico")}
            rate_frame = rows(contribution, model, scenario)
            for key, value in contribution.attrs.items():
                rate_frame[key] = value
            rate_frame["rotulo"] = "sensibilidad, no efecto estimado"
            rate_frames.append(rate_frame)
        original, _, _, _, _, _ = build(mode="from_2025q4")
        compare = origin_comparison({s: points[s] for s in ("base", "severo")}, original)
        compare.insert(0, "modelo", model)
        compare["DR_observado"] = [float(full.loc[quarter_to_period(q), "dralacbs"])
                                   if quarter_to_period(q) <= origin else "no aplica" for q in compare.trimestre_original]
        origin_frames.append(compare)
        values["sens_origen"][model] = {}
        for scenario, frame in original.items():
            values["sens_origen"][model][scenario] = {"nivel_final": float(frame.dr.iloc[-1]),
                "nivel_pico": float(frame.dr.max()), "nivel_pico_trimestre": quarter_label(frame.dr.idxmax())}
        values["sens_origen"][model]["severo"]["delta_k13"] = float(original["severo"].dr.iloc[-1] - original["base"].dr.iloc[-1])
        post, _, _, _, _, _ = build(mode="post_2026q2")
        post_delta = post["severo"].dr - post["base"].dr
        values["sens_cal"][model] = {"delta_final_2029t1": float(post_delta.iloc[-1]),
            "delta_principal_2029t1": float(delta_summaries["severo"].loc[pd.Period("2029Q1"), "delta"]),
            "delta_pico": float(post_delta.max())}
        sensitivity_rows.append({"modelo": model, "escenario": "severo", "sensibilidad": "calendario posterior",
            "regla": "post_2026q2", "nivel_final": float(post["severo"].dr.iloc[-1]),
            "nivel_pico": float(post["severo"].dr.max()), "nivel_pico_trimestre": quarter_label(post["severo"].dr.idxmax()),
            "delta_final": float(post_delta.iloc[-1]), "delta_principal_2029t1": values["sens_cal"][model]["delta_principal_2029t1"],
            "delta_pico": float(post_delta.max()), "n_trimestres": len(post_delta), "n_alcanzados": len(post_delta)})
        values["sens_cred"][model] = {s: {} for s in ("base", "severo")}
        for credit, label in (("zero", "cero"), ("mean", "media")):
            variants, _, _, _, _, _ = build(credit=credit)
            for scenario, frame in variants.items():
                attributes = {"nivel_final": float(frame.dr.iloc[-1]), "nivel_pico": float(frame.dr.max()),
                              "nivel_pico_trimestre": quarter_label(frame.dr.idxmax())}
                values["sens_cred"][model][scenario][label] = attributes
                sensitivity_rows.append({"modelo": model, "escenario": scenario, "sensibilidad": "crédito",
                    "regla": label, **attributes, "delta_final": float(variants["severo"].dr.iloc[-1] - variants["base"].dr.iloc[-1]),
                    "delta_principal_2029t1": "no aplica", "delta_pico": "no aplica", "n_trimestres": len(frame),
                    "n_alcanzados": len(frame) - observed_credit})
        for statement in fixed_limitations:
            limitation_rows.append({"modelo": model, "tipo": "fija", "limitacion": statement})
        for _, diagnostic in diagnostics[model].iterrows():
            if diagnostic["veredicto"] == "falla":
                limitation_rows.append({"modelo": model, "tipo": "detectada", "limitacion": str(diagnostic["prueba"]) + ": falla; discutir en informe."})
        for kind, condition, wording in (
            ("explosivas", values[model]["explosivas"]["n"] > 0, "Réplicas con |ρ| ≥ 1 reportadas, sin descartarlas."),
            ("fuera_rango", values[model]["fuera_rango"]["n"] > 0, "Niveles fuera de rango reportados, sin truncarlos."),
        ):
            if condition:
                limitation_rows.append({"modelo": model, "tipo": kind, "limitacion": wording})
    for _, forecast in oos.iterrows():
        limitation_rows.append({"modelo": "modelo1", "tipo": "fuera de muestra",
                               "limitacion": str(forecast["pronostico"]) + ": " + str(forecast["veredicto"]) + ", " + str(forecast["significancia"])})
    comparison = []
    for scenario in ("severo", "propio"):
        a, b = model_deltas["modelo1"][scenario].delta, model_deltas["modelo2"][scenario].delta
        difference = a - b
        # RF-11: difference between each model's peak, not the peak of a-b.
        values["dif_modelos"][scenario] = {"delta_final": float(difference.iloc[-1]),
                                            "delta_pico": float(a.max() - b.max())}
        for q in a.index:
            comparison.append({"escenario": scenario, "trimestre": quarter_label(q), "delta_modelo1": float(a.loc[q]),
                               "delta_modelo2": float(b.loc[q]), "diferencia_I_II": float(difference.loc[q])})
    tables = {"stress_paths": pd.DataFrame(path_rows), "stress_levels": pd.concat(level_frames, ignore_index=True),
              "stress_delta": pd.concat(delta_frames, ignore_index=True), "stress_rate_sensitivity": pd.concat(rate_frames, ignore_index=True),
              "stress_models": pd.DataFrame(comparison), "stress_sensitivity": pd.DataFrame(sensitivity_rows),
              "stress_origin": pd.concat(origin_frames, ignore_index=True), "stress_limitations": pd.DataFrame(limitation_rows)}
    return {"tables": tables, "graphics": graphics, "variables": stress_variables(values)}
