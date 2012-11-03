#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: engine_ttPlayer.py

from ttpClient import ttpClient
import engine
import re
import random
import urllib2
import chardet


class Parser(engine.engine):

    def __init__(self, artist, title):
        engine.engine.__init__(self, proxy=None, locale="utf-8")
        self.proxy = None
        self.netEncoder = 'utf8'
        self.artist = artist
        self.title = title
        t = 'ctc'
        #t = self.conf.get('engine', 'ttplayer_network')
        if(t == 'ctc'):
            self.network = 'http://ttlrcct.qianqian'
        else:
            self.network = 'http://ttlrccnc.qianqian'

    def ttplayerParser(self, a):
        b = []
        for i in a:
            c = re.search('id=\"(.*?)\" artist=\"(.*?)\" title=\"(.*?)\"', i)
            try:
                _artist = c.group(2)
                _title = c.group(3)
                _id = c.group(1)
                entities = {'&apos;': '\'', '&quot;': '"', '&gt;': '>', '&lt;': '<', '&amp;': '&'}
                for ii in entities:
                    _artist = _artist.replace(ii, entities[ii])
                    _title = _title.replace(ii, entities[ii])
                    _id = _id.replace(ii, entities[ii])
            except:
                pass
            else:
                url = '%s.com/dll/lyricsvr.dll?dl?Id=%d&Code=%d&uid=01&mac=%012x' % (self.network, int(_id), ttpClient.CodeFunc(int(_id), (_artist + _title)), random.randint(0, 0xFFFFFFFFFFFF))
                b.append([_artist, _title, url])
        return b

    def request(self, artist, title):
        url = '%s.com/dll/lyricsvr.dll?sh?Artist=%s&Title=%s&Flags=0' % (self.network, ttpClient.EncodeArtTit(unicode(artist, self.locale).replace(u' ', '').lower()), ttpClient.EncodeArtTit(unicode(title, self.locale).replace(u' ', '').lower()))
        #print url
        try:
            file = urllib2.urlopen(url, None, 3)
            webInfo = file.read()
            file.close()
        except IOError:
            return (None, True)
        else:
            tmpList = re.findall(r'<lrc.*?</lrc>', webInfo)
            if(len(tmpList) == 0):
                return (None, False)
            else:
                lrcList = self.ttplayerParser(tmpList)  # here lrcList must be the format like [[artist,title,url].....]
                return (lrcList, False)

    def parse(self):
        lrclist, check1 = self.request(self.artist, self.title)
        if lrclist is not None:
            lyrics, check2 = self.downIt(lrclist[0][2])
            detect_dict = chardet.detect(lyrics)
            confidence, encoding = detect_dict['confidence'], detect_dict['encoding']
            lyrics = lyrics.decode(encoding, 'ignore')
            lyrics = lyrics.encode("utf-8", "replace")
            return lyrics
