import time
import curses
import sys
import math

import locale

locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()

class Cactus:
    def __init__(self, x, y, stdscr):
        self.x = x
        self.y = y

        self.jumping = False
        self.stdscr = stdscr    

    def update(self):
        if self.x > 0:
            self.x -=1
            self.stdscr.addstr(self.y, self.x, 'dino!')

class Dino:
    def __init__(self, stdscr):
        self.x = 10
        self.y = 15

        self.dy = self.dy_yield()
        self.jumping = False
        self.stdscr = stdscr

        self.dino_map = [
            [0,0,0,0,0,1],
            [1,1,1,1,1,0],
            [1,1,1,1,1,0],
            [1,0,0,0,1,0],
            [1,0,0,0,1,0],
        ]
    
    def dy_yield(self):
        for i in range(5):
           yield i * -1
        for i in range(5):
           yield i
    
    def jump(self):
        if self.jumping == True:
            return 
        self.dy = self.dy_yield()
        self.jumping = True

    def update(self):
        if self.jumping:
            try:
                self.y += next(self.dy)
            except StopIteration as e:
                self.dy = 0
                self.jumping = False
        
        self.draw()
    
    def draw(self):
        for row_index, i in enumerate(self.dino_map):
            for col_index, j in enumerate(i):
                if j == 1:
                    self.stdscr.addstr(
                        self.y + row_index,
                        self.x +col_index,
                        bytes(u'\u2588'''.encode(code)))

class Game:
    def __init__(self):

        self.stdscr = curses.initscr()
        # tweak terminal settings
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)
        curses.curs_set(0)
        self.stdscr.nodelay(1)

        self.dino = Dino(self.stdscr)

        # update the screen
        self.stdscr.refresh()

    def update(self):
        self.stdscr.clear()
        k = self.stdscr.getch()
        if k == 27:
            self.destroy()
            sys.exit()
        
        elif k == 97:
            self.dino.jump()

        self.dino.update()
        self.stdscr.refresh()

    def destroy(self):
        # clear the screen
        self.stdscr.clear()

        # reverse terminal settings
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()

        # close the application
        curses.endwin()

if __name__ == "__main__":
    frame_rate = 30
    prev = 0
    game = Game()

    while True:
        time_elapsed = time.time() - prev
        if time_elapsed > 1./frame_rate:
            prev = time.time()
            game.update()

