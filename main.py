import time
import locale
import sys

from obstacle import Obstacle
from dino import Dino
from score import Score
from game import Game

from subprocess import PIPE, Popen, STDOUT
from threading import Thread
from textwrap import dedent

try:
    from queue import Queue, Empty
except ImportError:
    from Queue import Queue, Empty  # python 2.x

ON_POSIX = 'posix' in sys.builtin_module_names

def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()

def popen_and_call(on_exit, q, *popen_args):
    """
    Runs the given args in a subprocess.Popen, and then calls the function
    on_exit when the subprocess completes.
    on_exit is a callable object, and popen_args is a list/tuple of args that 
    would give to subprocess.Popen.
    """
    def run_in_thread(on_exit, popen_args):
        proc = Popen(popen_args, bufsize=1, stdout=PIPE, stderr=PIPE, close_fds=ON_POSIX, universal_newlines=True)
        t = Thread(target=enqueue_output, args=(proc.stdout, q))
        e = Thread(target=enqueue_output, args=(proc.stderr, q))
        t.daemon = True  # thread dies with the program
        t.start()
        e.daemon = True  # thread dies with the program
        e.start()
        on_exit()
        return
    thread = Thread(target=run_in_thread, args=(on_exit, popen_args))
    thread.start()
    # returns immediately after the thread starts
    return thread


locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()

def printonfinish():
    print('YO')
    sys.exit()


if __name__ == "__main__":
    frame_rate = 40
    prev = 0
    # args = sys.argv[1:]
    game = Game()

    q = Queue()
    popen_and_call(printonfinish, q, sys.executable, "-u", "-c", dedent("""
            import itertools, sys, time
            import sys
            for i in range(20):
                print(i, sys.argv[1])
                time.sleep(0.3)
            """), '1')

    while True:
        time_elapsed = time.time() - prev
        if time_elapsed > 1./frame_rate:
            prev = time.time()
            try:
                line = q.get_nowait()  # or q.get(timeout=.1)
            except Empty:
                line = ''
            game.update(line)
