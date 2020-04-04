import curses

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
