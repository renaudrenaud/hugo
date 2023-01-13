# hugo

Raspberry PICO with webserver and neopixel

This is project uses:  
* webserver running on a Raspberry PICO
* the neopixel library to control a neopixel strip


## Hardware

* The hardware is embedded into a lamp build with 3D printer and one surface is a litophane.
* The **litophane** is a picture that is **only visible when the light is behind** it. The picture is a picture of Hugo.
* The **neopixel ring** is a ring of 24 RGB LEDs, used to produce the light behind the litophane. The ring is connected to the Pico.
* We use the Raspberry Pico W from August 2022. **W** means WiFi.
* The Pico is a little microcontroler with 2MB of flash memory and is able to run micropython. The W is a version with WiFi and we use the WiFi to offer the control of the light via the webserver.


## Software

We use:
* The [micropython](micropython.org/) firmware for the Pico
* Pimoroni [phew!](https://github.com/pimoroni/phew) webserver library
* [neopixel](https://github.com/micropython/micropython/blob/master/docs/esp8266/tutorial/neopixel.rst) library to control the neopixel strip.
* we also use threads to run the webserver and the neopixel strip in parallel. The Pico is right now able to run only 2 threads:
    * the main thread offering the webserver
    * the neopixel thread


