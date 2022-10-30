import glob

import pyautogui
from PIL import Image


def find_main_actionbar():
    """
    Searches for the main action bar using actionbar anchor

    :return: action_bar_region, action_bar_slot_regions, action_bar_slot_region_centers
    """
    print("Trying to locate main actionbar...")

    action_bar_anchors = []
    for filename in glob.glob('Images/Actionbar/Anchor/*.png'):
        im = Image.open(filename)
        action_bar_anchors.append(im)

    action_bar_slot_regions = {}
    action_bar_slot_region_centers = {}

    while True:
        for anchor_image in action_bar_anchors:
            bar = pyautogui.locateOnScreen(anchor_image, confidence=0.95, region=ACTIVE_WINDOW_REGION)
            if bar is not None:
                action_bar_region = [bar.left, bar.top, 655, 95]
                for i in range(0, 14):
                    action_bar_slot_regions[i + 1] = [bar.left + 5 + i * 45, bar.top + 50, 40, 40]
                    action_bar_slot_region_centers[i + 1] = autogui.center(ACTION_BAR_SLOT_REGION[i + 1])
                print("Main actionbar located.")
                return action_bar_region, action_bar_slot_regions, action_bar_slot_region_centers

        print("Failed to find main actionbar.")
        print("Set interface transparency to 0%, interface scaling to 100% and your main actionbar horizontally.")
        print("Retrying to find main actionbar after 5 seconds...\n")
        time.sleep(5)
