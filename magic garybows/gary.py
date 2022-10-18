import math
import random
import sys
import threading
import time

import numpy as np
import pyautogui
import pygetwindow
from PIL import Image
from scipy import interpolate

DEFAULT_MAX_RUN_TIME = 6 * 60 * 60  # 4 hours

KEYBIND_FOR_PRESET = 'f2'
KEYBIND_FOR_LOG = '5'

ACTIVE_WINDOW_REGION = []

BANK_REGION = None
BANK_CENTER = None


def initialize_game_window():
    global ACTIVE_WINDOW_REGION
    global BANK_REGION
    global BANK_CENTER

    active_game_window = pygetwindow.getWindowsWithTitle("RuneScape")[0]
    active_game_window.activate()

    ACTIVE_WINDOW_REGION = [active_game_window.left, active_game_window.top, active_game_window.width, active_game_window.height]

    BANK_REGION = pyautogui.locateOnScreen(Image.open('bank.png'), confidence=0.95, region=ACTIVE_WINDOW_REGION)
    center = pyautogui.center(BANK_REGION)
    BANK_CENTER = [center[0], center[1]]


def point_dist(current_x: int, current_y: int, destination_x: int, destination_y: int):
    return math.sqrt(abs(destination_x - current_x) ** 2 + abs(destination_y - current_y) ** 2)


def get_position() -> [int, int]:
    position = pyautogui.position()
    return int(position[0]), int(position[1])


def perform_move(x: int, y: int, ms_variation=None):
    if ms_variation is None:
        ms_variation = [20, 40]

    current_x, current_y = get_position()
    cp = random.randint(3, 5)  # Number of control points. Must be at least 2.

    # Distribute control points between start and destination evenly.
    array_x = np.linspace(current_x, x, num=cp, dtype='int')
    array_y = np.linspace(current_y, y, num=cp, dtype='int')

    # Randomise inner points a bit (+-RND at most).
    rnd = 10
    xr = [random.randint(-rnd, rnd) for k in range(cp)]
    yr = [random.randint(-rnd, rnd) for k in range(cp)]
    xr[0] = yr[0] = xr[-1] = yr[-1] = 0
    array_x += xr
    array_y += yr

    # Approximate using Bezier spline.
    degree = 3 if cp > 3 else cp - 1  # Degree of b-spline. 3 is recommended.
    # Must be less than number of control points.
    try:
        tck, u = interpolate.splprep([array_x, array_y], k=degree)
        # Move up to a certain number of points
        u = np.linspace(0, 1, num=2 + int(point_dist(current_x, current_y, x, y) / 50.0))
        x_points, y_points = interpolate.splev(u, tck)
        xy_points = list(zip([int(x) for x in x_points], [int(y) for y in y_points]))

        # Move mouse.
        duration = random.randint(*ms_variation) / 100
        timeout = duration / len(xy_points)
        for point in xy_points:
            pyautogui.moveTo(*point)
            time.sleep(timeout)
    except:
        pass


def fletching_loop():
    inventories_done = 0
    while True:
        should_move = random.randint(0, 5)
        if should_move < 2:
            perform_move(BANK_CENTER[0] + random.randint(-125, 125),
                         BANK_CENTER[1] + random.randint(-125, 125))

        pyautogui.click()
        time.sleep(random.randint(12, 20) / 10)

        pyautogui.press(KEYBIND_FOR_PRESET, presses=random.randint(1, 3), interval=(random.randint(5, 10) / 100))
        time.sleep(random.randint(12, 20) / 10)

        pyautogui.press(KEYBIND_FOR_LOG)
        time.sleep(random.randint(12, 20) / 10)

        pyautogui.press('space', presses=random.randint(2, 4), interval=(random.randint(5, 10) / 100))
        time.sleep(random.randint(45, 55))

        inventories_done += 1
        print("invetory ", inventories_done, " done")


if __name__ == "__main__":
    """
    TODO: lets comment some stuff here once this gary works okay 
    """
    # The following default settings are overwritten for more human mouse movement
    pyautogui.MINIMUM_DURATION = 0
    pyautogui.MINIMUM_SLEEP = 0
    pyautogui.PAUSE = 0

    initialize_game_window()

    fletching_thread = threading.Thread(target=fletching_loop, daemon=True)
    fletching_thread.start()

    time.sleep(DEFAULT_MAX_RUN_TIME)
    sys.exit()
