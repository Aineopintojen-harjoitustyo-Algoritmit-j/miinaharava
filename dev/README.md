# Ohjeita kehitykseen
## Riippuvuuksien asennus:
`PYTHON_KEYRING_BACKEND=keyring.backends.fail.Keyring poetry install`

## Aja pytest:
`poetry run pytest`

## Generoi haarakattavuusraportti:
`poetry run covhtml`

## Avaa haarakattavuusraportti Firefoxilla:
`poetry run covff`

## Linttaus:
`poetry run pylint`

## Kaikki
`poetry run all`
