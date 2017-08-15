#!/usr/bin/env python
#-*- coding: utf-8 -*- 
import redis  
from tornado import gen
import tornado
import json
import time
import random
import getdis
from tornado.httpclient import AsyncHTTPClient
from tornado.httputil import url_concat

STORE_PATH="/www/html/fuwa/"
pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=1, password="aaa11bbb22")  
r = redis.Redis(connection_pool=pool)  

HOWFAR = 300
radius = 3000
def Query(longtitude, latitude):

    videos = r.georadius("video_g", longtitude, latitude, radius, unit="m", withdist=True)

    nearfuwas = list()
    for fuwa in near:
        fuwaid, distance = fuwa[0], fuwa[1]
        detail, pos, pic, idd = r.hmget(fuwaid, "detail", "pos", "pic", "id")
        geohash = r.geopos("fuwa_c", fuwaid)
        geo = "%f-%f"%(geohash[0][0], geohash[0][1])

        name, avatar, gender, signature, location, video, owner = r.hmget(fuwaid, "name", "avatar", "gender", "signature", "location", "video", "owner")

        result  = {"gid":fuwaid, "distance":distance, "pos":pos, "id":idd, "geo":geo, "pic":pic, "detail":detail,\
                  "name":name, "avatar":avatar, "gender":gender, "signature":signature, "location":location,\
                  "video":video, "hider": owner}
        nearfuwas.append(result)

    farfuwas = list()
    for fuwa in far:
        if len(farfuwas) >= 300:
            break
        fuwaid, distance = fuwa[0], fuwa[1]
        detail, pos, pic, idd = r.hmget(fuwaid, "detail", "pos", "pic", "id")
        geohash = r.geopos("fuwa_c", fuwaid)
        geo = "%f-%f"%(geohash[0][0], geohash[0][1])

        name, avatar, gender, signature, location, video, owner = r.hmget(fuwaid, "name", "avatar", "gender", "signature", "location", "video", "owner")

        result  = {"distance":distance, "pos":pos, "geo":geo, "pic":pic, "detail":detail,\
                  "name":name, "avatar":avatar, "gender":gender, "signature":signature, "location":location,\
                  "video":video, "hider": owner, "number":1}
        total = len(farfuwas)
        if total == 0:
            farfuwas.append(result)
            continue
        for x in xrange(total):
            if farfuwas[x]['geo'] == geo:
                farfuwas[x]['number'] += 1
                x = total
                break
        if x != total:
            farfuwas.append(result)

    return {"far":farfuwas, "near":nearfuwas}

BASE = "https://api.66boss.com/ucenter/userinfo/info?user_id="

@gen.engine
def getUserinfo(userid, uuid):
    http_client = AsyncHTTPClient()
    http_client.fetch(BASE + userid, callback=on_response, user_agent=uuid)

def on_response(response):
    uuid = response.request.headers['User-Agent']
    data = json.loads(response.body)
    dic = {"name": data['user_name'], "avatar": data['avatar'], "gender": data['sex'],\
          "location":data['district_str'], "signature":data['signature']}
    r.hmset(uuid, dic) 

def HideVideo(owner, longtitude, latitude, pos, detail, video, uuid, redevpnum, redevptotal):

    redevlp = list() 
    amount = float(redevptotal)
    number = int(redevpnum)

    if amount > 0 and number > 0:
        amount = amount *100
        redevlp = [1 for x in xrange(number)]
        remain = amount - number

        for x in xrange(number):
            if remain >= 0:
                howmuch = random.randint(0, remain)
                redevlp[x] += howmuch
                remain -= howmuch
        redevlp[0] += remain
        redevlps = [ round(m/100.0, 2) for m in redevlp]

        for x in redevlps:
            r.sadd(uuid + "_Money", x)

        #params = {"userid": owner, "amount":amount}
        #url = url_concat("http://127.0.0.1:7777/submoney?", params)
        #http_client = AsyncHTTPClient()
        #non = http_client.fetch(url, callback=None)
       
    nows = str(int(time.time()))

    hasmoney = "0"
    if amount > 0:
        hasmoney = "1"

    dic = {"pos":pos, "detail":detail, "video":video, "htime":nows, "uuid":uuid, "hider":owner, "money":hasmoney}
    r.hmset(uuid, dic)
    r.geoadd("video_g", longtitude, latitude, uuid)
    r.sadd(owner+"_pack", uuid

    getUserinfo(owner, uuid)

    return  True

def QueryMy(user):
    outs = list()
    results = r.smembers(user + "_pack")
    for uuid in results:
        out = dict()
        video, pos = r.hmget(uuid, "video", "pos")
        out["video"] = video
        out['pos'] = pos
        outs.append(out)
    return outs

def Huodong(gid):
    detail = r.hget(gid, "detail")
    if detail != None:
        pass
    else:
        detail = ""
    return detail

def Hit(filemd5, classid):
    score = r.zscore("video_" + classid, filemd5)
    if score != None:
        r.zincrby("video_" + classid, filemd5, amount=1)
    return True

def QueryVideo(classid, longtitude, latitude):
    location = (latitude, longtitude)
    filemd5s = r.zrevrange("video_" + classid, 0, 4)
    #filemd5s = [x for x in filemd5s if x != None]
    positions = r.geopos("video_g_" + classid, *filemd5s)
    distances = list()
    for pos in positions:
        dis = getdis.getdistance(location, (pos[1], pos[0]))
        distances.append(dis)
    results = list()
    myresults = list()
    which = 0
    for filemd5 in filemd5s:
        #this moment we can't see repeated
        #if myresults.count(filemd5) > 0:
        #    continue
        temp = dict()
        name, gender, avatar, userid, video, width, height = \
        r.hmget(filemd5, "name", "gender", "avatar", "userid", "video", "width", "height")
        temp['name'] = name
        temp['gender'] = gender
        temp['avatar'] = avatar
        temp['userid'] = userid
        temp['video'] = video
        temp['width'] = width
        temp['height'] = height
        temp['distance'] = distances[which]
        temp['filemd5'] = filemd5
        results.append(temp)
        myresults.append(filemd5)
        which += 1 

    videos = r.georadius("video_g_"+classid, longtitude, latitude, 10000, unit="m", withdist=True, count=100, sort="ASC")
    for video in videos:
        filemd5, far = video[0], video[1]
        if myresults.count(filemd5) > 0:
            continue
        temp = dict()
        name, gender, avatar, userid, video, width, height = \
        r.hmget(filemd5, "name", "gender", "avatar", "userid", "video", "width", "height")
        temp['name'] = name
        temp['gender'] = gender
        temp['avatar'] = avatar
        temp['userid'] = userid
        temp['video'] = video
        temp['width'] = width
        temp['height'] = height
        temp['distance'] = far
        temp['filemd5'] = filemd5
        results.append(temp)
        #myresults.append(filemd5)

    return results

