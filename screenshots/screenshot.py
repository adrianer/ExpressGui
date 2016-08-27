import sys
sys.path.append("..")
from express_gui.window import Window
import subprocess
from threading import Thread
from time import sleep

expressgui = Window()
mythread = Thread(target=expressgui.main)
mythread.start()
sleep(1)
subprocess.call(["gnome-screenshot", "-w", "-f", "window.png"])
expressgui.emit("destroy")
expressgui = Window()
expressgui.location_chooser_button.emit("clicked")
mythread = Thread(target=expressgui.main)
mythread.start()
sleep(1)
subprocess.call(["gnome-screenshot", "-w", "-f", "locationchooser.png"])
expressgui.emit("destroy")
