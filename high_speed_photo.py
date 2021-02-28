#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time,sys
from bluedot import BlueDot
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
flashPin = 22 
shutterPin = 12
dripValve = 25
shots = 0

delay_after_flash = 0.05
delay_after_trigger = .5
valveOpen = .095  # 95ms Set a delay variable for time (seconds) valve is open
valvePause = .020 # 20ms set delay between drips (seconds)
flashDelay = .290 # 290ms Set a delay for flash to be triggered: adjust
                  # this for part of collision you want to photograph
 
def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(flashPin,GPIO.OUT)
    GPIO.setup(shutterPin,GPIO.OUT)
    GPIO.setup(dripValve,GPIO.OUT)
    #wake up flash might be in 'sleep' mode
    GPIO.output(flashPin,GPIO.HIGH)
    time.sleep(delay_after_flash)
    GPIO.output(flashPin,GPIO.LOW)
    time.sleep(.5) #just incase flash was trigger (not in sleep mode)
    GPIO.output(shutterPin,GPIO.HIGH) # camera is in bulb mode
    
def event_loop():
    global shots
    
    print ('start......... #:%s'%shots)
    shots=+1
    GPIO.output(dripValve,GPIO.HIGH) #release 1st drop 
    time.sleep(valveOpen)
    GPIO.output(dripValve,GPIO.LOW)
    
    time.sleep(valvePause)
        
    GPIO.output(dripValve,GPIO.HIGH) #release 2nd drop to create collision
    time.sleep(valveOpen)
    GPIO.output(dripValve,GPIO.LOW)
    
    time.sleep(flashDelay)

    GPIO.output(flashPin,GPIO.HIGH)
    time.sleep(delay_after_flash)
    GPIO.output(flashPin,GPIO.LOW)
    time.sleep(.5)  # make sure flash is complete before closing shutter 
    GPIO.output(shutterPin,GPIO.LOW)
    
def destroy():
    GPIO.cleanup()                      # Release all GPIO

     
if __name__ == '__main__':    # Program entrance
    try:

        GPIO.setwarnings(False)
        bd = BlueDot()
        while (True):
            if bd.wait_for_press() :
                setup()
                event_loop()
                
    except KeyboardInterrupt:   # Press ctrl-c to end the program.
        destroy()
 
