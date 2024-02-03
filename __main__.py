""" __main__.py - Tästä suoritus alkaa """
import sys
from app import App

from tui import KEY_DESCRIPTIONS

from cmdline import args

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
