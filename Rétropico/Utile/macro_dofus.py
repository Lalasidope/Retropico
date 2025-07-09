import pyautogui
import time
import random

def move_randomized(x, y, offset=5):
    rx = x + random.randint(-offset, offset)
    ry = y + random.randint(-offset, offset)
    pyautogui.moveTo(rx, ry)

def move_precise_offset(x, y, offset=1):
    rx = x + random.randint(-offset, offset)
    ry = y + random.randint(-offset, offset)
    pyautogui.moveTo(rx, ry)

print('Tu as 5 secondes pour te placer sur la fenêtre Dofus...')
time.sleep(5)

move_precise_offset(1199, 673)
pyautogui.click()
time.sleep(0.016)

move_precise_offset(1198, 672)
pyautogui.click()
time.sleep(0.625)

move_precise_offset(1198, 671)
pyautogui.click()

move_precise_offset(1197, 671)
pyautogui.click()
time.sleep(0.062)

move_precise_offset(1196, 670)
pyautogui.click()
time.sleep(0.469)

move_precise_offset(1200, 674)
pyautogui.click()

move_precise_offset(1201, 675)
pyautogui.click()
time.sleep(0.015)

move_precise_offset(1220, 690)
pyautogui.click()

move_precise_offset(1221, 691)
pyautogui.click()
time.sleep(0.016)

move_precise_offset(1251, 715)
pyautogui.click()

move_precise_offset(1254, 718)
pyautogui.click()
time.sleep(0.016)

move_precise_offset(1288, 745)
pyautogui.click()

move_precise_offset(1290, 747)
pyautogui.click()
time.sleep(0.015)

move_precise_offset(1329, 775)
pyautogui.click()
