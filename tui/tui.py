import termios, fcntl, sys, os
fd = sys.stdin.fileno()

oldterm = termios.tcgetattr(fd)
newattr = termios.tcgetattr(fd)
newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
termios.tcsetattr(fd, termios.TCSANOW, newattr)

oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)


class Tui():
    def __init__(self):
        # https://stackoverflow.com/questions/983354/how-do-i-wait-for-a-pressed-key
        fd = sys.stdin.fileno()
        oldterm = termios.tcgetattr(fd)
        newattr = termios.tcgetattr(fd)
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, newattr)
        
    def __del__(self):
        termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
        
    def set_color(self, color):
        if color>=0 and color<16:
            print(end=f"\033[{'1;' if color//8 else ''}3{color%8}m")

    def set_bg(self, color):
        if color>=0 and color<8:
            print(end=f"\033[4{color}m")

    def cursor_up(self, lines):
        print(end=f"\033[{lines}F")

    def reset_color(self):
        print(end="\033[0m")
        
    def draw_tile(self, tile, hilighted):
        chars_and_colors = (
            (' ', 7, 0), ('1', 10, 0), ('2', 12, 0),
            ('3', 11, 0), ('4', 9, 0), ('5', 9, 0),
            ('6', 9, 0), ('7', 9, 0), ('8', 9, 0),
            ('9', 15, 1), ('#', 8, 7)
        )

        if hilighted:
            self.set_color(14)
            self.set_bg(6)
        else:
            self.set_color(chars_and_colors[tile][1])
            self.set_bg(chars_and_colors[tile][2])
            
        print(end=f"[{chars_and_colors[tile][0]}]")
        self.reset_color()
        
    def draw_matrix(self, matrix, hx, hy ):
        self.cursor_up(len(matrix[0]))
        for y in range(len(matrix[0])):
            for x in range(len(matrix)):
                self.draw_tile( matrix[x][y], 
                        x == hx and y == hy )
            print()
                
    def matrix_selector(self, matrix, x,y ):
        self.draw_matrix(matrix, x, y)
        while True:
            try:
                c = sys.stdin.read(1)
            except:
                continue
            match c:
                case 'A':
                    y-=1
                case 'B':
                    y+=1
                case 'C':
                    x+=1
                case 'D':
                    x-=1
                case '':
                    continue
                case 'q':
                    return (-1,-1)
                case ' ':
                    return (x,y)
                case _:
                    continue
            x = 0 if x < 0 else x
            y = 0 if y < 0 else y
            x = len(matrix)-1 if x >= len(matrix) else x
            y = len(matrix[0])-1 if y >= len(matrix[0]) else y
            
            self.draw_matrix(matrix, x, y)
            
        