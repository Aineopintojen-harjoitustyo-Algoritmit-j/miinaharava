""" __main__.py - Tästä suoritus alkaa """
import sys
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
    '-w',
    metavar='COUNT',
    type=int,
    help='Suorittaa ohelmaa COUNT kertaa ja tulostaa voitto-osuuden',
)

args = parser.parse_args()

if args.w is None:
    app = App(args)
    is_win = app.run()
    del app
    sys.exit(not is_win)	# Exit koodeissa 0 on onnistunut suoritus


win_count = 0
args.uncertain=True
for i in range(args.w):
    print(end=f"    \rSuoritus {i+1:>6}/{args.w} ")
    print(end=f"({100*win_count/(i if i else 1):.1f}%)..")
    if not args.quiet:
        print()
    app = App(args)
    win_count+=app.run()
    del app

print(f"\n## Voittoja {win_count}/{args.w} ({100*win_count/args.w:.1f}%)")
