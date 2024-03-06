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
" && exit 0

[ x$PIP = x ] && PIP="pipx"

echo "\033[32m>>> $0 $1 - started.\033[0m"

case $1 in

	install-poetry)
		$PIP install poetry
		;;

	poetry-dev-deps)
		PYTHON_KEYRING_BACKEND=keyring.backends.fail.Keyring \
		poetry install --no-root
		;;
	
	dev)
		$0 install-poetry \
		&& $0 poetry-dev-deps
		;;

	pytest)
		poetry run pytest -v
		;;

	pylint)
		poetry run python3 -m pylint src/miinaharava/
		;;

	coverage)
		poetry run python3 -m coverage run --branch -m pytest -v
		;;

	covhtml)
		$0 coverage \
		&& poetry run python3 -m coverage html
		;;

	covxml)
		$0 coverage \
		&& poetry run python3 -m coverage xml
		;;

	covff)
		$0 covhtml \
		&& firefox htmlcov/index.html
		;;

	all)	$0 covff \
		&& $0 pylint
		;;

	poetry-build)
		poetry build
		;;

	install-latest-build)
		$PIP install `ls dist/*.tar.gz -t -c -1 | head -1` \
		&& echo "For uninstall please use '$PIP uninstall ...'"
		;;

	install)
		$0 install-poetry \
		&& $0 poetry-build \
		&& $0 install-latest-build
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
