import time
import curses

class Dino:
    def __init__(self, stdscr):
        self.x = 0
        self.y = 20
        self.running = True
        self.stdscr = stdscr
    
    def update(self):
        self.stdscr.addstr(self.y, self.x, 'dino!')
        if self.y > 1:
            self.y -= 1

    def destroy(self):
        # clear the screen
        stdscr.clear()

        # reverse terminal settings
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()

        # close the application
        curses.endwin()
        
        
class Game:
    def __init__(self):

        self.stdscr = curses.initscr()

        # tweak terminal settings
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)
        curses.curs_set(0)

        # write something on the screen
        self.stdscr.addstr(5, 10, "Hello, world!")
        self.dino = Dino(self.stdscr)

        # update the screen
        self.stdscr.refresh()
    
    def update(self):
        self.stdscr.clear()
        self.dino.update()
        self.stdscr.refresh()

if __name__ == "__main__":
    frame_rate = 30
    prev = 0
    game = Game()
    while True:
        time_elapsed = time.time() - prev

        if time_elapsed > 1./frame_rate:
            prev = time.time()
            game.update()

# wait for 3 seconds
time.sleep(3)

