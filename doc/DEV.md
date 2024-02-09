# Ohjeita kehitykseen
## Riippuvuuksien asennus:
`PYTHON_KEYRING_BACKEND=keyring.backends.fail.Keyring poetry install --no-root`

## Aja pytest:
`poetry run python3 -m pytest`

## Generoi haarakattavuusraportti:
`poetry run python3 -m coverage run --branch -m pytest -v && poetry run python3 -m coverage html && firefox htmlcov/index.html`

## Linttaus:
`poetry run python3 -m pylint -v .`

## Kaikki samassa:
`poetry run python3 -m coverage run --branch -m pytest -v && poetry run python3 -m coverage html && firefox htmlcov/index.html && poetry run python3 -m pylint -v .`

