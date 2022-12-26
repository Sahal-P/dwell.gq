import pyautogui
import time

time.sleep(5)

count = 0
while count <= 10:
    pyautogui.typewrite("hello "+str(count))
    pyautogui.press("enter")
    count= count+ 1