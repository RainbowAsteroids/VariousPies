#!/usr/bin/python3
import RPi.GPIO as GPIO
from time import sleep as wait
from random import randrange as randomInt
import click
import random
import os


button1 = 4
button2 = 17
button3 = 27
button4 = 22
correctLED = 18
incorrectLED = 23
readyLED = 24
telegraphers = {
	1:12,
	2:7,
	3:8,
	4:25
}

passkey = [randomInt(1,5), randomInt(1,5), randomInt(1,5), randomInt(1,5)]
waitPeriod = .3
delay = 3
inputtedKey = []
loop = True
count = 0
colors = {
	"end":"\033[0m",
	"green":"\033[92m",
	"blue":"\033[94m",
	"yellow":"\033[93m",
	"red":"\033[91m",
	"bold":"\033[1m"
}

color = ("red", "green", "yellow", "blue")

GPIO.setmode(GPIO.BCM)
GPIO.setup(button1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(button2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(button3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(button4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(correctLED, GPIO.OUT)
GPIO.setup(incorrectLED, GPIO.OUT)
GPIO.setup(readyLED, GPIO.OUT)
for pin in list(telegraphers.values()):
	GPIO.setup(pin, GPIO.OUT)

def style(str, color, bold=False):
	return colors["bold" if bold else "end"]+colors[color]+str+colors["end"]


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
def rainbow(text, bold=True):
    str = ""
    text = list(text)
    for letter in text:
        str = str+style(letter, random.choice(color), bold)
    print(str)
def telegraph(key):
	for led in key:
		GPIO.output(telegraphers[led], 1)
		wait(.25)
		GPIO.output(telegraphers[led], 0)
		wait(.125)

try:
    startup()
    wait(.15)
    GPIO.output(readyLED, 1)
    os.system("clear")
    while True:
        while loop:
            if GPIO.input(button1):
                print(style("1", "red"))
                GPIO.output(telegraphers[1], 1)
                inputtedKey.append(1)
                wait(waitPeriod)
                GPIO.output(telegraphers[1], 0)
            if GPIO.input(button2):
                print( style("2", "green"))
                GPIO.output(telegraphers[2], 1)
                inputtedKey.append(2)
                wait(waitPeriod)
                GPIO.output(telegraphers[2], 0)
            if GPIO.input(button3):
                print(style("3", "yellow"))
                GPIO.output(telegraphers[3], 1)
                inputtedKey.append(3)
                wait(waitPeriod)
                GPIO.output(telegraphers[3], 0)
            if GPIO.input(button4):
                print(style("4", "blue"))
                GPIO.output(telegraphers[4], 1)
                inputtedKey.append(4)
                wait(waitPeriod)
                GPIO.output(telegraphers[4], 0)
            if len(inputtedKey) == len(passkey):
                loop = False
        if inputtedKey == passkey:
            GPIO.output(readyLED, 0)
            GPIO.output(correctLED, 1)
            rainbow("YOU WIN!!!")
            wait(3)
            GPIO.output(correctLED, 0)
            telegraph(inputtedKey)
            GPIO.output(readyLED, 1)
            click.echo("Press {}".format(style("1", "red"))+" to play again or press {}".format(style("2", "green"))+" to quit!")
            loop = True
            while loop:
                if GPIO.input(button1):
                    wait(waitPeriod)
                    delay = 1
                    resetKey()
                    inputtedKey = []
                    startup()
                    os.system("clear")
                    break
                elif GPIO.input(button2):
                    loop = False
                    GPIO.output(readyLED, 0)
                    startup(True)
                elif GPIO.input(button3):
                    telegraph(inputtedKey)
        else:
            GPIO.output(readyLED, 0)
            GPIO.output(incorrectLED, 1)
            print("Input 1 : {}".format(style("Correct!","green") if inputtedKey[0] == passkey[0] else style("Incorrect!", "red")))
            print("Input 2 : {}".format(style("Correct!","green") if inputtedKey[1] == passkey[1] else style("Incorrect!", "red")))
            print("Input 3 : {}".format(style("Correct!","green") if inputtedKey[2] == passkey[2] else style("Incorrect!", "red")))
            print("Input 4 : {}".format(style("Correct!","green") if inputtedKey[3] == passkey[3] else style("Incorrect!", "red")))
            wait(delay)
            GPIO.output(incorrectLED, 0)
            GPIO.output(readyLED, 1)
            delay = delay + 2
            loop = True
            inputtedKey = []
        if not loop:
            break
except KeyboardInterrupt:
    pass
GPIO.cleanup()
