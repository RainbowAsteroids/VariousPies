#!/usr/bin/python3
import RPi.GPIO as GPIO #Gives us access to GPIO pins
from time import sleep as wait #imports wait command

button1 = 4 #Sets first button to pin four
button2 = 17 #Sets second button to pin 17
button3 = 27 #Sets third button to pin 27
button4 = 22 #Sets fourth button to pin 22
correctLED = 18 #Sets the correct notification LED (green) to pin 18
incorrectLED = 23 #sets incorrect notification LED (red) to pin 23
readyLED = 24 #Sets ready notification LED (blue) to pin 24
passkey = [1, 2, 3, 4] #Sets desired passkey
waitPeriod = .15 #Wait time imbetween button presses
delay = 3 #Delay between incorrect guesses
inputtedKey = [] #Keeps the inputted key here
loop = True #Varible that keeps the second loop working

GPIO.setmode(GPIO.BCM) #Sets pinmode to BCM
GPIO.setup(button1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #Sets button1 in input mode with pull down resistors
GPIO.setup(button2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #Sets button2 in input mode with pull down resistors
GPIO.setup(button3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #Sets button3 in input mode with pull down resistors
GPIO.setup(button4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #Sets button4 in input mode with pull down resistors
GPIO.setup(correctLED, GPIO.OUT)
GPIO.setup(incorrectLED, GPIO.OUT)
GPIO.setup(readyLED, GPIO.OUT)

try:
    GPIO.output(readyLED, 1)
    while True:
        while loop:
            if GPIO.input(button1):
                print(1)
                inputtedKey.append(1)
                wait(waitPeriod)
            if GPIO.input(button2):
                print(2)
                inputtedKey.append(2)
                wait(waitPeriod)
            if GPIO.input(button3):
                print(3)
                inputtedKey.append(3)
                wait(waitPeriod)
            if GPIO.input(button4):
                print(4)
                inputtedKey.append(4)
                wait(waitPeriod)
            if len(inputtedKey) == len(passkey):
                loop = False
        if inputtedKey == passkey:
            GPIO.output(readyLED, 0)
            GPIO.output(correctLED, 1)
            wait(3)
            GPIO.output(correctLED, 0)
            break
        else:
            GPIO.output(readyLED, 0)
            GPIO.output(incorrectLED, 1)
            wait(delay)
            GPIO.output(incorrectLED, 0)
            GPIO.output(readyLED, 1)
            delay = delay + 2
            loop = True
            inputtedKey = []
except KeyboardInterrupt:
    pass
GPIO.cleanup()
exit()
