#!/usr/bin/env micropython
'''
menu part of passworddongle.py
have to load and unload in parts due to small memory
'''

import time

import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

import random
kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)

# all printable ascii chars, plus space, except double quote, tab, backslash
mychars="`aZ0+nM<bY1!oL>cX2@pK;dW3#qJ:eV4$rI'fU5%sH[gT6^tG]hS7&uF{iR8*vE}jQ9(wD-kP,)xC=lO.~yB_mN/ zA"
mylen=len(mychars)
# direction values
ENCRYPT=+1
DECRYPT=-1

def code2indexlist(key):
    # turn key into list of indexes
    keyi=[]
    for k in range(len(key)):
        keyi.append(mychars.index(key[k]))
    return keyi

def cryptchar(inchar,keyoffset,direction):
    try:
        charindex=mychars.index(inchar)
        encind=(charindex+direction*keyoffset)%mylen
        outchar=mychars[encind]
    except ValueError:
        print("invalid character used?")
        outchar="invalid"
    return outchar

def cryptstring(instring,keyi,direction):
    outstring=""
    keylen=len(keyi)
    keyindex=1%keylen   # allow 1 char key (even if not recommended)
    for eachchar in instring:
        keyoffset=keyi[keyindex]
        outletter=cryptchar(eachchar,keyoffset,direction)
        outstring+=outletter
        keyindex = (keyindex+1) % keylen
    return outstring

def tinydecrypt(code,key):
    try:
        keyi = code2indexlist(key)
        codelen=len(code)
        keylen=len(keyi)
        eachchar=code[0]
        keyoffset=keyi[0]
        lencode=cryptchar(eachchar,keyoffset,DECRYPT)
        totlen=mychars.index(lencode)
        encind=mychars.index(code[0])
        textlen=(totlen-keylen+mylen)%mylen
        plain=cryptstring(code[1:textlen+1],keyi,DECRYPT)
    except ValueError:
        print("invalid character used?")
        plain="invalid"
    return plain

def menu(key,buttons):
    # constants
    tick = 0.1
    bsp = chr(8) + " " + chr(8)  # backspace and overwrite with backspace
    action = ["up", "down", "enter"]

    data = [
        "work",
        ["rharolde", "rHDF1H.!O#3%8E+n.N>)f", "back", "back"],
        "home",
        ["rharold", "rHDF1H.!O#3%8E+n.N>)f", "back", "back"],
        "play",
        ["minecraft", ["dnsbob", "rHDF1H.!O#3%8E+n.N>)f", "back", ""], "back", ""],
    ]

    # variables
    current = data
    stack = []
    i = 0
    # print(current[i],end='')
    layout.write(current[i])
    old = current[i]
    button_num = 0
    button = buttons[0]
    while True:
        button_press = 0
        while not button_press:
            for button_num, button in enumerate(buttons):
                if button.value:
                    button_press = 1
                    dot[0] = (0, 0, 0)  # off
                    break
            time.sleep(tick)  # only if no button
        dot[0] = (0, 255, 0)  # green
        c = current[i]
        if action[button_num] == "down":
            i = (i + 2) % len(current)  # wrap at ends
        elif action[button_num] == "up":
            i = (i - 2) % len(current)  # wrap
        elif action[button_num] == "enter":
            v = current[i + 1]
            if type(v) == type("string"):
                if c == "back":
                    if stack:
                        i = stack.pop()
                        current = stack.pop()
                        c = current[i]
                else:
                    z="password:" + v
                    #z=plain=tinydecrypt(v,key)
                    # print(v,end='')
                    layout.write(z)
                    old = c
                    #return # testing memory use - debug
            elif type(v) == type(["list"]):
                old = current[i]
                stack.append(current)
                stack.append(i)
                current = v
                i = 0
        c = current[i]
        if c != old:  # only print if changed
            # print("".join([bsp for x in range(len(old))]),end='')    # erase
            layout.write("".join([bsp for x in range(len(old))]))  # erase
            # print(current[i],end='')
            layout.write(current[i])
            old = c
        while button.value:
            time.sleep(tick)  # wait for button release
