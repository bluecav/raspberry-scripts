#!/usr/bin/env python

import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

red_pin=11
yellow_pin=13
green_pin=15
reset_pin=29
early_green=31

# Want each light to be on for a set amount of time
# We pause every second and wait to see if we get an interupt
# If so we abort

light_delay=5
yellow_light_delay=2

# Red
GPIO.setup(red_pin,GPIO.OUT)
# Yellow
GPIO.setup(yellow_pin,GPIO.OUT)
# Green
GPIO.setup(green_pin,GPIO.OUT)
GPIO.setup(reset_pin, GPIO.IN)
GPIO.setup(early_green, GPIO.IN)

Upton, Eben; Halfacree, Gareth (2014-08-25). Raspberry Pi User Guide (p. 235). Wiley. Kindle Edition.


# here you would put all your code for setting up GPIO,
# we'll cover that tomorrow
# initial values of variables etc...
counter = 0
counter_limit=9000000
state="red_pin"

try:
    # here you put your main loop or block of code

    while counter < counter_limit:
        counter += 1

        # We start with a red light
        # Increment second by second until we hit either a reset switch or a 

        for x in range(0, light_delay):
            if state=="red_pin":
            elif state=="yellow_pin":
            elif state=="green_pin":
            else:
                print "Unknown state %s, aborting" % state

        GPIO.output(red_pin,False)
        GPIO.output(yellow_pin,False)
        GPIO.output(green_pin,True)

        time.sleep(light_delay)

        print "Target reached: %d" % counter

except KeyboardInterrupt:
    # here you put any code you want to run before the program 
    # exits when you press CTRL+C
    print "\n", counter # print value of counter

except:
    # this catches ALL other exceptions including errors.
    # You won't get any error messages for debugging
    # so only use it once your code is working
    print "Other error or exception occurred!"

finally:
    GPIO.cleanup() # this ensures a clean exit

