#-*-coding:utf-8
import urllib.request
import json
import time
import sys
import requests

class Logger(object):
    def __init__(self,filename = 'Default.log'):
        self.terminal = sys.stdout
        self.log = open(filename,'a')

    def write(self,message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass

def isLive(cid):
    live_api = 'https://api.live.bilibili.com/room/v1/Room/room_init?id={}'.format(cid)
    # print('liveapi:', live_api)
    req = urllib.request.Request(live_api)
    response = urllib.request.urlopen(req)
    data = response.read()
    data = data.decode('utf8')
    js = json.loads(data)
    # print('js', js)
    live = js['data']['live_status']
    # print(live)
    if int(live) == 1:
        print ('is live')
        return 1
    else:
        print ('is not live')
        return 0

def getdownloadurl(cid):
    liveurl_api = 'http://live.bilibili.com/api/playurl?cid={}&otype=json'.format(cid)
    # print('liveinfoapi:', liveurl_api)
    req = urllib.request.Request(liveurl_api)
    response = urllib.request.urlopen(req)
    data = response.read()
    data = data.decode('utf8')
    js = json.loads(data)
    # print('js',js)
    # print(data)
    # print(js)
    file_url = js['durl'][0]['url']
    return file_url

if __name__ == '__main__':
    sys.stdout = Logger('log.txt')
    start = 0
    # input the roomid and cid
    roomid = 16
    cid = 20006
    while(True):
        livestatue = 0
        try:
            livestatue = isLive(roomid)
        except Exception as e:
            print('isLive func')
            print(e)

        if livestatue != 1:
            time.sleep(30)
            continue
        try:
            file_url = getdownloadurl(cid)
        except Exception as e:
            print('getdownurl fuc')
            print(e)

        print(file_url)
        try:
            r = requests.get(file_url, stream=True,timeout = 10)
            print('download start')
            with open("python.flv", "wb") as flv:
                for chunk in r.iter_content():
                    if chunk:
                        flv.write(chunk)
        except Exception as e:
            print(e)



        try :
            r = urllib.request.urlopen(file_url,timeout=10)
            size = 8 * 1024
            start = 1
            t = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time()))
            filename = str(t) + '.flv'
            print(str(t),'started download')
            with open(filename, 'wb') as flv:
                while True:
                    chunk = r.read(size)
                    if not chunk:
                        break
                    flv.write(chunk)
        except Exception as e:
            print(e)
        if start == 1:
            t = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time()))
            print(str(t),'download finished')
            start = 0



