""" __main__.py - Tästä suoritus alkaa """
import sys
from argparse import ArgumentParser
from app import App

parser = ArgumentParser(
    prog='miinaharava',
    description='Klassisen miinaharavapelin terminaali toteutus.',
)
parser.add_argument(
    '-i', '--intermediate',
    help='Asettaa keskivaikean vaikeustaso (oletus on aloittelija)',
    action='store_true'
)
parser.add_argument(
    '-e', '--expert',
    help='Asettaa edistyneen vaikeustason (vaatii 100 merkkiä leveän terminaalin)',
    action='store_true'
)
parser.add_argument(
    '-s', '--simple',
    help='Käytä yksinkertaisempaa vain yhtä pistettä tutkivaa bottia',
    action='store_true'
)
parser.add_argument(
    '-a', '--auto',
    help='Antaa botin pelata automaattisesti',
    action='store_true'
)
parser.add_argument(
    '-u', '--uncertain',
    help='Antaa botille luvan tehdä myös epävarmoja valintoja (asettaa myös -a asetuksen)',
    action='store_true'
)
parser.add_argument(
    '-q', '--quiet',
    help='Tulostaa minimaalisesti (asettaa myös -a ja -u asetukset)',
    action='store_true'
)
parser.add_argument(
    '-c',
    metavar='COUNT',
    type=int,
    help='Suorittaa ohelmaa COUNT kertaa ja tulostaa voitto-osuuden.',
)
parser.add_argument(
    '-w',
    metavar='WIDTH',
    type=int,
    help='Mukautaa pelilaudan leveydelle WIDTH. (resetoi vaikeustason)',
)
parser.add_argument(
    '-H',
    metavar='HEIGHT',
    type=int,
    help='Mukautaa pelilaudan korkeudelle HEIGTH. (resetoi vaikeustason)',
)
parser.add_argument(
    '-b',
    metavar='BOMBS',
    type=int,
    help='Säätää pelilaulla olevien pommien määrän BOMBS:ksi. (resetoi vaikeustason)',
)

args = parser.parse_args()

if args.c is None:
    app = App(args)
    is_win = app.run()
    del app
    sys.exit(not is_win)	# Exit koodeissa 0 on onnistunut suoritus


win_count = 0
run_count = args.c
args.uncertain=True
for i in range(run_count):
    print(end=f"    \rSuoritus {i+1:>6}/{run_count} ")
    print(end=f"({100*win_count/(i if i else 1):.1f}%)..")
    if not args.quiet:
        print()
    app = App(args)
    win_count+=app.run()
    del app

print(f"\n## Voittoja {win_count}/{run_count} ({100*win_count/run_count:.1f}%)")
