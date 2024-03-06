#!/bin/sh

[ x$1 = x ] && echo "\
Pieni ja kevyt skripti helppoa kehitystyökalujen ajoa varten.

Käyttö: $0 <komento>

Komennot:

dev        Asenna devausymäristö
pytest     Aja yksikkötestit pytestillä
pylint     Tarkista muotoilu pylintillä
covhtml    Tee haarakattavuus raportti html muodossa
covxml     Sama mutta xml muoto (codecov tarvitsee tämän)
covff      Tee html haarakattavuusraportti ja avaa se firefoxissa
all        Sama kuin '$0 covff && $0 pylint'
install    Rakenna ja asenna paketti käyttäen pipx & poetry
uninstall  Poistaa paketin (pipx uninstall...)
" && exit 0

echo "\033[32m>>> $0 $1 - started.\033[0m"

case $1 in

	dev)
		pipx install poetry \
		&& PYTHON_KEYRING_BACKEND=keyring.backends.fail.Keyring \
	   	poetry install --no-root
		;;

	pytest)
		poetry run pytest -v
		;;

	pylint)
		poetry run python3 -m pylint src/miinaharava/
		;;

	covhtml)
		poetry run python3 -m coverage run --branch -m pytest -v \
		&& poetry run python3 -m coverage html
		;;

	covxml)
		poetry run python3 -m coverage run --branch -m pytest -v \
		&& poetry run python3 -m coverage xml
		;;

	covff)
		poetry run python3 -m coverage run --branch -m pytest -v \
		&& poetry run python3 -m coverage html \
		&& firefox htmlcov/index.html
		;;

	all)	poetry run python3 -m coverage run --branch -m pytest -v \
		&& poetry run python3 -m coverage html \
		&& firefox htmlcov/index.html \
		&& poetry run python3 -m pylint src/miinaharava/
		;;

	install)
		pipx install poetry \
		&& poetry build \
		&& pipx install `ls dist/*.tar.gz -t -c -1 | head -1`
		;;

	uninstall)
		pipx uninstall miinaharava
		;;

	*)	
		echo "\033[31m<<< $0 $1 - unknown command.\033[0m"
		exit 1
		;;
esac

STATUS=$?

[ $STATUS != 0 ] \
	&& echo "\033[31m<<< $0 $1 - exited with code $STATUS.\033[0m" \
	&& exit $STATUS
	
echo "\033[32m<<< $0 $1 - done.\033[0m"
