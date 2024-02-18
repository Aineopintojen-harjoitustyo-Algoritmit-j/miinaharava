#!/bin/sh
[ x$1 = x ] && echo "\
Pieni ja kevyt skripti helppoa kehitystyökalujen ajoa varten.

Käyttö: $0 <komento>

Komennot:

pytest     Aja yksikkötestit pytestillä
pylint     Tarkista muotoilu pylintillä
covhtml    Tee haarakattavuus raportti html muodossa
covxml     Sama mutta xml muoto (codecov tarvitsee tämän)
covff      Tee html haarakattavuusraportti ja avaa se firefoxissa
all        Sama kuin '$0 covff && $0 pylint'
"

[ $1 = pytest ] && poetry run pytest -v

[ $1 = pylint ] && poetry run python3 -m pylint src/miinaharava/

[ $1 = covhtml ] && poetry run python3 -m coverage run --branch -m pytest -v \
	&& poetry run python3 -m coverage html

[ $1 = covhtml ] && poetry run python3 -m coverage run --branch -m pytest -v \
	&& poetry run python3 -m coverage xml

[ $1 = covff ] && poetry run python3 -m coverage run --branch -m pytest -v \
	&& poetry run python3 -m coverage html && firefox htmlcov/index.html

[ $1 = all ] && poetry run python3 -m coverage run --branch -m pytest -v \
	&& poetry run python3 -m coverage html && firefox htmlcov/index.html \
	&& poetry run python3 -m pylint src/miinaharava/
