from gtts import gTTS
import json

def wget_mp3(word_list_file_name):
    f = open(word_list_file_name,'r')
    i = 0
    while True:
        i += 1
        tmp = f.readline()
        if 0 < len(tmp):
            tmp = tmp.replace("\n",'')
            arr.append(tmp)
            
            file_name = "./words/mp3/002_{:03d}.mp3".format(i)
            try:
                open(file_name, 'r')
            except: # if not exists
                print("Downloading mp3 ... ")
                a = gTTS(tmp,lang='ja')
                a.save(file_name)
        else: break
    f.close()


arr = []
wget_mp3('./words/day002.txt')


## Random Word Game
import os
import sys
import random
from playsound import playsound

import threading

def bg_run(word_idx):
    file_name = "words/mp3/002_{:03d}.mp3".format(word_idx+1)
    playsound(file_name)


idx = random.randint(0,len(arr)-1)
while True:
    word = arr[idx]
    print(word)
    user_input = sys.stdin.readline()
    if "?\n" == user_input:
        threading.Thread(target=bg_run, args=([idx])).start()
        pass
    else:
        if user_input.replace("\n",'') == word:
            print("GOOD!")
            idx = random.randint(0,len(arr)-1)
        else:
            print("Wrong. Try again!")
    print(user_input)