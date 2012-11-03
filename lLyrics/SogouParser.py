#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: engine_sogou.py

import engine
import re
import urllib2
import chardet


class Parser(engine.engine):

    def __init__(self, artist, title):
        engine.engine.__init__(self, proxy=None, locale="utf-8")
        self.artist = artist
        self.title = title
        self.found = True
        self.lyric_url = None
        self.lyrics = ""
        self.proxy = None
        self.net_encoder = 'gb18030'

    def changeUrlToGb(self, info):
        address = unicode(info, self.locale).encode('gb18030')
        return address

    def sogouParser(self, a):
        wList = []
        for i in a:
            b = urllib2.unquote(i.split('=')[-1])
            c = unicode(b, 'gb18030').encode('utf8')
            title, artist = c.split('-', 1)
            wList.append([artist, title, i])
        return wList

    def request(self, artist, title):
        url1 = 'http://mp3.sogou.com/lyric.so?query='
        url2_pre = '%s %s' % (self.changeUrlToGb(title), self.changeUrlToGb(artist))
        url2 = urllib2.quote(url2_pre)
        url = url1 + url2

        try:
            f = urllib2.urlopen(url, None, 3)
            lrc_gb = f.read()
            f.close()
        except IOError:
            return (None, True)
        else:
            tmp = unicode(lrc_gb, 'gb18030').encode('utf8')
            tmpList = re.findall('href=\"downlrc\.jsp\?tGroupid=.*?\"', tmp)
            if(len(tmpList) == 0):
                return (None, False)
            else:
                tmpList = map(lambda x: re.sub('href="|"', '', 'http://mp3.sogou.com/' + x), tmpList)
                lrcList = self.sogouParser(tmpList)
                return (lrcList, False)

    def parse(self):
        (lrcList, flag) = self.request(self.artist, self.title)
        if flag == True or lrcList is None:
            return ""
        else:
            lrcUrl = lrcList[0][2]
            print lrcUrl
            lyrics, check = self.downIt(lrcUrl)
            detect_dict = chardet.detect(lyrics)
            try:
                confidence, encoding = detect_dict['confidence'], detect_dict['encoding']
            except:
                encoding = 'gb18030'
            print encoding
            lyrics = lyrics.decode(encoding, 'ignore')
            lyrics = lyrics.encode("utf-8", "replace")
            return lyrics
