#!/usr/bin/python3
import RPi.GPIO as GPIO
from time import sleep as wait
from random import randrange as randomInt

button1 = 4
button2 = 17
button3 = 27
button4 = 22
correctLED = 18
incorrectLED = 23
readyLED = 24
passkey = [randomInt(1,5), randomInt(1,5), randomInt(1,5), randomInt(1,5)]
waitPeriod = .15
delay = 1
inputtedKey = []
loop = True
count = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(button1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(button2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(button3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(button4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(correctLED, GPIO.OUT)
GPIO.setup(incorrectLED, GPIO.OUT)
GPIO.setup(readyLED, GPIO.OUT)

def resetKey():
    global passkey
    passkey = [randomInt(1,5), randomInt(1,5), randomInt(1,5), randomInt(1,5)]
def startup(inverse=False):
    if not inverse:
        leds = [readyLED, incorrectLED, correctLED]
    else:
        leds = [correctLED, incorrectLED, readyLED]
    for LED in leds:
        GPIO.output(LED, 1)
        wait(.15)
        GPIO.output(LED, 0)

try:
    startup()
    wait(.15)
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
            print("YOU WIN!!!")
            wait(3)
            GPIO.output(correctLED, 0)
            GPIO.output(readyLED, 1)
            print("Press 1 to play again, press 2 to quit!")
            loop = True
            while loop:
                if GPIO.input(button1):
                    wait(waitPeriod)
                    delay = 1
                    resetKey()
                    inputtedKey = []
                    startup()
                    for i in range(1,100):
                        print()
                    break
                elif GPIO.input(button2):
                    loop = False
                    GPIO.output(readyLED, 0)
                    startup(True)
        else:
            GPIO.output(readyLED, 0)
            GPIO.output(incorrectLED, 1)
            print("Input 1 : {}".format("Correct!" if inputtedKey[0] == passkey[0] else "Incorrect!"))
            print("Input 2 : {}".format("Correct!" if inputtedKey[1] == passkey[1] else "Incorrect!"))
            print("Input 3 : {}".format("Correct!" if inputtedKey[2] == passkey[2] else "Incorrect!"))
            print("Input 4 : {}".format("Correct!" if inputtedKey[3] == passkey[3] else "Incorrect!"))
            wait(delay)
            GPIO.output(incorrectLED, 0)
            GPIO.output(readyLED, 1)
            delay = delay + 1
            loop = True
            inputtedKey = []
        if not loop:
            break
except KeyboardInterrupt:
    pass
GPIO.cleanup()
