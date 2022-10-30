import datetime
import math
import random
import threading
import time
from enum import Enum

import numpy as np
import pyautogui
import pygetwindow
from PIL import Image
from scipy import interpolate

DEFAULT_MAX_RUN_TIME = 4 * 60 * 60  # 4 hours

ACTIVE_WINDOW_REGION = []
ACTIVE_WINDOW_CENTER = None

RUNE_ESSENCE = None

NODES = {}
MESSAGES = {}

CURRENTLY_SIPHONING = -1
FOUND_BETTER = False


def initialize_game_window():
    global ACTIVE_WINDOW_REGION
    global ACTIVE_WINDOW_CENTER

    active_game_window = pygetwindow.getWindowsWithTitle("RuneScape")[0]
    active_game_window.activate()

    ACTIVE_WINDOW_REGION = [active_game_window.left, active_game_window.top, active_game_window.width, active_game_window.height - 500]
    ACTIVE_WINDOW_CENTER = pyautogui.center(ACTIVE_WINDOW_REGION)

    print("Game window initialization done, dont re-size or move your window.\n")


def initialize_images() -> str:
    global RUNE_ESSENCE

    test = []
    print("Trying to initialize and load images...")
    RUNE_ESSENCE = Image.open('Images/rune_essence.png')

    NODES[RunespanCreature.ESSWRAITH.name] = Image.open('Images/Nodes/soul_esswraith.png')
    MESSAGES[RunespanCreature.ESSWRAITH.name] = Image.open('Images/Messages/soul_esswraith.png')

    # NODES[RunespanCreature.CYCLONE.name] = Image.open('Images/Nodes/soul_esswraith.png')
    # MESSAGES[RunespanCreature.CYCLONE.name] = Image.open('Images/Messages/soul_esswraith.png')
    #
    # NODES[RunespanCreature.MIND_STORM.name] = Image.open('Images/Nodes/soul_esswraith.png')
    # MESSAGES[RunespanCreature.MIND_STORM.name] = Image.open('Images/Messages/soul_esswraith.png')
    #
    # NODES[RunespanCreature.WATER_POOL.name] = Image.open('Images/Nodes/soul_esswraith.png')
    # MESSAGES[RunespanCreature.WATER_POOL.name] = Image.open('Images/Messages/soul_esswraith.png')

    NODES[RunespanCreature.ROCK_FRAGMENT.name] = Image.open('Images/Nodes/rock_fragment.png')
    MESSAGES[RunespanCreature.ROCK_FRAGMENT.name] = Image.open('Images/Messages/rock_fragment.png')

    # NODES[RunespanCreature.FIRE_STORM.name] = Image.open('Images/Nodes/soul_esswraith.png')
    # MESSAGES[RunespanCreature.FIRE_STORM.name] = Image.open('Images/Messages/soul_esswraith.png')
    #
    # NODES[RunespanCreature.VINE.name] = Image.open('Images/Nodes/soul_esswraith.png')
    # MESSAGES[RunespanCreature.VINE.name] = Image.open('Images/Messages/soul_esswraith.png')

    NODES[RunespanCreature.SKULLS.name] = Image.open('Images/Nodes/skulls.png')
    MESSAGES[RunespanCreature.SKULLS.name] = Image.open('Images/Messages/skulls.png')

    # NODES[RunespanCreature.CHAOTIC_CLOUD.name] = Image.open('Images/Nodes/soul_esswraith.png')
    # MESSAGES[RunespanCreature.CHAOTIC_CLOUD.name] = Image.open('Images/Messages/soul_esswraith.png')

    NODES[RunespanCreature.BLOOD_POOL.name] = Image.open('Images/Nodes/blood_pool.png')
    MESSAGES[RunespanCreature.BLOOD_POOL.name] = Image.open('Images/Messages/blood_pool.png')

    NODES[RunespanCreature.SHIFTER.name] = Image.open('Images/Nodes/shifter.png')
    MESSAGES[RunespanCreature.SHIFTER.name] = Image.open('Images/Messages/shifter.png')

    NODES[RunespanCreature.NEBULA.name] = Image.open('Images/Nodes/nebula.png')
    MESSAGES[RunespanCreature.NEBULA.name] = Image.open('Images/Messages/nebula.png')

    NODES[RunespanCreature.BLOODY_SKULLS.name] = Image.open('Images/Nodes/bloody_skulls.png')
    MESSAGES[RunespanCreature.BLOODY_SKULLS.name] = Image.open('Images/Messages/bloody_skulls.png')

    NODES[RunespanCreature.LIVING_SOUL.name] = Image.open('Images/Nodes/living_soul.png')
    MESSAGES[RunespanCreature.LIVING_SOUL.name] = Image.open('Images/Messages/living_soul.png')

    NODES[RunespanCreature.UNDEAD_SOUL.name] = Image.open('Images/Nodes/undead_soul.png')
    MESSAGES[RunespanCreature.UNDEAD_SOUL.name] = Image.open('Images/Messages/undead_soul.png')

    if None in test:
        return "Failed to load some image, make sure you have all the images downloaded from github"

    print("Images initialized.")


def point_dist(current_x: int, current_y: int, destination_x: int, destination_y: int):
    return math.sqrt(abs(destination_x - current_x) ** 2 + abs(destination_y - current_y) ** 2)


def get_position() -> [int, int]:
    position = pyautogui.position()
    return int(position[0]), int(position[1])


def perform_move(x: int, y: int, ms_variation=None):
    if ms_variation is None:
        ms_variation = [10, 30]

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


def perform_click():
    pyautogui.click()
    time.sleep(random.randint(15, 25) / 100)
    move_mouse_after_click = random.randint(1, 12)
    if move_mouse_after_click < 3:
        current_x, current_y = get_position()
        x_to_move = random.randint(25, 75)
        y_to_move = random.randint(25, 75)
        perform_move(x=current_x + x_to_move,
                     y=current_y + y_to_move,
                     ms_variation=[15, 30])


def focus_minimap_north():
    x_to_click = COMPASS_CENTER[0] + random.randint(-10, 10)
    y_to_click = COMPASS_CENTER[1] + random.randint(-10, 10)
    perform_move(x_to_click, y_to_click)
    perform_click()


class RunespanCreature(Enum):
    ESSWRAITH = 0
    # CYCLONE = 1
    # MIND_STORM = 2
    # WATER_POOL = 3
    ROCK_FRAGMENT = 4
    # FIRE_STORM = 6
    # VINE = 7
    SKULLS = 8
    # CHAOTIC_CLOUD = 9
    BLOOD_POOL = 10
    SHIFTER = 11
    NEBULA = 12
    LIVING_SOUL = 13
    BLOODY_SKULLS = 14
    UNDEAD_SOUL = 15


def reset_mouse_south():
    perform_move(x=ACTIVE_WINDOW_CENTER[0] - random.randint(-300, 300),
                 y=ACTIVE_WINDOW_CENTER[1] + 300 - random.randint(-100, 100))


def start_siphoning(current_node, node_region):
    global CURRENTLY_SIPHONING
    global FOUND_BETTER

    print("current node name, value: ", current_node.name, current_node.value)
    reset_mouse_south()

    CURRENTLY_SIPHONING = current_node.value

    if current_node == RunespanCreature.ESSWRAITH:
        timeout = datetime.datetime.now() + datetime.timedelta(seconds=45)

        while datetime.datetime.now() < timeout and not FOUND_BETTER:
            time.sleep(2)
    else:
        retries = 3
        print("retries, fb:", retries, FOUND_BETTER)
        while retries > 0 and not FOUND_BETTER:
            print("retries: ", retries)
            node_alive = pyautogui.locateOnScreen(NODES[current_node.name], confidence=0.7, region=node_region)
            if node_alive is None:
                print("currently siphoning not found")
                retries -= 1
            time.sleep(3)

    # if the better one was started, the one which is turning off should set found better to false
    if FOUND_BETTER:
        FOUND_BETTER = False
    else:
        CURRENTLY_SIPHONING = -1


def garyspan_loop():
    global FOUND_BETTER

    while True:
        print("searching")
        rune_ess = pyautogui.locateOnScreen(RUNE_ESSENCE, confidence=0.8, region=ACTIVE_WINDOW_REGION)
        if rune_ess is None:
            print("todo fetch rune ess")
        for rc in RunespanCreature:
            node = pyautogui.locateOnScreen(NODES[rc.name], confidence=0.7, region=ACTIVE_WINDOW_REGION)
            if node is not None:
                print("found: ", rc.name)
                if rc.value > CURRENTLY_SIPHONING:
                    node_x, node_y = pyautogui.center(node)
                    perform_move(node_x, node_y)
                    confirmation_region = [node.left - 100, node.top - 30, node.width + 300, node.height + 300]
                    haha = pyautogui.screenshot(region=confirmation_region)
                    confirmation = pyautogui.locateOnScreen(MESSAGES[rc.name], confidence=0.7, region=confirmation_region)
                    if confirmation is not None:
                        if CURRENTLY_SIPHONING > 0:
                            FOUND_BETTER = True
                        perform_click()
                        siphon_thread = threading.Thread(target=start_siphoning, args=[rc, confirmation_region])
                        siphon_thread.start()
                    else:
                        reset_mouse_south()
                        time.sleep(2)
        time.sleep(2)


if __name__ == "__main__":
    pyautogui.MINIMUM_DURATION = 0
    pyautogui.MINIMUM_SLEEP = 0
    pyautogui.PAUSE = 0

    errors = [initialize_game_window(),
              initialize_images()]

    if any(errors):
        for error in errors:
            print(error)
        print("\nFailed to initialize gary, exiting program.")
        exit()

    rc_thread = threading.Thread(target=garyspan_loop, daemon=True)
    rc_thread.start()

    time.sleep(DEFAULT_MAX_RUN_TIME)
    sys.exit()
