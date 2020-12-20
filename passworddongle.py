#!/usr/bin/env micropython
"""
Combine one-line menu, capacitive touch buttons, keyboard hid, Morse code input,
and tiny encryption to make a password dongle in MicroPython on a Trinket M0
https://github.com/dnsbob/password-dongle
"""

# imports
import time
import sys

import board
import touchio
import adafruit_dotstar as dotstar

import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS


# constants
tick = 0.1
bsp = chr(8) + " " + chr(8)  # backspace and overwrite with backspace

# One pixel connected internally!
dot = dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.2)
dot[0] = (0, 255, 0)  # green

touch1 = touchio.TouchIn(board.D1)  # red, space
touch3 = touchio.TouchIn(board.D3)  # blue, dash
touch4 = touchio.TouchIn(board.D4)  # yellow, dot
buttons = [touch4, touch3, touch1]

action = ["up", "down", "enter"]

data = [
    "work",
    ["rharolde", "xxxx", "back", "back"],
    "home",
    ["rharold", "yyyy", "back", "back"],
    "play",
    ["minecraft", ["dnsbob", "zzzz", "back", ""], "back", ""],
]

kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)

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
                # print(v,end='')
                layout.write(v)
                old = c
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
