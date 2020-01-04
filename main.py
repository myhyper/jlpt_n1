from gtts import gTTS
import json
import os
import sys
import random
from playsound import playsound
import threading
import difflib

day_count = 4 # How many days we've done? 
level_name = "n1" # N1

#day_count = 1 # How many days we've done? 
#level_name = "n4" # N4

# JSON
# *.txt : make a list of word list manually
# *.json : [ {word, ans, idx, n_ok, n_ng} ] a json list will be generated automatically
original_data_file_name = "./words/{}_{:03d}.json".format(level_name,day_count) 

try:
    arr_words = json.load(open(original_data_file_name,'r')) # JSON
except: # json이 없는 경우 자동으로 새로 생성 하자.
    f = open(original_data_file_name.replace("json","txt"),'r')
    i = 0
    arr_words = []
    while True:
        i += 1
        line = f.readline()
        if len(line) <= 0: break
        line = line.replace("\n",'')
        arr_words.append({
            "idx":"{}".format(i),
            "word":line,
            "ans":line,
            "n_ok":"0",
            "n_ng":"0"
        })
    # Save the result
    json.dump(arr_words, open(original_data_file_name,'w+'), indent=4, ensure_ascii=False) # JSON
    
arr_word_sounds = []
def load_sound_files(word_json_file_name):
    arr = json.load(open(word_json_file_name,'r'))
    i = 0
    for obj in arr:
        i += 1
        #tmp = obj["ans"]
        tmp = obj["word"]
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

# Japanese Full width characters
wide_to_ascii = dict((i, chr(i - 0xfee0)) for i in range(0xff01, 0xff5f))


## Random Word Game Loop
idx = random.randint(0,len(arr_words)-1) # JSON
last_idx = -1
while True:
    obj_word = arr_words[idx] # JSON
    word = obj_word["word"]
    
    print("[Direction] Type the same sentence ( Commands =>  ? Pronunciation  / Furigana  q quit ) : ")
    print(word)
    
    # GET USER INPUT
    user_input = sys.stdin.readline().replace("\n",'') # Trim

    # Compare it into the logic
    if 0 == len(user_input):   continue
    elif 0 <= user_input.find("?") or 0 <= user_input.find("？"):   threading.Thread(target=bg_play_mp3, args=([idx])).start() # Sound
    elif 0 <= user_input.find("/") or 0 <= user_input.find("・"): print("Hint : ", obj_word["ans"]) # JSON
    elif "q" == user_input or "ｑ" == user_input: print("Good bye!");break
    else:
        str_a = user_input.replace(" ",'').translate(wide_to_ascii).strip()
        str_b = word.replace("\n",'').replace(" ",'').translate(wide_to_ascii).strip()
        if str_a == str_b:
            playsound("./bgm/nice-work.wav")
            print("[Direction] nice work!")
            obj_word["n_ok"] = str(int(obj_word["n_ok"])+1) # JSON
            
            # Next Word
            idx = random.randint(0,len(arr_words)-1)
            while last_idx == idx:
                idx = random.randint(0,len(arr_words)-1)
            last_idx = idx
        else:
            playsound("./bgm/no-1.wav")
            output_list = [li for li in difflib.ndiff(str_a, str_b) if li[0] != ' ']
            char = ""
            for ch in output_list:
                char += ch
            print("[Direction] no! try again! " + char)
            obj_word["n_ng"] = str(int(obj_word["n_ng"])+1) # JSON
            
        # Save the result
        json.dump(arr_words, open(original_data_file_name,'w+'), indent=4, ensure_ascii=False) # JSON