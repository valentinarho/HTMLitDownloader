#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

__author__ = 'valentinarho'

import os
import urllib
import string
import re
import chardet
from GuideParser import GuideParser as GuideParser
from ChapterParser import ChapterParser

n_images = 0


def downloadImg(url, img_name):
    global n_images
    n_images += 1
    try:
        opener = urllib.URLopener()
        opener.retrieve(url, img_name)
    except IOError:
        print "IOError downloading image: " + url


def getHTMLPage(url):
    print "Downloading page: " + url

    # open the connection to download the page
    connection = urllib.urlopen(url)
    code = connection.read()
    connection.close()

    return code

# TODO remove function
def preprocessPage(page):
    # replace quotes with a marker
    # reg-expr: >*<?
    # re-replace markers into
    regexpr = re.compile(">.*?<", re.DOTALL);
    print re.sub(regexpr);


if __name__ == '__main__':
    # get the guide first link
    main_url = raw_input("Insert Html.it guide link: ")

    # download first page
    guide_html = getHTMLPage(main_url)

    # get the chapters links
    gparser = GuideParser()
    gparser.feed(guide_html)
    chap_links = gparser.links

    # get the guide name
    guide_name = gparser.title
    guide_name = guide_name.strip()

    # create the folder for the new files
    error = 1;
    dir_name = guide_name.strip()
    dir_name = string.replace(dir_name, " ", "-")

    file_name = dir_name + ".md"

    while (error):
        try:
            os.mkdir(dir_name) #creo una dir
            break
        except OSError:
            # append a number to the folder name
            dir_name += str(error)
            error += 1
        else:
            error = 0

    # change the current directory
    os.chdir("./" + dir_name)

    # print all the links
    # for chap in chap_links:
    #     print chap+"\n";

    f_output = open(file_name, "w")
    f_output.write("#" + guide_name + "\n\n")

    # for each part of the guide
    for chap_url in chap_links:
        try:
            # download page
            chap_html = getHTMLPage(chap_url)

            # TODO preprocessPage(chap_html)

            # parse page
            parser = ChapterParser()
            parser.feed(chap_html)

            # save result in the main file
            chapter_md = parser.chapter

            # write the chapter in the output file
            f_output.write(chapter_md)
        except UnicodeDecodeError:
            chap_html = unicode(chap_html, errors='ignore')
            parser = ChapterParser()
            parser.feed(chap_html)

            # save result in the main file
            chapter_md = parser.chapter

            # write the chapter in the output file
            f_output.write(chapter_md)

            # f_output.write("**[UNICODE ERROR] Saltato url: "+chap_url+"**\n")
            # print "Unicode error: "+chap_url

    # write the end of file
    f_output.write("\n")
    f_output.close()

    print "Generazione documento .md completata."

    # os.system("../md2pdf/md2pdf " + file_name)

    # print "Conversione in pdf completata."

    pass
