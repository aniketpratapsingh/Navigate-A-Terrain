import random, time
import RPi.GPIO as GPIO

RUNNING = True
GPIO.setmode(GPIO.BCM)
red = 12
green = 16
blue = 20

GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)

Freq = 100 

RED = GPIO.PWM(red, Freq)
RED.start(100)
GREEN = GPIO.PWM(green, Freq)
GREEN.start(100)
BLUE = GPIO.PWM(blue, Freq)
BLUE.start(100)

def color(R, G, B, on_time):
    RED.ChangeDutyCycle(R)
    GREEN.ChangeDutyCycle(G)
    BLUE.ChangeDutyCycle(B)
    time.sleep(on_time)

    RED.ChangeDutyCycle(1)
    GREEN.ChangeDutyCycle(1)
    BLUE.ChangeDutyCycle(1)

try:
    while RUNNING:
        for x in range(1,-1,-1):
            for y in range(1,-1,-1):
                for z in range(1,-1,-1):
                    print (x,y,z)
                    for i in range(100,-1,-1):
                        color((x*i),(y*i),(z*i), .05)
                    for i in range(0,101):
                        color((x*i),(y*i),(z*i), .05)

except KeyboardInterrupt:
    RUNNING = False
    print "\Quitting"

finally:
    GPIO.cleanup()
