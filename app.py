from board.board import Board
from tui.tui import Tui

b = Board()
t = Tui()
x, y = 0, 0

while True:
    x, y = t.matrix_selector(b.get_view(), x, y)
    if x == -1:
        print("LOPETUS!")
        break
    if not b.make_guess(x, y):
        print("KUOLEMA!")
        break
    if b.is_winning():
        print("VOITTO!")
        break
        
t.draw_matrix(b.get_view(),-1,-1)