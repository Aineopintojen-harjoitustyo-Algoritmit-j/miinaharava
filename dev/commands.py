from subprocess import run
from sys import argv

usage = """
Komentoja kehitykseen:

poetry run dev <komento>

Komennot:
  pytest    Ajaa yksikkötestit
  pylint    Tarkistaa koodin ulkoasun
  coverage  Tutkii haarakattavuuden
  covhtml   Tekee coverage haarakattavuusraportin HTML muodossa
  covxml    Tekee coverage haarakattavuusraportin XML muodossa
  covff     Tekee haarakattavuusraportin ja avaa sen firefoxilla
  all       Sama kuin <covff> + <pylint>
"""

def dev_command():
    if len(argv)==2:
        match argv[1]:
            case "pytest":
                import pytest
                return pytest.main(["-v"])
            case "pylint":
                return run_pylint()
            case "coverage":
                return run_coverage()
            case "covhtml":
                return run_covhtml()
            case "covxml":
                return run_covxml()
            case "covff":
                return run_covff()
            case "all":
                if e := run_covff(): return e
                return run_pylint()
    print(usage)
    return 0

def run_pylint():
    import pylint
    return pylint.run_pylint(argv=["-v", "src/miinaharava"])

def run_coverage():
    return run(
        "poetry run python3 -m coverage run --branch -m pytest -v ".split()
        ).returncode

def run_covhtml():
    if e := run_coverage(): return e
    return run(
        "poetry run python3 -m coverage html".split()
        ).returncode
    
def run_covxml():
    if e := run_coverage(): return e
    return run(
        "poetry run python3 -m coverage xml".split()
        ).returncode
    
def run_covff():
    if e := run_covhtml(): return e
    return run(
        "firefox htmlcov/index.html".split()
        ).returncode
