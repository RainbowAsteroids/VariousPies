#!/usr/bin/python3
#Game created by Felix Zactor (RainbowAsteroids)
#https://github.com/RainbowAsteroids/VariousPies/blob/master/mastermind.py
#I connect 220 ohm resistors to LEDS and 1k ohm resistors to buttons
import RPi.GPIO as GPIO #Gives us access to GPIO pins
from time import sleep as wait #Gives us the command that "sleeps" the program
import random #Used for the rainbow function and generates a random key
import os #Used to clear terminal window of clutter


button1 = 4 #Pin for button 1
button2 = 17 #Pin for button 2
button3 = 27 #Pin for button 3
button4 = 22 #Pin for button 4
correctLED = 18 #Pin for led alerting you that you got it right (green)
incorrectLED = 23 #Pin alerting you that the inputted key was incorrect (red)
readyLED = 24 #Pin that tells you that the program is ready for input
telegraphers = { #Pins that light up telling you what you inputted or what the correct key is.
	1:12, #Red
	2:7, #Green
	3:8, #Yellow
	4:25 #Blue
}

passkey = [random.randrange(1,5), random.randrange(1,5), random.randrange(1,5), random.randrange(1,5)] #Randomly generated key
waitPeriod = .3 #Wait time inbetween button presses
delay = 3 #How long before key guesses
inputtedKey = [] #The key the user has inputted
loop = True #Controls the second while loop
colors = { #Color codes
	"end":"\033[0m",
	"green":"\033[92m",
	"blue":"\033[94m",
	"yellow":"\033[93m",
	"red":"\033[91m",
	"bold":"\033[1m"
}

color = ("red", "green", "yellow", "blue") #Colors that the program can access

GPIO.setmode(GPIO.BCM) #Set pinmode BCM
GPIO.setup(button1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #Sets these buttons to input mode with pull down resistors
GPIO.setup(button2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #^
GPIO.setup(button3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #^
GPIO.setup(button4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #^
GPIO.setup(correctLED, GPIO.OUT) #Sets up the correct LED to output mode
GPIO.setup(incorrectLED, GPIO.OUT) #Sets the incorrect LED to output mode
GPIO.setup(readyLED, GPIO.OUT) #Sets the ready LED to output mode
for pin in list(telegraphers.values()): #Sets up the telegrapher LEDs
	GPIO.setup(pin, GPIO.OUT)

def style(str, color, bold=False): #Returns a string with the desired color pre-built in
	return colors["bold" if bold else "end"]+colors[color]+str+colors["end"]


def resetKey(): #Resets the randomized key
    global passkey
    passkey = [randomInt(1,5), randomInt(1,5), randomInt(1,5), randomInt(1,5)]
def startup(inverse=False): #Shows a coolish startup/shutdown animation using the correct, incorrect, and ready LEDS
    if not inverse:
        leds = [readyLED, incorrectLED, correctLED]
    else:
        leds = [correctLED, incorrectLED, readyLED]
    for LED in leds:
        GPIO.output(LED, 1)
        wait(.15)
        GPIO.output(LED, 0)
def rainbow(text, bold=True): # Makes the inputted string rainbow looking
    str = ""
    text = list(text)
    for letter in text:
        str = str+style(letter, random.choice(color), bold)
    print(str)
def telegraph(key): #Shows a light show based off the generated key
	for led in key:
		GPIO.output(telegraphers[led], 1)
		wait(.25)
		GPIO.output(telegraphers[led], 0)
		wait(.125)

try:
    os.system("clear")
    startup()
    wait(.15)
    GPIO.output(readyLED, 1)
    while True:
        while loop:
            if GPIO.input(button1): #Detects if you pressed the button, flashes a light, and appends it to the inputted list
                print(style("1", "red"))
                GPIO.output(telegraphers[1], 1)
                inputtedKey.append(1)
                wait(waitPeriod)
                GPIO.output(telegraphers[1], 0)
            if GPIO.input(button2): #^
                print( style("2", "green"))
                GPIO.output(telegraphers[2], 1)
                inputtedKey.append(2)
                wait(waitPeriod)
                GPIO.output(telegraphers[2], 0)
            if GPIO.input(button3): #^
                print(style("3", "yellow"))
                GPIO.output(telegraphers[3], 1)
                inputtedKey.append(3)
                wait(waitPeriod)
                GPIO.output(telegraphers[3], 0)
            if GPIO.input(button4): #^
                print(style("4", "blue"))
                GPIO.output(telegraphers[4], 1)
                inputtedKey.append(4)
                wait(waitPeriod)
                GPIO.output(telegraphers[4], 0)
            if len(inputtedKey) == len(passkey): #When the inputted key is as long as the generated key, it 'breaks' the loop
                loop = False
        if inputtedKey == passkey: #Runs the victory code
            GPIO.output(readyLED, 0) #Turns off ready LED and turns on the correct LED
            GPIO.output(correctLED, 1)
            rainbow("YOU WIN!!!") #Prints a win message
            wait(3) #Hangs for three seconds
            GPIO.output(correctLED, 0) #Turns off correct LED
            telegraph(inputtedKey) #Plays a little light show
            GPIO.output(readyLED, 1) #Turns on the readyLED
            print("Press {}".format(style("1", "red"))+" to play again or press {}".format(style("2", "green"))+" to quit!") #Asks the user if they wish to play again
            loop = True
            while loop:
                if GPIO.input(button1): #Runs the code to prepare the game again
                    wait(waitPeriod)
                    delay = 1
                    resetKey()
                    inputtedKey = []
                    startup()
                    os.system("clear")
                    break
                elif GPIO.input(button2): #Runs the code to end the game
                    loop = False
                    GPIO.output(readyLED, 0)
                    startup(True)
                elif GPIO.input(button3): #EASTER EGG!!!
                    telegraph(inputtedKey) #Replays the cool light show!
        else: #Runs the incorrect code
            GPIO.output(readyLED, 0) #Turns off the ready LED
            GPIO.output(incorrectLED, 1) #Turn on the annoying incorrect LED
            print("Input 1 : {}".format(style("Correct!","green") if inputtedKey[0] == passkey[0] else style("Incorrect!", "red"))) #Prints out the status of the numbered input
            print("Input 2 : {}".format(style("Correct!","green") if inputtedKey[1] == passkey[1] else style("Incorrect!", "red"))) #^
            print("Input 3 : {}".format(style("Correct!","green") if inputtedKey[2] == passkey[2] else style("Incorrect!", "red"))) #^
            print("Input 4 : {}".format(style("Correct!","green") if inputtedKey[3] == passkey[3] else style("Incorrect!", "red"))) #^
            wait(delay) #Hangs for a LOOOOOOONNGG time
            GPIO.output(incorrectLED, 0) #Turns off incorrect LED
            GPIO.output(readyLED, 1) #Turns on ready LED
            delay = delay + 2 #Increases the LOOOOOOOOOOOO00O0O0OONNNNnNNNNGGggGG time
            loop = True 
            inputtedKey = [] #Resets the inputted key
        if not loop: #Breaks the outter loop if the inner loop was disabled (during the shutdown phase
            break
except KeyboardInterrupt: #Detects if someone tried to exit the program
    pass
GPIO.cleanup() #Cleans up the GPIO
