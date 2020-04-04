import curses

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
