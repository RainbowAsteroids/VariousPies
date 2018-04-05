#!/usr/bin/python3
import RPi.GPIO as GPIO #Gives us access to GPIO pins

inputPin = 17 #Sets inputPin to your desired choice

GPIO.setmode(GPIO.BCM) #Sets pinmode to BCM
GPIO.setup(inputPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #Sets inputPin to input mode and activates pull down resistors

try:
    while True:
        if GPIO.input(inputPin): #Checks if inputPin is HIGH
            print("Button Pressed!") #Prints that your button is pressed
except KeyboardInterrupt: #Checks if Ctrl+C is pressed
    GPIO.cleanup() #Resets the GPIO
    exit() #Quits the program
