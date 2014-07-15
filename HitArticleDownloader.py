# -*- coding: iso-8859-15 -*-
__author__ = 'valentinarho'

# TODO NON FUNZIONA
# bisogna creare un ArticleParser da usare al posto di
# ChapterParser perchè l'html dei capitoli delle guide è diverso da quello degli articoli

import os
import HTMLitDownloader
from ChapterParser import ChapterParser

if __name__ == '__main__':
    # get the guide first link
    main_url = raw_input("Insert Html.it page link: ")
    titolo = raw_input("Insert Html.it page title: ")

    # create the folder for the new files
    error = 1;

    file_name = titolo + ".md"

    while (error):
        try:
            os.mkdir(titolo) #creo una dir
            break
        except OSError:
            # append a number to the folder name
            titolo += str(error)
            error += 1
        else:
            error = 0

    # change the current directory
    os.chdir("./" + titolo)

    # print all the links
    # for chap in chap_links:
    #     print chap+"\n";

    f_output = open(file_name, "w")
    f_output.write("#" + titolo + "\n\n")

    try:
        # download page
        chap_html = HTMLitDownloader.getHTMLPage(main_url)

        # TODO preprocessPage(chap_html)

        # parse page
        parser = ChapterParser()
        parser.feed(chap_html)

        # save result in the main file
        chapter_md = parser.chapter

        # write the chapter in the output file
        f_output.write(chapter_md)
    except UnicodeDecodeError:
        f_output.write("**[UNICODE ERROR] Saltato url: "+main_url+"**\n")
        print "Unicode error: "+main_url

    # write the end of file
    f_output.write("\n")
    f_output.close()

    print "Generazione documento .md completata."

    # os.system("../md2pdf/md2pdf " + file_name)

    # print "Conversione in pdf completata."

    pass


