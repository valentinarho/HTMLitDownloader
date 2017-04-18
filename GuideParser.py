#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

__author__ = 'valentinarho'

from HTMLParser import HTMLParser
import re

# create a subclass and override the handler methods
class GuideParser(HTMLParser):
    title = ""
    links = []

    is_header = 0
    is_title = 0

    lesson_counter = -1

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            for name, value in attrs:
                if name == 'class' and value == 'article-header-item':
                    self.is_header = 1

        elif tag == 'h1' and self.is_header:
            self.is_title = 1
            self.lesson_counter = 1

        elif tag == 'a' and self.lesson_counter > 0:
            get_href = 0
            for name, value in attrs:
                if name == 'id' and re.match(r'lesson[0-9]+', value) is not None:
                    get_href = 1;
                elif name == 'href' and get_href:
                    self.links.append(value);
                    self.lesson_counter += 1
        else:
            return

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        if self.is_title:
            self.title = data;
            self.is_title = 0
        else:
            return

