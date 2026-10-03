---
description: Cierre de sesión - actualiza MEMORY.md y propone el commit antes de que se agote la ventana de uso
argument-hint: "[notas]"
model: sonnet
allowed-tools: Bash(git status *) Bash(git diff *)
disable-model-invocation: true
---
Estado de git:
!`git status --short`

!`git diff --stat`

1. Actualiza MEMORY.md: estado actual, decisiones nuevas con su porqué, errores a evitar y próximo paso exacto (herramienta + comando). Máximo ~50 líneas: resume o elimina lo que ya no aporte.
2. Si algo se volvió regla permanente, propón (no apliques) el cambio en AGENTS.md.
3. Propón un mensaje de commit (prefijos: spec, plan, audit, feat, fix, data, test, docs) y espera mi OK antes de hacer `git commit`.

Notas del usuario: $ARGUMENTS
