# number of concurrent spiders to be created
num_spiders = 7

# splitting the url list into <num_spiders> files
with open("url_set.txt",'r',encoding="UTF-8")as f:
    lines = f.readlines()

split = len(lines)//num_spiders
# creating sub files of urls sets
for i in range(num_spiders):
    if i+1<num_spiders:
        with open(f"url_set_part{i+1}.txt",'w',encoding="UTF-8")as f:
            for line in lines[i*split:(i+1)*split]:
                f.write(line)
    else:
        with open(f"url_set_part{i+1}.txt",'w',encoding="UTF-8")as f:
            for line in lines[i*split:]:
                f.write(line)

# reading the the raw code to create a spider
with open("raw_spider_code.txt",'r')as f:
    lines = f.readlines()
# creating the spiders
for i in range(num_spiders):
    raw_spider_code = ""
    for line in lines:
        raw_spider_code += line
    raw_spider_code = raw_spider_code.replace("spider_name",f"spider{i+1}")
    raw_spider_code = raw_spider_code.replace("part_",f"part{i+1}")

    with open(f"./text_extractor/spiders/spider{i+1}.py",'w')as f:
        f.write(raw_spider_code)

        #scrapy crawl spider1 -s JOBDIR=./crawls/spider1