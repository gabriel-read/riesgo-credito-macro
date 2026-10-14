"""Pure source registry and editorial routing; no estimation, disk, or network."""
import csv
import hashlib
import io
import re

from src.report_tables import TITLES

ANNEX_TITLES = {
    'A': 'Datos y transformaciones', 'B': 'Modelo I', 'C': 'Modelo II',
    'D': 'Estrés', 'E': 'Literatura verificada', 'F': 'Desviaciones y reproducibilidad',
}
FIGURE_TITLES = {
    'delinquency_unemployment_ffr': 'Morosidad, desempleo y tasa de fondos federales',
    'model1_coefficients': 'Modelo I — coeficientes', 'model1_cusum': 'Modelo I — CUSUM',
    'model1_oos': 'Modelo I — evaluación fuera de muestra',
    'model2_cusum': 'Modelo II — CUSUM', 'model2_profile': 'Modelo II — perfil de rezagos',
    'model2_response': 'Modelo II — respuestas dinámicas',
    'stress_model1': 'Estrés — Modelo I', 'stress_model2': 'Estrés — Modelo II',
}
BODY_TABLES = {
    'fred_manifest',
    'lit_estudios', 'model1_coefficients', 'model1_diagnostics', 'model2_reading',
    'model2_inputs63', 'stress_delta',
}
BODY_ORDER = ['lit_estudios', 'fred_manifest', 'model1_coefficients', 'model1_diagnostics',
              'model2_reading', 'model2_inputs63', 'stress_delta']


def _route(name: str, kind: str) -> tuple[str, str]:
    if name.endswith('_deviations') or name == 'fred_manifest':
        annex = 'F'
    elif name.startswith('model1_'):
        annex = 'B'
    elif name.startswith('model2_'):
        annex = 'C'
    elif name.startswith('stress_'):
        annex = 'D'
    elif name == 'lit_estudios':
        annex = 'E'
    else:
        annex = 'A'
    prefix = 'AT' if kind == 'table' else 'AF'
    suffix = name.replace('model1_', 'M1-').replace('model2_', 'M2-').replace('stress_', 'EST-')
    overrides = {'model1_robustness_estimates': 'M1-ROB', 'model2_lp': 'M2-LP'}
    return annex, prefix + '-' + overrides.get(name, suffix).replace('_', '-').upper()


def build_report_registry(tables: dict[str, bytes], figures: dict[str, bytes]) -> list[dict]:
    """Route every approved CSV/PNG once; IDs never depend on row order or pagination."""
    entries = []
    for kind, sources, titles, folder, extension in (
        ('table', tables, TITLES, 'tables', 'csv'),
        ('figure', figures, FIGURE_TITLES, 'figures', 'png'),
    ):
        for name, content in sorted(sources.items()):
            if name not in titles:
                raise ValueError(f'Fuente editorial desconocida: {name}')
            annex, slug = _route(name, kind)
            entries.append({'name': name, 'kind': kind, 'slug': slug, 'anchor': slug.lower(),
                            'source': 'data/raw/manifest.csv' if name == 'fred_manifest' else f'outputs/{folder}/{name}.{extension}',
                            'sha256': hashlib.sha256(content).hexdigest(), 'annex': annex,
                            'title': titles[name], 'body': 'reducida' if name in BODY_TABLES and kind == 'table'
                            else 'esencial sin recortar' if kind == 'figure' and name in ('delinquency_unemployment_ffr', 'model2_response', 'stress_model1', 'stress_model2')
                            else 'ninguno'})
    entries.sort(key=lambda r: (r['annex'], r['kind'], r['slug']))
    if len({r['slug'] for r in entries}) != len(entries):
        raise ValueError('Identificador editorial duplicado')
    counters = {}
    for entry in entries:
        key = (entry['annex'], entry['kind'])
        counters[key] = counters.get(key, 0) + 1
        label = 'Tabla' if entry['kind'] == 'table' else 'Figura'
        entry['visible_id'] = f"{label} {entry['annex']}.{counters[key]}"
    return entries


def registry_csv(entries: list[dict]) -> str:
    buffer = io.StringIO()
    if entries:
        writer = csv.DictWriter(buffer, fieldnames=list(entries[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(entries)
    return buffer.getvalue()


def registry_interface(entries: list[dict]) -> str:
    lines = ['## Registro editorial: identificadores y destinos', '',
             'La verificación estructural de enlaces no equivale a un clic comprobado en Google Docs o Word.', '',
             '| Identificador | Fuente | Destino completo | En el cuerpo |', '| --- | --- | --- | --- |']
    lines.extend(f"| {r['slug']} | `{r['source']}` | Anexo {r['annex']}; `{r['anchor']}` | {r['body']} |" for r in entries)
    return '\n'.join(lines) + '\n'


def pdf_named_destination_pages(content: bytes) -> dict[str, int]:
    """Read native Typst PDF destinations; pagination is presentation, not estimation."""
    try:
        objects = {int(n): value for n, value in re.findall(
            rb'(?:^|\n)(\d+) 0 obj\s*(.*?)\s*endobj', content, re.S)}
        catalog = next(value for value in objects.values() if re.search(rb'/Type\s*/Catalog\b', value))
        root = int(re.search(rb'/Pages\s*(\d+) 0 R', catalog)[1])
        def descendants(number):
            obj = objects[number]
            if re.search(rb'/Type\s*/Page\b', obj):
                return [number]
            children = re.search(rb'/Kids\s*\[(.*?)\]', obj, re.S)[1]
            return [page for child in re.findall(rb'(\d+) 0 R', children)
                    for page in descendants(int(child))]
        pages = descendants(root)
        result = {}
        for anchor, reference in re.findall(rb'\((a[tf]-[a-z0-9-]+)\)\s*(\d+) 0 R', catalog):
            destination = re.match(rb'\[(\d+) 0 R\s*/XYZ\b', objects[int(reference)])
            if not destination:
                raise ValueError('Destino PDF no compatible')
            result[anchor.decode('ascii')] = pages.index(int(destination[1])) + 1
        return result
    except (KeyError, TypeError, ValueError, StopIteration, RecursionError) as error:
        raise ValueError('Destinos PDF incompatibles; regenerar el anexo') from error


def link_registry_csv(entries: list[dict], pages: dict[str, int] | None = None) -> str:
    rows = [{'slug': r['slug'], 'anchor': r['anchor'], 'pdf': 'anexo-tecnico.pdf#nameddest=' + r['anchor']
             + ('&page=' + str(pages[r['anchor']]) if pages and r['anchor'] in pages else ''),
             'docx': 'anexo-tecnico.docx#' + r['anchor'], 'external_url': '',
             'verification': 'destino generado; clic en visor pendiente'} for r in entries]
    return registry_csv(rows)


def build_editorial_documents(registry: list[dict], sources: dict[str, str], presentation: dict) -> dict:
    """Compose complete annexes once and essential CSV subsets, preserving original values."""
    from src.report_tables import SELECTED, _markdown, display_cell, presentation_note, _label
    filenames = {'A': 'A-datos.qmd', 'B': 'B-modelo-i.qmd', 'C': 'C-modelo-ii.qmd',
                 'D': 'D-estres.qmd', 'E': 'E-literatura.qmd', 'F': 'F-reproducibilidad.qmd'}
    groups = {key: [f'# Anexo {key}. {title} {{#anexo-{key.lower()}}}', ''] for key, title in ANNEX_TITLES.items()}
    body_files, body_trace = {}, {}
    for entry in registry:
        group = groups[entry['annex']]
        group.extend([f"## {entry['visible_id']}. {entry['title']} — {entry['slug']} {{#{entry['anchor']}}}",
                      '', ''])
        name = entry['name']
        if entry['kind'] == 'figure':
            # Approved figures already carry their source inside the image.
            caption = entry['title']
            if name == 'delinquency_unemployment_ffr':
                caption += '. Fuente: FRED; elaboración propia. Las franjas grises indican períodos de recesión según USREC.'
            group.extend([f"![{caption}](../{entry.get('presentation_source', entry['source'])})", ''])
            continue
        trace = presentation['trace'][name]
        if trace.get('source_note'):
            group.extend([f"{{{{< include ../outputs/informe/{name}_nota.md >}}}}", ''])
        for index, panel in enumerate(trace['annex_panels'], 1):
            group.extend([f"### Panel {index}", '', 'Columnas: ' + '; '.join(_label(c) for c in panel['columns']) + '.',
                          '', f"{{{{< include ../outputs/informe/{panel['file']} >}}}}", ''])
        if entry['body'] != 'reducida':
            continue
        raw = list(csv.DictReader(io.StringIO(sources[name])))
        fields = list(raw[0]) if raw else trace['columns']
        columns = [c for c in SELECTED.get(name, fields[:5]) if c in fields]
        if name == 'lit_estudios':
            raw = [row for row in raw if row['seccion_principal'] == '2.5']
            columns = ['estudio', 'dependiente', 'regresores', 'metodo', 'signo']
        elif name == 'model1_coefficients':
            raw = [row for row in raw if row['termino'] in {'gdp_growth', 'd_unemp', 'inflation', 'd_ffr', 'credit_growth'}]
        elif name == 'model1_diagnostics':
            columns = [c for c in ['prueba', 'estadistico', 'estadístico', 'p_valor', 'veredicto'] if c in fields]
        elif name == 'model2_reading':
            columns = [c for c in ['elemento', 'resultado'] if c in fields]
        elif name == 'stress_delta':
            columns = [c for c in ['modelo', 'escenario', 'delta_final', 'delta_pico', 'pico_trimestre'] if c in fields]
            seen, unique = set(), []
            for row in raw:
                key = (row['modelo'], row['escenario'])
                if key not in seen:
                    unique.append(row)
                    seen.add(key)
            raw = unique
        rows = [[display_cell(row[c], c) for c in columns] for row in raw]
        number = BODY_ORDER.index(name) + 1
        body_files[name + '_cuerpo.md'] = (f"**Tabla {number}**\n\n*{entry['title']}*\n\n"
                                         f"Tabla completa: [Anexo {entry['annex']}, {entry['slug']}](anexo-tecnico.pdf#nameddest={entry['anchor']}).\n\n"
                                         + _markdown(columns, rows, entry['source']))
        if trace.get('source_note'):
            note = re.sub(r'Fuente:.*?(?=Advertencia:|$)', '', presentation_note(trace['source_note']))
            body_files[name + '_cuerpo.md'] += '\n' + note.strip() + '\n'
        if name == 'model1_diagnostics':
            body_files[name + '_cuerpo.md'] += '\nVIF no es una prueba con p-valor. CUSUM no exporta estadístico ni p-valor en esta salida; los vacíos no representan ceros.\n'
        if name == 'lit_estudios':
            notes = []
            for row in raw:
                if row.get('clave') == 'golitsis2022':
                    provenance = re.search(r'\((texto completo,[^)]*)\)', row['signo'])
                    if provenance:
                        notes.append('Procedencia de Golitsis et al.: ' + provenance[1] + '.')
            notes.append('El guion de Obradović y Grubišić remite al signo de la tasa de préstamo explicado en el texto. '
                         'Esa tasa difiere de la tasa de política; el guion no significa un coeficiente cero ni un signo ausente.')
            caption = 'Fuente: matriz de literatura verificada; elaboración propia.'
            table = body_files[name + '_cuerpo.md'].replace('\n\n' + caption, '')
            body_files[name + '_cuerpo.md'] = ('::: {.literature-summary}\n\n' + table.rstrip() + '\n\n'
                + f'**Nota de la Tabla {number}.** ' + ' '.join(notes) + ' ' + caption + '\n\n:::\n')
        if name in {'fred_manifest', 'model1_diagnostics', 'model2_inputs63'}:
            body_files[name + '_cuerpo.md'] = ('::: {.compact-body-table}\n\n'
                + body_files[name + '_cuerpo.md'].rstrip() + '\n\n:::\n')
        body_trace[name] = {'slug': entry['slug'], 'columns': columns, 'rows': rows,
                            'source': entry['source'], 'source_sha256': entry['sha256']}
    for filename, content in list(body_files.items()):
        name = filename.removesuffix('_cuerpo.md')
        anchor = next(r['anchor'] for r in registry if r['name'] == name)
        body_files[filename.replace('_cuerpo.md', '_cuerpo_combinado.md')] = content.replace('anexo-tecnico.pdf#nameddest=' + anchor, '#' + anchor).replace('anexo-tecnico.docx#' + anchor, '#' + anchor)
    return {'annex_files': {filenames[key]: '\n'.join(lines) + '\n' for key, lines in groups.items()},
            'body_files': body_files, 'body_trace': body_trace}


def combined_source(main_text: str, sections: dict[str, str], bodies: dict[str, str], registry: list[dict]) -> str:
    """Alternative single-file delivery: same prose and figures, one complete annex, internal links."""
    import re
    def section(match):
        name = match.group(1)
        if name not in sections:
            raise ValueError(f'Sección combinada ausente: {name}')
        return sections[name]
    text = re.sub(r'\{\{< include (secciones/[^ >]+) >\}\}', section, main_text)
    by_name = {r['name']: r for r in registry}
    def body(match):
        filename = match.group(1)
        if filename not in bodies:
            raise ValueError(f'Tabla combinada ausente: {filename}')
        name = filename.removesuffix('_cuerpo.md')
        anchor = by_name[name]['anchor']
        return '{{< include ../outputs/informe/' + filename.replace('_cuerpo.md', '_cuerpo_combinado.md') + ' >}}'
    text = re.sub(r'\{\{< include ../outputs/informe/([a-z0-9_]+_cuerpo.md) >\}\}', body, text)
    text = text.replace('---\n', '---\nannex-links-internal: true\n', 1)
    return text + '\n\n' + '\n'.join(f'{{{{< include anexos/{name} >}}}}'
                                     for name in ['A-datos.qmd', 'B-modelo-i.qmd', 'C-modelo-ii.qmd',
                                                  'D-estres.qmd', 'E-literatura.qmd', 'F-reproducibilidad.qmd']) + '\n'


def linkify_slug_references(text: str, registry: list[dict], combined: bool = False) -> str:
    """Resolve explicit source slugs using the same registry as the Pandoc filter."""
    import re
    entries = {r['slug']: r for r in registry}
    def replace(match):
        slug = match.group(1)
        if slug not in entries:
            raise ValueError(f'Slug desconocido: {slug}')
        row = entries[slug]
        target = ('#' if combined else 'anexo-tecnico.pdf#nameddest=') + row['anchor']
        return f"[Anexo {row['annex']}, {slug}]({target})"
    return re.sub(r'\*\*((?:AT|AF)-[A-Z0-9-]+)\*\*', replace, text)
