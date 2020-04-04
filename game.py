import curses
import time
import random
import sys

from obstacle import Obstacle
from dino import Dino
from score import Score
from ascii_numbers import ascii_numbers, clear_text

class Game:
    def __init__(self):
        self.reset()

    def curses_initialize_screen(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)
        curses.curs_set(0)
        self.stdscr.nodelay(1)

    def set_max_dimensions(self):
        self.rows_max, self.cols_max = self.stdscr.getmaxyx()

    def initialize_obstacles(self):
        self.array_obstacles = [
            Obstacle(self, self.cols_max - 1, self.ground_level, 2)
        ]
        self.next_obstacle_generate_time = 0

    def reset(self):
        self.curses_initialize_screen()
        self.set_max_dimensions()

        self.ground_level = self.rows_max - 3
        self.ground_string = '=' * (self.cols_max - 3)

        self.dino = Dino(self)
        self.score = Score(self.stdscr)
        self.initialize_obstacles()

        self.show_loading_animation()

    def show_loading_animation(self):

        def draw_multiline_string(s):
            for y, line in enumerate(s.splitlines(), 2):
                self.stdscr.addstr(y, 2, line)

            self.stdscr.refresh()

        self.stdscr.refresh()
        self.update()

        for ascii_number in ascii_numbers:
            draw_multiline_string(clear_text)
            draw_multiline_string(ascii_number)
            time.sleep(1)

    def handle_key_press(self):
        k = self.stdscr.getch()
        if k == curses.ERR:
            return
        if k == 27:
            self.destroy()
            sys.exit()

        elif k == 98:
            self.reset()

        elif k == 97:
            self.dino.jump()

    def draw_obstacles(self):
        for obstacle in self.array_obstacles:
            obstacle.draw()

    def generate_next_obstacle(self):
        if self.next_obstacle_generate_time - time.time() < 0:
            self.next_obstacle_generate_time = time.time() + random.randint(1, 5)
            self.array_obstacles.append(
                Obstacle(self, self.cols_max - 1, self.ground_level, random.randint(2,4))
            )

    def draw_ground(self):
        self.stdscr.addstr(self.ground_level, 3, self.ground_string)


    def update(self):
        self.stdscr.clear()
        self.set_max_dimensions()
        self.handle_key_press()
        self.draw_obstacles()
        self.generate_next_obstacle()

        self.dino.update()
        self.score.update()
        self.draw_ground()
        self.stdscr.refresh()

    def destroy(self):
        self.stdscr.clear()
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()
