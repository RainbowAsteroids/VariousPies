#!/usr/bin/python3
import RPi.GPIO as GPIO #Gives us access to GPIO pins

outputPin = 18 #This is the pin the buzzer will be connected to

GPIO.setmode(GPIO.BCM) #Sets pinmode to BCM
GPIO.setup(outputPin, GPIO.OUT) #Sets outputPin to output mode

p = GPIO.PWM(18, 100)  # channel=12 frequency=100Hz
p.start(0) #Starts the buzzer and sets it to zero
try:
    p.ChangeDutyCycle(50) #Changes the buzzer to 50, it should be making noice
    while True:
        pass #Keeps the code running
except KeyboardInterrupt: #Ends the code if you press Ctrl+C
    pass
p.stop() #Stops our buzzer
GPIO.cleanup() #Cleans up GPIO
