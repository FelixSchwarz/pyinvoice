
from collections import namedtuple
import importlib.util
import sys


__all__ = ['check_invoice', 'MetaInfo']

MetaInfo = namedtuple('MetaInfo', ('config', 'config_dir', 'invoice_filename'))
CheckResult = namedtuple('CheckResult', ('key', 'message'))

def check_invoice(invoice, meta):
    all_errors = []
    checks = discover_checks(meta.config_dir)
    for check in checks:
        error = check(invoice, meta)
        if error:
            all_errors.append(error)
    return all_errors


def discover_checks(path):
    checker_path = path / 'checks'
    if not checker_path.is_dir():
        return []

    checks = []
    for py_path in checker_path.glob('*.py'):
        filename = py_path.name
        if filename.startswith('.') or filename.startswith('_'):
            continue
        elif '.' in py_path.stem:
            sys.stderr.write(f'file name "{str(py_path)}" contains more than on ".", skipping file.\n')
            continue
        checker_mod = load_checker_from_path(py_path)
        checks.append(checker_mod.check_invoice)
    return checks


def load_checker_from_path(py_path):
    module_name = f'schwarz.pyinvoice.contrib.checks.{py_path.stem}'
    spec = importlib.util.spec_from_file_location(module_name, py_path)
    checker_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checker_mod)
    return checker_mod

