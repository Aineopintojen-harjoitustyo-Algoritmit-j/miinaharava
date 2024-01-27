""" __main__.py - Tästä suoritus alkaa """
from argparse import ArgumentParser
from app import App

parser = ArgumentParser(
    prog='miinaharava',
    description='Klassisen miinaharavapelin terminaali toteutus.',
)
parser.add_argument(
    '-b', '--beginner',
    help='Asettaa aloittelijan vaikeustason (oletus)',
    action='store_true',
)
parser.add_argument(
    '-i', '--intermediate',
    help='Asettaa keskivaikean vaikeustaso',
    action='store_true'
)
parser.add_argument(
    '-e', '--expert',
    help='Asettaa edistyneen vaikeustason (vaatii 100 merkkiä leveän terminaalin)',
    action='store_true'
)
parser.add_argument(
    '-a', '--auto',
    help='Antaa botin pelata automaattisesti',
    action='store_true'
)
parser.add_argument(
    '-u', '--uncertain',
    help='Antaa botille luvan tehdä myös epävarmoja valintoja',
    action='store_true'
)

args = parser.parse_args()

app = App(args)
app.run()
