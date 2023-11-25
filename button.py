# FaceRecognitionDoorbell/button_listener.py
import RPi.GPIO as GPIO
import time
import requests

GPIO.setmode(GPIO.BOARD)
ledPin = 12
buttonPin = 16
GPIO.setup(ledPin, GPIO.OUT)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def capture():
    GPIO.output(ledPin, GPIO.HIGH)  # Turn on the LED
    # Call your capture function here
    requests.post('http://localhost:5001/ring')
    print("Button pressed, capture triggered")
    time.sleep(2)  # Keep the LED on for 5 seconds, or during capture
    GPIO.output(ledPin, GPIO.LOW)  # Turn off the LED

try:
    while True:
        buttonState = GPIO.input(buttonPin)
        if buttonState == False:
            capture()
        else:
            GPIO.output(ledPin, GPIO.LOW)
finally:
    GPIO.cleanup()