#!/usr/bin/env micropython
"""
Combine one-line menu, capacitive touch buttons, keyboard hid, Morse code input,
and tiny encryption to make a password dongle in MicroPython on a Trinket M0
https://github.com/dnsbob/password-dongle
"""

# imports
import sys
import gc

import board
import touchio

#import gc

key="password"

# constants

touch1 = touchio.TouchIn(board.D1)  # red, space
touch3 = touchio.TouchIn(board.D3)  # blue, dash
touch4 = touchio.TouchIn(board.D4)  # yellow, dot
buttons = [touch4, touch3, touch1]


#print("free before:",gc.mem_free())
import morseword
#print("free after morseword import:",gc.mem_free())
key=morseword.morseword(buttons)
#print("key:",key)
del sys.modules[morseword.__name__]
del morseword
#print("free after morseword:",gc.mem_free())


gc.collect()
#print("free after gc:",gc.mem_free())
import pwmenu
#print("free after pwmenu import:",gc.mem_free())
pwmenu.menu(key, buttons)
#print("free after pwmenu:",gc.mem_free())
