from gtts import gTTS
import json
import os
import sys
import random
from playsound import playsound
import threading
import difflib

# 62 63 64 65 66 67 68
# 69 70 71 72 73 74 75
day_count = 62 # How many days we've done? 
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
    cnt = 0
    for i in range(1,day_count):
        #file_name = "./words/{}_{:03d}_{:03d}.json".format(level_name, day_count, i)
        file_name = "./words/{}_{:03d}.json".format(level_name, day_count)
        objs = json.load(open(file_name,'r'))
        cnt += len(objs)
        print(cnt)
        
        
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
if False:
    threading.Thread(target=bg_load_sound_files, args=()).start()


def bg_play_mp3(word_idx):
    #file_name = "words/mp3/{}_{:03d}_{:03d}.mp3".format(level_name, day_count, word_idx+1)
    #file_name = "words/mp3/{}_{:03d}_{:03d}.mp3".format(level_name, day_count, word_idx+1)
    file_name = "words/mp3_native1/N1v_{:04d}s.mp3".format(day_count * 10 + (word_idx+1))
    print("mp3 load : ", file_name)
    try:
        playsound(file_name)
    except:
        playsound(file_name.replace("s.mp3", "s1.mp3"))

# Japanese Full width characters
wide_to_ascii = dict((i, chr(i - 0xfee0)) for i in range(0xff01, 0xff5f))


#
def get_next_word(last_idx):
    max_idx = -1;i=0
    max_val = -1
    min_idx = 999
    min_val = 999
    for word in arr_words:
        v = int(word["n_ok"])
        if max_val < v: 
            max_idx = i
            max_val = v
        if v < min_val:
            min_idx = i
            min_val = v
        i += 1
    idx = random.randint(0,len(arr_words)-1)
    while last_idx == idx or min_val < int(arr_words[idx]["n_ok"]):
        idx = random.randint(0,len(arr_words)-1)
        if min_idx == idx: break # if it's very low, pop it
    print("You've rotated : ", arr_words[min_idx]["n_ok"])
    return idx

## Random Word Game Loop
idx = random.randint(0,len(arr_words)-1) # JSON
last_idx = -1
while True:
    obj_word = arr_words[idx] # JSON
    word = obj_word["word"]
    
    print("[Commands] ? Pronunciation ")
    print("[Commands] / Furigana ")
    print("[Commands] q quit ")
    print("[Commands] n next (skip) ")
    print("[Direction] Type the same sentence ( Commands =>  ? Pronunciation  / Furigana  q quit ) : ")
    if 0 == int(obj_word["n_ok"]): # if it's first time
        print("idx : ", idx)
        threading.Thread(target=bg_play_mp3, args=([idx])).start() # Sound
    
    print(word)
    # GET USER INPUT
    user_input = sys.stdin.readline().replace("\n",'') # Trim

    # Compare it into the logic
    if 0 == len(user_input):   continue
    elif 0 <= user_input.find("?") or 0 <= user_input.find("？"):   threading.Thread(target=bg_play_mp3, args=([idx])).start() # Sound
    elif 0 <= user_input.find("/") or 0 <= user_input.find("・"): print("Hint : ", obj_word["ans"]) # JSON
    elif "q" == user_input or "ｑ" == user_input: print("Good bye!");break
    else:
        if "n" == user_input or "ｎ" == user_input: #skip
            idx = last_idx = get_next_word(last_idx)
        else:
            str_a = user_input.replace(" ",'').translate(wide_to_ascii).strip()
            str_b = word.replace("\n",'').replace(" ",'').translate(wide_to_ascii).strip()
            if str_a == str_b:
                if False:
                    playsound("./bgm/nice-work.wav")
                print("[Direction] nice work!")
                obj_word["n_ok"] = str(int(obj_word["n_ok"])+1) # JSON
                
                # Next Word
                idx = last_idx = get_next_word(last_idx)
            else:
                if False:
                    playsound("./bgm/no-1.wav")
                output_list = [li for li in difflib.ndiff(str_a, str_b) if li[0] != ' ']
                char = ""
                for ch in output_list:
                    char += ch
                print("[Direction] no! try again! " + char)
                obj_word["n_ng"] = str(int(obj_word["n_ng"])+1) # JSON
        
        print("")
        # Save the result
        json.dump(arr_words, open(original_data_file_name,'w+'), indent=4, ensure_ascii=False) # JSON