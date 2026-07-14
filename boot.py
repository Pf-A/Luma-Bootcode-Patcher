# PATCHED LUMA BOOTCODE
# COPYRIGHT 2026 MICHAEL CARLSON
# mcar3101@mpsedu.org

# This program has 3 Confirmed Kills.

# for more information, go to 
# https://pf-a.github.io/l/index.html

# THIS CODE HAS TO BE PAIRED WITH THE 
# PATCHED LUMA.py FILE OR ELSE 
# SOME FEATURES WILL NOT WORK!

# This LUMA was patched on 
# {TODAYSDATE}
# by {YOURNAME}


import storage
import board
import pwmio
import time
from digitalio import DigitalInOut, Direction, Pull

try: 
    import neopixel
    pixel = neopixel.NeoPixel(board.GP9, 4, brightness=0.2, auto_write=False)
    pixel[2] = (255,0,0)
    pixel.show()
except: 
    pass

button_black = DigitalInOut(board.GP6)
button_black.direction = Direction.INPUT

if not button_black.value: #if button pressed, mount USB drive as writeable (default) - play tone
    piezo = pwmio.PWMOut(board.GP22, duty_cycle=0, frequency=440, variable_frequency=True)
    piezo.frequency = 880 
    piezo.duty_cycle = 65535 // 2  # On 50%
    time.sleep(.25)
    piezo.frequency = 880 
    piezo.duty_cycle = 65535 // 2  # On 50%
    time.sleep(.25)
    piezo.duty_cycle = 0  # off
    
    # next bit is commented out
    # changing it in the past has broken luma's

#    new_name = "LUMA"
#    storage.remount("/", readonly=False)
#    m = storage.getmount("/")
#    m.label = new_name
#    storage.remount("/", readonly=True) #Host can write to USB drive, CP cannot



# this is default for when the robot starts up

if button_black.value: # (Default) if button is unpressed, mount USB drive as write protected 
    
     # next bit is commented out
    # changing it in the past has broken luma's

#    new_name = "LUMA" # set custom name for luma
#    storage.remount("/", readonly=False)
#    m = storage.getmount("/")
#    m.label = new_name
     storage.disable_usb_drive()	  # disables LUMA mounting as a USB drive
     storage.remount("/", readonly=False) # CP can write to internal filesystem, Host cannot
 

