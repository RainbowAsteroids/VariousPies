#!/usr/bin/python3
import time #Imports time for our wait command
import RPi.GPIO as GPIO #Gives us access to the GPIO pins

wait = time.sleep #Renames time.sleep to wait

outputPin = 18 #Sets our buzzer pin
inputPin = 17 #Sets our button pin
ledPin = 27 #Sets our LED pin
waitPeriod = .15 #How long the code stops inbetween button presses
strobe = .1 #How long the light waits before toggling

GPIO.setmode(GPIO.BCM) #Sets pinmode to BCM
GPIO.setup(inputPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #Sets inputPin to input  mode and activates pull down resistors
GPIO.setup(outputPin, GPIO.OUT) #Sets outputPin to output mode
GPIO.setup(ledPin, GPIO.OUT) #Sets ledPin to output mode

p = GPIO.PWM(outputPin, 200) #Sets up our buzzer
p.start(0) #Starts buzzer at zero
GPIO.output(ledPin, 0) #Turns off our LED

try:
    while True:
        if GPIO.input(inputPin): #Waits until button press
            wait(waitPeriod)
            print("Alarm On") #Prints out confirmation
            ledOn = False
            p.ChangeDutyCycle(50) #Turns on buzzer
            while True:
                GPIO.output(ledPin, 1) #Turns on our LED
                wait(strobe)
                GPIO.output(ledPin, 0) #Turns off our LED
                wait(strobe)
                if GPIO.input(inputPin): #Checks if the button has been pressed
                    wait(waitPeriod)
                    print("Alarm Off") #Prints confirmation
                    p.ChangeDutyCycle(0) #Turns off buzzer
                    break
except KeyboardInterrupt: #Checks if you've presses Ctrl+C
    p.stop() #Stops our buzzer
    GPIO.cleanup() #Cleans up GPIO
