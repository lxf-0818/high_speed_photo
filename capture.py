#!/usr/bin/python
import subprocess 
import time

def take_picute(filename):

    test = subprocess.Popen([
        "gphoto2",
        "--capture-image-and-download",
        "--filename",filename, 
        "--bulb=3"],
        stdout=subprocess.PIPE)

    output = test.communicate()[0]
    print (output)


if __name__ == '__main__':
    filename = time.strftime("%Y%m%d-%H%M%S.jpg")
    take_picute(filename)
            
    
