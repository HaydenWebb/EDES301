# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
Blink USR3
--------------------------------------------------------------------------
License:   
Copyright 2025 - Hayden Webb

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, 
this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE 
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF 
THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------

Simple code that will blink the USR3 LED of the BeagleBoard periodically

Error conditions:
  - Invalid operator --> Program should exit
  - Invalid number   --> Program should exit

--------------------------------------------------------------------------
"""

import Adafruit_BBIO.GPIO as GPIO
import time

def get_user_input():
    """ Gets time input from the user.
        Returns single :    (number) or 
                            (None) if inputs invalid
    """
    try:
        input1 = int(input("How long do you want the URS3 to blink?"))
        return (input1)
        
    except:
        print("Invalid Input")
        return (None, None, None)

def blink(timeUp):
    """ Gets time input from the user.
        Returns: Blink of 5Hz for specified time
    """    

    GPIO.setup("USR%d" % 3, GPIO.OUT)
    
    for i in range(timeUp):
        for j in range(5):
            GPIO.output("USR%d" % 3, GPIO.HIGH)
            time.sleep(0.2)
            GPIO.output("USR%d" % 3, GPIO.LOW)
            time.sleep(0.2)
        
        
if __name__ == "__main__":
    while(True):
        input1 = get_user_input()
        
        if (input1 == None):
            print("Invalid Input")
            break
        else:
            blink(input1)
        
        print("Hope you enjoyed the blinking!")