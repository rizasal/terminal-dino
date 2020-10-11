import time
import locale
import sys

from obstacle import Obstacle
from dino import Dino
from score import Score
from game import Game, ExitGame
from bcolors import bcolors

from subprocess import PIPE, Popen, STDOUT
from threading import Thread
import threading
from textwrap import dedent
from process_runner import read_popen_pipes


try:
    from queue import Queue, Empty
except ImportError:
    from Queue import Queue, Empty  # python 2.x

ON_POSIX = 'posix' in sys.builtin_module_names


locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()

if __name__ == "__main__":
    frame_rate = 40
    prev = 0
    # args = sys.argv[1:]
    game = Game()

    q_out = Queue()
    q_err = Queue()

    proc = Popen([sys.executable, "-u", "-c", dedent("""
            import itertools, sys, time
            import sys
            for i in range(5):
                print(i, sys.argv[1])
                # time.sleep(0.5)
            raise Exception("HAHAHAHAHA")
            """), '1'], bufsize=1, stdout=PIPE, stderr=PIPE, close_fds=ON_POSIX, universal_newlines=True)

    gen=read_popen_pipes(proc)
    output = ''
    stopIteration = False
    try:
        while True:
            time_elapsed = time.time() - prev
            if time_elapsed > 1./frame_rate:
                prev = time.time()
                if not stopIteration:
                    try:
                        out_line, err_line = next(gen)
                        output += out_line + bcolors.FAIL + err_line + bcolors.ENDC
                    except StopIteration:
                        stopIteration = True
                game.update(out_line)
    except KeyboardInterrupt:
        game.destroy()
    except ExitGame:
        pass
    print(output)
