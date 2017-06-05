import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
PWMR = GPIO.PWM(24, 60)
PWMR1 = GPIO.PWM(23, 60)
PWML = GPIO.PWM(27, 60)
PWML1 = GPIO.PWM(22, 60)
PWMR.start(0)
PWMR1.start(0)
PWML.start(0)
PWML1.start(0)
def move_forward():
    print "Going Forward"
    PWMR.ChangeDutyCycle(100)
    #PWMR1.ChangeDutyCycle(0)
    PWML.ChangeDutyCycle(97)
    #PWML1.ChangeDutyCycle(0)
    time.sleep(10)
    PWMR.stop()
    PWML.stop()
def move_backward():
    print "Going Backward"
    #PWMR.ChangeDutyCycle(0)
    PWMR1.ChangeDutyCycle(100)
    #PWML.ChangeDutyCycle(0)
    PWML1.ChangeDutyCycle(96)
    time.sleep(10)
    PWMR1.stop()
    PWML1.stop()
def main():
    move_forward()
    move_backward()
if __name__=='__main__':
    main()
    GPIO.cleanup
