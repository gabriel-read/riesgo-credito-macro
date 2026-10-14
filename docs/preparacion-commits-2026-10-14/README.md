# Preparación de commits — 14 de octubre de 2026

Preparación solamente: no se ha creado ningún commit ni ejecutado push. HEAD de partida: `7a3dd2ad76bf09a8401534679e4311400fb3a4aa`, rama `spec/004-modelo-ii`. El índice estaba vacío.

## Entrega académica R7

Se recalcularon las huellas de los bytes actuales, sin renderizar. Coinciden con `delivered_sha256` del manifiesto aprobado `docs/huellas-paquete-auditoria-006-ronda7.json` (SHA-256 `69003c83a7c6ccbc69c5cbd23bbeeb43bde0b970792f53748df302ca574535e5`).

| Ruta absoluta | SHA-256 |
|---|---|
| C:\Users\gabri\orca\riesgo-credito-macro\outputs\preview-006\report\informe.pdf | 658814c512685718f8a06ec3362ef3fa07d4636653ed38d34f79b208a1a487ad |
| C:\Users\gabri\orca\riesgo-credito-macro\outputs\preview-006\report\anexo-tecnico.pdf | 73bbdfabd0f4cd84b347507fc602d990bac6f3267595fb3569383ddc142a0fcd |

La guía oficial no confirma hora límite, extensión, formato de entrega, aceptación de dos archivos ni formato/duración de exposición. La fecha de portada no confirma la fecha límite. El ensayo del autor sigue pendiente: no se marca realizado ni se cierra 006/T12. Google Docs fue retirado mediante el cambio autorizado; no se añade como requisito.

## Separación y límites

`academico.paths` enumera fuentes, implementación 005/006, pruebas, historial documental y seis entregables R7. `linkedin.paths` enumera 007, su muestra y herramientas/dependencias de PPTX. `inventario.json` registra bytes y SHA-256 de cada archivo al preparar los grupos. La muestra no forma parte de la asignación académica.

El pipeline compartido se separa mediante `pipeline-academico.patch`: agrega únicamente 005/006 al índice académico; el segundo commit añade la etapa deck desde el archivo actual. `git apply --cached --check` pasó. El archivo de trabajo permanece intacto. No se declara validado un clon limpio de estos grupos: el arnés local queda fuera, con sus cambios conservados.

Se excluyen cambios del arnés, README de migración, la eliminación local del documento Plan Macro, intermedios Typst, carpetas temporales de reproducibilidad, copias binarias históricas y capturas QA masivas. Nada se elimina. Las evidencias históricas y copias excluidas siguen disponibles localmente. MEMORY es registro compartido y se añade al primer commit; describe 007 como trabajo separado.

No se repitieron pruebas: la suite vigente es 989 passed, 567 warnings, rc 0, sin exclusiones (`docs/pytest-completo-007-D2B.log`); no hubo cambios de código en esta preparación.

## Comandos locales propuestos (PowerShell)

Revisar el inventario antes de ejecutar. Estos comandos crean dos commits y una referencia académica; no hacen push.

```powershell
Set-Location 'C:\Users\gabri\orca\riesgo-credito-macro'
git add --pathspec-from-file=docs/preparacion-commits-2026-10-14/academico.paths
git add -- MEMORY.md docs/preparacion-commits-2026-10-14
git apply --cached docs/preparacion-commits-2026-10-14/pipeline-academico.patch
git diff --cached --stat
git commit -m "feat(academico): conserva informe y anexo R7 aprobados y avance 005-006"
git branch entrega/r7-academico
git add --pathspec-from-file=docs/preparacion-commits-2026-10-14/linkedin.paths
git diff --cached --stat
git commit -m "feat(linkedin): agrega muestra editable D2B de 007, fase B pendiente"
git branch trabajo/007-linkedin
```

## Push, exclusivamente a cargo del usuario

Publicar solo el avance académico:

```powershell
git push origin entrega/r7-academico
```

Publicar también el trabajo separado de LinkedIn cuando se quiera:

```powershell
git push origin trabajo/007-linkedin
```

Son ramas distintas; la académica termina antes del commit LinkedIn. No se cambia la rama de trabajo ni se publica durante esta preparación.
