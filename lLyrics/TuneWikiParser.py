#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: engine_tuneWiki.py 


import hmac, urllib, re, engine


class Parser(engine.engine):
	
	def __init__(self, artist, title):
		engine.engine.__init__(self, proxy = None, locale = "utf-8")
		#self.netEncoder = 'utf8'
		self.email = "none@example.com"
		self.key = "403dc1f0f66afd5d8af5a01d25a17683"
		self.secret = "a2a19880f43095ba22965f0ceaaf3bcc"
		self.artist = artist
		self.title = title
		self.LRC = ""
	
	def decryptTiming(self, t):
		if t == "0":
			return 0
		k = int(t[0])
		t = "".join(reversed(t[1:]))
		t = t[:k] + "".join(reversed(list(t[2*k:])))
		return int(t)/k
	
	def getAuthenticatedUrl(self, url, params):
		m = hmac.new(self.secret)
		a = "".join( ("%s" % i for i in params.values()) )
		m.update(a+self.key)
		apiPass = m.hexdigest()
		
		query = urllib.urlencode(params)
		if params:
			query += "&"
		query += "apiKey=%s&apiPass=%s" % (self.key, apiPass)
		return "%s?%s" % (url, query)
	
	def request(self, artist, title, album=""):
		params = {
			"title" : title,
			"album" : album,
			"artist" : artist,
			"device" : 2002,
			"ver" : 0,
			"user" : self.email
		}
		url = "http://lyrics.tunewiki.com/tunewiki/services/getLyric"
		url = self.getAuthenticatedUrl(url, params)
		try:
			f = urllib.urlopen(url)
			xml = f.read()
			f.close()
		except:
			return (None,True)
		else:
			ret_title = re.findall(r'<title( id="\d+")?>(.*?)</title>',xml,re.DOTALL)
			ret_title = '' if not ret_title else ret_title[0][1]
			ret_album = re.findall(r'<album( id="\d+")?>(.*?)</album>',xml,re.DOTALL)
			ret_album = '' if not ret_album else ret_album[0][1]
			ret_artist = re.findall(r'<artist( id="\d+")?>(.*?)</artist>',xml,re.DOTALL)
			ret_artist = '' if not ret_artist else ret_artist[0][1]
			xml = re.findall(r'<lyric>(.*?)</lyric>',xml,re.DOTALL)
			xml = xml[0]
			if xml.strip() != '':
				lines = re.findall(r'<line timing="(\d+)">(.*?)</line>',xml,re.DOTALL)
				self.LRC += "[ar:%s]\r\n" % ret_artist
				self.LRC += "[al:%s]\r\n" % ret_album
				self.LRC += "[ti:%s]\r\n" % ret_title
				for timing, text in lines:
					ms = self.decryptTiming(timing)
					sec, ms = divmod(ms,1000)
					min, sec = divmod(sec,60)
					ms = ("%d" % ms).zfill(3)
					sec = ("%d" % sec).zfill(2)
					min = ("%d" % min).zfill(2)
					self.LRC += "[%s:%s.%s]%s\r\n" % (min,sec,ms,text)
				return([[ret_artist, ret_title, None]], False)
			else:
				return (None, False)
	
	def parse(self):
		self.request(self.artist, self.title)
		return self.LRC

	def downIt(self, url):
		return self.LRC, False