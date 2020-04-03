import time
import curses
import sys
import math
import random
import locale

locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()

ascii_numbers = [
'''
 3333
33  33
   333
33  33
 3333
''','''
 2222
22  22
   22
  22
222222
''',
'''
1111
  11
  11
  11
111111''',
]
clear_text = '''
                               
                             
                            
                          
'''

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
                        '|', curses.A_STANDOUT)
    
    def update(self):
        self.x -= 1.5

        if self.x < 3:
            self.game_object.array_obstacles.remove(self)

        if self.x < 15:
            dino = self.game_object.dino

            if dino.x-1 <= self.x <= (dino.x + dino.dino_box_dimension[0]):
                if dino.y <= self.y <=dino.y + dino.dino_box_dimension[1] or dino.y <= self.y+ self.h <=dino.y + dino.dino_box_dimension[1]:
                    # self.game_object.destroy()
                    self.game_object.reset()


class Dino:
    def __init__(self, game_object):
        self.game_object = game_object
        self.rows_max, self.cols_max = game_object.stdscr.getmaxyx()


        self.dy = self.dy_yield()
        self.jumping = False
        self.stdscr = game_object.stdscr

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
        self.y = self.game_object.ground_level - len(self.dino_map[0])


    
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
                        '.', curses.A_STANDOUT)
        self.dino_map_array_pointer += 1

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

if __name__ == "__main__":
    frame_rate = 40
    prev = 0
    game = Game()

    while True:
        time_elapsed = time.time() - prev
        if time_elapsed > 1./frame_rate:
            prev = time.time()
            game.update()

