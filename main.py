import time
import locale

from obstacle import Obstacle
from dino import Dino
from score import Score
from game import Game

locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()

if __name__ == "__main__":
    frame_rate = 40
    prev = 0
    game = Game()

    while True:
        time_elapsed = time.time() - prev
        if time_elapsed > 1./frame_rate:
            prev = time.time()
            game.update()

