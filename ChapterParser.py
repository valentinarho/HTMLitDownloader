#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

__author__ = 'valentinarho'

from HTMLParser import HTMLParser
import string
import re, urlparse

# create a subclass and override the handler methods
class ChapterParser(HTMLParser):
    images = []
    chapter = ""

    is_h1 = 0
    is_h3 = 0
    is_p = 0
    is_li = 0
    is_code = 0
    is_strong = 0
    is_in_guide = 0

    def urlEncodeNonAscii(self, b):
        return re.sub('[\x80-\xFF]', lambda c: '%%%02x' % ord(c.group(0)), b)

    def iriToUri(self, iri):
        parts = urlparse.urlparse(iri)
        return urlparse.urlunparse(
            part.encode('idna') if parti == 1 else re.sub('[\x80-\xFF]', lambda c: '%%%02x' % ord(c.group(0)),
                                                          part.encode('utf-8'))
                for parti, part in enumerate(parts)
        )

    def cleanString(self, data):
        #print "\n\nCLEAN: "+data;
        data = data.strip()
        data = string.replace(data, "<", "&lt;")
        data = string.replace(data, ">", "&gt;")
        data = string.replace(data, ">", "&amp;")
        data = string.replace(data, "\"", "\\\"")
        data = string.replace(data, "\'", "\\\'")
        try:
            data = string.replace(data, "″", "\\\'")
        except UnicodeDecodeError:
            pass
        #print "\nCLEANED:"+data;
        return data

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            for name, value in attrs:
                if name == 'class' and value.find('guide-item') != -1:
                    self.is_in_guide = 1
                elif name == 'class' and value.find('responsive-grid') != -1:
                    self.is_in_guide = 0
        elif tag == 'img' and self.is_in_guide:
            for name, value in attrs:
                if name == 'src':
                    self.images.append(value)
                    self.chapter += "![image](" + self.iriToUri(value) + ") \n\n"
        elif tag == 'h1':
            self.is_h1 = 1
            self.chapter += "\n##"
        elif tag == 'h3' and self.is_in_guide:
            self.is_h3 = 1
            self.chapter += "\n##"
        elif (tag == 'p' or tag == 'span') and self.is_in_guide:
            self.is_p = 1
            for name, value in attrs:
                if name == 'class' and value.find('codice') != -1:
                    self.chapter += "<code>"
                    self.is_code = 1;
        elif tag == 'strong' and self.is_in_guide:
            self.is_p = 1
            self.chapter += " "
        elif tag == 'ul' and self.is_in_guide:
            self.chapter += "\n<ul>"
        elif tag == 'li' and self.is_in_guide:
            self.is_li = 1
            self.chapter += "\n<li>"
        elif tag == 'code' and self.is_in_guide:
            self.chapter += "\n<code>"
        elif tag == 'br' and self.is_code:
            self.chapter += " <br> "


    def handle_endtag(self, tag):
        if (tag == 'p') and self.is_in_guide:
            if self.is_code:
                self.is_code = 0
                self.chapter += "</code>"
            self.is_p = 0
            self.chapter += " \n\n"
        elif tag == 'h1':
            self.is_h1 = 0
            self.chapter += "\n"
        elif tag == 'h3':
            self.is_h3 = 0
            self.chapter += "\n"
        elif tag == 'strong' and self.is_in_guide:
            self.chapter += " "
        elif tag == 'ul' and self.is_in_guide:
            self.chapter += "\n</ul>"
        elif tag == 'li' and self.is_in_guide:
            self.is_li = 0
            self.chapter += "\n</li>"
        elif tag == 'code' and self.is_in_guide:
            self.chapter += "</code> "

        pass

    def handle_data(self, data):
        if self.is_h1 or self.is_h3 or self.is_p or self.is_li or self.is_code or self.is_strong:
            # print "\n DATA  " + data
            data = self.cleanString(data)
            self.chapter += " " + data

            #elif self.is_in_guide and ( string.find(data, "“") != -1 or string.find(data, "\"")!= -1 ):
            # ci sono delle virgolette
            #   print "IN DATA"+data

    def handle_entityref(self, ref):
        if self.is_h1 or self.is_h3 or self.is_p or self.is_li or self.is_code or self.is_strong:
            self.chapter += "&"+ref+";";


