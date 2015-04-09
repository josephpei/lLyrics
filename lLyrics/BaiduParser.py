# Parser for LYRDB.com

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import urllib.request, urllib.parse, urllib.error
import chardet
from bs4 import BeautifulSoup


class Parser():
    """download lyrics from baidu"""
    def __init__(self, artist, title):
        self.artist = artist
        self.title = title
        self.found = True
        self.lyric_url = None
        self.lyrics = ""
        self.proxy = None

    def request(self):
        url1 = 'http://music.baidu.com/search/lrc?key='
        url2_pre = '%s %s' % (self.title, self.artist)
        url2 = urllib.parse.quote(url2_pre)
        url = url1 + url2

        try:
            #request = urllib.request.Request(url)
            #request.add_header('User-Agent', UA);
            #r = urllib.request.urlopen(request)
            #opener = urllib.request.build_opener()
            #opener.add_headers = [('User-Agent', UA)]
            #content = opener.open(request).read()
            content = urllib.request.urlopen(url).read()
        except IOError:
            return (None, True)
        else:
            lrc_list = []
            soup = BeautifulSoup(content)
            # num = soup.find(attrs={'class': re.compile("number")}).get_text()
            try:
                li = soup.find(name='div', attrs={'class': r"lrc-list"}).find_all('li')
            except:
                return (None, True)
            for i in li:
                try:
                    ti = i.find(attrs={'class': 'song-title'}).get_text().split()[1]
                except:
                    ti = ''
                try:
                    ar = i.find(attrs={'class': 'artist-title'}).get_text().split()[1]
                except:
                    ar = ''
                try:
                    al = i.find(attrs={'class': 'album-title'}).get_text().split()[1]
                except:
                    al = ''
                try:
                    lrc_url = i.find(attrs={'class': 'down-lrc-btn'}).get('class')[2].split("'")[3]
                    lrc_url = "http://music.baidu.com" + lrc_url
                except:
                    lrc_url = ''
                lrc_list.append([ti, ar, al, lrc_url])
        return (lrc_list, False)

    def parse(self):
        (lrcList, flag) = self.request()
        if flag == True or lrcList is None:
            return ""
        else:
            lrcUrl = lrcList[0][3]
            #print(lrcUrl)
            try:
                lyrics = urllib.request.urlopen(lrcUrl).read().decode('utf-8')
            except:
                return ""
            return lyrics
