import pytest
import pylint
from subprocess import run

def dev_pylint():
    return pylint.run_pylint(argv=["-v", "src/miinaharava"])

def dev_pytest():
    return pytest.main(["-v"])

def dev_coverage():
    return run(
        "poetry run python3 -m coverage run --branch -m pytest -v ".split()
        ).returncode
    
def dev_covhtml():
    if e := dev_coverage(): return e
    return run(
        "poetry run python3 -m coverage html".split()
        ).returncode
    
def dev_covxml():
    if e := dev_coverage(): return e
    return run(
        "poetry run python3 -m coverage xml".split()
        ).returncode
    
def dev_covff():
    if e := dev_covhtml(): return e
    return run(
        "firefox htmlcov/index.html".split()
        ).returncode

def dev_all():
    if e := dev_covff(): return e
    return dev_pylint()
