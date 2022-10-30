import datetime
import random
import time

import pyautogui
from PIL import Image

from gary.generic.base import CustomAutoGui
from gary.initialize.active_window import initialize_game_window

DEFAULT_MAX_RUN_TIME = 5 * 60 * 60  # 5 hours

KEYBIND_FOR_PRESET = 'f2'
KEYBIND_FOR_SPELL = '2'

if __name__ == "__main__":
    """
    This guy uses spin flax spell
    """
    active_window_region, _, _ = initialize_game_window()

    bank_center = pyautogui.center(pyautogui.locateOnScreen(Image.open('bank.png'), confidence=0.9, region=active_window_region))
    end_time = datetime.datetime.now() + datetime.timedelta(seconds=DEFAULT_MAX_RUN_TIME)

    cag = CustomAutoGui()

    inventories_done = 0
    while datetime.datetime.now() < end_time:
        should_move = random.randint(0, 10)
        if should_move < 2:
            cag.perform_move(x=bank_center[0] + random.randint(-125, 125),
                             y=bank_center[1] + random.randint(-125, 125))

        pyautogui.click()
        time.sleep(random.randint(12, 20) / 10)

        pyautogui.press(KEYBIND_FOR_PRESET, presses=random.randint(1, 3), interval=(random.randint(10, 15) / 100))
        time.sleep(random.randint(12, 20) / 10)

        pyautogui.press(KEYBIND_FOR_SPELL)
        time.sleep(random.randint(100, 120) / 10)

        inventories_done += 1
        print("inventory ", inventories_done, " done")
