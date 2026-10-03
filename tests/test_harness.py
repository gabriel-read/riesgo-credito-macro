"""Guardarraíles del arnés agéntico.

Se ejecutan con `uv run pytest -q` y en GitHub Actions. No necesitan red ni dependencias.
Comprueban que el contexto de los agentes siga corto y que las specs, tareas, citas y
cifras respeten las reglas de la skill sdd y de la constitución.
"""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SPEC_DIRS = sorted(p for p in (ROOT / "specs").glob("[0-9][0-9][0-9]-*") if p.is_dir())
TASK_LINE = re.compile(r"^- \[[ xX]\] \*\*T\d+")

# RNF-4: cifras escritas a mano en el informe. El lookbehind excluye números
# precedidos de palabra, punto o coma (p. ej. «2000T1», «{{< var ... >}}»).
HAND_TYPED_NUMBER_PATTERNS = (
    re.compile(r"(?<![\w.,])\d+[.,]\d+"),
    re.compile(r"(?<![\w.,])\d+\s?%"),
)


def find_hand_typed_numbers(text: str) -> list[str]:
    """Devuelve las cifras escritas a mano en `text` (RNF-4).

    Detecta decimales con coma o punto («0,8 pp», «3.1») y porcentajes
    («15 %», «50%»). Pasa por alto trimestres («2000T1»), variables de
    Quarto («{{< var datos.muestra_fin >}}») y fechas («2026-10-03»).
    """
    found: list[str] = []
    for pattern in HAND_TYPED_NUMBER_PATTERNS:
        found.extend(pattern.findall(text))
    return found


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_context_files_exist():
    for name in ["AGENTS.md", "CLAUDE.md", "MEMORY.md", "docs/constitution.md", "docs/guia-profesor.md"]:
        assert (ROOT / name).is_file(), f"Falta {name}"


def test_agents_md_is_short():
    lines = len(_read(ROOT / "AGENTS.md").splitlines())
    assert lines <= 45, f"AGENTS.md tiene {lines} líneas: mueve el detalle a una skill (objetivo ≤ 40)"


def test_memory_md_is_short():
    lines = len(_read(ROOT / "MEMORY.md").splitlines())
    assert lines <= 60, f"MEMORY.md tiene {lines} líneas: resume o elimina lo que ya no aporte (objetivo ~50)"


def test_constitution_has_at_most_six_principles():
    principles = re.findall(r"^\d+\.\s", _read(ROOT / "docs/constitution.md"), flags=re.MULTILINE)
    assert 1 <= len(principles) <= 6, "La constitución debe tener entre 1 y 6 principios"


def test_specs_declare_state():
    for d in SPEC_DIRS:
        for name in ["spec.md", "plan.md"]:
            f = d / name
            if f.exists():
                assert re.search(r"Estado:\s*(borrador|aprobada|implementada)", _read(f)), f"{f}: falta 'Estado:'"


def test_plan_requires_approved_spec():
    for d in SPEC_DIRS:
        plan, spec = d / "plan.md", d / "spec.md"
        if plan.exists() and re.search(r"Estado:\s*aprobada", _read(plan)):
            assert spec.exists() and re.search(r"Estado:\s*(aprobada|implementada)", _read(spec)), (
                f"{plan}: plan aprobado sobre una spec que no está aprobada"
            )


def test_tasks_are_verifiable_and_small_in_number():
    for d in SPEC_DIRS:
        tasks = d / "tasks.md"
        if not tasks.exists():
            continue
        lines = _read(tasks).splitlines()
        idx = [i for i, line in enumerate(lines) if TASK_LINE.match(line)]
        assert len(idx) <= 15, f"{tasks}: {len(idx)} tareas; divide la spec (objetivo ≤ 10)"
        for i in idx:
            window = "\n".join(lines[i : i + 4])
            assert "Hecho cuando" in window, f"{tasks}:{i + 1}: la tarea no tiene 'Hecho cuando'"
            assert "agente:" in lines[i], f"{tasks}:{i + 1}: la tarea no declara su agente"


def _report_prose(text: str) -> str:
    """Texto del informe sin front matter, bloques de código ni shortcodes de Quarto."""
    text = re.sub(r"\A---.*?\n---\n", "", text, flags=re.DOTALL)
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    return re.sub(r"\{\{<.*?>\}\}", "", text)


def test_report_citations_exist_in_bib():
    bib = ROOT / "report" / "references.bib"
    qmds = list((ROOT / "report").glob("*.qmd"))
    if not bib.exists() or not qmds:
        return
    keys = set(re.findall(r"@\w+\{([^,\s]+),", _read(bib)))
    for qmd in qmds:
        cited = set(re.findall(r"(?<![\w@.])@([a-z][a-z_]*\d{4}[a-z]?)\b", _report_prose(_read(qmd))))
        missing = sorted(cited - keys)
        assert not missing, f"{qmd.name}: citas sin entrada en references.bib: {missing}"


def test_report_has_no_hand_typed_numbers():
    """Principio 5: las cifras del informe salen de report/_variables.yml con {{< var ... >}}."""
    for qmd in (ROOT / "report").glob("*.qmd"):
        found = find_hand_typed_numbers(_report_prose(_read(qmd)))
        assert not found, f"{qmd.name}: cifras escritas a mano {found[:5]}; usa {{{{< var ... >}}}}"


def test_find_hand_typed_numbers_detects_decimals_and_percent():
    assert find_hand_typed_numbers("La morosidad subió 0,8 pp en el trimestre.")
    assert find_hand_typed_numbers("El desempleo cae al 15 % anual.")


def test_find_hand_typed_numbers_ignores_variables_and_quarters():
    assert find_hand_typed_numbers("{{< var datos.muestra_fin >}}") == []
    assert find_hand_typed_numbers("La muestra empieza en 2000T1.") == []
