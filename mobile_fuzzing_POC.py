### LIBRARIES ###
import usb_hid
import board
import time
import digitalio

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

### VARIABLES ###
button = digitalio.DigitalInOut(board.GP9)
led = digitalio.DigitalInOut(board.GP8)
led.direction = digitalio.Direction.OUTPUT
button.switch_to_input(pull = digitalio.Pull.UP)
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
while True:
  if button.value == False: # If the button is pressed
    try:
      with open(filePath, "r") as file:
        for line in file:
          led.value = True
          words = line.strip().split(',')
          login = words[0]
          password = words[1]
          typeCredentials(login, password)
          time.sleep(1)
          led.value = False
    except: print("[-] Error")
