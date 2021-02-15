#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
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
delay_after_flash = 0.1
delay_after_trigger = .3

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(soundPin,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.setup(flashPin,GPIO.OUT)
    GPIO.setup(shutterPin,GPIO.OUT)
    #wake up flash might be in 'sleep' mode 
    GPIO.output(flashPin,GPIO.HIGH)
    time.sleep(delay_after_flash)
    GPIO.output(flashPin,GPIO.LOW)
    # sleep otherwise the sound from the flash will trigger the sound in the loop()
    time.sleep(.1)
      
def sound_loop():
 
    GPIO.wait_for_edge(soundPin, GPIO.FALLING)
    #if GPIO.input(soundPin) == GPIO.LOW:
    print ('sound detected....\nset trigger')
    GPIO.output(shutterPin,GPIO.HIGH)
    time.sleep(delay_after_trigger)  # delay to ensure shutter is fully open using bulb mode
    GPIO.output(flashPin,GPIO.HIGH)
    time.sleep(delay_after_flash)
    GPIO.output(flashPin,GPIO.LOW)
    time.sleep(1)  # make sure flash is complete before closing shutter 
    GPIO.output(shutterPin,GPIO.LOW)
    freeGPIOchannels()
        
           
def freeGPIOchannels():
    GPIO.cleanup()
    
if __name__ == '__main__':    # Program entrance
    print ('Program is starting ... \n')
    setup()
    try:
        sound_loop()
    except KeyboardInterrupt:   # Press ctrl-c to end the program.
        freeGPIOchannels()
