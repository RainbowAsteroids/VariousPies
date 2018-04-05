#!/usr/bin/python3
import RPi.GPIO as GPIO #Gives us access to GPIO pins

"""Varibles"""
inputPin = 17
ledPin = 18

"""Setup"""
GPIO.setmode(GPIO.BCM) #Sets pinmode to BCM
GPIO.setup(inputPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #Sets up inputPin to input mode and activates some pull down resistors
GPIO.setup(ledPin, GPIO.OUT) #Sets up ledPin to output mode

try:
    while True:
        if GPIO.input(inputPin): #Checks if inputPin is HIGH
            GPIO.output(ledPin, 1) #Turns/Keeps LED on
        else:
            GPIO.output(ledPin, 0) #Keeps/Turns LED off
except KeyboardInterrupt: #Checks if user inputs Ctrl+C
    GPIO.cleanup() #Resets GPIO
    exit() #Quits program
