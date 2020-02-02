arr = []
def load_words():
    cnt = 0
    for _ in range(1,34):
        f = open("words/n1_{:03d}.txt".format(_),"r")
        for line in f:
            cnt += 1
            print(cnt, line.strip())
            arr.append(line)
load_words()
def save_words():
    n1 = -1
    cnt = 0
    for _ in range(0,len(arr)):
        if (_ % 10) is 0:
            n1 += 1
            f = open("words/n1_{_03d}.txt".format(n1),"w")
        #print("{:03d}".format(n1), cnt)
        
        f.write(arr[_-1])
        cnt += 1
save_words()