import pyautogui


def find_minimap(active_window_region):
    """
    Finds the minimap on a game window
    :param active_window_region:
    :return: minimap_region, compass_center
    """
    if active_window_region is None:
        raise Exception("No active window region provided, cant initialize minimap")

    while True:
        try:
            compass_box = pyautogui.locateOnScreen('Images/Minimap/compass_half.png', confidence=0.8, region=active_window_region)
            hometele_box = pyautogui.locateOnScreen('Images/Minimap/hometele.png', confidence=0.7, region=active_window_region)
            run_energy_box = pyautogui.locateOnScreen('Images/Minimap/full_run_energy.png', confidence=0.9, region=active_window_region)

            compass_center = pyautogui.center(compass_box)
            width = abs(compass_center[0] - pyautogui.center(run_energy_box)[0])
            height = abs(compass_center[1] - pyautogui.center(hometele_box)[1])

            # Use left, top, width, and height to define where minimap is on the client for faster recognition cycles
            # 50px is the approx amount of lost data

            minimap_region = [compass_box.left, compass_box.top, width + 50, height + 50]
            compass_center = [compass_center[0], compass_center[1]]

            print("Minimap found and initialized.\n")
            return minimap_region, compass_center

        except Exception as e:
            print("Failed to configure minimap, check that run energy is 100% and compass points north (click compass once and move mouse away)")
