from gtts import gTTS
import json
import os
import sys
import random
from playsound import playsound
import threading

#day_count = 3 # How many days we've done? 
#level_name = "n1" # N1

day_count = 1 # How many days we've done? 
level_name = "n4" # N4

# JSON
# *.txt : make a list of word list manually
# *.json : [ {word, ans, idx, n_ok, n_ng} ] a json list will be generated automatically
original_data_file_name = "./words/{}_{:03d}.json".format(level_name,day_count) 

arr_words = json.load(open(original_data_file_name,'r')) # JSON
arr_word_sounds = []
def load_sound_files(word_json_file_name):
    arr = json.load(open(word_json_file_name,'r'))
    i = 0
    for obj in arr:
        i += 1
        tmp = obj["ans"]
        if 0 < len(tmp):
            tmp = tmp.replace("\n",'')
            arr_word_sounds.append(tmp)
            
            file_name = "./words/mp3/{}_{:03d}_{:03d}.mp3".format(level_name,day_count, i)
            try:
                open(file_name, 'r')
            except: # if not exists
                print("\t(Now downloading mp3 ... )")
                a = gTTS(tmp,lang='ja')
                a.save(file_name)
        else: break

# Pre Loading...
def bg_load_sound_files():
    load_sound_files(original_data_file_name)
threading.Thread(target=bg_load_sound_files, args=()).start()


def bg_play_mp3(word_idx):
    file_name = "words/mp3/{}_{:03d}_{:03d}.mp3".format(level_name,day_count, word_idx+1)
    playsound(file_name)


## Random Word Game Loop
idx = random.randint(0,len(arr_words)-1) # JSON
while True:
    obj_word = arr_words[idx] # JSON
    word = obj_word["word"]
    
    print("[Direction] Type the same sentence ( Commands =>  ? Pronunciation  / Furigana  q quit ) : ")
    print("[Direction] This : ", word)
    
    # GET USER INPUT
    user_input = sys.stdin.readline().replace("\n",'') # Trim

    # Compare it into the logic
    if "?" == user_input:   threading.Thread(target=bg_play_mp3, args=([idx])).start() # Sound
    elif "/" == user_input: print("Hint : ", obj_word["ans"]) # JSON
    elif "q" == user_input: print("Good bye!");break
    else:
        if user_input.replace(" ",'') == word.replace("\n",'').replace(" ",''):
            playsound("./bgm/chime_up.wav")
            print("[Direction] GOOD!")
            obj_word["n_ok"] = str(int(obj_word["n_ok"])+1) # JSON
            
            # Next Word
            idx = random.randint(0,len(arr_words)-1)
        else:
            playsound("./bgm/cough_x.wav")
            print("[Direction] Wrong. Try again!")
            obj_word["n_ng"] = str(int(obj_word["n_ng"])+1) # JSON
            
        # Save the result
        json.dump(arr_words, open(original_data_file_name,'w+'), indent=4, ensure_ascii=False) # JSON