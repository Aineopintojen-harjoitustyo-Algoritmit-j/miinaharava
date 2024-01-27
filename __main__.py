""" __main__.py - Tästä suoritus alkaa """
from argparse import ArgumentParser
from app import App

parser = ArgumentParser(
    prog='miinaharava',
    description='Klassisen miinaharavapelin terminaali toteutus.',
)
parser.add_argument(
    '-b', '--beginner',
    help='Aseta aloittelijan vaikeustaso (oletus)',
    action='store_true',
)
parser.add_argument(
    '-i', '--intermediate',
    help='Aseta keskivaikea vaikeustaso',
    action='store_true'
)
parser.add_argument(
    '-e', '--expert',
    help='Aseta edistynyt vaikeustaso (vaatii 100 merkkiä leveän terminaalin)',
    action='store_true'
)


args = parser.parse_args()

app = App(args)
app.run()
