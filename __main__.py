""" __main__.py - Tästä suoritus alkaa """
import sys
from argparse import ArgumentParser
from app import App

from tui import KEY_DESCRIPTIONS

parser = ArgumentParser(
    prog='miinaharava',
    description='Klassisen miinaharavapelin terminaali toteutus.',
    add_help=False
)
level_group = parser.add_argument_group('Vaikeustaso')
level_group.add_argument(
    '-i', '--intermediate',
    help='keskivaikea (oletus on aloittelija)',
    action='store_true'
)
level_group.add_argument(
    '-e', '--expert',
    help='edistynyt (vaatii 100 merkkiä leveän terminaalin)',
    action='store_true'
)


custom_group = parser.add_argument_group('Mukautettu vaikeustaso')
def board_size(wxh_string):
    """ parser for dimensions. throws error on bad input"""
    w, h = wxh_string.split('x')
    return (int(w), int(h))
custom_group.add_argument(
    '-s', '--size',
    metavar='<S>',
    type= board_size,
    dest='size',
    help='Pelikentän koko, missä <S> on {leveys}x{korkeus}.'
)
custom_group.add_argument(
    '-m', '--mines',
    metavar='<M>',
    type=int,
    dest='mines',
    help='Säätää pelilaulla olevien pommien määrän <M>:ksi.',
)


hint_group = parser.add_argument_group('Tekoäly')
hint_group.add_argument(
    '-a', '--auto',
    dest='autoplay',
    default=0,
    action='count',
    help='Pelaa tekoälyn vihjeet. [-aa] Pelaa myös epävarmat.'
)
hint_group.add_argument(
    '-b', '--bot', metavar='<B>',
    choices=range(2),
    type=int,
    default=2,
    help='Valitsee tekoälyn <B>, missä: 0: Ei tekoälyä  1: Yksinkertainen, 2: DSSP (oletus)',
)

batch_group = parser.add_argument_group('Automatisointi')
batch_group.add_argument(
    '-q', '--quiet',
    help='Tulostaa minimaalisesti (asettaa myös [-aa])',
    action='store_true'
)
batch_group.add_argument(
    '-c', '--count',
    metavar='<C>',
    type=int,
    dest='count',
    help='Suorittaa ohelmaa <C> kertaa ja tulostaa voitto-osuuden.',
)

misc_group = parser.add_argument_group('Sekalaista')
misc_group.add_argument(
    '-h', '--help',
    help='Tulostaa tämän viestin',
    action='store_true'
)
misc_group.add_argument(
    '-k', '--keys',
    help='Tulostaa pelin näppäinkartan.',
    action='store_true'
)

args = parser.parse_args()

if args.help:
    parser.print_help()
    sys.exit()

if args.keys:
    print(end=KEY_DESCRIPTIONS)
    sys.exit()

if args.count is None:
    app = App(args)
    is_win = app.run()
    del app
    sys.exit(not is_win)	# Exit koodeissa 0 on onnistunut suoritus


win_count = 0
run_count = args.count
args.autoplay = 2
for i in range(run_count):
    print(end=f"    \rSuoritus {i+1:>6}/{run_count} ")
    print(end=f"({100*win_count/(i if i else 1):.1f}%)..")
    if not args.quiet:
        print()
    app = App(args)
    win_count+=app.run()
    del app

print(f"\n## Voittoja {win_count}/{run_count} ({100*win_count/run_count:.1f}%)")
