
import pynput
import time
from pynput.mouse import Button,Controller
c=Controller()
for i in range(2000):
    c.position=(1896,947)
    c.click(Button.left)
    time.sleep(0.01)