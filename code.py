### LIBRARIES ###
import usb_hid
import board
import time
import digitalio

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

### VARIABLES ###
startButton = digitalio.DigitalInOut(board.GP9)
readyLED = digitalio.DigitalInOut(board.GP7)
runningLED = digitalio.DigitalInOut(board.GP4)
readyLED.direction = digitalio.Direction.OUTPUT
runningLED.direction = digitalio.Direction.OUTPUT
startButton.switch_to_input(pull = digitalio.Pull.UP)
filePath = "./wordlist.txt"
kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)

### FUNCTIONS ###
def typeCredentials(login, password):
  layout.write(login)
  kbd.send(Keycode.TAB)
  layout.write(password)
  kbd.send(Keycode.TAB)
  kbd.send(Keycode.ENTER)
  time.sleep(1)
  kbd.send(Keycode.TAB)
  kbd.send(Keycode.ENTER)
  kbd.send(Keycode.TAB)

### MAIN LOOOP ###
readyLED.value = True
runningLED.value = False
time.sleep(20)
while True:
  if startButton.value == False: # If the startButton is pressed
    try:
      with open(filePath, "r") as file:
        readyLED.value = False
        runningLED.value = True
        for line in file:
          words = line.strip().split(',')
          login = words[0]
          password = words[1]
          typeCredentials(login, password)
          time.sleep(1)
        
        readyLED.value = True
        runningLED.value = False  
    except: print("[-] Error")
