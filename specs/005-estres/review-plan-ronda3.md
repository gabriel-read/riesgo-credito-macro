VEREDICTO: CAMBIOS NECESARIOS

Revisión independiente acotada, **ronda 3**, de la v4 del borrador de spec y plan de la 005 (Estrés), 11-oct-2026. Autor: subagente `revisor-econometrico` de Claude Code (otra instancia que las de las rondas 1 y 2), con solo rutas, criterios y el alcance indicado por el usuario. Las rondas anteriores se conservan en `review-plan-ronda1.md` y `review-plan-ronda2.md`. Revisión de plan/pre-registro: no se estimó ni proyectó con datos reales. Los borradores no están aprobados y esta revisión no los aprueba. Informe copiado tal cual lo entregó el subagente; los cambios 1 a 7 se incorporaron después en la v5 (ver nota final).

**En corto.** La v4 resuelve casi todo lo que pidieron las rondas 1 y 2. El diseño es sólido y no hace falta rediseñar nada. Quedan dos defectos de texto que conviene corregir antes de aprobar:
- **Propiedad A.** Uno de sus supuestos casos de fallo es falso.
- **RF-12c.** Le faltan reglas para que sus niveles sean únicos.

Lo demás son verificaciones que ya se pueden cerrar con la descarga hecha (huellas completas, regla de corte de D) y detalles menores. Ningún punto exige un cambio SDD de 001, 003 ni 004. No modificó nada del repositorio.

## Qué comprobó y cómo
- **Documentos leídos:** spec y plan v4, las dos rondas previas, los dos documentos de Codex, constitución, guía (§7–8), los JSON y `panel.csv`.
- **Código citado:** `src/forecast.py`, `panel.py`, `fred_io.py` y `model1.py` (`out_of_sample`, `OOSResult`), además de `design.py`, `design2.py` y `estimation.py`. Lo comprobó con grep y lectura directa.
- **JSON:**
  - Bloques sin dummies de 7 (Modelo I) y 8 (Modelo II) términos.
  - Autovalor mínimo 7,00e-7 y 7,08e-7; Cholesky sin error.
  - Asimetría ≤ 1,1e-16 (no es exactamente 0, pero es irrelevante).
- **Archivos de la Fed** (`data/scenarios/fed/2026-final/2026-10-11/`, todavía sin versionar):
  - Las tres huellas sha256 coinciden con las de la ronda 2 (Historic `6d08aadc…f653`, Baseline `76e23669…1cbc`, Severely Adverse `45c2859a…ebbb`).
  - Los CSV tienen finales de línea CRLF y `core.autocrlf=true`.
  - `git check-attr` da `text: unset`, y `git hash-object` con y sin filtros produce el mismo blob: los bytes se preservan.
  - El manifiesto existe, con BOM y con `downloaded_at_utc` = 2026-10-12T03:25Z; el nombre del directorio usa la fecha local.
- **`data/raw/manifest.csv`:** la última descarga de todas las series es la del 2026-10-02. `outputs/tables/stationarity.csv` existe.
- **Simulación sintética** con coeficientes inventados del orden de los reales, en el scratchpad (`simA.py`, `simA3.py`), para los dos modelos.
- **Tests:** `uv run pytest -q` da 774 passed.

## Derivación de la recursión de δ
Con β común, Y en primera diferencia y un solo rezago de ΔDR (así son los dos JSON):

δ_t = ρ·δ_{t−1} + Σ_j β_j·[x_j^a(t) − x_j^b(t)] + (ε^a_t − ε^b_t), con δ_{T0} = 0 si el ancla ΔDR es común, y Δ(T0+k) = Σ_{i≤k} δ.

Cómo entra cada regresor en esa diferencia:
- **ΔU y ΔFFR**, con rezago ℓ:
  - La diferencia en el paso i es D_{i−ℓ}, donde D_m = (p^a_m − p^b_m) − (p^a_{m−1} − p^b_{m−1}) y p_0 es la referencia común. Si i ≤ ℓ, es 0 (lo observado es común).
  - En el Modelo II (ℓ = 1) con θ = 0, Δ(1) = 0 exactamente. Lo confirmó: con θ libre, Δ(1) = θ₀·D₁.
- **PIB y π interanuales en logaritmos**, con L^s(T0+i) = L_obs(T0) + Σ_{m≤i} a^s_m:
  - La diferencia es 100·Σ_{m=max(1, i−3)}^{i} (a^a_m − a^b_m).
  - El crecimiento observado de t−4 y el nivel del origen se cancelan, sin depender del origen. Con rezago 1, se desplaza un paso.
- **CRED(t−4)**, mitad observado y mitad supuesto: común a los dos escenarios, se cancela.

## Resultados de la simulación sintética

| Caso | Modelo I | Modelo II | ¿Coincide al mover el origen? |
|---|---|---|---|
| Se cumplen las condiciones, θ = 0 | 6,7e-16 | 4,4e-16 | sí |
| Se cumplen las condiciones, θ libre | 1,1e-15 | 2,2e-16 | sí |
| Paso 1 medido contra el **observado** del origen (referencia común) | 1,8e-15 | 8,9e-16 | **sí**: la spec dice que no |
| Innovaciones idénticas no nulas | 8,9e-16 | 4,4e-16 | sí |
| Innovaciones distintas | 0,26 | 0,61 | no |
| β distintos entre escenarios | 0,074 | 0,029 | no |
| Interanual con variación % simple (no logarítmica) | 6,5e-3 | 7,2e-4 | no |
| Y en logit | 1,45 | 0,44 | no |
| Referencia del paso 1 distinta en cada escenario | 0,047 | 0,082 | no |
| Ancla DR o ΔDR distinta entre escenarios, en un solo origen | 0,27 / 0,17 | 0,33 / 0,23 | no |
| U observado en T0 distinto solo en la base | **6,7e-16** | 0,11 | Modelo I: sí (U(T0) no entra) |
| Tramo truncado (RF-12a) frente al completo | 1,45 | 1,19 | no (es lo esperado) |

Sobre las tolerancias:
- **RNF-5 (`atol` 1e-12):** con escalas realistas el error es ≈ 1e-15. Con escalas grandes (constante 50, β = 1, ρ = 0,9, niveles ~3 000) sube a 9e-13, justo en el límite.
- **RF-12c (`atol` 1e-9):** holgada.

## Estado de hallazgos previos

| Ronda | # | Estado | Dónde (v4) |
|---|---|---|---|
| R1 | 1 Recorte del escenario | Resuelto | spec:29-32, :98-99; plan:75 |
| R1 | 2 Condicionada | Resuelto | spec:72-73, :126; plan:68 |
| R1 | 3 Identidades | **Parcial**: falta el caso de test de π con la base 2025T4 de dos meses | spec:35-36, :108; plan:78 |
| R1 | 4 Entradas de `stress` | Resuelto | plan:17-18; spec:26 |
| R1 | 5 S3 | Resuelto (sustituido por D) | spec:57 |
| R1 | 6 RF-10(c) | Resuelto | spec:96, :126 |
| R1 | 7 D-CRED | Resuelto | spec:38, :83, :98 |
| R1 | 8 Puntual, pico, comparación | Resuelto | spec:40-41, :77, :97 |
| R1 | 9 Pre-registros del plan | Resuelto (Cholesky con error en vez de truncar) | spec:70-71; plan:54, :59 |
| R1 | 10 Archivos de la Fed | **Parcial**: las huellas solo van abreviadas | plan:24-27 |
| R1 | 11 RF-5 | Resuelto | spec:90; plan:19 |
| R1 | 12–18 | Resueltos | spec:11, :64, :26, :110, :101, :95; plan:21, :24 |
| R2 | 1 Invariancia y opciones | Resuelto, pero su formulación tiene un error (cambio 1) | spec:31, :48, :98-99, :110 |
| R2 | 2 RF-10 verificable | Resuelto | spec:96; plan:46 |
| R2 | 3 sha256 frente a git | Resuelto (el patrón difiere del plan, cambio 3) | plan:23; `.gitattributes` |
| R2 | 4 Nombres y huellas | **Parcial**: huellas abreviadas | plan:26 |
| R2 | 5 Regresores del Modelo II | Resuelto (RF-5b) | spec:91; plan:47 |
| R2 | 6 Incertidumbre | Resuelto | spec:42-44 |
| R2 | 7 Claves `estres.*` | **Parcial**: `sens_cred` sin escenario y RF-12c sin claves | plan:59 |
| R2 | 8 Caso degenerado del pico | Resuelto | spec:41 |
| R2 | 9–12, 14, 16–18 | Resueltos | spec:98, :109, :90, :110, :88, :106, :28, :31; plan:11, :36 |
| R2 | 13 Regla de corte de D | **Parcial**: sigue [VERIFICAR] y no es operativa | spec:57 |
| R2 | 15 Cobertura RF → funciones | No resuelto (menor) | plan:84 |

## Cambios necesarios
1. **Importante: la propiedad A enumera un caso de fallo falso** (`spec.md:48`).
   - **Qué está mal:** «No vale … si las trayectorias se miden en niveles contra el observado del origen» es incorrecto para Δ. Si el paso 1 se mide contra un valor común a los dos escenarios, sea la Fed 2025 Q4 o el observado del origen, esa referencia se cancela: Δ es idéntico entre orígenes y también idéntico al de la referencia Fed (tercera fila de la simulación). Lo que cambia es el **nivel**, por un salto común a los dos escenarios; esa es la razón real de P8 (`plan.md:74`).
   - **Consecuencia:** la condición (v) presenta «el paso 1 contra 2025 Q4» como necesaria cuando solo es suficiente. RNF-5 pide mostrar que «deja de valer si se viola cada una», y con esta condición ese test es imposible.
   - **Se espera:**
     - en (v): «referencia del paso 1 común a ambos escenarios (aquí, la Fed 2025 Q4)» y «interanuales **en logaritmos**», porque con la variación porcentual simple la invariancia se rompe;
     - en «No vale»: sustituir ese caso por «si la referencia del paso 1 difiere entre escenarios o si el escenario se trunca o desplaza (RF-12a)».
2. **Importante: RF-12c deja sus niveles ambiguos** (`spec.md:99`, `:83`).
   - **Qué falta:**
     - (a) La regla del crédito con origen 2025T4: hay `loans_yoy` observado hasta 2026T2, así que no está claro si CRED(t−4) es observado hasta 2027Q2 o supuesto desde 2027Q1, ni con qué valor. Cambia los niveles que RF-12c reporta.
     - (b) La referencia de ΔU y ΔFFR en el paso 1: debe ser la misma regla (Fed 2025 Q4).
     - (c) Que los niveles de 2026T1–T2 en esa variante son contrafactuales y que se presentan junto al DR observado, o se declara que no se comparan.
     - (d) Que la comparación de niveles es por paso k: el final es 2029Q1 frente a 2029T3.
     - (e) Si Δ no coincide: como las condiciones se cumplen por construcción, una discrepancia sería un error de código. Debe **detener** el pipeline, no reportarse.
   - **Se espera** fijar (a)–(e) en la spec.
3. **Verificación de la descarga, ya posible** (`plan.md:26`, `:23`; RF-1 `spec.md:86`; RNF-1 `:106`).
   - El plan cita las huellas abreviadas y remite a `review-plan.md`, pero RNF-1 exige que consten en el plan aprobado.
   - **Se espera:**
     - escribir los tres sha256 completos y los tamaños (16 936, 1 692 y 1 824 bytes);
     - alinear `.gitattributes` con el plan: hoy tiene tres rutas explícitas y el plan dice `data/scenarios/** -text` (cualquiera vale, pero una sola);
     - declarar que la fecha del directorio es la fecha local de la descarga (America/Santo_Domingo) y que la UTC está en el manifiesto.
4. **Menor: claves de RF-12** (`plan.md:59`, `:62`).
   - `estres.sens_cred.{m}.{cero,media}.*` no incluye el escenario: el adverso principal y el base colisionan.
   - RF-12c no tiene claves ni una tabla nombrada en §6.
   - `prop_c_pos` no dice en qué trimestre se mide.
5. **Menor: falta un test** (`spec.md:108`, `plan.md:78`). RNF-3 y §8 deben incluir el caso de π(2026T4), que usa como base 2025T4 promediado con dos meses (pendiente desde la ronda 1).
6. **Menor: la propiedad B no nombra la linealidad** (`spec.md:49`). Hay que añadir «modelo lineal en la forma de Y» como condición: con Y en logit, innovaciones idénticas no se cancelan.
7. **Menor: regla de corte de D** (`spec.md:57`). Debe ser operativa, con su URL verificada: «del trimestre de la primera alza del rango objetivo del FOMC (marzo de 2022) al de la última (julio de 2023)». Así se cierra el [VERIFICAR] y se explica por qué 2023T4 (+0,07, efecto del promedio) queda fuera.

## Compatibilidad técnica (punto 2)
- **Funciones citadas:** todas existen con esos nombres y el comportamiento que el plan supone:
  - `load_latest_raw` (`fred_io.py:234`): no descarga; su mensaje de error sugiere `--download`, y el plan ya prohíbe seguirlo.
  - `parse_raw` (`panel.py:55`) y `quarterly_from_monthly` (`:143`, con el hueco de octubre de 2025 tratado según RF-11).
  - `quarterly_from_quarterly` (`:208`) y `yoy` (`:292`, en logaritmos).
  - `read_decisions` y `check_expected_forms` (`design.py:51` y `:71`).
  - `out_of_sample` (`model1.py:588`): devuelve `train_fit`, `test_design` y `series['dinamico']`.
  - `forecast.dynamic` (`forecast.py:45`): exige la columna `y_lag` y la sobrescribe. `forecast.to_level` (`:71`): espera una serie y un período.
- **RF-5:** se reproduce con `atol` 1e-12, porque es la misma aritmética.
- **Diseño del Modelo II:** lo construye `design2.build_design2`, no `build_design`. Conviene nombrarlo en `plan.md:11` para RF-5b.
- **`project` con nivel escalar** (`plan.md:41`): debe decir cómo reutiliza `to_level`, por ejemplo envolviendo `dr_origin` en una serie indexada en el origen. Si no, reimplementa la suma acumulada (P5).
- **Ruta y manifiesto:** coinciden con la propuesta de Codex. El manifiesto lleva BOM: se lee con `utf-8-sig`.
- **Documentos de Codex desactualizados respecto de la v4:**
  - compatibilidad, puntos 3 y 4 (los «7 trimestres» de D-CRED, S3) y referencias a «§3.1»;
  - fuentes: «solo los lectores incorporados», «H = 11», «D-CRED siete», «S3», «RF-10(c)» y «no se ha creado el directorio ni descargado archivos» (hoy está congelado, sin versionar).
  - Siguen vigentes y la v4 los respeta: la ruta de los niveles, el fixture de RF-5 y los lectores. La v4 no contradice a Codex en nada sustantivo.

## Guía oficial (punto 4)
Las secciones 7 y 8 no exigen el equivalente en dólares ni un estimador restringido. La §7 pide el riesgo bajo el escenario adverso frente al base y el cambio; la §8 nombra la «planificación de capital» como tema de discusión. Lo que dice `spec.md:127` es correcto.

## Observaciones opcionales
- **Diseño de los tests negativos de RNF-5:**
  - Deben comparar contra la recursión de δ calculada solo con las diferencias del escenario. Comparar entre dos orígenes con la misma perturbación no la detecta.
  - Deben perturbar insumos que de verdad entran: en el Modelo I, U(T0) no entra y el test pasaría sin probar nada.
  - Conviene usar `rtol` además de `atol` si las escalas sintéticas son grandes.
- **D frente a la base:** D usa cambios de FEDFUNDS y la base cambios de la letra a 3 meses. En la sensibilidad de RF-10 se mezclan las dos medidas; añadirlo a RF-14.
- **Recursión con un solo rezago de ΔDR:** decir que vale para los JSON actuales; con p rezagos sería un AR(p).
- **Cobertura del plan:** `plan.md:84` apunta RF-11/12/14 a tareas, no a funciones.

## Bloqueos restantes
- **Antes de aprobar (texto):** los cambios 1 y 2.
- **Verificaciones de la descarga, ya posibles:** los cambios 3 y 7, y el commit previo de los CSV, `manifest.csv` y `.gitattributes` (RNF-1).
- **No bloquean:** los cambios 4–6 y las observaciones; se pueden resolver al pasar a tareas.

**Lo que defendería ante el profesor**
- El Δ por trimestre del escenario no depende del origen: lo comprobó algebraicamente y con simulación (≈ 1e-15) en ambos modelos. Solo cambian los niveles y las fechas.
- La regla de la tasa en cero viene pre-registrada desde la 004. La sensibilidad con los coeficientes estimados va aparte, réplica a réplica, con el rótulo «sensibilidad, no efecto estimado».
- Los archivos de la Fed están congelados con huella verificada y sus bytes sobreviven a git.

**Lo que preguntaría el profesor**
1. Si el Δ es el mismo arrancando en 2025T4, ¿qué cambia en los niveles y por qué los de 2026T1–T2 no coinciden con lo observado?
2. Su escenario con alza de tasas da la misma morosidad que el adverso: ¿qué aporta entonces al ejemplo de la guía?
3. ¿Por qué medir el primer cambio de desempleo contra la Fed 2025 Q4 y no contra el dato observado, si Δ no cambia?

---
**Nota de Claude Code (no es parte del informe del revisor).** Los cambios 1 a 7 de esta ronda se incorporaron después en la v5 de `spec.md` y `plan.md`, junto con las observaciones sobre tests negativos, D frente a la base, un solo rezago de ΔDR y cobertura RF → funciones. La v5 no ha sido revisada de forma independiente. Actualización posterior (v6): por decisión del autor se mantienen las tres reglas de ruta exacta de `.gitattributes` que implementó Codex, sin ampliarlas a `data/scenarios/**` (el cambio 3 se resolvió en ese sentido, no con el patrón único); la regla de corte de D se verificó con los comunicados del FOMC (enlaces en `spec.md`).
