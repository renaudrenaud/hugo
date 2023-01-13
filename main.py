###############################################################
# WS2812 RGB LED Ring Light Breathing
# with the Raspberry Pi Pico Microcontroller
#
# by Joshua Hrisko, Maker Portal LLC (c) 2021
#
# Based on the Example neopixel_ring at:
# https://github.com/raspberrypi/pico-micropython-examples
#
# Added some mix of different things by renaudrenaud
###############################################################
#
import array, time
import machine
from machine import Pin
import neopixel
import rp2
import _thread


#
############################################
# RP2040 PIO and Pin Configurations
############################################
#
# WS2812 LED Ring Configuration
led_count = 16 # number of LEDs in ring light
PIN_NUM = 13 # pin connected to ring light
brightness = .1 # 0.1 = darker, 1.0 = brightest


# For the button on GP5 / Pin 7
interrupt_flag = False
pin = Pin(5,Pin.IN,Pin.PULL_UP)
print("running")

# For neopixel ASSEMBLER
@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24) # PIO configuration


# define WS2812 parameters
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1)               .side(0)    [T3 - 1]
    jmp(not_x, "do_zero")   .side(1)    [T1 - 1]
    jmp("bitloop")          .side(1)    [T2 - 1]
    label("do_zero")
    nop()                   .side(0)    [T2 - 1]
    wrap()


# Create the StateMachine with the ws2812 program, outputting on pre-defined pin
# at the 8MHz frequency
sm = rp2.StateMachine(0, ws2812, freq=8_000_000, sideset_base=Pin(PIN_NUM))

# Activate the state machine
sm.active(1)

# Range of LEDs stored in an array
ar = array.array("I", [0 for _ in range(led_count)])

#
############################################
# Functions for RGB Coloring
############################################
#
def pixels_show(brightness_input=brightness):
    dimmer_ar = array.array("I", [0 for _ in range(led_count)])
    for ii,cc in enumerate(ar):
        r = int(((cc >> 8) & 0xFF) * brightness_input) # 8-bit red dimmed to brightness
        g = int(((cc >> 16) & 0xFF) * brightness_input) # 8-bit green dimmed to brightness
        b = int((cc & 0xFF) * brightness_input) # 8-bit blue dimmed to brightness
        dimmer_ar[ii] = (g<<16) + (r<<8) + b # 24-bit color dimmed to brightness
    sm.put(dimmer_ar, 8) # update the state machine with new colors
    time.sleep_ms(10)

def pixels_set(i, color):
    ar[i] = (color[1]<<16) + (color[0]<<8) + color[2] # set 24-bit color
        
def breathing_led(color):
    global interrupt_flag
    step = 3
    breath_amps = [ii for ii in range(0,127,step)]
    breath_amps.extend([ii for ii in range(127,-1,-step)])
    while True:
        for ii in breath_amps:
            for jj in range(len(ar)):
                pixels_set(jj, color) # show all colors
            
                if interrupt_flag == True:
                    interrupt_flag = False
                    return
            pixels_show(ii/127)
            time.sleep(0.05)
        

# The callback interrupt to catch button pressed
def callback(pin):
    global interrupt_flag
    interrupt_flag = True
    print("Button is pressed !") 

#
############################################
# Main Calls and Loops
############################################
#
# color specifications
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
cyan = (0,255,255)
white = (255,255,255)
blank = (0,0,0)


rgbLightYellow3 = (255,255,51)
rgbLightYellow4 = (255,255,102)
rgbPastelPink = (222, 165, 164)
rgbPastelBlue = (174, 198, 207)
rgbDustyRose = (220, 174, 150)


# colors = [red,green,blue,yellow,cyan,white]
colors = [white, 
          yellow,
          rgbLightYellow3, 
          rgbLightYellow4, 
          cyan,
          blank,
          rgbDustyRose, 
          rgbPastelPink,
          rgbPastelBlue,
          blank,
          red, 
          green,
          blue,
          blank
          ]

led = machine.Pin(17, machine.Pin.OUT)


pin.irq(trigger=Pin.IRQ_FALLING, handler=callback)

while True: # loop indefinitely
    color = (255,0,0) # looping color
    blank = (0,0,0) # color for other pixels
    cycles = 10 # number of times to cycle 360-degrees
   
    for color in colors: # emulate breathing LED (similar to Amazon's Alexa)
        breathing_led(color)
        time.sleep(0.1) # wait between colors

    for color in colors:
        if color != blank:
            for ii in range(int(cycles*len(ar))+1):
                for jj in range(len(ar)):
                    if jj==int(ii%led_count): # in case we go over number of pixels in array
                        pixels_set(jj,color) # color and loop a single pixel
                    else:
                        pixels_set(jj,blank) # turn others off
                    if interrupt_flag == True:
                        # interrupt_flag == False
                        break
                if interrupt_flag == True:
                    interrupt_flag == False
                    break
                pixels_show() # update pixel colors
                time.sleep(0.05) # wait 50ms
                if ii % 2 == 0:
                    led.value(1)
                else:
                    led.value(0)
         



