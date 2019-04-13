#!/usr/bin/env python2

from collections import deque

class Dispatcher(object):
    def __init__(self, tasks):
        self.tasks = deque(tasks)

    def next(self):
        return self.tasks.pop()

    def run(self):
        while len(self.tasks):
            task = self.next()
            try:
                next(task)
            except StopIteration:
                pass
            else:
                self.tasks.appendleft(task)

def greeting(name, times):
    for i in range(times):
        yield
        print("Hello, %s.%d!" % (name, i))

dispatcher = Dispatcher([greeting('Liam', 5),
    greeting('Sophia', 4),
    greeting('Cancan', 6)])

dispatcher.run()

