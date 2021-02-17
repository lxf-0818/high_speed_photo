#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time,signal,sys
'''

bulb mode and manual focus
camera wired remote:
white gnd; red focus ; yellow shutter 

red pin 4 Opto isolator
yellow + white pin 5 Opto isolator

flash either wire:
pin 4
pin 5
'''
soundPin = 19 
flashPin = 22 
shutterPin = 18
switch = 17
delay_after_flash = 0.05
delay_after_trigger = .5

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)


def setup():
    GPIO.setmode(GPIO.BCM)
    
    GPIO.setup(soundPin,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.setup(switch,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.setup(flashPin,GPIO.OUT)
    GPIO.setup(shutterPin,GPIO.OUT)
    #wake up flash might be in 'sleep' mode 
    GPIO.output(flashPin,GPIO.HIGH)
    time.sleep(delay_after_flash)
    GPIO.output(flashPin,GPIO.LOW)
   
    time.sleep(.1) #if not sleep will fire delay before openning shutter in bulb mode 
    GPIO.output(shutterPin,GPIO.HIGH)
    time.sleep(delay_after_trigger)  # delay to ensure shutter is fully open using bulb mode

    GPIO.add_event_detect(soundPin, GPIO.FALLING, callback=event_loop, bouncetime=2000) #2000ms 2sec
    GPIO.add_event_detect(switch, GPIO.FALLING, callback=event_loop, bouncetime=20)

def event_loop(channel):
    
    my_dict = {soundPin:'sound detected',switch:'start switch'}

    for i in my_dict:
        GPIO.remove_event_detect(i)
       # print ('removing event %s'%my_dict[i])
        
    print (my_dict[channel])
    
    GPIO.output(flashPin,GPIO.HIGH)
    time.sleep(delay_after_flash)
    GPIO.output(flashPin,GPIO.LOW)
    time.sleep(1)  # make sure flash is complete before closing shutter 
    GPIO.output(shutterPin,GPIO.LOW)
    GPIO.cleanup()
    #sys.exit(0)

  
if __name__ == '__main__':    # Program entrance
    print ('Program is starting ... \n')
    GPIO.setwarnings(False)
    setup()
    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()
 
