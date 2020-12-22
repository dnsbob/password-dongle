#!/usr/bin/env micropython

import time

def morseword(buttons):
    sleep=.01
    # note that Morse code does not have separate uppercase and lowercase
    asciinum2morse=[
            "", "", "", "", "", "", "", "",
            "", "", "", "", "", "", "", "",
            "", "", "", "", "", "", "", "",
            "", "", "", "", "", "", "", "",
            # space, !, ", #, $, %, &, '
            "", "-.-.--", ".-..-.", "", "", "", "", ".----.",
            # ( ) * + , - . /
            "-.--.", "-.--.-", "", ".-.-.", "--..--", "-....-", ".-.-.-", "-..-.",
            # 0 1 2 3 4 5 6 7
            "-----", ".----", "..---", "...--", "....-", ".....", "-....", "--...",
            # 8 9 : ; < = > ?
            "---..", "----.", "---...", "-.-.-.", "", "-...-", "", "..--..",
            # @ A B C D E F G
            ".--.-.", ".-", "-...", "-.-.", "-..", ".", "..-.", "--.",
            # H I J K L M N O
            "....", "..", ".---", "-.-", ".-..", "--", "-.", "---",
            # P Q R S T U V W
            ".--.", "--.-", ".-.", "...", "-", "..-", "...-", ".--",
            # X Y Z [ \ ] ^ _
            "-..-", "-.--", "--..", "", "", "", "", "..--.-",
            # ' a b c d e f g
            "", ".-", "-...", "-.-.", "-..", ".", "..-.", "--.",
            # h i j k l m n o
            "....", "..", ".---", "-.-", ".-..", "--", "-.", "---",
            # p q r s t u v w
            ".--.", "--.-", ".-.", "...", "-", "..-", "...-", ".--",
            # x y z { | } ~ DEL
            "-..-", "-.--", "--..", "", "", "", "", ""
    ]
    '''record dots and dashes in a strings, list of strings separated by space button
    two consecutive space button ends the list and returns it
    pass in a list of buttons for dot, dash, and space
    '''
    buttonuse=['dot','dash','space']
    chars=[]
    dotdashlist=[]  # more efficient to add to a list of characters and join at the end
    buttonprev={}
    run=1
    while run:
        for i,button in enumerate(buttons):
            buttonnew=button.value
            if buttonnew != buttonprev.get(i):
                #print(i,buttonuse[i],buttonnew)
                buttonprev[i]=buttonnew
                if buttonnew==True:
                    if i == 0:  # dot
                        dotdashlist.append(".")
                        #print(".",end="")
                    elif i==1:  # dash
                        dotdashlist.append("-")
                        #print("-",end="")
                    else:       # space
                        if dotdashlist:
                            dotdash="".join(dotdashlist)
                            dotdashlist=[]
                            #char=morse2ascii.get(dotdash)
                            try:
                                char=asciinum2morse.index(dotdash)
                                disp=chr(char)
                            except ValueError:
                                char=None
                                disp="#"
                            chars.append(disp)
                            #print('found:',dotdash, char, disp)
                        else:
                            run=0
                    while button.value:
                        time.sleep(sleep)   # wait for button to be released
        time.sleep(sleep)   # debounce
    word="".join(chars)
    return word
