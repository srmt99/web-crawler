import string
import glob
import html2text
import random
import threading
import time
import os

def is_persian(word):
    '''
    this function checks if <word> has only persian characters
    '''
    if word=='':
        return False
    return (all(ord(x)>1547 for x in word) and all(ord(x)<1791 for x in word)) or ((all(ord(x)>1870 for x in word) and all(ord(x)<1919 for x in word)))

def eng_betw_per(word,prev,nxt):
    '''
    this function checks if <word> is an english word between pesrisn words.
    if any of the three surrounding words are persian, the output is True. 
    '''
    if word=='':
        return False
    return any(is_persian(x) for x in prev) and any(is_persian(x) for x in nxt)

def is_redundant(word):
    redundant_list = ["CONTENT","END","filesize","meta","function"] # just a bunch of redundant words which i saw in the outputs
    if word =='' or (not is_persian(word) and len(word)>14) or word in redundant_list:
        return True
    return False

def extract_text(list_of_files,t_id):
    '''
    this function takes a list of files (containing text) and cleans it
    and writes the clean text in a text file assosiataed with it's Thread id (t_id)
    '''
    for file_name in list_of_files[:10000]:
        with open(file_name,encoding="UTF-8") as f:
            lines = f.readlines()

        text = ""
        for line in lines:
            text = text + line

        h = html2text.HTML2Text()
        h.ignore_links = True
        # words = h.handle(text).split(" ")
        table = str.maketrans('', '', "#$%&'*+;<=>?@[]^_`{|}~") # removing unwanted punctuations
        try:
            words = h.handle(text).split("\n")
        except:
            pass
        text = ""
        for w in words:
            text = text + w.replace("\n","")
        words=text.split(" ")
        temp = []
        stripped = []
        for w in words:
                temp.append(w.translate(table))
        for w in temp:
            if w!='':
                stripped.append(w)

        with open(f"./raw_text/Thread{t_id}_temp_text.txt",'a',encoding="UTF-8") as f:
            for i in range(3,len(stripped)-4): # having three words before and after as neighbour words.
                word = stripped[i]
                if is_redundant(word):
                    continue
                prev = stripped[i-3:i]
                nxt = stripped[i+1:i+4]
                if is_persian(word) or eng_betw_per(word,prev,nxt):
                    f.write(word+" ")

### main ###
# the program starts here

num_threads = 5
threads = []

list_of_files = glob.glob(".\\downloaded_content\\*\\*.html")
random.shuffle(list_of_files)
split = len(list_of_files)//num_threads

tic = time.clock() # capturing the amount of time the program takes to compelete

for i in range(num_threads):
    if i+1<num_threads:
        thread = threading.Thread(target=extract_text, args=(list_of_files[i*split:(i+1)*split],i,))
        threads.append(thread)
        thread.start()
    else:
        thread = threading.Thread(target=extract_text, args=(list_of_files[i*split:],i,))
        threads.append(thread)
        thread.start()

for thread in threads:
    thread.join()

toc = time.clock()
print("[+] extracting done")
print("time:",toc - tic)
print("[+] putting all reslut in <text.txt>")
with open(".\\raw_text\\text.txt",'a',encoding="UTF-8")as w:
    for filename in glob.glob(".\\raw_text\\T*.txt"):
        with open(filename,'r',encoding='UTF-8')as r:
            while True:
                chunk = r.read(1000000)
                if not chunk:
                    break
                w.write(chunk)
for filename in glob.glob(".\\raw_text\\Thread*.txt"):
    os.remove(filename)
print("[+] program finished")
print("     (results can be found in text.txt)")