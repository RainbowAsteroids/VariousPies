#!/usr/bin/python3
import RPi.GPIO as GPIO
from time import sleep as wait
from random import choice as random

lights = (14, 4, 17, 27, 22, 15, 23, 10, 18, 24)

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
	
def flow():
	while True:
		for pin in lights:
			lightup(pin)
		for pin in list(reversed(lights)):
			lightup(pin)
		GPIO.output(lights[0], 1)
		wait(.125)
	
	
def menu():
	choices = ("Flow", "Random")
	message = "What lightshow do you want?\n"
	exit = False
	if type(choices) != list:
		print("Please put in a list of choices!")
	for i in choices:
		print(str(choices.index(i)+1)+".", i)
	if exit:
		print("0. Exit")
	try:
		choice = int(input(message))
	except:
		print("Please input a number.")
	if choice in range(len(choices)+2):
		return choice
	else:
		print("Invalid Option!!!")

def random():
	while True:
		lightup(random(lights))

commands = {
	1:flow,
	2:random
}

try:
	GPIO.output(22, 0)
	commands[menu()]()
except KeyboardInterrupt:
	end()