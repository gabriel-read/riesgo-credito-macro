"""Configuración del pre-registro del Modelo II (spec 004).

Constantes, términos, variantes R1–R3, umbrales y etiquetas. Sin acceso a red, disco ni gráficos
(RNF-7). RF-5, RF-6, RF-14, RF-22, RF-23.
"""

from __future__ import annotations

from dataclasses import dataclass

from scipy.stats import norm

# --- Constantes generales ---

SEED2 = 20261008
K_MAX = 8
K_RANGE = tuple(range(1, K_MAX + 1))
H_MAX = 12
ZERO_RATE_MAX = 0.25                 # promedio trimestral de la tasa ≤ 0,25 % ⇒ tramo de tasa cero
LP_BAND_Z = float(norm.ppf(0.95))    # 1,6449: banda del 90 % de las proyecciones locales
RHO_WARN = 0.95
CHOW_POST_MIN = 30                   # nota de tamaño del Chow si los posteriores útiles son menos
PEAK_TIE_TOL = 1e-12                 # empate del pico de |ψ_h|: gana el menor h (D18)
IC_TIE_TOL = 1e-9                    # empate de AIC o BIC entre dos K: gana el menor K
EXCLUDE_COVID = ("2020Q1", "2021Q4")  # R2: rango inclusivo
EXPECTED_FORM = "ambigua (primera diferencia)"   # DRALACBS, RF-2
EVIDENCE = ("evidencia fuerte", "evidencia parcial", "sin evidencia")


def dffr_cols(K: int) -> list[str]:
    """Columnas de ΔFFR(t), ΔFFR(t−1), …, ΔFFR(t−K)."""
    return [f"d_ffr_l{j}" for j in range(K + 1)]


# término → (columna de la historia, rezago)
CONTROLS: dict[str, tuple[str, int]] = {
    "gdp_l1": ("gdpc1_yoy", 1),
    "d_unemp_l1": ("unrate_d", 1),
    "inflation_l1": ("cpiaucsl_yoy", 1),
    "credit_l4": ("loans_yoy", 4),
}

COVID_QUARTERS = ("2020Q2", "2020Q3", "2020Q4", "2021Q1")
COVID_NAMES = tuple(f"covid_{q.lower()}" for q in COVID_QUARTERS)


@dataclass(frozen=True)
class Spec2:
    """Especificación de la principal o de una robustez del Modelo II."""

    id: str
    label: str
    k_source: str = "bic"                          # "bic" | "aic"
    exclude_range: tuple[str, str] | None = None   # rango inclusivo (primer, último) excluido
    exclude_zero_rate: bool = False
    covid_dummies: bool = True


MAIN2 = Spec2("main", "Especificación principal")
ROBUST2 = [
    Spec2("R1", "K elegido por AIC", k_source="aic"),
    Spec2("R2", "Sin 2020–2021", exclude_range=EXCLUDE_COVID, covid_dummies=False),
    Spec2("R3", "Sin tramos de tasa cero", exclude_zero_rate=True, covid_dummies=False),
]


# --- Etiquetas en español ---

TERM_LABELS2: dict[str, str] = {
    "const": "Constante",
    "y_lag": "ΔDR(t−1) — rezago de la dependiente",
    "d_ffr_l0": "ΔFFR(t) (cambio trimestral de la tasa de la Fed, pp)",
    **{f"d_ffr_l{j}": f"ΔFFR(t−{j})" for j in range(1, K_MAX + 1)},
    "gdp_l1": "PIB(t−1) (variación interanual del PIB real, %)",
    "d_unemp_l1": "ΔU(t−1) (cambio trimestral del desempleo, pp)",
    "inflation_l1": "π(t−1) (inflación interanual, %)",
    "credit_l4": "CRED(t−4) (variación interanual de préstamos, %)",
}


def term_label2(term: str) -> str:
    """Etiqueta en español de un término del Modelo II (incluidas las dummies COVID)."""
    if term in TERM_LABELS2:
        return TERM_LABELS2[term]
    if term.startswith("covid_"):
        year, q = term.removeprefix("covid_").split("q")
        return f"Dummy COVID {year}T{q}"
    return term
