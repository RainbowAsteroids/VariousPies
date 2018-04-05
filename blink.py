#!/usr/bin/python3
import RPi.GPIO as GPIO #For access to the raspberry pi's GPIO pins
import time #To blink the light
wait = time.sleep #Changing name of a function

"""Setup"""
GPIO.setmode(GPIO.BCM) #Setting the pinmode to BCM
GPIO.setup(18, GPIO.OUT) #Setting pin 18 to output

"""Code"""
try:
    while True:
        GPIO.output(18, 1) #Turning on LED
        wait(1) #Waiting a second
        GPIO.output(18,0) #Turns off LED
        wait(0.3) #Waits about a third of a second
except KeyboardInterrupt: #Runs this code if the user presses Ctrl+C
    GPIO.cleanup() #Cleans up the GPIO setup
    exit() #Quits the program
