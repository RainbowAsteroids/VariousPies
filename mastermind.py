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
colors = ["red","green","yellow","blue"]

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
def rainbow(text, nl=True, bold=True):
    text = list(text)
    x = text[-1]
    text.pop(-1)
    for letter in text:
        click.secho(letter, bold=bold, nl=False, fg=random.choice(colors))
    click.secho(x, bold=bold, nl=nl, fg=random.choice(colors))
def telegraph(key):
	for led in key:
		GPIO.output(telegraphers[led], 1)
		wait(.5)
		GPIO.output(telegraphers[led], 0)

try:
    startup()
    wait(.15)
    GPIO.output(readyLED, 1)
    os.system("clear")
    while True:
        while loop:
            if GPIO.input(button1):
                click.secho("1", bold=True, fg=colors[0])
                inputtedKey.append(1)
                wait(waitPeriod)
            if GPIO.input(button2):
                click.secho("2", bold=True, fg=colors[1])
                inputtedKey.append(2)
                wait(waitPeriod)
            if GPIO.input(button3):
                click.secho("3", bold=True, fg=colors[2])
                inputtedKey.append(3)
                wait(waitPeriod)
            if GPIO.input(button4):
                click.secho("4", bold=True, fg=colors[3])
                inputtedKey.append(4)
                wait(waitPeriod)
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
            click.echo("Press {}".format(click.style("1", bold=True, fg=colors[0]))+" to play again or press {}".format(click.style("2", bold=True, fg=colors[1]))+" to quit!")
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
                    os.system("clear")
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
            delay = delay + 2
            loop = True
            inputtedKey = []
        if not loop:
            break
except KeyboardInterrupt:
    pass
GPIO.cleanup()
