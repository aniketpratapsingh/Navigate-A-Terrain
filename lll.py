import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
#GPIO.setup(22, GPIO.OUT)
PWMR = GPIO.PWM(12, 60)
PWMR1 = GPIO.PWM(16, 60)
PWML = GPIO.PWM(21, 60)
#PWML1 = GPIO.PWM(22, 60)
PWMR.start(0)
PWMR1.start(0)
PWML.start(0)
#PWML1.start(0)
print "Going Forward"
PWMR.ChangeDutyCycle(100)
#PWMR1.ChangeDutyCycle(0)
PWML.ChangeDutyCycle(97)
#PWML1.ChangeDutyCycle(0)
time.sleep(10)
PWMR.stop()
PWML.stop()
print "Going Backward"
#PWMR.ChangeDutyCycle(0)
PWMR1.ChangeDutyCycle(100)
#PWML.ChangeDutyCycle(0)
#PWML1.ChangeDutyCycle(95)
time.sleep(10)

PWMR1.stop()

#PWML1.stop()
GPIO.cleanup
