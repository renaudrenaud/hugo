"""
2023-01
In January 2023 Hugo arrived in this world

Catherine & Renaud built a lamp for his birth
The lamp is a lithophabe 


https://github.com/renaudrenaud/hugo

"""
import array, time
from machine import Pin
import neopixel
import rp2

import _thread

from phew import logging, server, connect_to_wifi
from phew.template import render_template
from secret import ssid, password

interrupt_flag = False

#
############################################
# RP2040 PIO and Pin Configurations
############################################
#
# WS2812 LED Ring Configuration
led_count = 16 		# number of LEDs in ring light
PIN_NUM = 13 		# pin connected to ring light
brightness = .3 	# 0.1 = darker, 1.0 = brightest


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
          yellow
          ]


colors_name = ["white", "yellow", "rgbLightYellow3", "rgbLightYellow4","cyan",
              "blank",
               "rgbDustyRose", "rgbPastelPink", "rgbPastelBlue",
               "blank",
               "red", "green","blue","yellow"
              ]

current_color = 0


led = machine.Pin(17, machine.Pin.OUT)

def running_led(color, led_count):
    global interrupt_flag
    interrupt_flag = False
    
    # number of times to cycle 360-degrees
    cycles = 10 
    print("Running pixel")
    # Range of LEDs stored in an array
    ar = array.array("I", [0 for _ in range(led_count)])
    
    blank = (0,0,0)

    while True:
        for ii in range(int(cycles*len(ar))+1):
            for jj in range(len(ar)):
                if jj==int(ii%led_count): # in case we go over number of pixels in array
                    pixels_set(jj,color) # color and loop a single pixel
                else:
                    pixels_set(jj,blank) # turn others off
            pixels_show() # update pixel colors
            
            if interrupt_flag == True:
                interrupt_flag == False
                return
                break
            time.sleep(0.05) # wait 50ms
            if ii % 2 == 0:
                led.value(1)
            else:
                led.value(0)



def neopixel_animation():
    global interrupt_flag
    print("starting Core 0")
    while True: # loop indefinitely
        color = (255,0,0) # looping color
        blank = (0,0,0) # color for other pixels
        cycles = 10 # number of times to cycle 360-degrees
       
        for color in colors: # emulate breathing LED (similar to Amazon's Alexa)
            print("calling breathe")
            breathing_led(color)
            time.sleep(0.1) # wait between colors

        for color in colors:
            print("calling running led")
            running_led(color, led_count)
            


###################################################################

print("ip: " + connect_to_wifi(ssid, password))
username = ""
logged = False


@server.route("/")
def index(request):
    if logged == False:
        message = "Press Next in the top to go to the next lamp animation."
    
    return render_template("index2.html", name=username, title="Hugo Lamp", message=message)

@server.route("/about")
def about(request):
    global interrupt_flag
    interrupt_flag = True
    return render_template("about.html", name=username, title="About this Site")

@server.route("/next")
def about(request):
    """
    We want to show the next animation
    """
    global interrupt_flag
    global current_color
    global cur_col
    
    interrupt_flag = True
    current_color = current_color + 1
    
    if current_color < 14:
        cur_col = colors_name[current_color]
        cur_col = " breathe " + cur_col
    elif current_color < 28:
        cur_col = " run " + colors_name[current_color - 14]
    else:
        current_color = -1
        cur_col = " breathe " + colors_name[current_color]
    
    return render_template("next.html", current_color=str(cur_col), title="Activate Next animation")

@server.route("/login", ["POST",'GET'])
def login_form(request):
    print(request.method)
    if request.method == 'GET':
        return render_template("login.html")
    if request.method == 'POST':    
        username = request.form.get("username", None)
        password = request.form.get("password", None)

        if username == "hugo" and password == "hugo":
            logged = True
            message = """<p>Welcome back, let s define the light.</p>
                          <div class='mb-3'>
                          <button type="submit" value="Login">White</button>
                          <button type="submit" value="Login">Blue</button>
                          <button type="submit" value="Login">Red</button>
                          <button type="submit" value="Login">Stop</button>
                            </div>
                        """
            # global interrupt_flag
            interrupt_flag = True
            print("Button is pressed !") 

            return render_template('index2.html', message=message) #content = f"<h1>Welcome back {username}!</h1>")
            
        else:
            logged = False
            return render_template('default.html', content = "Sorry, invalid username or password")

"""@server.catchall()
def my_catchall(request):
  return "No matching route", 404
"""

_thread.start_new_thread(neopixel_animation,())

print("starting core 1")
server.run()

