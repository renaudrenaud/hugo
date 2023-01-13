# hugo

Raspberry PICO with webserver and neopixel

This project uses:  
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

Learned a lot from Kevin McAleer:
* [Pico W Phew!](https://www.youtube.com/watch?v=0sPPxIq4hg8)
* [Use both cores on Pico](https://www.youtube.com/watch?v=QeDnjcdGrpY&t=1995s)


## Thonny

Thonny is a "Python IDE for beginners. It is easy to use and has a lot of features. It is also possible to use the Pico with Thonny."

In fact this piece of software is a nightmare especially when you are compare with Visual Studio Code in professionnal devs. But sadly this is the way to use micropython with the Pico.

Please keep in mind
* The Version 3 of Thonny is real crappy, near unusable (lot of deconnections, plenty of functions are not available, like the package manager...)
* I never was able to find a way to install V4 because I am not a Windows or a Mac User: it is a mystery to me how to install Thonny v4 with Linux and arm64
* I **finally** found a way in January 2023 to install it on the Orange Pi 5 with Debian
* On Linux, The V4 installation is a bash [script available here](https://github.com/thonny/thonny/releases/tag/v4.0.1). Please change the address in case the version has changed (ie v4.0.2 instead of v4.0.1)


`wget -O thonny-latest.sh https://thonny.org/installer-for-linux`

`chmod +x thonny-latest.sh`

`./thonny-latest.sh`

* The installation is done in the user directory. You can start it with the command `./thonny` in the directory where you installed it.

* The installation is done in the user directory /apps/thonny. A virtual env is created so you have first to source it:

`$ source ~/apps/thonny/bin/activate`

Once sourced, you can see (thonny) in front of the prompt:

`(thonny) renaud@orangepi5:~/apps/thonny$ source ~/apps/thonny/bin/activate`

And then you can run thonny:

`(thonny) renaud@orangepi5:~/apps/thonny$ thonny`

So all in all Thonny v4 is working. I have to say that I am not a big fan of the IDE but it is the only way to use micropython with the Pico.


### Manage Packages

Thonny V4 is working for Managing Package with "Tools, Manage Package". In the "Install" tab, you can search for a package and install it, in the virtual env. You can see the list of installed packages in the "Installed" tab.

Please install the following packages:
* micropython_phew
* micropython_upip

## Conclusion

In general terms, I do not understand:
* how it is so complicated how to find how to start with Thonny especially when (fuck Microsoft and fuck Apple) you are a Linux user
* if it us an educational project, how the fuck it can be so complicated to start with micropython and the Pico and how the fuck the tools are so crappy. All the components are here to go to Windows or Mac and this is exactly the contrary of a learning platform. Microsoft Windows is just a joke and Apple is a golden jail.

Speaking about what I've done, yes my code is ugly but I consider it's mainly because of Thonny, to much difficulties to organize the code.

Anyway I've learn a lot in the process and I am happy to have a working project. I am also happy to have a working webserver + a working neopixel on the Pico. I am sure it will be a base for next devs on this platform.

