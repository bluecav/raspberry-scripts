#!/usr/bin/env python

import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

red_pin=11
yellow_pin=13
green_pin=15
reset_pin=16
early_green_pin=18

# Want each light to be on for a set amount of time
# We pause every second and wait to see if we get an interupt
# If so we abort

light_delay=5
yellow_light_delay=2
state_counter=0

# Red
GPIO.setup(red_pin,GPIO.OUT)
# Yellow
GPIO.setup(yellow_pin,GPIO.OUT)
# Green
GPIO.setup(green_pin,GPIO.OUT)
GPIO.setup(reset_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(early_green_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  

# This is for debouncing
time_stamp = time.time() 

def set_traffic_lights(red,yellow,green):
    GPIO.output(red_pin,red)
    GPIO.output(yellow_pin,yellow)
    GPIO.output(green_pin,green)

def reset_callback(channel):
    global state
    global state_counter
    global time_stamp       # put in to debounce
    time_now = time.time()
    if (time_now - time_stamp) >= 0.3:
        print "Reset button was pressed"
        state="reset"
        set_traffic_lights(1,1,1)
        time.sleep(1)
        set_traffic_lights(1,1,0)
        time.sleep(1)
        set_traffic_lights(1,0,0)
        while state_counter !=0:
            state="red"
    time_stamp=time_now

def early_green_callback(channel):
    global state
    global state_counter
    global time_stamp       # put in to debounce
    time_now = time.time()
    if (time_now - time_stamp) >= 0.3:
        print "Early green light trigger button was pressed"
        if state=="red":
            state="early"
            # Pause for 1 second, then go green
            # Just in case, force the red light first
            set_traffic_lights(1,0,0)
            sleep(1)
            set_traffic_lights(0,0,1)
            state="green"
            state_counter=0
            print "Triggered an early red light"

        else:
            # We never stop a green or a yellow, only cause a red to end early
            print "Ignoring button press, this isn't a red light"
    time_stamp=time_now

GPIO.add_event_detect(reset_pin, GPIO.FALLING, callback=reset_callback)
GPIO.add_event_detect(early_green_pin, GPIO.FALLING, callback=early_green_callback)

# here you would put all your code for setting up GPIO,
# we'll cover that tomorrow
# initial values of variables etc...
counter = 0
counter_limit=9000000
state="red"

try:
    # here you put your main loop or block of code

    while counter < counter_limit:
        counter += 1
        # We start with a red light
        # Increment second by second until we hit either a reset switch or a 
        for state_counter in range(0, light_delay):
            print "%s  %s" % (state,state_counter)
            if state=="red":
                set_traffic_lights(1,0,0)
            elif state=="yellow":
                if state_counter>=yellow_light_delay:
                    break
                set_traffic_lights(0,1,0)
            elif state=="green":
                set_traffic_lights(0,0,1)
            else:
                print "Unknown state %s, leaving lights as is" % state
                #counter=counter_limit
            time.sleep(1)    
        
        # At this point we've finished a light so we need to step to the next light
        if state=="red":
            print "Red->Green"
            state="green"
        elif state=="yellow":
            print "Yellow->Red"
            state="red"
        elif state=="green":
            print "Green->Yellow"
            state="yellow"
        

        #print "Target reached: %d" % counter

except KeyboardInterrupt:
    # here you put any code you want to run before the program 
    # exits when you press CTRL+C
    print "\n", counter # print value of counter
    GPIO.cleanup() # this ensures a clean exit

except:
    # this catches ALL other exceptions including errors.
    # You won't get any error messages for debugging
    # so only use it once your code is working
    print "Other error or exception occurred!"
    GPIO.cleanup() # this ensures a clean exit

finally:
    GPIO.cleanup() # this ensures a clean exit

