""" __main__.py - Käynnistellään ohjelma src/miinaharava kansiosta """
from runpy import run_path
from pathlib import Path

my_path = Path(__file__).parent.resolve()
run_path(f"{my_path}/src/miinaharava", run_name="miinaharava")
