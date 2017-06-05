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
    
print("""Ensure the following GPIO connections: R-11, G-13, B-15
Colors: Red, Green, Blue, Yellow, Cyan, Magenta, and White
Use the format: color on/color off""")

def main():
    while True:
        cmd = raw_input("-->")


        if cmd == "red on":
            redOn()
        elif cmd == "red off":
            redOff()
        elif cmd == "green on":
            greenOn()
        elif cmd == "green off":
            greenOff()
        elif cmd == "blue on":
            blueOn()
        elif cmd == "blue off":
            blueOff()
        elif cmd == "yellow on":
            yellowOn()
        elif cmd == "yellow off":
            yellowOff()
        elif cmd == "cyan on":
            cyanOn()
        elif cmd == "cyan off":
            cyanOff()
        elif cmd == "magenta on":
            magentaOn()
        elif cmd == "magenta off":
            magentaOff()
        elif cmd == "white on":
            whiteOn()
        elif cmd == "white off":
            whiteOff()
        else:
            print("Not a valid command")
        
        
    return
    

main()
    
