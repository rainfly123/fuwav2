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
pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0, password="aaa11bbb22")  
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
def getUserinfo(self, userid, uuid):
    http_client = AsyncHTTPClient()
    http_client.fetch(BASE + userid, callback=on_response, user_agent=uuid)

def on_response(self, response):
    uuid = response.request.headers['User-Agent']
    data = json.loads(response.body)
    dic = {"name": data['user_name'], "avatar": data['avatar'], "gender": data['sex'],\
          "location":data['district_str'], "signature":data['signature']}
    r.hmset(uuid, dic) 

def HideVideo(owner, longtitude, latitude, pos, detail, video, uuid, redevpnum, redevptotal)

    redevlp = list() 
    amount = float(redevptotal)
    number = int(redevpnum)

    if amount > 0 and number > 0:
        redevlp = [0.01 for x in xrange(number)]
        remain = amount - 0.01 * number

        for x in xrange(number):
            if remain >= 0:
                howmuch = round(random.uniform(0, remain), 2)
                redevlp[x] += howmuch
                remain -= howmuch
        redevlp[0] += remain
       
    nows = str(int(time.time()))

    hasmoney = "0"
    if amount > 0:
        hasmoney = "1"
        params = {"userid": owner, "amount":amount}
        url = url_concat("http://127.0.0.1:7777/submoney?", params)
        http_client = AsyncHTTPClient()
        non = http_client.fetch(url, callback=None)

    dic = {"pos":pos, "detail":detail, "video":video, "htime":nows, "uuid":uuid, "hider":owner, "money":hasmoney}
    r.geoadd("video_g", longtitude, latitude, uuid)
    r.hmset(uuid, dic)
    getUserinfo(owner, uuid)

    return  True

def CaptureFuwa(pic, user, gid):
    import os
    import imgcmp

    filename = os.path.basename(pic)
    fullpath = os.path.join(STORE_PATH, filename)
    clue = r.hget(gid, "pic") 
    filenamec = os.path.basename(clue)
    fullpathc = os.path.join(STORE_PATH, filenamec)
    ok = imgcmp.ImgCmp(fullpathc, fullpath)
    if ok < 45:
        return False

    pipe = r.pipeline()
    pipe.hset(gid, "owner", user)
    pipe.sadd(user + "_pack", gid)
    if gid.find('c') > 0:
        pipe.zrem("fuwa_c", gid)
    else:
        pipe.zrem("fuwa_i", gid)
    pipe.execute()
    return True

def Capturev2Fuwa(user, gid):
    ###limit captues number

    limit = r.hget(user+"_lmt", "total")
    if limit != None and int(limit) >= 10:
        return False

    creator = r.hget(gid, "creator")
    limit = r.hget(user+"_lmt", creator)
    if limit != None and int(limit) >= 3:
        return False

    val = 0
    if gid.find('c') > 0:
        val = r.zrem("fuwa_c", gid)
        r.zrem("fuwa_c_"+creator, gid)
    else:
        val = r.zrem("fuwa_i", gid)
        r.zrem("fuwa_i_"+creator, gid)

    if val == 0 :
        return False

    r.hset(gid, "owner", user)
    r.sadd(user + "_pack", gid)

    filemd5, classid = r.hmget(gid, "filemd5", "classid")
    if filemd5 != None:
        usedby = r.hincrby(filemd5, "usedby", amount=-1)
        if usedby <= 0:
            r.zrem("video_g_" + classid, filemd5)
            r.zrem("video_" + classid, filemd5)

    r.hincrby(user+"_lmt", "total", amount=1)
    r.hincrby(user+"_lmt", creator, amount=1)

    return True

def QueryMy(user):
    outs = list()
    
    results = r.smembers(user + "_pack")
    for gid in results:
        out = dict()
        creator, name, pos, awarded, idd = r.hmget(gid, "creator", "name", "pos", "awarded", "id")
        out['creatorid'] = creator 
        out['creator'] = name 
        out['pos'] = pos
        out["gid"] = gid
        out["id"] = idd
        if awarded is '0':
            out['awarded'] = False
        else:
            out['awarded'] = True
        outs.append(out)
    return outs

def QueryMyApply(user):
    outs = list()

    results = r.smembers(user + "_apply")
    for gid in results:
        creator, idd = r.hmget(gid, "name", "id")
        out = {'creator':creator, "gid":gid, "id":idd}
        outs.append(out)
    return outs

def QueryMyfortop(user):
    outs = dict()
    fuwas = list()
    results = r.smembers(user + "_pack")
    for gid in results:
        idd = r.hget(gid, "id")
        if outs.has_key(idd):
            outs[idd] += 1
        else:
            outs[idd] = 1

    for key in sorted(outs.keys(), key=lambda x:int(x)):
        fuwa = dict()
        fuwa['id'] = key
        fuwa['number'] = outs[key]
        fuwas.append(fuwa)

    return fuwas

def QueryDetail(gid):
    outs = dict()

    creator, pos, awarded = r.hmget(gid, "name", "pos", "awarded")

    outs['creator'] = creator
    outs['pos'] = pos
    if awarded is '0':
        outs['awarded'] = False
    else:
        outs['awarded'] = True
    
    return outs

def Donate(touser, gid, fromuser):
    if len(touser) != 9:
        return 1
    outs = dict()
    i=r.srem(fromuser + "_pack", gid)
    if i == 0:
        return 1
    r.sadd(touser + "_pack", gid)
    r.hset(gid, "owner", touser)
    params = {"owner": touser, "buyer":fromuser}
    url = url_concat("http://127.0.0.1:2688/donatemsg?", params)
    http_client = AsyncHTTPClient()
    non = http_client.fetch(url, callback=None)
    return 0

MES1 = u"你不是福娃的生成者"
MES2 = u"此福娃已兑奖"
MES0 = u"成功"

def Award(user, gid):
    creator, awarded = r.hmget(gid, "creator", "awarded")
    if creator != user:
        return 1, MES1

    if awarded is '1':
        return 2, MES2

    r.hset(gid, "awarded", "1")
    return 0, MES0

def Huodong(gid):
    detail = r.hget(gid, "detail")
    if detail != None:
        pass
    else:
        detail = ""
    return detail

aclass =[{"name":"美食", "classid":"1"}, {"name":"服饰", "classid":"2"}, {"name":"生活", "classid":"3"},\
        {"name":"服务", "classid":"4"}, {"name":"综合", "classid":"5"}]

def Class():
    return aclass

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

def QueryStrVideo(longtitude, latitude):
    location = (latitude, longtitude)
    filemd5s = r.zrevrange("video_i", 0, 4)
    #filemd5s = [x for x in filemd5s if x != None]
    positions = r.geopos("video_g_i", *filemd5s)
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

    videos = r.georadius("video_g_i", longtitude, latitude, 10000, unit="m", withdist=True, count=100, sort="ASC")
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

def APP(longtitude, latitude, radius):
    fuwas = r.georadius("fuwa_c", longtitude, latitude, int(radius), unit="m", withdist=True)
    near = [x for x in fuwas if x[1] <= HOWFAR]
    near = sorted(near, key=lambda x: int(x[0][7:]), reverse=True)
    near = near[:100]
    total = 1
    nearfuwas = list()
    for fuwa in near:
        fuwaid = fuwa[0]
        geohash = r.geopos("fuwa_c", fuwaid)
        result = dict()
        result['id'] = total
        total += 1
        result['longitude'] = geohash[0][0]
        result['latitude'] = geohash[0][1]
        result['width'] = 33
        result['height'] = 50
        result['iconPath'] = "/images/fuwa_local.png"
        nearfuwas.append(result)

    return {"far":[], "near":nearfuwas}

#print QueryMyApply("100000076")
#print QueryMy("100000320")
#print CaptureFuwa("http://afa/daf/pic.jpg", "john", "fuwa_1")
#print QueryStrFuwaNew(113.3, 23.09 , 9000, "0")
