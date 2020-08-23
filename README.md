web-crawler
===========
web crawler , text extractor and (persian) text cleaner.

the aim of this project is to provide a corpus for Persian (or any other) language.
aside from the wikipedia dataset for Persian (or any other) language which might not be large enough, it is a good idea to crawl the world wide web in order to extract web page materials to build our own data set for when dealing with problems which require a large data set of raw text.

for this project, except for the open source python packages `aaronsw/html2text` is also used. for more info please visit https://github.com/aaronsw/html2text

how it works:
-----------------------
in order to create such dataset we go through the following steps:
1. we create a list of initial web page URLs which we will strat from
2. we will extract sublinks form the said initial list (in this project the BFS method has been used)
3. we go through all the extracted URLs and download the contained text in each.
4. we go through the downloaded text, and remove unwanted text such as: html tags, front-end/back-end codes, redundant words, characters and...
5. finally, we save the clean and raw output text for further use.

how to use this project:
-----------------------
first of all, if you are looking for the already gathered persian text file, i have put the download link below:

`NO-LINK-YET`

but if you wish to create your own data set, here are the steps to take:

1. open the terminal in the prefered directory and run the command: `scrapy startproject text_extractor` (needless to say, you should have the scrapy package installed)
2. go in the `./text_exctractor` directory (every thing is done here) then fill a `listOfInitialSites.txt` file with the desired URLs
3. run `subLink_extractor.py` (the results should be in a `subLink` folder)
4. run the `url_set_creator.py` to gather all the extracted URLs in one place (`url_set.txt`)
5. run the `spider_creator.py` to create the spiders
6. depending on the `num_spiders` which is set at the begining of the `spider_creator.py` you should run as many terminals independently (default value is 7)
7. in each terminal run the command: `scrapy crawl spider$ -s JOBDIR=crawls/spider$` and put the spider number instead of `$` (for example for the first spider to run you shoudl type: `scrapy crawl spider1 -s JOBDIR=crawls/spider1`)

NOTE: since this part could take several hours to several days (depending on the volume of your url_set) this process can be halted at any moment, and the progress is saved as it runs. thus if the program stops for any reason (ctrl+c, unwanted exception, power-cut etc.) the progress is not lost, and by running the exact same command -`scrapy crawl spider$ -s JOBDIR=crawls/spider$`- the program will run from the point it was interrupted.

8. the downloaded content should be in a `downloaded_content` folder
9. run the `text_cleaner.py` to have the final output. (placed in a `raw_text `folder)

have in mind that the text_cleaner.py which i wrote only works correctly on Persian language, and if you wish to use the project for any other, you should implement the 9th step on your own. (or change the code i've written which is not as hard as you might think!)

please fill free to dm me if you come across any problems or questions.
