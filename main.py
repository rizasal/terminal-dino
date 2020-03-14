import time
import curses
import sys
import math
import random
import locale

locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()

class Obstacle:
    def __init__(self, game_object, x, y, h):
        self.x = x
        self.y = y - h - 1
        self.h = h

        self.obstacle_map =[
            [1]
        ] * (h+1)

        self.stdscr = game_object.stdscr
        self.game_object = game_object

    def draw(self):
        self.update()
        for row_index, i in enumerate(self.obstacle_map):
            for col_index, j in enumerate(i):
                if j == 1:
                    self.stdscr.addstr(
                        self.y + row_index,
                        int(self.x) +col_index,
                        bytes(u'\u2588'.encode(code)))
    
    def update(self):
        self.x -= 1.5

        if self.x < 3:
            self.game_object.array_obstacles.remove(self)

        if self.x < self.game_object.cols_max / 4:
            dino = self.game_object.dino

            if dino.x-1 <= self.x <= (dino.x + dino.dino_box_dimension[0]):
                if dino.y <= self.y <=dino.y + dino.dino_box_dimension[1] or dino.y <= self.y+ self.h <=dino.y + dino.dino_box_dimension[1]:
                    self.game_object.destroy()
                    sys.exit()


class Dino:
    def __init__(self, stdscr):
        self.rows_max, self.cols_max = stdscr.getmaxyx()


        self.dy = self.dy_yield()
        self.jumping = False
        self.stdscr = stdscr

        self.dino_map_array_pointer = 0
        self.dino_map = [[
            [0,0,0,0,0,0,0,1,1,0],
            [0,1,1,1,1,1,1,1,1,1],
            [0,1,1,1,1,1,1,0,0,0],
            [0,0,1,0,0,0,0,1,0,0],
        ],
        [
            [0,0,0,0,0,0,0,1,1,0],
            [0,1,1,1,1,1,1,1,1,1],
            [0,1,1,1,1,1,1,0,0,0],
            [0,1,0,0,0,0,1,0,0,0],
        ]]
        self.use_dino_map = 0
        self.dino_box_dimension = (len(self.dino_map), len(self.dino_map[0]))

        self.x = 10
        self.y = self.rows_max - len(self.dino_map[0])


    
    def dy_yield(self):
        for i in range(7):
           yield i * -1
        for i in range(7):
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
        if self.dino_map_array_pointer > 5:
            self.use_dino_map = (self.use_dino_map +1 ) % 2
            self.dino_map_array_pointer = 0
        for row_index, i in enumerate(self.dino_map[self.use_dino_map]):
            for col_index, j in enumerate(i):
                if j == 1 and self.y + row_index > 0:
                    self.stdscr.addstr(
                        self.y + row_index,
                        self.x + col_index,
                        bytes(u'''\u2588'''.encode(code)))
        self.dino_map_array_pointer += 1

class Game:
    def __init__(self):

        self.stdscr = curses.initscr()
        # tweak terminal settings
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)
        curses.curs_set(0)
        self.stdscr.nodelay(1)
        self.rows_max, self.cols_max = self.stdscr.getmaxyx()

        self.dino = Dino(self.stdscr)

        self.array_obstacles = [
            Obstacle(self, self.cols_max - 1, self.rows_max, 2)
        ]
        self.next_obstacle_generate_time = 0

        # update the screen
        self.stdscr.refresh()

    def update(self):
        self.stdscr.clear()
        self.rows, self.cols = self.stdscr.getmaxyx()
        k = self.stdscr.getch()
        if k == 27:
            self.destroy()
            sys.exit()
        
        elif k == 97:
            self.dino.jump()

        for obstacle in self.array_obstacles:
            obstacle.draw()

        if self.next_obstacle_generate_time - time.time() < 0:
            self.next_obstacle_generate_time = time.time() + random.randint(1, 6)
            self.array_obstacles.append(
                Obstacle(self, self.cols_max - 1, self.rows_max, random.randint(1,3))
            )
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

