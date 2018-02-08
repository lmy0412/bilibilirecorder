#-*-coding:utf-8
# # api:http://live.bilibili.com/api/playurl?cid=44221&otype=json
import urllib.request
import json
import time


def isLive(cid):
    live_api = 'http://live.bilibili.com/bili/getRoomInfo/{}'.format(cid)
    # print('liveapi:', live_api)
    req = urllib.request.Request(live_api)
    response = urllib.request.urlopen(req)
    data = response.read()
    data = data.decode('utf8')
    pos = data.find('roomStatus')
    data = data[pos:]
    pos = data.find(':')
    live = (data[pos+1])
    # print(live)
    if int(live) == 1:
        print ('is not live')
        return 0
    else:
        print ('is live')
        return 1

def getdownloadurl(cid):
    liveurl_api = 'http://live.bilibili.com/api/playurl?cid={}&otype=json'.format(cid)
    # print('liveinfoapi:', liveurl_api)
    data = urllib.request.Request(liveurl_api)
    req = urllib.request.Request(liveurl_api)
    response = urllib.request.urlopen(req)
    data = response.read()
    data = data.decode('utf8')
    js = json.loads(data)
    # print(data)
    # print(js)
    file_url = js['durl'][0]['url']
    print(file_url)
    return file_url

if __name__ == '__main__':
    cid = 5440  #test
    while(True):
        livestatue = 0
        try:
            livestatue = isLive(cid)
        except Exception as e:
            print('isLive func')
            print(e)

        if livestatue == 0:
            time.sleep(10)
            continue
        try:
            file_url = getdownloadurl(cid)
        except Exception as e:
            print('getdownurl fuc')
            print(e)

        import requests
        # r = requests.get(file_url, stream=True)
        # print('download start')
        # with open("python.flv", "wb") as flv:
        #     for chunk in r.iter_content():
        #         if chunk:
        #             flv.write(chunk)
        try :
            r = urllib.request.urlopen(file_url,timeout=10)
            chunk = 8 * 1024
            start = time.time()
            t = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time()))
            filename = str(t) + '.flv'
            with open(filename, 'wb') as flv:
                while True:
                    chunk = r.read(chunk)
                    if not chunk:
                        break
                    flv.write(chunk)
        except Exception as e:
            print(e)
        print('download finished')
        try :
            print('duration', time.time() - start)
        except Exception as e:
            print(e)




