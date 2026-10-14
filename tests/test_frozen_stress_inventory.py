"""Harness regressions: protected output mutations and unrelated QA isolation."""
from pathlib import Path

import pytest

from tests import test_frozen_stress as frozen


def write_scientific_fixture(root):
    for name in frozen.SCIENTIFIC_OUTPUTS:
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(name.encode('utf-8'))


def test_modification_of_a_protected_output_is_detected(tmp_path):
    write_scientific_fixture(tmp_path)
    before = frozen.scientific_inventory(tmp_path)
    (tmp_path / 'outputs/models/model1_main.json').write_bytes(b'changed')
    with pytest.raises(AssertionError):
        frozen.assert_protected(before, frozen.scientific_inventory(tmp_path))


def test_deletion_of_a_protected_output_is_detected(tmp_path):
    write_scientific_fixture(tmp_path)
    before = frozen.scientific_inventory(tmp_path)
    after = dict(before)
    del after['outputs/tables/model2_lp.csv']
    with pytest.raises(AssertionError):
        frozen.assert_protected(before, after)


@pytest.mark.parametrize('name', ['stress_unapproved.csv', 'other_unapproved.csv'])
def test_unexpected_scientific_output_is_rejected_even_with_stress_prefix(tmp_path, name):
    write_scientific_fixture(tmp_path)
    (tmp_path / 'outputs/tables' / name).write_bytes(b'unexpected')
    with pytest.raises(AssertionError, match='unexpected'):
        frozen.scientific_inventory(tmp_path)


def test_missing_required_model_input_is_rejected_before_copy(tmp_path):
    source, destination = tmp_path / 'source', tmp_path / 'destination'
    write_scientific_fixture(source)
    (source / 'outputs/models/model2_main.json').unlink()
    with pytest.raises(AssertionError, match='missing'):
        frozen.copy_scientific_outputs(source, destination)
    assert not destination.exists()


def test_qa_and_exact_editorial_exclusions_are_not_copied(tmp_path):
    source, destination = tmp_path / 'source', tmp_path / 'destination'
    write_scientific_fixture(source)
    excluded = ['outputs/informe/stress_levels.csv',
                'outputs/smoke-006/report/informe.pdf',
                'outputs/preview-006/qa-anexo/page-001.png',
                'outputs/preview-006-combinada/report/entrega-combinada.pdf',
                'outputs/tables/lit_estudios.csv', 'outputs/tables/lit_estudios.md']
    for name in excluded:
        path = source / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b'QA or editorial')
    frozen.copy_scientific_outputs(source, destination)
    assert all(not (destination / name).exists() for name in excluded)
    assert frozen.scientific_inventory(destination) == frozen.scientific_inventory(source, allow_editorial=True)


def test_exact_mutable_set_does_not_exempt_an_added_stress_output(tmp_path):
    write_scientific_fixture(tmp_path)
    before = frozen.scientific_inventory(tmp_path)
    after = dict(before)
    after['outputs/tables/stress_unapproved.csv'] = 'unexpected'
    with pytest.raises(AssertionError):
        frozen.assert_protected(before, after)
