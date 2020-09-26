import time
import random
import tkinter as tk

arr = []


# shorts
# 0 ~ 3
GameNumber = 3
file_name = "./shorts/n1_%03d.txt" % (GameNumber)

# subs
# 1 ~ 1
GameNumber = 1
file_name = "./subs/gangnam/%03d.txt" % (GameNumber)

with open(file_name) as f:
    s = 1
    cnt = 0
    while s:
        s = f.readline().strip()
        if not s: break
        cnt += 1
        if ', ' in s:
            obj = s.split(', ')
            arr.append({
                'kanji': obj[0],
                'furigana': obj[1],
                'kr': obj[2],
                'cnt': 0
            })
        elif '　' in s:
            obj = s.split('　')
            arr.append({
                'kanji': obj[0],
                'furigana': obj[1],
                # 'kr': obj[2],
                'cnt': 0
            })
def sample (arr):
    LEN = len(arr)
    MIN = 99999
    for el in arr:
        if el['cnt'] < MIN:
            MIN = el['cnt']
    arrTmp = []
    for i in range(LEN):
        el = arr[i]
        if MIN == el['cnt']:
            arrTmp.append(el)
    rtv = random.choice(arrTmp)
    rtv['cnt'] += 1
    return rtv

DELAY = 0.5

if 0: # CUI
    for i in range(len(arr)):
        el = sample(arr)

        print("%02d) " % (i+1), end='')
        for k in el.keys():
            if 'cnt' == k: continue
            v = el[k]
            print(v, end='')
            if not 'kr' == k:
                print(' → ', end='')
            time.sleep(DELAY + 0.1 * len(v))
        print('')
else: # GUI
    master = tk.Tk()
    label = tk.Label(master, text="First Name", font=("Osaka", 64)).grid(row=0)
    tk.Label(master, text="Last Name", font=("Osaka", 64)).grid(row=1)
    def show_entry_fields(event=None):
        # print("First Name: %s\nLast Name: %s" % (e1.get(), e2.get()))
        el = sample(arr)
        for k in el.keys():
            v = el[k]
            if 'cnt' == k: continue
            elif 'kanji' == k:
                tk.Label(master, text=v, font=("Osaka", 64)).grid(row=0, sticky='nesw')
            elif 'furigana' == k:
                tk.Label(master, text=v, font=("Osaka", 64)).grid(row=1, sticky='nesw')
            # elif 'kr' == k:
            #     tk.Label(master, text=v, font=("Osaka", 64)).grid(row=0)


    e1 = tk.Entry(master)
    e2 = tk.Entry(master)

    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)

    tk.Button(master, 
            text='Show', command=show_entry_fields).grid(row=3, 
                                                        column=0, 
                                                        sticky=tk.W, 
                                                        pady=4)
    tk.Button(master, 
            text='Quit', 
            command=master.quit).grid(row=3, 
                                        column=1, 
                                        sticky=tk.W, 
                                        pady=4)

    master.bind("<space>", show_entry_fields)

    master.geometry("960x500")
    tk.mainloop()