#Program asks for user input to determine color to shine.

import time, sys
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)

red = GPIO.PWM(12, 60)
green = GPIO.PWM(16, 60)
blue = GPIO.PWM(21, 60)

red.start(0)
green.start(0)
blue.start(0)
    
def redOn():
    red.ChangeDutyCycle(100)

def redOff():
    red.ChangeDutyCycle(0)

def greenOn():
    green.ChangeDutyCycle(100)

def greenOff():
    green.ChangeDutyCycle(0)

def blueOn():
    blue.ChangeDutyCycle(100)

def blueOff():
    blue.ChangeDutyCycle(0)

def yellowOn():
    red.ChangeDutyCycle(100)
    green.ChangeDutyCycle(100)

def yellowOff():
    red.ChangeDutyCycle(0)
    green.ChangeDutyCycle(0)

def skyblueOn():
    blue.ChangeDutyCycle(100)
    green.ChangeDutyCycle(100)

def skyblueOff():
    blue.ChangeDutyCycle(0)
    green.ChangeDutyCycle(0)

def pinkOn():
    blue.ChangeDutyCycle(100)
    red.ChangeDutyCycle(100)

def pinkOff():
    blue.ChangeDutyCycle(0)
    red.ChangeDutyCycle(0)

def whiteOn():
    blue.ChangeDutyCycle(100)
    red.ChangeDutyCycle(100)
    green.ChangeDutyCycle(100)

def whiteOff():
    blue.ChangeDutyCycle(0)
    red.ChangeDutyCycle(0)
    green.ChangeDutyCycle(0)
