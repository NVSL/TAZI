import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
def resetPins():
    for i in range(28):
        GPIO.setup(i, GPIO.OUT)
        GPIO.output(i, GPIO.LOW)

if __name__ == "__main__": resetPins()
