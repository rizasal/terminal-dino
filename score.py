import curses

class Score:
    def __init__(self, stdscr):
        self.score = 0
        self.stdscr = stdscr
        self.y, self.x = 2, stdscr.getmaxyx()[1] - 15

    def update(self):
        self.score += 1
        self.draw()

    def draw(self):
        self.stdscr.addstr(self.y, self.x, 'SCORE :{}'.format(str(self.score)), curses.A_STANDOUT)
