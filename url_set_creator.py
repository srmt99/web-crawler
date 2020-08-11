import glob

with open("url_set.txt",'a',encoding="UTF-8")as writer:
    for filename in glob.glob("subLinks/*.txt"):
        with open(filename,'r',encoding="UTF-8")as reader:
            lines = reader.readlines()
        for line in lines:
            writer.write(line)