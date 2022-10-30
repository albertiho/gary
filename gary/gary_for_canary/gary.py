#! python3import threading

import random
import sys
import threading
import time

import pyautogui
from pynput.mouse import Button, Listener

DEFAULT_MAX_RUN_TIME = 2 * 60 * 60  # 2 hours is our max runtime
DEFAULT_CLICK_INTERVAL = [2.5 * 60, 4.75 * 60]  # default click interval between 2.5 and 4.75 minutes
DEFAULT_GOTE_REFILL_INTERVAL = [9 * 60, 14 * 60]  # default to filling GOTE between 9 and 14 minutes

click_area_coordinates = []
click_area_x_limits = {}
click_area_y_limits = {}
gote_area_coordinates = []
gote_area_x_limits = {}
gote_area_y_limits = {}
gote_refilling = False
gote_clicks = {}
gote_height = 0


def coordinate_initialization(x, y, button, pressed):
    global click_area_coordinates
    global gote_area_coordinates
    if pressed:
        # on left click, add coordinate to list
        if button == Button.right:
            if (len(click_area_coordinates)) < 4:
                click_area_coordinates.append([x, y])
                if (len(click_area_coordinates)) == 4:
                    print("\nClick area configured. Press right-click to continue or use middle mouse to configure GOTE click area.")
            else:
                listener.stop()

        # on right click empty list
        if button == Button.left:
            click_area_coordinates = []
            gote_area_coordinates = []
            print("Click area and GOTE area coordinates reset.")
        # use middle click to define gote area
        if button == Button.middle:
            if (len(gote_area_coordinates)) < 4:
                gote_area_coordinates.append([x, y])
                if (len(gote_area_coordinates)) == 4:
                    print("\nGOTE area configured. Press middle-click to continue or use right click to configure click area.")
            else:
                listener.stop()


def gote_charge_initialization(x, y, button, pressed):
    global gote_clicks
    if "right" in gote_clicks and "left" in gote_clicks:
        listener.stop()
    if pressed:
        if button == Button.right:
            gote_clicks["right"] = [x, y]
        if button == Button.left:
            gote_clicks["left"] = [x, y]
        if button == Button.middle:
            gote_clicks = {}
            print("\nGOTE charge height reset.")


def autoclick_main():
    global gote_refilling
    while True:
        time.sleep(random.randint(*DEFAULT_CLICK_INTERVAL))
        # wait gote refill if it would unluckily happen at the same time
        if gote_refilling:
            time.sleep(5)
        if cursor_in_clicking_area():
            should_move_mouse = random.randint(1, 10)
            if should_move_mouse < 3:
                perform_move()
        else:
            perform_move()
        perform_click()


def cursor_in_clicking_area():
    current_x, current_y = pyautogui.position()
    if current_x > click_area_x_limits["max"] or current_x < click_area_x_limits["min"]:
        return False
    if current_y > click_area_y_limits["max"] or current_y < click_area_y_limits["min"]:
        return False
    return True


def perform_move():
    move_speed = random.randint(20, 40) / 100
    move_to_x = random.randint(click_area_x_limits["min"], click_area_x_limits["max"])
    move_to_y = random.randint(click_area_y_limits["min"], click_area_y_limits["max"])
    pyautogui.moveTo(move_to_x, move_to_y, move_speed)


def perform_click():
    should_doubleclick = random.randint(1, 12)
    if should_doubleclick < 3:
        # generate random number between 0.15 and 0.3s as the time between doubleclick
        doubleclick_interval = random.randint(15, 30) / 100
        pyautogui.click(clicks=2, interval=doubleclick_interval)
    else:
        pyautogui.click()
    move_mouse_after_click = random.randint(1, 12)
    if move_mouse_after_click < 3:
        current_x, current_y = pyautogui.position()
        x_to_move = random.randint(40, 240)
        y_to_move = random.randint(30, 240)
        move_speed = random.randint(20, 40) / 100
        pyautogui.moveTo(current_x + x_to_move, current_y + y_to_move, move_speed)


def perform_gote_refill():
    global gote_refilling
    while True:
        time.sleep(*DEFAULT_GOTE_REFILL_INTERVAL)
        # stop the mouse from moving while gote refill is happening
        gote_refilling = True
        move_to_gote_x = random.randint(gote_area_x_limits["min"], gote_area_x_limits["max"])
        move_to_gote_y = random.randint(gote_area_y_limits["min"], gote_area_y_limits["max"])
        move_speed = random.randint(20, 60) / 100
        pyautogui.moveTo(move_to_gote_x, move_to_gote_y, move_speed)
        pyautogui.click(button="right")
        gote_x_variation = random.randint(-10, 10)
        menu_move_speed = random.randint(15, 25) / 100
        pyautogui.moveTo(move_to_gote_x + gote_x_variation, move_to_gote_y - gote_height, menu_move_speed)
        pyautogui.click()
        gote_refilling = False


def compute_areas():
    click_area_x_coordinates = [coordinate[0] for coordinate in click_area_coordinates]
    click_area_x_limits["max"] = max(click_area_x_coordinates)
    click_area_x_limits["min"] = min(click_area_x_coordinates)

    click_area_y_coordinates = [coordinate[1] for coordinate in click_area_coordinates]
    click_area_y_limits["max"] = max(click_area_y_coordinates)
    click_area_y_limits["min"] = min(click_area_y_coordinates)

    if len(gote_area_coordinates) > 0:
        gote_area_x_coordinates = [coordinate[0] for coordinate in gote_area_coordinates]
        gote_area_x_limits["max"] = max(gote_area_x_coordinates)
        gote_area_x_limits["min"] = min(gote_area_x_coordinates)

        gote_area_y_coordinates = [coordinate[1] for coordinate in gote_area_coordinates]
        gote_area_y_limits["max"] = max(gote_area_y_coordinates)
        gote_area_y_limits["min"] = min(gote_area_y_coordinates)


if __name__ == "__main__":
    """
        This function is executed first when you start up gary, and it will perform the following steps:
        1. Configure the area you want gary to poke
        2. Draw the area on screen
        3. Start the clicking loop
    """

    print("Create a rectangle by RIGHT-clicking the corners of the click area.")
    print()
    print("Use the MIDDLE-mouse button to click the corners of your GOTE if you want to enable gote charging.")
    print()
    print("You can reset click and gote area initialization values with LEFT-click.")

    with Listener(on_click=coordinate_initialization) as listener:
        listener.join()

    print()
    print("Currently selected click area coordinates: ", click_area_coordinates)
    print("Currently selected gote area coordinates: ", gote_area_coordinates)

    compute_areas()

    print("\nUse the \"Charge all porters\" option on your GOTE once to configure GOTE charge height.")

    with Listener(on_click=gote_charge_initialization) as listener:
        listener.join()

    gote_height = gote_clicks["right"][1] - gote_clicks["left"][1]
    print("\nGOTE charge height configured, height is " + str(gote_height) + " pixels. (value should be negative)")
    print("\nStarting auto-click cycle.")
    print("This process can be stopped by pressing CTRL+C a few times with the terminal as active window.")

    main_thread = threading.Thread(target=autoclick_main, daemon=True)
    main_thread.start()

    gote_refill_thread = threading.Thread(target=perform_gote_refill, daemon=True)
    gote_refill_thread.start()

    time.sleep(DEFAULT_MAX_RUN_TIME)
    sys.exit()
