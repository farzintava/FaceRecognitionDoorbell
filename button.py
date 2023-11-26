# FaceRecognitionDoorbell/button_listener.py
import RPi.GPIO as GPIO
import time
import requests
from RPLCD.gpio import CharLCD



GPIO.setmode(GPIO.BOARD)
ledPin = 12
buttonPin = 16
GPIO.setup(ledPin, GPIO.OUT)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        buttonState = GPIO.input(buttonPin)
        if buttonState == False:
            GPIO.output(ledPin, GPIO.HIGH)  # Turn on the LED
            response = requests.post('http://localhost:5001/ring')
            
            
            lcd = CharLCD(cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[40, 38, 36, 32, 33, 31, 29, 23],numbering_mode=GPIO.BOARD,charmap='A02',
              auto_linebreaks=True)
            
            if response.status_code == 200:
                if response.content.decode('utf-8') != "Unknown":
                    lcd.write_string(u'Access Granted!')
                    lcd.crlf()
                    lcd.write_string(u'Welcome ')
                    lcd.write_string(response.content.decode('utf-8'))
                    # lcd.write_string(response.content)
                    
                else:
                    lcd.write_string(u'Access Denied!')
            elif response.status_code == 404:
                lcd.write_string(u'No Face Detected')
            
            print("Button pressed, capture triggered")
            GPIO.output(ledPin, GPIO.LOW)  # Turn off the LED
            time.sleep(2)
            lcd.close(clear=True)
        else:
            GPIO.output(ledPin, GPIO.LOW)
finally:
    GPIO.cleanup()