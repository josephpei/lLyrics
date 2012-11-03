#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: lrcParser.py


import re


def parse_lrc(data):
    offset = 0
    offsetList = re.search('\[offset:(.*?)\]', data)
    if(offsetList):
        try:
            offset = int(offsetList.group(1) / 1000)
        except:
            offset = 0
    else:
        offset = 0

    origin = re.findall('\[\d+:\d+.*?\n|\[\d+:\d+.*?$', data)
    if origin is None:
        return (data, None)

    splitted = []
    for i in origin:
        line_text = i.split(']')[-1]
        for j in re.findall('\[\d+:\d+.*?\]', i):
            splitted.append(j)
            splitted.append(line_text)

    dd = {}
    lyrics = ''
    for i in range(len(splitted)):
        if i % 2 == 0:
            dd[time_to_seconds(splitted[i], offset)] = splitted[i + 1]

    tags = sorted(dd.items(), key=lambda d: d[0])
    for k, v in tags:
        lyrics += v
    return (lyrics, tags)


def time_to_seconds(time, offset):
    time = time[1:-1].replace(":", ".")
    t = time.split(".")
    return 60 * int(t[0]) + int(t[1]) + offset


class lrcParser:
    def __init__(self, string):
        self.string = string
        self.offset = 0
        self.lrc_type = 'text'

    def format(self):
        offsetList = re.search('\[offset:(.*?)\]', self.string)
        if(offsetList):
            try:
                self.offset = int(offsetList.group(1))
            except:
                self.offset = 0
        else:
            self.offset = 0
        origin = re.findall('\[\d+:\d+.*?\n|\[\d+:\d+.*?$', self.string)

        if len(origin) == 0:
            self.lrc_type = "text"
            time_tag = []
            return (time_tag, self.string)
        else:
            self.lrc_type = "lrc"
            text1 = []
            for i in origin:
                line_text = i.split(']')[-1]
                for j in re.findall('\[\d+:\d+.*?\]', i):
                    text1.append(j + line_text)
            text2 = []
            for k in text1:
                pp = k.split(']')[0][1:]  # time tag, no ']' or '['
                qq = k.split(']')[1].strip()  # line of lyrics
                qq = re.sub('<|>', '', qq)

                searchGroup = re.search('(\d+):(\d+)(.*)', pp)
                a1 = int(searchGroup.group(1)) * 60000
                a2 = int(searchGroup.group(2)) * 1000
                try:
                    tmp = searchGroup.group(3)[1:]
                    a3 = int(tmp) * 10 ** (3 - len(tmp))
                except:
                    a3 = 0

                ms = str(a1 + a2 + a3 - self.offset + 10000000) + '$#$#' + qq
                text2.append(ms)
            text2.sort()

            tag = []
            context = []
            for e in text2:
                tag.append(int(e.split('$#$#')[0]) - 10000000)
                context.append(e.split('$#$#')[1])

            ########## filter lyrics function  #########

            # if(enableFilter == 'yes'):
            #     cloneContext = context[:]
            #     lineIndex = -1
            #     #expre = unicode(filterRule, 'utf8')
            #     if(abCase == 'yes'):
            #         reRule = re.compile(filterRule, re.I)
            #     else:
            #         reRule = re.compile(filterRule)

            #     for l in cloneContext:
            #         lineIndex += 1
            #         if(reRule.search(l)):
            #             del tag[lineIndex]
            #             del context[lineIndex]
            #             lineIndex -= 1

            lrcFile = ''
            for g in context:
                lrcFile = lrcFile + g + '\n'
            return (tag, lrcFile)
