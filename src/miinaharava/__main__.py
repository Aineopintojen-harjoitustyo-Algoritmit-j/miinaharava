""" __main__.py - Tästä suoritus alkaa """
import sys

from app import App
from cmdline import args

vars(args)['board'] = None

if args.count is None and args.file is None:
    app = App(args)
    IS_WIN = app.run()
    del app
    sys.exit(not IS_WIN)	# Exit koodeissa 0 on onnistunut suoritus

WIN_COUNT = 0

if args.file is None:
    args.autoplay = 2
    RUN_COUNT = args.count
    for i in range(RUN_COUNT):
        print(end=f"    \rSuoritus {i+1:>6}/{RUN_COUNT} ")
        print(end=f"({100*WIN_COUNT/(i if i else 1):.1f}%)..")
        if not args.quiet:
            print()
        app = App(args)
        WIN_COUNT+=app.run()
        del app
else:
    RUN_COUNT = 0
    with open(args.file, "r", encoding="utf-8") as bfile:
        board = []
        while True:
            line = bfile.readline()
            if not line or (line[0]!='.' and line[0]!='@'):
                if board:
                    WIN_PERCENT = (100*WIN_COUNT/RUN_COUNT) if RUN_COUNT else 0
                    print(end=
                        f"    \rAjo ...{args.file[-18:]:} ({RUN_COUNT+1}): "
                        f"({WIN_PERCENT:.1f}%).."
                    )
                    if not args.quiet:
                        print()
                    args.board = board
                    app = App(args)
                    WIN_COUNT += app.run()
                    RUN_COUNT += 1
                    del app
                    board = []
                if not line:
                    break
                continue
            board.append([x=='@' for x in line if x in ('.', '@')])

print(
    f"\n## Voittoja {WIN_COUNT}/{RUN_COUNT} "
    f"({(100*WIN_COUNT/RUN_COUNT) if RUN_COUNT else 0:.1f}%)"
)
