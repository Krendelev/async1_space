#!/usr/bin/env python3
import asyncio
import curses
import time
from random import choice, random, randrange

from animation import blink, fire, animate_spaceship
from settings import STARS_COUNT, STARS_SYMBOLS, TIC_TIMEOUT


def draw(canvas):
    curses.curs_set(0)
    # canvas.box()
    rows, columns = canvas.getmaxyx()
    coroutines = [
        blink(
            canvas,
            randrange(2, rows - 2),
            randrange(2, columns - 2),
            choice(STARS_SYMBOLS),
        )
        for _ in range(STARS_COUNT)
    ]
    coroutines.append(fire(canvas, rows // 2, columns // 2))
    coroutines.append(animate_spaceship(canvas, rows // 2, columns // 2))
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