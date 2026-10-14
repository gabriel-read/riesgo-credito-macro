# MEMORY.md — Riesgo de crédito y macroeconomía
Copia activa única: C:/Users/gabri/orca/riesgo-credito-macro. Desktop/OneDrive atrasada, no sincronizar ni reiniciar 002.
## Estado (13-oct-2026)
- Codex: implementación, pruebas, pipeline y validación del autor. Claude: metodología, specs/planes y auditoría independiente. Una sola herramienta escribe en el checkout. OpenCode histórico/inactivo; arnés local preservado sin formalización adicional.
- HEAD 7a3dd2a, rama spec/004-modelo-ii; no push. Fuentes 005 commit 5ba4ada (5 archivos) antes del pre-registro 7a3dd2a (spec/plan v6 y 4 revisiones). No nuevos commits autorizados.
- 001 datos y 002 literatura cerradas. 002: 17 estudios + 4 datos/método, auditoría ronda 4 aprobada; asiamah2026/koskei2023 pendiente-lectura. No reiniciar T4 ni corregir FRED/T3 histórico; observación reservada para 006.
- 003 implementada, auditoría ronda 4 aprobada; pre-registro 667b313 y C1–C3 anteriores a resultados. Validación histórica 504 tests y all ×2. No modificar contrato ni código/salidas por menores.
- 004 implementación y validación aprobadas, auditoría independiente ronda 2 APROBADA sobre 2f4c401; T9 marcada completa. Ronda 1 intacta; revisiones/T9 locales sin commit conservadas, no incluidas en commits de 005.
- 005 CERRADA, T1–T10 completas: validación del autor ronda 3 APROBADA y auditoría independiente ronda 3 APROBADA; Codex cotejó seis SHA actuales (código/test/dos MD/spec/plan) con el informe. Cierre autorizado condicionalmente por el usuario el 12-oct; contratos originales intactos, rondas 1/2 conservadas y opcionales sin aplicar. SHA spec 6d9713dd1917b4b9b5a2ffc87c7f202869981e9102c9e8e11bf60daac99c77bb; plan 8b0fc56b3ba2577a0c142a8ab70568af96caed9bf2bbcf18949f42c8ad3d232a. Encabezados originales borrador conservados; no reabrir aprobación ni cambiar bytes.
- Preservación de pre-registro: blobs spec/plan sin filtros CRLF/LF para coincidir con SHA aprobado; .gitattributes solo tres CSV Fed exactos. No ampliar reglas ni corregir opcionales.
## Implementación y evidencia 005
- Código: src/scenarios.py, stress.py, stress_tables.py, stress_figures.py; etapa stress y all en src/pipeline.py. Sin nuevas dependencias, escritura en raw ni modificación de 003/004.
- Tests primero por tarea/bloqueante; última suite 837 passed, 567 warnings, 855.75 s, rc 0; presentación 7 passed. Regresión 0,0105 primero en rojo, luego verde. Advertencias de clases ya existentes; no repetir por notas/documentación.
- CLI stress rc 0 en copia activa. Ocho tablas CSV/MD, dos PNG y bloque estres en report/_variables.yml; bloques datos/modelo1/modelo2 preservados.
- all ×2 anterior conservado en docs/reproducibilidad-005-2026-10-12.json: 79 archivos idénticos, 54 modelos iguales en contenido (LF/PNG por bytes). Ronda 2: stress ×2 en pytest-682/stress0050 idéntica; stress activa rc 0, 18 salidas y YAML coincidentes por bytes; 103 archivos protegidos intactos. Huellas: docs/reproducibilidad-005-ronda2-2026-10-12.json.
- T9 corrigió warmup CRED de 1998 (fuera de muestra), formato de columna mixta/booleanos, nombre de modelo en error Cholesky y validación de panel guardado. No imputar ni relajar tolerancias.
- Validación del autor ronda 3: specs/005-estres/review-validate.md; auditoría independiente ronda 3 APROBADA: review-audit.md, cuatro SHA exactos de corrección más spec/plan. Rondas 1/2 de ambas revisiones conservadas. Paquete actualizado con rutas absolutas y SHA: docs/paquete-auditoria-005-2026-10-12.md; independencia es de Claude/revisor, no de Codex.
- Bloqueantes 1–5: árbol exacto estres/24 hojas renombradas; conteos/extremos y notas fuera de rango; diferencia de picos; Markdown/encabezados españoles; negativos RNF-5 frente a δ independiente y lenguaje en 16 textos/estres. Solo stress.py, stress_tables.py y tests de estrés; nueve opcionales sin aplicar.
- Única cifra derivada corregida: estres.dif_modelos.{severo,propio}.delta_pico 0,626→0,612 pp (max(Δ_I)−max(Δ_II)); no confundir con max(Δ_I−Δ_II). Trayectorias/bandas/sensibilidades/PNG y demás valores YAML intactos tras renombres.
- Ronda 3: solo stress_tables.py (tres float) y test de redondeo. Solo stress_levels.md/stress_delta.md cambian 0,010→0,011 en el pie; 0,0105 exacto y YAML intactos. Stress ×2 pytest-684 más activa coinciden; 192 archivos protegidos intactos. Evidencia: docs/reproducibilidad-005-ronda3-2026-10-12.json; opcionales rondas 1/2 sin aplicar.
- Fuentes Fed congeladas: data/scenarios/fed/2026-final/2026-10-11/ (fecha local; hora UTC en manifiesto). SHA propios recalculados 3/3 coinciden con plan/blobs; bytes originales CRLF.
- Vintage FRED 2026-10-02 fijado por nombres/fecha/filas/último dato/SHA LF; trimestre común 2026T2. PanelResult.full tiene historia desde 1998 y cola parcial; panel.csv termina en 2026T2.
## Decisiones científicas conservadas
- Frecuencia trimestral; principal 2000T1–2026T2 (106), descarga desde 1998 para transformaciones. GDP nominal y muestra larga 1985T1 son robusteces pre-registradas; declarar desviación de corte de la guía.
- PIB principal GDPC1; PIB/CPI/crédito en variación interanual logarítmica. CPI y desempleo 2025T4 usan noviembre/diciembre por ausencia de octubre; nunca rellenar silenciosamente.
- 005: origen 2026T2, 13 pasos hasta 2029T3, Fed 2026Q1–2029Q1 adaptada; RF-12a recorta 11, RF-12c compara 13 desde 2025T4 por paso.
- D cambia solo tasa (2022T1–2023T3 y luego ceros), no es estanflacionario; coincide con severo en principal y difiere en sensibilidad. Decisión del autor conservada.
- Crédito lag 4 observado hasta 2027T2; desde 2027T3 fijo a loans_yoy de 2026T2, común; sensibilidades cero/media sobre niveles. Sin equivalente en dólares.
- Tasa cero por regla heredada sin evidencia fuerte; sensibilidad separada con coeficientes libres, pareo y distribución marginal. No condicionamiento/reestimación restringida ni límites IC acumulado.
- Bandas solo de parámetros, sin innovaciones ni incertidumbre de escenario/especificación/endogeneidad; no intervalos de predicción. No descartar réplicas explosivas ni truncar niveles.
- Ajuste OOS 003: entrenamiento 2000T1–2019T4, ancla 2021T4, evaluación 2022T1–2026T2; reconstruir procedimiento aprobado, no nueva selección ni usar JSON principal como entrenamiento.
## Para 006/007 y defensa
- 003: rho≈0.63; inflación/crédito significativos y no I(0); ΔFFR negativa no significativa. BG/CUSUM pasan, BP/White/JB/RESET/Chow fallan. Dinámico pierde frente a ingenuo; a un paso no se distingue significativamente.
- 004: K_AIC=K_BIC=1, sin evidencia rezagada positiva; Granger/C2 mismo Wald. S≈−0.048 (p≈0.200), S_rez≈0.036 (p≈0.355); phi_h≈3.2 describe ciclo, no alza aislada. VIF de ΔU artefacto de dummies COVID; discutir diagnósticos fallidos.
- No implementar menores de 004: columna_panel/forma, −0.000, ubicación h_star en perfil y hueco CUSUM; explicar en 006. Rondas y autoría original intactas.
- 006 T4: n_series conciliado a 13 códigos del manifiesto; historia 1998T1, literatura 17/8/3/4 y D 7/6 desde fuentes. Justificar clasificación bernanke1995/pesaran2006/segoviano2006/gertler2015; C2 sin estadístico separado, no inventarlo. Cifras de outputs/variables, asociación y límites.
- 006 change editorial aprobado: spec v4 SHA481537c0… y plan v3 SHA668dece3…; versiones previas exactas conservadas. Tasks v3 conT13–T15/nuevoorden; ledger change-editorial-applied.md. Fecha/formato y material separado pendientes profesor.
## Límites y aprendizajes
- No .env/credenciales, push, raw/guía editados ni commits sin autorización. Conservar cambios ajenos del arnés/docs/006/debug.log; no incluirlos en trabajo de 005.
- Auditoría independiente obligatoria para 003–006; tests verdes y validación del implementador no sustituyen auditoría. Si falta cuota, registrar continuidad y no transferirla al implementador.
- FRED User-Agent predeterminado; no redescargar por revisiones de PIB. pandas-datareader≥0.11; variantes probadas con sintéticos y semillas independientes X/ruido.
- Dummies de impulso: residuo nulo, rango HAC reducido; simular solo bloque sin dummies; White elimina colinealidad por rango. Pre-registro antes de resultados, change ante cambios de contrato.
- Formato: convertir escalares NumPy a float antes de fmt_es en pies, igual que celdas/variables; round(np.float64(0.0105)) y round(float) difieren a tres decimales. Test de mitad protege esa consistencia.
## Siguiente acción y cierre de sesión (13-oct)
- 006 ronda7: 974 passed, 567 warnings, 1093.01 s; rc 0, sin exclusiones. Primera corrida interrumpida, reiniciada completa; siete regresiones nuevas/42 focalizadas. Codex autor, no auditor independiente. R6 y anteriores preservados.
- Claude R5-6 en02 SHA01a299dd…ac73 recibida; otras ocho intactas, alcance de verificación/candidatos conservados. AnexoE concordante con respaldo existente, guion sin convertirlo en signo general.
- R5-1–R5-5: bloques PDF completos Tablas2/4/6, Motivo para lector, pre-registro no tautológico, notaTabla1 sin autocita, ambos coeficientes desde estimaciones principales, matriz solo generalizados/FGLS. Sin cambios científicos ni numéricos.
- Preparación investigada por archivos generados/mapa páginas. Final/repetición ocho renders rc0, 369 entradas SHA antes/después sin diferencias; huellas finales congeladas. PDF/DOCX contenido reproducible, solo metadatos; GFM exacto, Report×2 208 iguales.
- Entrega PDF/DOCX/GFM outputs/preview-006/report/, 35p/149p; 116 protegidos/25 módulos intactos, YAML/BibTeX/spec/plan conservados. Celdas/figuras/slugs y clics 53+167 internos/55URI actuales documentados. Visual sin Word nativo ni GoogleDocs afirmados.
- Paquete nuevo docs/paquete-auditoria-006-ronda7.md/manifiesto SHA completos; Codex congela y entrega turno para comprobación acotada de cambios. Guía docs/importacion-google-docs-006-ronda7.md preparada, autor importa dosDOCX y aporta URLs reales.
- Pendientes: comprobación acotada, GoogleDocsRF14b obligatorio, 006/T12 y confirmacionesprofesor; 007 sigue sin aprobación/deck. Sin commit/push, ampliación de alcance ni modificaciones de arnes/raw/.env.
