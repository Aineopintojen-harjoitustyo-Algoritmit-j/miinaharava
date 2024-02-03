""" __main__.py - Tästä suoritus alkaa """
import sys
from app import App

from cmdline import args

if args.count is None and args.file is None:
    app = App(args)
    is_win = app.run()
    del app
    sys.exit(not is_win)	# Exit koodeissa 0 on onnistunut suoritus

win_count = 0
args.autoplay = 2

if args.file is None:
    run_count = args.count
    for i in range(run_count):
        print(end=f"    \rSuoritus {i+1:>6}/{run_count} ")
        print(end=f"({100*win_count/(i if i else 1):.1f}%)..")
        if not args.quiet:
            print()
        app = App(args)
        win_count+=app.run()
        del app
else:
    run_count = 0
    print(f"Pelataan miinaharavat tiedostosta {args.file}")
    with open(args.file, "r", encoding="utf-8") as bfile:
        board = []
        while True:
            line = bfile.readline()
            if not line or (line[0]!='.' and line[0]!='@'):
                if board:
                    args_dict = vars(args)
                    args_dict['board'] = board
                    app = App(args)
                    win_count += app.run()
                    run_count += 1
                    del app
                    board = []
                if not line:
                    break
                continue
            board.append([x=='@' for x in line if x in ('.', '@')])

print(
    f"\n## Voittoja {win_count}/{run_count} "
    f"({(100*win_count/run_count) if run_count else 0:.1f}%)"
)
