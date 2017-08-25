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

radius = 3000
def Query(longtitude, latitude):

    videos = r.georadius("video_g", longtitude, latitude, radius, unit="m", withdist=True , count=100, sort="ASC")

    videosinfo = list()
    for video in videos:
        md5, distance = video[0], video[1]
        geohash = r.geopos("video_g", md5)
        geo = "%f-%f"%(geohash[0][0], geohash[0][1])

        money = r.hget(md5,"money")
        result  = {"uuid":md5, "distance":distance, "geo":geo, "money":money}

        videosinfo.append(result)

    return  videosinfo

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
            r.lpush(uuid + "_Money", x)

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
    r.sadd(owner+"_pack", uuid)

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
        out['uuid'] = uuid
        outs.append(out)
    return outs

def Huodong(gid):
    hider, gender, avatar, detail, name = r.hmget(gid, "hider", "gender", "avatar",\
                                                  "detail", "name")
    if detail == None:
        detail = ""
    return {"hider":hider, "gender":gender, "avatar":avatar, "name":name, "detail":detail}

def Info(gid):
    video, money, width, height = r.hmget(gid, "video", "money", "width", "height")
    return {"video":video, "money":money, "width":width, "height": height }


def Hit(filemd5, classid):
    score = r.zscore("video_" + classid, filemd5)
    if score != None:
        r.zincrby("video_" + classid, filemd5, amount=1)
    return True

def QueryVideo(longtitude, latitude):

    videos = r.georadius("video_g", longtitude, latitude, radius, unit="m", withdist=True , count=100, sort="ASC")

    videosinfo = list()
    for video in videos:
        md5, distance = video[0], video[1]

        pos, name, avatar, gender, signature, location, video, hider, money, width, height  =\
        r.hmget(md5, "pos", "name", "avatar", "gender", "signature", "location",\
               "video", "hider", "money", "width", "height")

        result = {"uuid":md5, "distance":distance, "pos":pos, "name":name, "avatar":avatar, \
                  "gender":gender, "signature":signature, "location":location, "video":video,\
                  "hider": hider, "money":money, "width":width, "height":height}

        videosinfo.append(result)

    return  videosinfo

#open red evelop
def Openredevp(userid, uuid):
    money = r.hget(uuid, "money")
    if money == '1':
        howmany = r.lpop(uuid + "_Money")
        if howmany != None:
            pass
    else:
        couponid = r.lpop(uuid + "_Coupon")
        if couponid != None:
            r.sadd(useid+"_coupon", couponid)

