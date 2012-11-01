#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: engine_baidu.py

import engine, re, urllib
import chardet

class Parser(engine.engine):

    def __init__(self, artist, title):
        engine.engine.__init__(self, proxy = None, locale = "utf-8")
        self.artist = artist
        self.title = title
        self.found = True
        self.lyric_url = None
        self.lyrics = ""
        self.proxy = None


    def parse(self):
        url1 = 'http://music.baidu.com/search/lrc?key='
        url2_pre = '%s %s' % (self.title, self.artist)
        url2 = urllib.quote_plus(url2_pre)
        url = url1 + url2

        try:
            file = urllib.urlopen(url, None, self.proxy)
            source = file.read()
            file.close()
        except IOError:
            return ""
        else:
            match = re.search('down-lrc-btn { \'href\':\'.*?\'', source)
            if match is not None:
                # print match.group()
                lrcUrl = 'http://music.baidu.com' + match.group()[23:-1]
                # print lrcUrl
                lyrics, check = self.downIt(lrcUrl)
                detect_dict = chardet.detect(lyrics)
                confidence, encoding = detect_dict['confidence'], detect_dict['encoding']
                lyrics = lyrics.decode(encoding, 'ignore')
                lyrics = lyrics.encode("utf-8")
                return lyrics
            else:
                return ""
