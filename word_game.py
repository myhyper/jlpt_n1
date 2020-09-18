import time
import random

arr = []
file_name = "./shorts/n1_%03d.txt" % (0)
with open(file_name) as f:
    s = 1
    cnt = 0
    while s:
        s = f.readline().strip()
        if not s: break
        cnt += 1
        obj = s.split(', ')
        arr.append({
            'kj': obj[0],
            'fr': obj[1],
            'kr': obj[2],
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