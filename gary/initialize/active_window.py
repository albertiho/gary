import pyautogui
import pygetwindow


def initialize_game_window():
    print("Trying to find and initialize the game window...")
    print("Running in a windowed client should be faster when locating items on screen (smaller area to search from)")

    active_game_window = pygetwindow.getWindowsWithTitle("RuneScape")[0]
    active_game_window.activate()

    active_window_region = [active_game_window.left, active_game_window.top, active_game_window.width, active_game_window.height]

    # This is used every time we rotate camera to start from an area which shouldn't have interfaces
    active_window_center = pyautogui.center(active_window_region)

    # limits the area that we search stuff for to 1/2 of the active game window size
    active_window_middle_region = [active_game_window.left + int(1 / 4 * active_game_window.width),
                                   active_game_window.top + int(1 / 5 * active_game_window.height),
                                   active_game_window.width - int(1 / 2 * active_game_window.width),
                                   active_game_window.height - int(1 / 3 * active_game_window.height)]

    print("Game window initialization done, dont re-size or move your window.\n")
    return active_window_region, active_window_center, active_window_middle_region
