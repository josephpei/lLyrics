#!/usr/bin/python
# -*- coding: utf-8 -*-


import urllib, re, os, sys


def parse_lrc(data):
    tag_regex = "(\[\d+\:\d+\.\d*])"
    match = re.search(tag_regex, data)

    # no tags
    if match is None:
        return (data, None)

    data = data[match.start():]
    splitted = re.split(tag_regex, data)[1:]

    tags = []
    lyrics = ''
    for i in range(len(splitted)):
        if i % 2 == 0:
            # tag
            tags.append((time_to_seconds(splitted[i]), splitted[i+1]))
        else:
            # lyrics
            lyrics += splitted[i]

    return (lyrics, tags)


def time_to_seconds(time):
    time = time[1:-1].replace(":", ".")
    t = time.split(".")
    return 60 * int(t[0]) + int(t[1])


def order_results(results, artist, title):
    comp = [artist, title]
    results = map(lambda x: x[1], reversed(sorted(((cmp_result(comp, i), i) for i in results))))
    return results


def cmp_result(result, comp):
    value = similarity(result[0],comp[0])    #artist
    value += similarity(result[1],comp[1])    #title
    value = value / 2
    return value


def similarity(string1, string2):
    if string1.lower() == string2.lower():
        return 1
    string1 = tokenize(string1.lower())
    string2 = tokenize(string2.lower())
    count = len(tuple((i for i in string1 if i in string2)))
    return float(count) / max((len(string2), 1))


def tokenize(string):
    string = tuple((i.lower() for i in re.findall("\w+", string) if i.lower() not in ('a', 'an', 'the')))
    return string


def valid_lrc(lrc):
    partial = "".join( (i for i in lrc if(ord(i) < 128 and ord(i) != 0)))
    return bool(re.search('\[\d+:\d+.*?\]', partial))


class engine:

    def __init__(self, proxy = None, locale = "utf-8", check = True):
        if locale == None:
            locale = "utf-8"
        self.locale = locale
        self.proxy = proxy
        self.net_encoder = None
        self.need_check = check

    def request(self, artist, title):
        raise NotImplementedError('request must be implemented in subclass')

    def downIt(self, url):
        try:
            ff = urllib.urlopen(url, None, self.proxy)
            original_lrc = re.sub('<br/>', '\n', ff.read())
            ff.close()
        except IOError:
            return (None, True)
        else:
            if(self.need_check):
                if(self.net_encoder == None or self.net_encoder.startswith("utf-16") or self.net_encoder.startswith("utf-32")):
                    if not self.valid_lrc(original_lrc):
                        original_lrc = None
                    elif(not re.search('\[\d+:\d+.*?\]', original_lrc)):
                        original_lrc = None
            return (original_lrc, False)

    def order_results(self,results, artist, title):
        return order_results(results, artist, title)

    def valid_lrc(self, lrc):
        return valid_lrc(lrc)
