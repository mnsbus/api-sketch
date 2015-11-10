import sched
import time


class PyCron(object):
    """

        A cron-like snippet drawing on the Python standard lib:
        http://www.diegor.it/2014/06/19/howto-schedule-repeating-events-with-python/

    """
    def __init__(self):
        self.scheduler = sched.scheduler(time.time, time.sleep)

    def setup(self, interval, action, actionargs=()):
        action(*actionargs)
        self.scheduler.enter(interval, 1, self.setup,
                        (interval, action, actionargs))

    def run(self):
        self.scheduler.run()
