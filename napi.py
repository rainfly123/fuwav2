#!/usr/bin/env python
#-*- coding:utf-8 -*- 
import os
import tornado
import tornado.ioloop
import tornado.web
import datetime
from tornado.httputil import url_concat
from tornado.httpclient import AsyncHTTPClient
import tornado.web
import tornado.gen
import urllib
import string
import random
import json
import redi
import hashlib
import base64
import time

ACCESS_PATH = "http://wsim.66boss.com/fuwa/"
STORE_PATH="/www/html/fuwa/"

class Queryv2Handler(tornado.web.RequestHandler):
    def get(self):
        resp = dict() 

        geohash = self.get_argument("geohash", strip=True)
        radius = self.get_argument("radius", strip=True)
        biggest = self.get_argument("biggest", strip=True)
        geo = geohash.split('-')
        if len(geo) != 2 or len(radius) < 1:
            resp['code'] =  1
            resp['message'] = "Parameter Error" 
            self.write(json.dumps(resp))
            return
        
        longitude, latitude = geo[0], geo[1] 
        resp['code'] =  0
        resp['message'] = "OK" 
        resp['data'] = redi.QueryFuwaNew(longitude, latitude, radius, biggest)
        self.write(json.dumps(resp))

class Queryv3Handler(tornado.web.RequestHandler):
    def get(self):
        resp = dict() 

        geohash = self.get_argument("geohash", strip=True)
        radius = self.get_argument("radius", strip=True)
        biggest = self.get_argument("biggest", strip=True)
        userid = self.get_argument("userid", strip=True)
        geo = geohash.split('-')
        if len(geo) != 2 or len(radius) < 1:
            resp['code'] =  1
            resp['message'] = "Parameter Error" 
            self.write(json.dumps(resp))
            return
        
        longitude, latitude = geo[0], geo[1] 
        resp['code'] =  0
        resp['message'] = "OK" 
        resp['data'] = redi.QueryFuwav3(longitude, latitude, radius, biggest, userid)
        self.write(json.dumps(resp))

class QueryStrangerv2Handler(tornado.web.RequestHandler):
    def get(self):
        resp = dict() 

        geohash = self.get_argument("geohash", strip=True)
        radius = self.get_argument("radius", strip=True)
        biggest = self.get_argument("biggest", strip=True)
        geo = geohash.split('-')
        if len(geo) != 2 or len(radius) < 1:
            resp['code'] =  1
            resp['message'] = "Parameter Error" 
            self.write(json.dumps(resp))
            return
        
        longitude, latitude = geo[0], geo[1] 
        resp['code'] =  0
        resp['message'] = "OK" 
        resp['data'] = redi.QueryStrFuwaNew(longitude, latitude, radius, biggest)
        self.write(json.dumps(resp))

class QueryStrangerv3Handler(tornado.web.RequestHandler):
    def get(self):
        resp = dict() 

        geohash = self.get_argument("geohash", strip=True)
        radius = self.get_argument("radius", strip=True)
        biggest = self.get_argument("biggest", strip=True)
        userid = self.get_argument("userid", strip=True)
        geo = geohash.split('-')
        if len(geo) != 2 or len(radius) < 1:
            resp['code'] =  1
            resp['message'] = "Parameter Error" 
            self.write(json.dumps(resp))
            return
        
        longitude, latitude = geo[0], geo[1] 
        resp['code'] =  0
        resp['message'] = "OK" 
        resp['data'] = redi.QueryStrFuwav3(longitude, latitude, radius, biggest, userid)
        self.write(json.dumps(resp))


def getFileName():
    source = list(string.lowercase) 
    random.shuffle(source)
    temp = source[:15]
    return "".join(temp)

class Hidev2Handler(tornado.web.RequestHandler):
    def myget(self, pic, video, filemd5):
        resp = dict()
        pos = self.get_argument("pos", strip=True)
        geohash = self.get_argument("geohash", strip=True)
        owner = self.get_argument("owner", strip=True)
        detail = self.get_argument("detail", strip=True)
        number = self.get_argument("number", strip=True)
        purpose = self.get_argument("type", default='1', strip=True)
        classid = self.get_argument("class", default='i', strip=True)
        videogeo = "video_g_" + classid
        geo = geohash.split('-')
        if len(geo) != 2 or len(number) < 1:
            resp['code'] =  1
            resp['message'] = "Parameter Error" 
            self.write(json.dumps(resp))
            return
        
        longtitude, latitude = geo[0], geo[1] 
        users = redi.HideFuwaNew(longtitude, latitude, pos, pic, owner, detail, video, int(number), purpose, videogeo, filemd5, \
                        classid)
        resp['code'] =  0
        resp['message'] = "Ok" 
        resp['data'] =  users
        self.write(json.dumps(resp))

    def post(self):
        pic = str()
        video = str()
        filemd5 = str()

        file_metas = self.request.files['file']   
        for meta in file_metas:
            suffix = os.path.splitext(meta['filename'])[1]
            filename = getFileName() + suffix
            filepath = os.path.join(STORE_PATH, filename)
            with open(filepath,'wb') as up:
                up.write(meta['body'])
            pic = ACCESS_PATH + filename

        if self.request.files.has_key('video'):
            video_metas = self.request.files['video']   
            for meta in video_metas:
                temppath = os.path.join(STORE_PATH, getFileName())
                with open(temppath, 'wb') as up:
                    up.write(meta['body'])

                sign = hashlib.md5()
                sign.update(meta['body'])
                filemd5 = sign.hexdigest()

                suffix = os.path.splitext(meta['filename'])[1]
                filename = filemd5 + suffix
                filepath = os.path.join(STORE_PATH, filename)

                os.rename(temppath, filepath)
                video = ACCESS_PATH + filename

        self.myget(pic, video, filemd5)

class QuerymyHandler(tornado.web.RequestHandler):
    def get(self):
        resp = dict()
        user = self.get_argument("user", strip=True)
        if len(user) < 2 :
            resp['code'] =  1
            resp['message'] = "Parameter Error" 
            self.write(json.dumps(resp))
            return
        
        data = redi.QueryMy(user)
        resp['code'] =  0
        resp['message'] = "Ok" 
        resp['data'] = data 
        self.write(json.dumps(resp))

class QuerymyapplyHandler(tornado.web.RequestHandler):
    def get(self):
        resp = dict()
        user = self.get_argument("user", strip=True)
        if len(user) < 2 :
            resp['code'] =  1
            resp['message'] = "Parameter Error" 
            self.write(json.dumps(resp))
            return
        
        data = redi.QueryMyApply(user)
        resp['code'] =  0
        resp['message'] = "Ok" 
        resp['data'] = data 
        self.write(json.dumps(resp))


class QuerymyfortopHandler(tornado.web.RequestHandler):
    def get(self):
        resp = dict()
        user = self.get_argument("user", strip=True)
        if len(user) < 2 :
            resp['code'] =  1
            resp['message'] = "Parameter Error" 
            self.write(json.dumps(resp))
            return
        
        data = redi.QueryMyfortop(user)
        resp['code'] =  0
        resp['message'] = "Ok" 
        resp['data'] = data 
        self.write(json.dumps(resp))
"""
class QuerysellHandler(tornado.web.RequestHandler):
    def get(self):
        data = mysql.Query()
        self.write(json.dumps(data))

class NoticeHandler(tornado.web.RequestHandler):
    def get(self):
        orderid = self.get_argument("orderid", strip=True)
        buyer = self.get_argument("buyer", strip=True)
        data = mysql.Done(orderid, buyer)
        self.write(json.dumps(data))

class sellHandler(tornado.web.RequestHandler):
    def get(self):
        fuwaid = self.get_argument("id", strip=True)
        fuwagid = self.get_argument("fuwagid", strip=True)
        amount = self.get_argument("amount", strip=True)
        owner = self.get_argument("owner", strip=True)
        data = mysql.Create(fuwaid, fuwagid, amount, owner)
        self.write(json.dumps(data))
"""

class QuerydetailHandler(tornado.web.RequestHandler):
    def get(self):
        resp = dict()
        gid = self.get_argument("fuwagid", strip=True)
        if len(gid) < 2 :
            resp['code'] =  1
            resp['message'] = "Parameter Error" 
            self.write(json.dumps(resp))
            return
        
        data = redi.QueryDetail(gid)
        resp['code'] =  0
        resp['message'] = "Ok" 
        resp['data'] = data 
        self.write(json.dumps(resp))



class CaptureHandler(tornado.web.RequestHandler):
    def mycmp(self, pic):
        sign = hashlib.md5()
        resp = dict()
        user = self.get_argument("user", strip=True)
        gid = self.get_argument("gid", strip=True)
        signin = self.get_argument("sign", strip=True)
        if len(signin) < 5 or len(user) < 2 or len(pic) < 10 or len(gid) < 3:
            resp['code'] =  1
            resp['message'] = "Parameter Error" 
            self.write(json.dumps(resp))
            return
        where = self.request.uri.find("&sign=") 
        src = self.request.uri[:where] + "&platform=boss66"
        sign.update(src)
        signout = sign.hexdigest()
        if signin != signout:
            print signout, signin
            resp['code'] =  2
            resp['message'] = "Sign Error" 
            self.write(json.dumps(resp))
            return

        data = redi.CaptureFuwa(pic, user, gid)
        if data == False:
            resp['code'] =  3
            resp['message'] = "明天再来吧"
            self.write(json.dumps(resp))
            return

        resp['code'] =  0
        resp['message'] = "Ok" 
        resp['data'] = data 
        self.write(json.dumps(resp))

    def post(self):
        file_metas = self.request.files['file']   
        filepath = str()
        for meta in file_metas:
            suffix = os.path.splitext(meta['filename'])[1]
            filename = getFileName() + suffix
            filepath = os.path.join(STORE_PATH, filename)
            with open(filepath, 'wb') as up:
                up.write(meta['body'])
        self.mycmp(filepath)

class Capturev2Handler(tornado.web.RequestHandler):
    def get(self):
        sign = hashlib.md5()
        resp = dict()
        user = self.get_argument("user", strip=True)
        gid = self.get_argument("gid", strip=True)
        signin = self.get_argument("sign", strip=True)
        if len(signin) < 5 or len(user) < 2 or len(gid) < 3:
            resp['code'] =  1
            resp['message'] = "Parameter Error" 
            self.write(json.dumps(resp))
            return
        where = self.request.uri.find("&sign=") 
        src = self.request.uri[:where] + "&platform=boss66"
        sign.update(src)
        signout = sign.hexdigest()
        if signin != signout:
            print signout, signin
            resp['code'] =  2
            resp['message'] = "Sign Error" 
            self.write(json.dumps(resp))
            return

        data = redi.Capturev2Fuwa(user, gid)
        if data == False:
            resp['code'] =  3
            resp['message'] = "明天再来吧"
            self.write(json.dumps(resp))
            return

        resp['code'] =  0
        resp['message'] = "Ok" 
        resp['data'] = data 
        self.write(json.dumps(resp))
"""
class toplistHandler(tornado.web.RequestHandler):
    def get(self):
        resp = dict()
        uid = self.get_argument("user", strip=True)
        if len(uid) < 2 :
            resp['code'] =  1
            resp['message'] = "Parameter Error" 
            self.write(json.dumps(resp))
            return
        
        data = toplist.GetToplist(uid)
        resp['code'] =  0
        resp['message'] = "Ok" 
        resp['data'] = data 
        self.write(json.dumps(resp))
"""

class donateHandler(tornado.web.RequestHandler):
    def get(self):
        resp = dict()
        sign = hashlib.md5()
        token = self.get_argument("token", strip=True)
        fromuser = self.get_argument("fromuser", strip=True)
        gid = self.get_argument("fuwagid", strip=True)
        signin = self.get_argument("sign", strip=True)
        if len(gid) < 2 or len(token) < 2 or len(signin) < 5:
            resp['code'] =  1
            resp['message'] = "Parameter Error" 
            self.write(json.dumps(resp))
            return
        where = self.request.uri.find("&sign=") 
        src = self.request.uri[:where] + "&platform=boss66"
        sign.update(src)
        signout = sign.hexdigest()
        if signin != signout:
            print signout, signin
            resp['code'] =  2
            resp['message'] = "Sign Error" 
            self.write(json.dumps(resp))
            return

        touser = base64.b64decode(token)  
        val = redi.Donate(touser, gid, fromuser)
        if val == 0:
            resp['code'] =  0
            resp['message'] = "Ok" 
        else:
            resp['code'] =  1
            resp['message'] = "No User" 
        self.write(json.dumps(resp))

class awardHandler(tornado.web.RequestHandler):
    def get(self):
        resp = dict()
        user = self.get_argument("userid", strip=True)
        gid = self.get_argument("fuwagid", strip=True)
        if len(gid) < 2 or len(user) < 2:
            resp['code'] =  1
            resp['message'] = "Parameter Error" 
            self.write(json.dumps(resp))
            return
        code, message = redi.Award(user, gid)
        resp['code'] =  code
        resp['message'] =  message
        self.write(json.dumps(resp))

class huodongHandler(tornado.web.RequestHandler):
    def get(self):
        resp = dict()
        gid = self.get_argument("fuwagid", strip=True)
        if len(gid) < 2:
            resp['code'] =  1
            resp['message'] = "Parameter Error" 
            self.write(json.dumps(resp))
            return
        data = redi.Huodong(gid)
        resp['code'] = 0 
        resp['message'] = "Ok" 
        resp['data'] =  data
        self.write(json.dumps(resp))

class classHandler(tornado.web.RequestHandler):
    def get(self):
        resp = dict()
        resp['code'] = 0 
        resp['message'] = "Ok" 
        resp['data'] =  redi.Class()
        self.write(json.dumps(resp))

class hitHandler(tornado.web.RequestHandler):
    def get(self):
        sign = hashlib.md5()
        resp = dict()
        filemd5 = self.get_argument("filemd5", strip=True)
        classid = self.get_argument("class", strip=True)
        timein = self.get_argument("time", strip=True)
        signin = self.get_argument("sign", strip=True)
        if len(signin) < 5 or len(classid) < 1 or len(filemd5) < 3 or len(timein) < 5:
            resp['code'] =  1
            resp['message'] = "Parameter Error"
            self.write(json.dumps(resp))
            return
        where = self.request.uri.find("&sign=")
        src = self.request.uri[:where] + "&platform=boss66"
        sign.update(src)
        signout = sign.hexdigest()
        if signin != signout:
            print signout, signin
            resp['code'] =  2
            resp['message'] = "Sign Error"
            self.write(json.dumps(resp))
            return

        timeplay = int(timein)
        now = int(time.time())

        data = False
        if now - timeplay < 20:
            data = redi.Hit(filemd5, classid)

        resp['code'] =  0
        resp['message'] = "Ok"
        resp['data'] = data
        self.write(json.dumps(resp))

class queryvideoHandler(tornado.web.RequestHandler):
    def get(self):
        resp = dict() 

        geohash = self.get_argument("geohash", strip=True)
        classid = self.get_argument("class", strip=True)
        geo = geohash.split('-')
        if len(geo) != 2 or len(classid) < 1:
            resp['code'] =  1
            resp['message'] = "Parameter Error" 
            self.write(json.dumps(resp))
            return
        
        longitude, latitude = geo[0], geo[1] 
        resp['code'] =  0
        resp['message'] = "OK" 
        resp['data'] = redi.QueryVideo(classid, longitude, latitude)
        self.write(json.dumps(resp))

class querystrvideoHandler(tornado.web.RequestHandler):
    def get(self):
        resp = dict() 

        geohash = self.get_argument("geohash", strip=True)
        geo = geohash.split('-')
        if len(geo) != 2:
            resp['code'] =  1
            resp['message'] = "Parameter Error" 
            self.write(json.dumps(resp))
            return
        
        longitude, latitude = geo[0], geo[1] 
        resp['code'] =  0
        resp['message'] = "OK" 
        resp['data'] = redi.QueryStrVideo(longitude, latitude)
        self.write(json.dumps(resp))

class APPHandler(tornado.web.RequestHandler):
    def get(self):
        resp = dict()
        geohash = self.get_argument("geohash", strip=True)
        geo = geohash.split('-')
        if len(geo) != 2:
            resp['code'] =  1
            resp['message'] = "Parameter Error"
            self.write(json.dumps(resp))
            return
        longitude, latitude = geo[0], geo[1]
        resp['code'] =  0
        resp['message'] = "OK"
        resp['data'] = redi.APP(longitude, latitude, 300)
        self.write(json.dumps(resp))

application = tornado.web.Application([
    (r"/queryv2", Queryv2Handler),
    (r"/querystrangerv2", QueryStrangerv2Handler),
    (r"/queryv3", Queryv3Handler),
    (r"/querystrangerv3", QueryStrangerv3Handler),
    (r"/hidev2", Hidev2Handler),
    (r"/capture", CaptureHandler),
    (r"/capturev2", Capturev2Handler),
    (r"/querymy", QuerymyHandler),
    (r"/querymyapply", QuerymyapplyHandler),
    (r"/querymyfortop", QuerymyfortopHandler),
    (r"/querydetail", QuerydetailHandler),
    (r"/querysell", QuerysellHandler),
    (r"/notice", NoticeHandler),
    (r"/sell", sellHandler),
    (r"/toplist", toplistHandler),
    (r"/donate", donateHandler),
    (r"/award", awardHandler),
    (r"/huodong", huodongHandler),
    (r"/queryclass", classHandler),
    (r"/queryvideo", queryvideoHandler),
    (r"/querystrvideo", querystrvideoHandler),
    (r"/hit", hitHandler),
    (r"/app", APPHandler),
])

if __name__ == "__main__":
    application.listen(55555)
    tornado.ioloop.IOLoop.instance().start()

