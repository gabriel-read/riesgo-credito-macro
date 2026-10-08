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


# --- Textos fijos de limitaciones y desviaciones (RF-25, RF-26) ---
# Solo texto: ninguna cifra se escribe a mano. Los números y los trimestres detectados los añade el código.

FIXED_LIMITATIONS2: list[tuple[str, str]] = [
    (
        "Endogeneidad de la tasa de fondos federales",
        "La Fed reacciona a la economía y los controles van rezagados un trimestre, por lo que ΔFFR(t) "
        "conserva esa reacción: θ0, S y β_h pueden arrastrar esa endogeneidad.",
    ),
    (
        "ΔFFR es una variación observada, no un shock identificado",
        "La asociación dinámica entre ΔFFR y la morosidad no identifica el efecto de la política monetaria.",
    ),
    (
        "Tramos de tasa cero",
        f"En los tramos con promedio trimestral de la tasa ≤ {str(ZERO_RATE_MAX).replace('.', ',')} % ΔFFR casi "
        "no varía, y los θ_j se identifican con pocos trimestres; R3 excluye esos tramos.",
    ),
    (
        "COVID y proyecciones locales",
        "Las dummies COVID neutralizan 2020T2–2021T1 en la principal, pero las ventanas de resultado de las "
        "proyecciones locales (t + h) que tocan ese período arrastran su efecto sin dummy.",
    ),
    (
        "Efectos base de 2021T2–2022T2 sin dummy",
        "El rebote interanual del PIB, que entra en 2021T3–2022T2 por el rezago, y el crédito del PPP, que "
        "entra en 2021T2–2022T1, no llevan dummy; R2 (sin 2020–2021) sirve de contraste.",
    ),
    (
        "No estacionariedad de π y CRED(t−4)",
        "π y CRED(t−4) figuran «no I(0)» en la spec 001 y entran en su forma fija: la regresión es "
        "desbalanceada y los Wald pueden no seguir su distribución asintótica.",
    ),
    (
        "Granger mide precedencia",
        "La prueba de Granger mide precedencia temporal condicional a los rezagos incluidos; no identifica "
        "el efecto de la política monetaria.",
    ),
    (
        "Inferencia condicional al K elegido",
        "K se elige con los mismos datos con que se estima, y la inferencia posterior no incorpora la "
        "incertidumbre de esa elección.",
    ),
]

# (decisión, referencia, motivo) que no dependen de cifras del código
FIXED_DEVIATIONS2: list[tuple[str, str, str]] = [
    (
        "K elegido por BIC en la principal y por AIC como robustez R1",
        "Skill de econometría de series de tiempo",
        "La skill pide AIC y BIC sobre la misma muestra efectiva; cuando difieren, la principal usa BIC y la "
        "otra va como robustez.",
    ),
    (
        "Controles rezagados y forma fija de los regresores en lugar de la regla de estacionariedad para todas "
        "las series",
        "Skill de econometría de series de tiempo",
        "PIB, ΔU y π se rezagan un trimestre para no condicionar sobre variables macro del mismo trimestre; "
        "conservan su interpretación económica y su no estacionariedad residual se declara como limitación.",
    ),
    (
        "Tramo de tasa cero definido por regla (promedio trimestral de FEDFUNDS ≤ 0,25 %)",
        "Spec 004, robustez R3",
        "La regla fija los trimestres excluidos sin mirar resultados.",
    ),
    (
        "El GDP nominal no se prueba como robustez y la muestra larga desde 1985 queda fuera",
        "Guía, secciones 3.3 y 11",
        "El PIB es aquí un control rezagado y no la variable de interés, y la historia congelada empieza en "
        "1998.",
    ),
]

# Entradas de «Desviaciones del pre-registro» de la spec 004: (fecha, cambio, motivo)
PREREG_DEVIATIONS2: list[tuple[str, str, str]] = [
    (
        "2026-10-08",
        "C1: White es «no calculable» si n − rango(Z_aux) < 30",
        "Con la muestra M la auxiliar completa tiene más columnas que observaciones desde K = 4; la regla se "
        "fijó antes de estimar y sin conocer K.",
    ),
]
