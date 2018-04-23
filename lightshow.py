#!/usr/bin/python3
import RPi.GPIO as GPIO
from time import sleep as wait
from random import choice as random

lights = (14, 15, 18, 23, 24, 4, 17, 27, 22, 10)

GPIO.setmode(GPIO.BCM)
for pin in lights:
	GPIO.setup(pin, GPIO.OUT)

def lightup(pin):
	GPIO.output(pin, 1)
	wait(.125)
	GPIO.output(pin, 0)

def end():
	GPIO.cleanup()
	quit()

def main():
	while True:
		lightup(random(lights))

try:
	main()
except KeyboardInterrupt:
	end()