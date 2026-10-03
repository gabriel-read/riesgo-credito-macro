---
description: Fábrica · Lleva una spec aprobada de tareas a validada con el coordinador (uso - /fabrica 001-datos [contexto])
agent: coordinator
---
Lleva la spec specs/$1/ por la fábrica siguiendo tus fases: tareas → implementación (una tarea por vez) → validación → correcciones → cierre.

Contexto adicional del usuario (puede estar vacío): $2

Empieza comprobando que spec.md y plan.md dicen "Estado: aprobada" (o "implementada" si el contexto trae correcciones) y dime en una línea en qué fase arrancas.
