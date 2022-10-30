import math
import random
import time

import numpy as np
import pyautogui
from scipy import interpolate


class CustomAutoGui:
    def __init__(self):
        # Override some settings here to avoid doing it everywhere
        pyautogui.MINIMUM_DURATION = 0
        pyautogui.MINIMUM_SLEEP = 0
        pyautogui.PAUSE = 0

    @staticmethod
    def __point_dist(current_x: int, current_y: int, destination_x: int, destination_y: int):
        return math.sqrt(abs(destination_x - current_x) ** 2 + abs(destination_y - current_y) ** 2)

    @staticmethod
    def get_position() -> [int, int]:
        position = pyautogui.position()
        return int(position[0]), int(position[1])

    def perform_move(self, x: int, y: int, ms_variation=None):
        if ms_variation is None:
            ms_variation = [20, 40]

        current_x, current_y = self.get_position()
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
        degree = 3 if cp > 3 else cp - 1  # Degree of b-spline. 3 is recommended. Must be less than number of control points.

        # TODO: this guy crashes on some error, i think its due to having more degrees than items in the lists,
        # TODO: might want to have if-else clause instead for more controlled execution as this can surprisingly fail
        try:
            tck, u = interpolate.splprep([array_x, array_y], k=degree)
            # Move up to a certain number of points
            u = np.linspace(0, 1, num=2 + int(self.__point_dist(current_x, current_y, x, y) / 50.0))
            x_points, y_points = interpolate.splev(u, tck)
            xy_points = list(zip([int(x) for x in x_points], [int(y) for y in y_points]))

            # Move mouse.
            duration = random.randint(*ms_variation) / 100
            timeout = duration / len(xy_points)
            for point in xy_points:
                pyautogui.moveTo(*point)
                time.sleep(timeout)
        except Exception as e:
            print("Failed to perform move.")
            print(e)
            pass

    @staticmethod
    def perform_click(allow_doubleclick: bool = True):
        if allow_doubleclick:
            if random.randint(1, 12) < 3:
                doubleclick_interval = random.randint(5, 10) / 100
                pyautogui.click(clicks=2, interval=doubleclick_interval)
            else:
                pyautogui.click()
        else:
            pyautogui.click()
        move_mouse_after_click = random.randint(1, 12)
        if move_mouse_after_click < 3:
            current_x, current_y = get_position()
            x_to_move = random.randint(25, 75)
            y_to_move = random.randint(25, 75)
            perform_move(x=current_x + x_to_move,
                         y=current_y + y_to_move,
                         ms_variation=[15, 30])
