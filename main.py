#!/usr/bin/env python3
import asyncio
import curses
import time
from random import choice, randrange

from animation import animate_spaceship, blink, fire
from settings import STARS_COUNT, STARS_SYMBOLS, TIC_TIMEOUT


def draw(canvas):
    curses.curs_set(0)
    canvas.nodelay(True)

    rows, columns = canvas.getmaxyx()
    coroutines = [
        blink(canvas, randrange(rows), randrange(columns), choice(STARS_SYMBOLS),)
        for _ in range(STARS_COUNT)
    ]
    coroutines.append(animate_spaceship(canvas, rows // 2, columns // 2))
    # coroutines.append(fire(canvas, rows // 2, columns // 2))
    while True:
        try:
            for coroutine in coroutines.copy():
                coroutine.send(None)
        except StopIteration:
            coroutines.remove(coroutine)
        canvas.refresh()
        time.sleep(TIC_TIMEOUT)


if __name__ == "__main__":
    curses.update_lines_cols()
    curses.wrapper(draw)
