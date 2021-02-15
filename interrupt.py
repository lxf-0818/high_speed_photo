#!/usr/bin/env python3          
                                
import signal                   
import sys
import RPi.GPIO as GPIO

BUTTON_GPIO_0 = 16
LED_GPIO_0 = 20

BUTTON_GPIO_1 = 12
LED_GPIO_1 = 5


def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

def button_callback(channel):
    print (channel)
    
    #GPIO.remove_event_detect(channel)
    my_dict = {BUTTON_GPIO_0: LED_GPIO_0, BUTTON_GPIO_1: LED_GPIO_1}
    if GPIO.input(channel):
        GPIO.output(my_dict[channel], GPIO.LOW)
    else:
        GPIO.output(my_dict[channel], GPIO.HIGH)
    

if __name__ == '__main__':
    
    GPIO.setmode(GPIO.BCM)
    
    GPIO.setup(BUTTON_GPIO_0, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(LED_GPIO_0, GPIO.OUT)   
    GPIO.setup(BUTTON_GPIO_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(LED_GPIO_1, GPIO.OUT)   

    GPIO.add_event_detect(BUTTON_GPIO_0, GPIO.BOTH, 
            callback=button_callback, bouncetime=100)
    
    GPIO.add_event_detect(BUTTON_GPIO_1, GPIO.BOTH, 
            callback=button_callback, bouncetime=100)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()
       