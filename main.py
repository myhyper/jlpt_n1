from gtts import gTTS
import json
import os
import sys
import random
from playsound import playsound
import threading

day_count = 3 # 몇일째 단어장인가? 
#level_name = "day" # N1급

day_count = 1 # 몇일째 단어장인가? 
level_name = "n4_" # N4급

# JSON
original_data_file_name = "./words/{}{:03d}.json".format(level_name,day_count) 

arr_words = json.load(open(original_data_file_name,'r')) # JSON
arr_word_sounds = []
def load_sound_files(word_list_file_name):
    f = open(word_list_file_name,'r')
    i = 0
    while True:
        i += 1
        tmp = f.readline()
        if 0 < len(tmp):
            tmp = tmp.replace("\n",'')
            arr_word_sounds.append(tmp)
            
            file_name = "./words/mp3/{}{:03d}_{:03d}.mp3".format(level_name,day_count, i)
            try:
                open(file_name, 'r')
            except: # if not exists
                print("\t(Now downloading mp3 ... )")
                a = gTTS(tmp,lang='ja')
                a.save(file_name)
        else: break
    f.close()

def bg_load_sound_files():
    load_sound_files(original_data_file_name.replace("json","txt"))
threading.Thread(target=bg_load_sound_files, args=()).start()


def bg_play_mp3(word_idx):
    file_name = "words/mp3/{}{:03d}_{:03d}.mp3".format(level_name,day_count, word_idx+1)
    playsound(file_name)


## Random Word Game
idx = random.randint(0,len(arr_words)-1) # JSON
while True:
    obj_word = arr_words[idx] # JSON
    word = obj_word["word"]
    
    print("[Direction] Type the same sentence ( Commands =>  ? Pronunciation  / Furigana  q quit ) : ")
    print("[Direction] This : ", word)
    
    # GET USER INPUT
    user_input = sys.stdin.readline().replace("\n",'') # Trim

    # Compare it into the logic
    if "?" == user_input:
        threading.Thread(target=bg_play_mp3, args=([idx])).start() # Sound
    elif "/" == user_input:
        print("Hint : ", obj_word["ans"]) # JSON
    elif "q" == user_input:
        print("Hint : ", obj_word["ans"]) # JSON
    else:
        if user_input.replace(" ",'') == word.replace("\n",'').replace(" ",''):
            print("[Direction] GOOD!")
            obj_word["n_ok"] = str(int(obj_word["n_ok"])+1) # JSON
            
            # Next Word
            idx = random.randint(0,len(arr_words)-1)
        else:
            print("[Direction] Wrong. Try again!")
            obj_word["n_ng"] = str(int(obj_word["n_ng"])+1) # JSON
            
        # Save the result
        json.dump(arr_words, open(original_data_file_name,'w+'), indent=4) # JSON