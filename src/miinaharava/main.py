""" main.py """
from runpy import run_path
from pathlib import Path

def main():
    """ Ajaa moduulin hakemistossa jossa tämä tiedosto on """
    my_path = Path(__file__).parent.resolve()
    run_path(f"{my_path}", run_name="miinaharava")

if __name__ == "__main__":
    main()
