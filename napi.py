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
import uuid

ACCESS_PATH = "http://wsim.66boss.com/fuwa/"
STORE_PATH="/www/html/fuwa/"

class QueryHandler(tornado.web.RequestHandler):
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
        resp['data'] = redi.Query(longitude, latitude)
        self.write(json.dumps(resp))


def getFileName():
    source = list(string.lowercase) 
    random.shuffle(source)
    temp = source[:15]
    return "".join(temp)

class HideHandler(tornado.web.RequestHandler):
    def myget(self, video, uuid):
        resp = dict()
        pos = self.get_argument("pos", strip=True)
        geohash = self.get_argument("geohash", strip=True)
        owner = self.get_argument("owner", strip=True)
        detail = self.get_argument("detail", strip=True)
        redevpnum = self.get_argument("redevpnum", strip=True)
        redevptotal = self.get_argument("redevptotal", strip=True)

        geo = geohash.split('-')
        if len(geo) != 2 or len(number) < 1:
            resp['code'] =  1
            resp['message'] = "Parameter Error" 
            self.write(json.dumps(resp))
            return
        
        longtitude, latitude = geo[0], geo[1] 
        users = redi.HideVideo(longtitude, latitude, pos, owner, detail, video, uuid, redevpnum, redevptotal)
        resp['code'] =  0
        resp['message'] = "Ok" 
        resp['data'] =  users
        self.write(json.dumps(resp))

    def post(self):
        video = str()
        uuid = uuid.uuid1().hex

        if self.request.files.has_key('video'):
            video_metas = self.request.files['video']   
            for meta in video_metas:
                temppath = os.path.join(STORE_PATH, getFileName())
                with open(temppath, 'wb') as up:
                    up.write(meta['body'])


                suffix = os.path.splitext(meta['filename'])[1]
                filename = uuid + suffix
                filepath = os.path.join(STORE_PATH, filename)

                os.rename(temppath, filepath)
                video = ACCESS_PATH + filename

        self.myget(video, uuid)


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

class huodongHandler(tornado.web.RequestHandler):
    def get(self):
        resp = dict()
        gid = self.get_argument("uuid", strip=True)
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


class queryvideoHandler(tornado.web.RequestHandler):
    def get(self):
        resp = dict() 

        geohash = self.get_argument("geohash", strip=True)
        geo = geohash.split('-')
        if len(geo) != 2 :
            resp['code'] =  1
            resp['message'] = "Parameter Error" 
            self.write(json.dumps(resp))
            return
        
        longitude, latitude = geo[0], geo[1] 
        resp['code'] =  0
        resp['message'] = "OK" 
        resp['data'] = redi.QueryVideo(longitude, latitude)
        self.write(json.dumps(resp))


class QuerymyHandler(tornado.web.RequestHandler):
    def get(self):
        resp = dict()
        user = self.get_argument("userid", strip=True)
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

class hitHandler(tornado.web.RequestHandler):
    def get(self):
        sign = hashlib.md5()
        resp = dict()
        uuid = self.get_argument("uuid", strip=True)
        timein = self.get_argument("time", strip=True)
        signin = self.get_argument("sign", strip=True)
        if len(signin) < 5 or len(uuid) < 3 or len(timein) < 5:
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
            data = redi.Hit(uuid)

        resp['code'] =  0
        resp['message'] = "Ok"
        resp['data'] = data
        self.write(json.dumps(resp))

application = tornado.web.Application([
    (r"/query", QueryHandler),
    (r"/hide", HideHandler),
    (r"/huodong", huodongHandler),
    (r"/queryvideo", queryvideoHandler),
    (r"/querymy", huodongHandler),
    (r"/openmoney", OpenHandler),
    (r"/hit", HitHandler),
])

if __name__ == "__main__":
    application.listen(55555)
    tornado.ioloop.IOLoop.instance().start()

