import requests
from urllib.request import urlparse, urljoin
from bs4 import BeautifulSoup
import threading
import tkinter as tk
import time
import numpy as np
import random

def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_all_website_links(url):
    """
    Returns all URLs that is found on `url` in which it belongs to the same website
    """
    # all URLs found in `url`
    urls = set()
    
    # print("rq:","<"+url+">",end="")
    content = requests.get(url,timeout=1).content
    soup = BeautifulSoup(content, "html.parser")

    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            # href empty tag
            continue
        # join the URL if it's relative (not absolute link)
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        # remove URL GET parameters, URL fragments, etc.
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not is_valid(href):
            # not a valid URL
            continue
        if href not in urls and "http" in href and href[-4:]!=".jpg":
            # print(f"[*] Internal link: {href}")
            urls.add(href)
    # print(" > Done")
    return urls

def bfs_crawl(urls,t_id):
    """
    will keep on extracting extra urls from the set 'urls' and adding them to the same set
    until the total number of urls is no less than 'max_urls'.
    
    urls : a set of initial urls (which will expand in size)
    t_id : the id of the thread which is running this function.
    """
    global terminate_threads
    global max_urls
    visited = set()
    
    while len(urls)<max_urls and not terminate_threads:
        to_explore = []
        while len(to_explore)< 3 and not terminate_threads : # pick 3 random urls to explore each time
            temp = random.sample(urls,1).pop()
            urls.remove(temp)
            if temp not in visited and "https://fa.wikipedia.org" not in temp and "http" in temp and temp[-4]!=".":
                to_explore.append(temp)
                visited.add(temp)
        for link in to_explore:
            try:
                sub_links = []
                link = link.replace("\n", "")
                if link[-1]=="/":
                    link=link[:-1]
                sub_links = get_all_website_links(link)
            except:
                pass
            for sub_link in sub_links:
                if sub_link not in urls:
                    urls.add(sub_link)
        print(f"\rthread {t_id} : {len(urls)} found",end='')

    for url in visited:
        urls.add(url)
    with open(f"subLinks/Thread{t_id}_links.txt",'a',encoding="UTF_8") as f:
        for url in urls:
            f.write(url+"\n")
    print(f"\nThread{t_id} DONE______")

def run_threads(urls, depth, t_id):
    """
    runs {2**thread power} threads on the function 'bfs_crawl' each with a different
    part of the initial list of sites to crawl.

    urls : initial list of urls
    depth : current depth (number of time the urls list has been sliced into half)
    t_id : the thread id
    """
    if depth>=thread_power:
        print(f"[+] Thread{t_id+1}/{2**thread_power} started")
        thread = threading.Thread(target=bfs_crawl, args=(set(urls),t_id,))
        threads.append(thread)
        thread.start()
    else:
        half_indx = len(urls)//2
        run_threads(urls[:half_indx], depth+1,t_id)
        run_threads(urls[half_indx:], depth+1,t_id+2**depth)

def thread_status(labels, threads):
    terminated = len(threads)-1
    while terminated>0 and not terminate_threads:
        index = 0
        for thread in threads:
            if not thread.is_alive():
                labels[index].configure(text=f"thread {index} is done", bg="red")
                terminated+=1
            index+=1
        time.sleep(1)

def thread_terminator(window):
    global terminate_threads
    print("[*] TERMINATING ALL Threads")
    print("    saving current progress")
    print("    this could take a few seconds...")
    terminate_threads = True
    window.destroy()

def controler(threads):
    global terminate_threads
    try:
        r = tk.Tk() 
        r.title('URL extractor control panel')

        frames = []
        for _ in range(16):
            frame = tk.Frame(master=r, width=200, height=100)
            frame.pack()
            frames.append(frame)

        frame = tk.Frame(master=r, width=200, height=100)
        frame.pack()
        frames.append(frame)

        labels = []
        for frame in frames[:-1]:
            row = np.mod(len(labels),len(frames)-1)
            for column in range(4):
                w = tk.Label(frame, text=f'thread{len(labels)} running', bg="green", fg="white") 
                w.grid(row=row, column=column)
                labels.append(w)

        button = tk.Button(frames[-1], text='Stop', width=25 , command=lambda: thread_terminator(r))
        button.grid(row=7, column=1, columnspan=2, rowspan=2, padx=5, pady=5)

        threading.Thread(target=thread_status, args=(labels,threads,)).start()

        r.mainloop()

    except :
        pass
    finally:
        terminate_threads = True
### main ###
# the script starst here...

thread_power = 6
# thread power shows the number of threads to use in order to extract urls concurrently.
# number_of_threads = thread_power ** 2

list_of_urls = [] # reading the list of initial urls which should be in 'listOfSites.txt'
with open("listOfInitialSites.txt",'r',encoding="UTF-8")as f:
    lines = f.readlines()
for line in lines:
    list_of_urls.append(line)

tic = time.clock() # capturing the amount of time the program takes to compelete
threads = []
max_urls = len(list_of_urls)*1000//(2**thread_power)
thread_id = 0

print("____Parameters____________")
print(f"number of threads = {2**thread_power}")
print(f"max url per thread = {max_urls}")
print(f"number of initial sites = {len(list_of_urls)}")

terminate_threads = False
run_threads(list_of_urls,0,0)

thread = threading.Thread(target=controler, args=(threads,))
threads.append(thread)
thread.start()

for t in threads:
    t.join() # waiting for all threads to terminate

toc = time.clock()
print("[*] program finished")
print("time:",toc - tic)
