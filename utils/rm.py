import time

import pyautogui
time.sleep(2)
im1 = pyautogui.screenshot()
im1.save('my_screenshot.png')
im2 = pyautogui.screenshot('my_screenshot2.png')