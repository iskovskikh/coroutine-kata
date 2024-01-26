from collections import deque
from time import time


class Scheduler:

    def __init__(self):
        self.queue = deque()

    def add(self, callback: callable):
        self.queue.append(callback)

    def run(self):
        while self.queue:
            callback = self.queue.popleft()
            callback()

    def create_task(self, coroutine):
        task = Task(coroutine, self)
        return task


class Task:

    def __init__(self, coroutine, scheduler):
        self.coroutine = coroutine
        # self.stack = []
        self.scheduler = scheduler
        self.schedule()

    def step(self):
        try:
            self.coroutine.send(None)

        except StopIteration:
            pass
        else:
            self.schedule()

    def schedule(self):
        self.scheduler.add(self.step)


def sleep(delay=0):
    d = time() + delay
    while True:
        yield
        if d <= time():
            break


def courutine():
    result = 0
    for number in range(10):
        result += number
        print('Now yielding!')
        yield
    return result


def tick():
    # for _ in range(10):
    #     print('Tick')
    #     yield sleep(2)
    result = yield from courutine()
    print(result)


def tock():
    # yield sleep(1)
    for _ in range(10):
        print('Tock')
        # yield sleep(2)
        yield


def main():
    scheduler = Scheduler()
    scheduler.create_task(tick())
    scheduler.create_task(tock())
    scheduler.run()


if __name__ == '__main__':
    main()
