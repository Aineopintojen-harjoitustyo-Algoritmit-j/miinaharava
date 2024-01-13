from board.board import Board
from tui.tui import Tui, Action

b = Board(13)
t = Tui()
x, y = 0, 0

for _ in range(b.size):
    print()

while True:
    action, x, y = t.matrix_selector(b.get_view(), x, y)
    match action:
        case Action.QUIT:
            #            t.draw_matrix(b.get_view(),-1,-1)
            print("LOPETUS!")
            break
        case Action.OPEN:
            if b.get_mask(x, y) and not b.make_guess(x, y):
                t.draw_matrix(b.get_view(), -1, -1)
                print("KUOLEMA!")
                break
            elif b.is_winning():
                t.draw_matrix(b.get_view(), -1, -1)
                print("VOITTO!")
                break
        case Action.FLAG:
            b.flag_tile(x, y)
