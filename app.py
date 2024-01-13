from board.board import Board
from tui.tui import Tui

b = Board(10)
t = Tui()
x, y = 0, 0

for _ in range(b.size):
    print()

while True:
    x, y = t.matrix_selector(b.get_view(), x, y)
    if x == -1:
        t.draw_matrix(b.get_view(),-1,-1)
        print("LOPETUS!")
        break
    if b.get_mask(x,y) and not b.make_guess(x, y):
        t.draw_matrix(b.get_view(),-1,-1)
        print("KUOLEMA!")
        break
    if b.is_winning():
        t.draw_matrix(b.get_view(),-1,-1)
        print("VOITTO!")
        break

