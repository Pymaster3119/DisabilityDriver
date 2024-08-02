import pyautogui
import time

# Brief delay to allow you to switch to the target application
time.sleep(5)

for i in range(1, 1000):
    # Move the mouse to the starting position
    pyautogui.moveTo(460, 1048)

    # Click and drag up to the target position
    pyautogui.dragTo(650, 650, duration=0.105, button='left')

    # pyautogui.moveTo(460, 1048)

    # # Click and drag up to the target position
    # pyautogui.dragTo(1635, 275, duration=0.105, button='left')