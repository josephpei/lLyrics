# Parser for kuwo.cn

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

import time
import socket
import re
import zlib
import base64
from urllib import request, parse


class Parser():

    def __init__(self, artist, title):
        self.artist = artist
        self.title = title

    def parse(self):
        try:
            url = ''.join([
                'http://search.kuwo.cn/r.s?ft=music&rn=1', '&newsearch=1&primitive=0&cluster=0&itemset=newkm&rformat=xml&encoding=utf8&artist=', 
                Parser.parse_quote(self.artist),
                '&all=',
                Parser.parse_quote(self.title),
                '&pn=0'
            ])
            reqContent = Parser.url_open(url)
            songs, hit = Parser.parse_songs_wrap(reqContent)
            if hit == 0 or not songs:
                return None
            musicId = songs[0][3]
            if not musicId:
                return None
            lrcContent = Parser.get_lrc_from_musicid(musicId)
            return lrcContent if lrcContent else None
        except:
            return None

    def get_lrc_from_musicid(musicId):
        url = ('http://newlyric.kuwo.cn/newlyric.lrc?' +
            Parser.encode_lrc_url(musicId))
        try:
            req = request.urlopen(url)
            if req.status != 200 or req.reason != 'OK':
                return None
            reqContent = req.read()
        except:
            return None
        if not reqContent:
            return None
        try:
            lrcContent = Parser.decode_lrc_content(reqContent)
            return lrcContent if lrcContent else None
        except:
            return None

    def parse_songs_wrap(str):
        hit = int(re.search('Hit\=(\d+)', str).group(1))
        songs_wrap = []
        str_list = str.split('\r\n\r\n')
        for i in range(1, 16):
            if str_list[i]:
                song_list = str_list[i].split('\r\n')
                songname = song_list[0][9:]
                artist = song_list[1][7:]
                album = song_list[2][6:]
                music_id = song_list[6][15:]
                score = song_list[18][9:]
                songs_wrap.append([songname, artist, album, music_id, score])
                continue
            break
        return songs_wrap, hit

    def parse_quote(str):
        return parse.quote(str, safe='~@#$&()*!+=:;,.?/\'')

    def url_open(url, retries=4):
        socket.setdefaulttimeout(3)
        while retries:
            try:
                req = request.urlopen(url, timeout=3)
                req = req.read()
                reqContent = req.decode()
                reqContent = reqContent.lstrip()
                return reqContent
            except:
                retries -= 1
                time.sleep(0.05)
                continue
        return None

    def encode_lrc_url(musicId):
        param = ('user=12345,web,web,web&requester=localhost&req=1&rid=MUSIC_%s' % musicId)
        str_bytes = Parser.xor_bytes(param.encode())
        output = base64.encodebytes(str_bytes).decode()
        return output.replace('\n', '')

    def decode_lrc_content(lrc, is_lrcx=False):
        if lrc[:10] != b'tp=content':
            return None
        index = lrc.index(b'\r\n\r\n')
        lrc_bytes = lrc[index+4:]
        str_lrc = zlib.decompress(lrc_bytes)
        print(str_lrc)
        if not is_lrcx:
            # print(str_lrc.decode('gb18030'))
            return str_lrc.decode('gb18030')
        str_bytes = base64.decodebytes(str_lrc)
        return Parser.xor_bytes(str_bytes).decode('gb18030')

    def xor_bytes(str_bytes, key='yeelion'):
        xor_bytes = key.encode('utf8')
        str_len = len(str_bytes)
        xor_len = len(xor_bytes)
        output = bytearray(str_len)
        i = 0
        while i < str_len:
            j = 0
            while j < xor_len and i < str_len:
                output[i] = str_bytes[i] ^ xor_bytes[j]
                i += 1
                j += 1
        return output
