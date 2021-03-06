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
shutterPin = 12
startSwitch = 17
photogate = 26
continueSwitch = 16
dripValve = 25
delay_after_flash = 0.05
delay_after_trigger = .5
valveOpen = .095  # Set a delay variable for time (seconds) valve is open
valvePause = .020 # set delay between drips (seconds)
flashDelay = .290 # Set a delay for flash to be triggered: adjust 
                  # this for part of collision you want to photograph
 

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)


def setup():
    GPIO.setmode(GPIO.BCM)
    
    GPIO.setup(soundPin,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.setup(startSwitch,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.setup(photogate,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.setup(flashPin,GPIO.OUT)
    GPIO.setup(shutterPin,GPIO.OUT)
    GPIO.setup(dripValve,GPIO.OUT)
    #wake up flash might be in 'sleep' mode 
    GPIO.output(flashPin,GPIO.HIGH)
    time.sleep(delay_after_flash)
    GPIO.output(flashPin,GPIO.LOW)
    
    time.sleep(.1) #just incase flash was trigger (not in sleep mode)
    GPIO.output(shutterPin,GPIO.HIGH) # camera is in bulb mode
    time.sleep(delay_after_trigger)  # delay to ensure shutter is fully open
   
    GPIO.add_event_detect(soundPin, GPIO.FALLING, callback=event_loop, bouncetime=2000) #2000ms 2sec
    GPIO.add_event_detect(startSwitch, GPIO.FALLING, callback=event_loop, bouncetime=2000)
    GPIO.add_event_detect(photogate, GPIO.FALLING, callback=event_loop, bouncetime=2000)

def event_loop(channel):
    
    my_dict = {soundPin:'sound detected',startSwitch:'start startSwitch',photogate:'photogate'}
    print (my_dict[channel])

    GPIO.output(dripValve,GPIO.HIGH) #release 1st drop 
    time.sleep(valveOpen)
    GPIO.output(dripValve,GPIO.LOW)
    time.sleep(valvePause)           #    
    GPIO.output(dripValve,GPIO.HIGH) #release 2nd drop to create collision 
    time.sleep(valveOpen)
    GPIO.output(dripValve,GPIO.LOW)
    
    time.sleep(flashDelay)
    
    GPIO.output(flashPin,GPIO.HIGH)
    time.sleep(delay_after_flash)
    GPIO.output(flashPin,GPIO.LOW)
    time.sleep(1)  # make sure flash is complete before closing shutter 
    GPIO.output(shutterPin,GPIO.LOW)
    GPIO.cleanup()
    sys.exit(0)
     
if __name__ == '__main__':    # Program entrance
    print ('Program is starting ... \n')
    setup()
    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()
 

