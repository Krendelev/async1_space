import asyncio
import curses
import os
import random

from curses_tools import draw_frame, get_frame_size, read_controls
from settings import STARS_COUNT, TIC_TIMEOUT, FRAMES_DIR


def load_frames(item):
    files = [entry for entry in os.scandir(FRAMES_DIR) if entry.name.startswith(item)]
    frames = []
    for entry in files:
        with open(entry) as fh:
            frames.append(fh.read())
    return frames


async def animate_spaceship(canvas, row, column):
    frames = load_frames("rocket")

    row_max, column_max = canvas.getmaxyx()
    height, width = get_frame_size(frames[0])

    row_max -= height
    column_max -= width
    row -= height // 2
    column -= width // 2

    while True:
        for frame in frames:
            rows_direction, columns_direction, _ = read_controls(canvas)

            new_row = row + rows_direction
            new_column = column + columns_direction

            row = min(new_row, row_max) if new_row >= 0 else 0
            column = min(new_column, column_max) if new_column >= 0 else 0

            draw_frame(canvas, row, column, frame)
            await asyncio.sleep(0)
            draw_frame(canvas, row, column, frame, negative=True)


async def blink(canvas, row, column, symbol="*"):
    styles = ("A_DIM", "A_NORMAL", "A_BOLD", "A_NORMAL")
    delays = (2, 0.3, 0.5, 0.3)
    for _ in range(round(random.random() * STARS_COUNT)):
        await asyncio.sleep(0)
    while True:
        for style, delay in zip(styles, delays):
            canvas.addch(row, column, symbol, getattr(curses, style))
            for _ in range(round(delay / TIC_TIMEOUT)):
                await asyncio.sleep(0)


async def fire(canvas, start_row, start_column, rows_speed=-0.3, columns_speed=0):
    """Display animation of gun shot. Direction and speed can be specified."""

    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), "*")
    await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), "O")
    await asyncio.sleep(0)
    canvas.addstr(round(row), round(column), " ")

    row += rows_speed
    column += columns_speed

    symbol = "-" if columns_speed else "|"

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), " ")
        row += rows_speed
        column += columns_speed
