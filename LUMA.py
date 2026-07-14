# Patched Luma Bootcode
# SCRIPT 2 of 2
# Copyright 2026 Michael Carlson

# CircuitPython module for Pitsco SideKick Robot
# Import in main program
# Written by Paul W. Uttley
# Pitsco Education
# 08/18/2022
# Version 1.0

import time
import board
import busio
from digitalio import DigitalInOut, Direction, Pull
#import adafruit_hcsr04
from rainbowio import colorwheel
import neopixel
import pwmio
import random
import supervisor
from hcsr04 import HCSR04

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#NOTES
OFF = 0
B0 = 31
C1 = 33
CS1 = 35
D1 = 37
DS1 = 39
E1 = 41
F1 = 44
FS1 = 46
G1 = 49
GS1 = 52
A1 = 55
AS1 = 58
B1 = 62
C2 = 65
CS2 = 69
D2 = 73
DS2 = 78
E2 = 82
F2 = 87
FS2 = 93
G2 = 98
GS2 = 104
A2 = 110
AS2 = 117
B2 = 123
C3 = 131
CS3 = 139
D3 = 147
DS3 = 156
E3 = 165
F3 = 175
FS3 = 185
G3 = 196
GS3 = 208
A3 = 220
AS3 = 233
B3 = 247
C4 = 262
CS4 = 277
D4 = 294
DS4 = 311
E4 = 330
F4 = 349
FS4 = 370
G4 = 392
GS4 = 415
A4 = 440
AS4 = 466
B4 = 494
C5 = 523
CS5 = 554
D5 = 587
DS5 = 622
E5 = 659
F5 = 698
FS5 = 740
G5 = 784
GS5 = 831
A5 = 880
AS5 = 932
B5 = 988
C6 = 1047
CS6 = 1109
D6 = 1175
DS6 = 1245
E6 = 1319
F6 = 1397
FS6 = 1480
G6 = 1568
GS6 = 1661
A6 = 1760
AS6 = 1865
B6 = 1976
C7 = 2093
CS7 = 2217
D7 = 2349
DS7 = 2489
E7 = 2637
F7 = 2794
FS7 = 2960
G7 = 3136
GS7 = 3322
A7 = 3520
AS7 = 3729
B7 = 3951
C8 = 4186
CS8 = 4435
D8 = 4699
DS8 = 4978

#animation sequences

from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.sparklepulse import SparklePulse
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.animation.sparkle import Sparkle
from adafruit_led_animation.animation.rainbowchase import RainbowChase
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.animation.colorcycle import ColorCycle
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.customcolorchase import CustomColorChase
from adafruit_led_animation.sequence import AnimationSequence
from adafruit_led_animation.color import PURPLE, WHITE, AMBER, JADE, MAGENTA, ORANGE, BLACK, RED, YELLOW, GREEN, TEAL, CYAN, BLUE, PINK, AQUA

pixels = neopixel.NeoPixel(board.GP9, 4, brightness=0.3, auto_write=False)

blink = Blink(pixels, speed=0.5, color=JADE)
colorcycle = ColorCycle(pixels, speed=0.4, colors=[PURPLE, WHITE, AMBER, JADE, MAGENTA, ORANGE, RED, YELLOW, GREEN, TEAL, CYAN, BLUE, PINK, AQUA])
comet = Comet(pixels, speed=0.01, color=TEAL, tail_length=4, bounce=True)
chase = Chase(pixels, speed=0.1, size=3, spacing=6, color=WHITE)
fade = Pulse(pixels, speed=0.1, period=3, color=MAGENTA)
sparkle = Sparkle(pixels, speed=0.1, color=WHITE, num_sparkles=50)
solid = Solid(pixels, color=BLACK)# USED TO TURN ANIMATION OFF
rainbow = Rainbow(pixels, speed=0.1, period=2)
sparkle_fade = SparklePulse(pixels, speed=0.1, period=3, color=JADE)
rainbow_comet = RainbowComet(pixels, speed=0.1, tail_length=4, bounce=True)
rainbow_chase = RainbowChase(pixels, speed=0.1, size=3, spacing=2, step=8)
rainbow_sparkle = RainbowSparkle(pixels, speed=0.1, num_sparkles=50)
custom_color_chase = CustomColorChase(pixels, speed=0.1, size=2, spacing=3, colors=[ORANGE, WHITE, JADE])

#sensor_sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP7, echo_pin=board.GP8, timeout=0.07)
sonar = HCSR04(board.GP7, board.GP8)

piezo = pwmio.PWMOut(board.GP22, duty_cycle=0, frequency=440, variable_frequency=True)

button_green = DigitalInOut(board.GP11)
button_green.direction = Direction.INPUT

button_black = DigitalInOut(board.GP6)
button_black.direction = Direction.INPUT

LED_green = DigitalInOut(board.GP25)
LED_green.direction = Direction.OUTPUT
LED_green.value = False

sensor_line = DigitalInOut(board.GP13)
sensor_line.direction = Direction.INPUT

busy = DigitalInOut(board.GP10)
busy.direction = Direction.INPUT

enable = DigitalInOut(board.GP12)
enable.direction = Direction.OUTPUT
enable.value = False

i2c = busio.I2C(board.GP5, board.GP4)

pixels[0] = (0,0,0)
pixels[1] = (0,0,0)
pixels[2] = (0,0,0)
pixels[3] = (0,0,0)
pixels.show()

def wait_for_start():
    blink_pixel('pixel_all', '#FFFFFF', 2)
    #correct_effect()
    pixels.brightness = 0.2
    LED_green.value = True
    pixels[2] = (0,255,0)
    pixels.show()
    play_tone(523, 0.2)

    while button_green.value:
        pass
    LED_green.value = False
    pixels[2] = (0,0,0)
    pixels.show()
    pixels.brightness = 0.3
    correct_effect()
    enable.value = True
    time.sleep(1)
    
def reboot():
    supervisor.reload()

def green_button(state):
    if state == "pressed":
        return not button_green.value
    if state == "not_pressed":
        return button_green.value

def black_button(state):
    if state == "pressed":
        return not button_black.value
    if state == "not_pressed":
        return button_black.value

def ultrasonic_distance_old():
    try:
       #print(sensor_sonar.distance)
        return sensor_sonar.distance
    except RuntimeError:
       #print("Out of Range!")
        return 400 # return max distance if out of range
        pass
    time.sleep(0.1)

def ultrasonic_distance():
    time.sleep(.05)
    try:
        #time.sleep(.05)
        distance = sonar.dist_cm()
        #print(distance)
        if(distance <= 2):  #reading below 2cm is erroneous noise
            distance = 400 #error - set to max
        return distance
    except RuntimeError:
        #time.sleep(.05)
        return 400 # return max distance if out of range
        pass
    #sonar.deinit()

def line_finder():
    return not sensor_line.value

def reflected_light_sensor():
    return not sensor_line.value

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def set_pixel(pixel, color, bright):
    bright = int(bright)  # cannot be a float
    rgb = hex_to_rgb(color)
    outval = int(min(max(bright, 0), 100))
    pixels.brightness = outval / 100

    if pixel == 'pixel_1':
        pixels[0] = (rgb)
        pixels.show()
    if pixel == 'pixel_2':
        pixels[1] = (rgb)
        pixels.show()
    if pixel == 'pixel_3':
        pixels[2] = (rgb)
        pixels.show()
    if pixel == 'pixel_4':
        pixels[3] = (rgb)
        pixels.show()
    if pixel == 'pixel_all':
        pixels[0] = (rgb)
        pixels[1] = (rgb)
        pixels[2] = (rgb)
        pixels[3] = (rgb)
        pixels.show()

def show_pixel_animation(pattern, loop):
    loop = int(loop)  # cannot be a float
    pixels.brightness = 0.3 # set brightness to 30%
    loop = loop * 1000
    x = 0
    while x <= loop:
        pattern.animate()
        x += 1
        time.sleep(.001)
    solid.animate()  #Set to black, turns out all the pixels

def blink_pixel(pixel, color, loop):
    loop = int(loop)  # cannot be a float
    rgb = hex_to_rgb(color)
    pixels.brightness = 0.3 # set brightness to 30%

    if pixel == 'pixel_1':
        x = 0
        while x < loop:
            x += 1
            pixels[0] = (rgb)
            pixels.show()
            time.sleep(.25)
            pixels[0] = BLACK
            pixels.show()
            time.sleep(.25)

    if pixel == 'pixel_2':
        x = 0
        while x < loop:
            x += 1
            pixels[1] = (rgb)
            pixels.show()
            time.sleep(.25)
            pixels[1] = BLACK
            pixels.show()
            time.sleep(.25)

    if pixel == 'pixel_3':
        x = 0
        while x < loop:
            x += 1
            pixels[2] = (rgb)
            pixels.show()
            time.sleep(.25)
            pixels[2] = BLACK
            pixels.show()
            time.sleep(.25)

    if pixel == 'pixel_4':
        x = 0
        while x < loop:
            x += 1
            pixels[3] = (rgb)
            pixels.show()
            time.sleep(.25)
            pixels[3] = BLACK
            pixels.show()
            time.sleep(.25)

    if pixel == 'pixel_all':
        x = 0
        while x < loop:
            x += 1
            pixels[0] = (rgb)
            pixels[1] = (rgb)
            pixels[2] = (rgb)
            pixels[3] = (rgb)
            pixels.show()
            time.sleep(.25)
            pixels[0] = BLACK
            pixels[1] = BLACK
            pixels[2] = BLACK
            pixels[3] = BLACK
            pixels.show()
            time.sleep(.25)




def color_chase(color, speed):
    speed = int(speed)  # cannot be a float
    pixels.brightness = 0.3 # set brightness to 30%
    for i in range(4):
        pixels[i] = color
        time.sleep(speed)
        pixels.show()
    time.sleep(speed)


def color_rainbow(fade):
    fade = int(fade)  # cannot be a float
    pixels.brightness = 0.3 # set brightness to 30%
    for j in range(255):
        for i in range(4):
            rc_index = (i * 256 // 4) + j
            pixels[i] = colorwheel(rc_index & 255)
        pixels.show()
        time.sleep(fade)

def play_tone(f, length):
    f = int(f)  # cannot be a float
    if f == 0:
        piezo.duty_cycle = 0
        return
    piezo.frequency = f
    piezo.duty_cycle = 65535 // 2  # On 50%
    if length > 0:
        time.sleep(length)
        piezo.duty_cycle = 0

def play_note(n, length):
    n = int(n)  # cannot be a float
    if n == 0:
        piezo.duty_cycle = 0
        return
    piezo.frequency = n
    piezo.duty_cycle = 65535 // 2  # On 50%
    if length > 0:
        time.sleep(length)
        piezo.duty_cycle = 0

def sound_off():
    piezo.duty_cycle = 0

def set_move_speed(speed):
    speed = int(speed)  # cannot be a float
    speed = int(min(max(speed, 0), 100))
    speedH = ((speed >> 8) & 0xff)
    speedL = speed & 0xff
    while not i2c.try_lock():
        pass
    try:
        time.sleep(0.01) # pace I2C bus
        i2c.writeto(12, bytes([7, speedH, speedL]))
    finally:
        i2c.unlock()


def move_distance(direction, distance):
    distance = int(distance)
    if direction == "reverse":
        distance = -distance
    LdisH = ((distance >> 8) & 0xff)
    LdisL = distance & 0xff
    RdisH = ((distance >> 8) & 0xff)
    RdisL = distance & 0xff
    while not i2c.try_lock():
        pass
    try:
        time.sleep(0.01) # pace I2C bus
        i2c.writeto(12, bytes([1, LdisH, LdisL, RdisH, RdisL]))
    finally:
        i2c.unlock()

    time.sleep(0.25) # give time for busy to be set
    while busy.value:# wait here while motors are moving to position
        pass

def move_start(whichway):
    Ldir = 0
    Rdir = 0

    if whichway == "forward":
        Ldir = 1
        Rdir = 1
    if whichway == "reverse":
        Ldir = -1
        Rdir = -1
    if whichway == "spin_cw":
        Ldir = 1
        Rdir = -1
    if whichway == "spin_ccw":
        Ldir = -1
        Rdir = 1
    if whichway == "pivot_right":
        Ldir = 1
        Rdir = 0
    if whichway == "pivot_left":
        Ldir = 0
        Rdir = 1

    LdirH = ((Ldir >> 8) & 0xff)
    LdirL = Ldir & 0xff
    RdirH = ((Rdir >> 8) & 0xff)
    RdirL = Rdir & 0xff
    while not i2c.try_lock():
        pass
    try:
        time.sleep(0.01) # pace I2C bus
        i2c.writeto(12, bytes([2, LdirH, LdirL, RdirH, RdirL]))
    finally:
        i2c.unlock()

def move_spin(direction, degrees):
    degrees = int(degrees)  # cannot be a float
    degrees = int(degrees)
    degrees = abs(degrees)
    if direction == "counterclockwise":
        degrees = -degrees
    degreesH = ((degrees >> 8) & 0xff)
    degreesL = degrees & 0xff
    while not i2c.try_lock():
        pass
    try:
        time.sleep(0.01) # pace I2C bus
        i2c.writeto(12, bytes([3, degreesH, degreesL]))
    finally:
        i2c.unlock()
    time.sleep(0.25) # give time for busy to be set
    while busy.value:# wait here while motors are moving to position
        pass

def move_pivot(direction, degrees):
    degrees = int(degrees)  # cannot be a float
    degrees = int(degrees)
    degrees = abs(degrees)
    if direction == "left":
        degrees = -degrees
    degreesH = ((degrees >> 8) & 0xff)
    degreesL = degrees & 0xff
    while not i2c.try_lock():
        pass
    try:
        time.sleep(0.01) # pace I2C bus
        i2c.writeto(12, bytes([4, degreesH, degreesL]))
    finally:
        i2c.unlock()
    time.sleep(0.25) # give time for busy to be set
    while busy.value:# wait here while motors are moving to position
        pass

def move_steering(direction, Lspeed, Rspeed):
    Lspeed = int(Lspeed)  # cannot be a float
    Rspeed = int(Rspeed)  # cannot be a float
    Lspeed = int(min(max(Lspeed, 0), 100))
    Rspeed = int(min(max(Rspeed, 0), 100))
    if direction == "reverse":
        Lspeed = -Lspeed
        Rspeed = -Rspeed
    LspeedH = ((Lspeed >> 8) & 0xff)
    LspeedL = Lspeed & 0xff
    RspeedH = ((Rspeed >> 8) & 0xff)
    RspeedL = Rspeed & 0xff
    while not i2c.try_lock():
        pass
    try:
        time.sleep(0.01) # pace I2C bus
        i2c.writeto(12, bytes([8, LspeedH, LspeedL, RspeedH, RspeedL]))
    finally:
        i2c.unlock()

def move_stop():
    while not i2c.try_lock():
        pass
    try:
        time.sleep(0.01) # pace I2C bus
        i2c.writeto(12, bytes([5]))
    finally:
        i2c.unlock()

def move_servo(motor, position, speed):
    position = int(position)  # cannot be a float
    speed = int(speed)  # cannot be a float
    if motor == "servo_1":
        motor = 1
    if motor == "servo_2":
        motor = 2
    if motor == "servo_1_2":
        motor = 3
    positionH = ((position >> 8) & 0xff)
    positionL = position & 0xff
    speedH = ((speed >> 8) & 0xff)
    speedL = speed & 0xff
    while not i2c.try_lock():
        pass
    try:
        time.sleep(0.01) # pace I2C bus
        i2c.writeto(12, bytes([6, motor, positionH, positionL, speedH, speedL]))
    finally:
        i2c.unlock()

def play_sound_effect(effect):
    if effect == 'siren':
        siren_effect()
    if effect == 'whistle_down':
        whistle_down_effect()
    if effect == 'whistle_up':
        whistle_up_effect()
    if effect == 'correct':
        correct_effect()
    if effect == 'incorrect':
        incorrect_effect()
    if effect == 'r2d2':
        r2d2_effect()
    if effect == 'phaser':
        phaser_effect()
    if effect == 'happy_birthday':
        happy_bday_effect()
    if effect == 'close_encounters':
        close_encounters_effect()
    if effect == 'super_mario':
        super_mario_effect()
    if effect == 'up_and_down':
        up_down_effect()
    if effect == 'random_sounds':
        random_effect()
    if effect == 'red_alert':
        red_alert_effect()
    if effect == 'whoops':
        whoops_effect()
    if effect == 'buzz_buzz_buzz':
        buzzer_effect()


#################SOUND EFFECTS

def siren_effect():
    piezo.duty_cycle = 65535 // 2  # On 50%
    for i in range(300,700):
        piezo.frequency = i
        time.sleep(0.001)
    for i in range(700,300,-1):
        piezo.frequency = i
        time.sleep(0.001)
    piezo.duty_cycle = 0

def whistle_down_effect():
    piezo.duty_cycle = 65535 // 2  # On 50%
    for i in range(1000,100,-1):
        piezo.frequency = i
        time.sleep(i//2000)
    piezo.duty_cycle = 0

def whistle_up_effect():
    piezo.duty_cycle = 65535 // 2  # On 50%
    for i in range(100,1000):
        piezo.frequency = i
        time.sleep(1 // i)
    piezo.duty_cycle = 0

def correct_effect():
    piezo.duty_cycle = 65535 // 2  # On 50%
    piezo.frequency = 523
    time.sleep(0.2)
    piezo.frequency = 698
    time.sleep(0.2)
    piezo.duty_cycle = 0

def incorrect_effect():
    piezo.duty_cycle = 65535 // 2  # On 50%
    piezo.frequency = 698
    time.sleep(0.2)
    piezo.frequency = 349
    time.sleep(0.2)
    piezo.duty_cycle = 0

def r2d2_effect():
    piezo.duty_cycle = 65535 // 2  # On 50%
    piezo.frequency = 3520
    time.sleep(.1)
    piezo.frequency = 3135
    time.sleep(.1)
    piezo.frequency = 2637
    time.sleep(.1)
    piezo.frequency = 2093
    time.sleep(.1)
    piezo.frequency = 2349
    time.sleep(.1)
    piezo.frequency = 3951
    time.sleep(.1)
    piezo.frequency = 2793
    time.sleep(.1)
    piezo.frequency = 4186
    time.sleep(.1)
    piezo.frequency = 3520
    time.sleep(.1)
    piezo.frequency = 3135
    time.sleep(.1)
    piezo.frequency = 2637
    time.sleep(.1)
    piezo.frequency = 2093
    time.sleep(.1)
    piezo.frequency = 2349
    time.sleep(.1)
    piezo.frequency = 3951
    time.sleep(.1)
    piezo.frequency = 2793
    time.sleep(.1)
    piezo.frequency = 4186
    time.sleep(.1)
    piezo.duty_cycle = 0

def phaser_effect():
    piezo.duty_cycle = 65535 // 2  # On 50%
    for i in range(50,1000,5):
        piezo.frequency = i
        time.sleep(i // 1000)
    piezo.duty_cycle = 0


def happy_bday_effect():
    piezo.duty_cycle = 65535 // 2  # On 50%
    piezo.frequency = 262
    time.sleep(.2)
    piezo.duty_cycle = 0
    time.sleep(.02)
    piezo.duty_cycle = 65535 // 2
    piezo.frequency = 262
    time.sleep(.2)
    piezo.frequency = 294
    time.sleep(.4)
    piezo.frequency = 262
    time.sleep(.4)
    piezo.frequency = 349
    time.sleep(.4)
    piezo.frequency = 330
    time.sleep(.3)
    piezo.duty_cycle = 0

def close_encounters_effect():
    piezo.duty_cycle = 65535 // 2  # On 50%
    piezo.frequency = 392
    time.sleep(.3)
    piezo.frequency = 440
    time.sleep(.3)
    piezo.frequency = 349
    time.sleep(.3)
    piezo.frequency = 175
    time.sleep(.3)
    piezo.frequency = 262
    time.sleep(.3)
    piezo.duty_cycle = 0

def super_mario_effect():
    piezo.duty_cycle = 65535 // 2  # On 50%
    piezo.frequency = 330
    time.sleep(.15)
    piezo.duty_cycle = 0
    time.sleep(.05)
    piezo.duty_cycle = 65535 // 2
    piezo.frequency = 330
    time.sleep(.15)
    piezo.duty_cycle = 0
    time.sleep(.1)
    piezo.duty_cycle = 65535 // 2
    piezo.frequency = 330
    time.sleep(.3)
    piezo.duty_cycle = 65535 // 2
    piezo.frequency = 262
    time.sleep(.2)
    piezo.frequency = 330
    time.sleep(.3)
    piezo.frequency = 392
    time.sleep(.6)
    piezo.frequency = 196
    time.sleep(.4)
    piezo.duty_cycle = 0

def up_down_effect():
    piezo.duty_cycle = 65535 // 2  # On 50%
    for i in range(50,1000,5):
        piezo.frequency = i
        time.sleep(i // 1000)
    for i in range(1000,50,-5):
        piezo.frequency = i
        time.sleep(1 // i)
    piezo.duty_cycle = 0

def random_effect():
    piezo.duty_cycle = 65535 // 2  # On 50%
    for i in range(0,20):
        f = random.randrange(100, 1000)
        piezo.frequency = f
        time.sleep(.1)
    piezo.duty_cycle = 0

def red_alert_effect():
    piezo.duty_cycle = 65535 // 2  # On 50%
    i = 440
    while i < 1200:
        i += 1
        piezo.frequency = i
        time.sleep(.001)
    piezo.duty_cycle = 0
    time.sleep(.05)
    piezo.duty_cycle = 65535 // 2  # On 50%
    i = 440
    while i < 1200:
        i += 1
        piezo.frequency = i
        time.sleep(.001)
    piezo.duty_cycle = 0
    time.sleep(.05)
    piezo.duty_cycle = 65535 // 2  # On 50%
    i = 440
    while i < 1200:
        i += 1
        piezo.frequency = i
        time.sleep(.001)
    piezo.duty_cycle = 0

def whoops_effect():
    for i in range (0, 3):
        piezo.duty_cycle = 65535 // 2
        piezo.frequency = 1500
        time.sleep(.1)
        piezo.duty_cycle = 0
        time.sleep(.009)
    for i in range (0, 3):
        piezo.duty_cycle = 65535 // 2
        piezo.frequency = 100
        time.sleep(.1)
        piezo.duty_cycle = 0
        time.sleep(.009)

def buzzer_effect():
    for i in range (0, 5):
        piezo.duty_cycle = 65535 // 2
        piezo.frequency = 523
        time.sleep(.01)
        piezo.duty_cycle = 0
        time.sleep(.009)
    time.sleep(.1)
    for i in range (0, 5):
        piezo.duty_cycle = 65535 // 2
        piezo.frequency = 523
        time.sleep(.01)
        piezo.duty_cycle = 0
        time.sleep(.009)
    time.sleep(.1)
    for i in range (0, 5):
        piezo.duty_cycle = 65535 // 2
        piezo.frequency = 523
        time.sleep(.01)
        piezo.duty_cycle = 0
        time.sleep(.009)

# wait for a green button press before running code.py
wait_for_start()
