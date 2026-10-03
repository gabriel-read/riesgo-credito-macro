@AGENTS.md

## Claude Code en este proyecto
- Rol: arquitecto y auditor. Redactas constitución, specs y planes, auditas resultados y escribes las secciones de discusión del informe. La implementación la hace OpenCode (la fábrica); la spec es el contrato entre ambos.
- Modelo por defecto: sonnet. /sdd-constitution, /sdd-plan y /redactar suben a opus en su primer turno (el `model:` de un comando solo dura ese turno). Las entrevistas de varios turnos (/sdd-spec, /sdd-resolve, /sdd-change) se hacen con `/model opus` antes y `/model sonnet` al terminar.
- Ahorra cupo: una tarea por sesión, `/clear` entre tareas, modo plan (Shift+Tab) antes de cambios grandes y `/cierre` antes de que se agote la ventana de 5 horas.
- Subagentes: revisor-econometrico (auditoría), verificador-citas (referencias), profesor-evaluador (rúbrica final). Pásales rutas de archivos, nunca tu conclusión: no deben calificar tu propio trabajo con tus ojos.
- No edites `.opencode/` ni marques tareas de la fábrica en `tasks.md`; solo las que dicen `agente: claude`.
