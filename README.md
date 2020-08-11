web-crawler
===========
web crawler and (persian) text extractor\nthe aim of this project is to provide a corpus for Persian (or any other) language.
aside from wikipedia dataset for Persian (or any other) language , it is a good ideato crawl the world wide web in order to extract web page materials , which could latercome in handy, when dealing with problems which require a large data set of raw text.

how to use this project:
-----------------------
in order to create such dataset we go through the folloing steps:
1_ 'we create a list of initial web page URLs which we will strat from'
2_ 'we will extract sublinks form the said initial list (in this project the BFS method has been used)'
3_ "we go through all the extracted URLs and download the contained text in each."
4_ `we go through the downloaded text, and remove unwanted text such as:
html tags, front-end/back-end codes, redundant words, characters and...`
5_ `finally, we save the clean and raw output text for further use.`
