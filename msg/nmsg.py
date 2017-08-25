#!/usr/bin/env python
#-*- coding:utf-8 -*- 
#https://api.66boss.com/ucenter/userinfo/info?user_id=
import os
import cjson
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
import mysql
import hashlib
import redis

pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0, password="aaa11bbb22")  
r = redis.Redis(connection_pool=pool)  

class QuerysellHandler(tornado.web.RequestHandler):
    def get(self):
        data = mysql.Query()
        self.write(cjson.encode(data))

class QuerymysellHandler(tornado.web.RequestHandler):
    def get(self):
        user = self.get_argument("userid", strip=True)
        data = mysql.Myquery(user)
        self.write(cjson.encode(data))

class NoticeHandler(tornado.web.RequestHandler):
    def get(self):
        sign = hashlib.md5()
        orderid = self.get_argument("orderid", strip=True)
        buyer = self.get_argument("buyer", strip=True)
        gid = self.get_argument("fuwagid", strip=True)
        signin = self.get_argument("sign", strip=True)

        where = self.request.uri.find("&sign=") 
        src = self.request.uri[:where] + "&platform=boss66"
        sign.update(src)
        signout = sign.hexdigest()
        if signin != signout:
            print signout, signin
            resp = dict()
            resp['code'] =  2
            resp['message'] = "Sign Error" 
            self.write(cjson.encode(resp))
            return

        data = mysql.Done(orderid, buyer)
        r.hset(gid, "owner", buyer)
        r.sadd(buyer + "_pack", gid)
        self.write(cjson.encode(data))

class topupHandler(tornado.web.RequestHandler):
    def get(self):
        sign = hashlib.md5()
        userid = self.get_argument("userid", strip=True)
        amount = self.get_argument("amount", strip=True)
        signin = self.get_argument("sign", strip=True)

        where = self.request.uri.find("&sign=") 
        src = self.request.uri[:where] + "&platform=boss66"
        sign.update(src)
        signout = sign.hexdigest()
        if signin != signout:
            print signout, signin
            resp = dict()
            resp['code'] =  2
            resp['message'] = "Sign Error" 
            self.write(cjson.encode(resp))
            return

        data = mysql.Topup(userid, amount)
        self.write(cjson.encode(data))

class submoneyHandler(tornado.web.RequestHandler):
    def get(self):
        userid = self.get_argument("userid", strip=True)
        amount = self.get_argument("amount", strip=True)

        data = mysql.YuheSub(userid, amount)
        self.write(cjson.encode(data))

class sellHandler(tornado.web.RequestHandler):
    def get(self):
        sign = hashlib.md5()
        fuwaid = self.get_argument("id", strip=True)
        fuwagid = self.get_argument("fuwagid", strip=True)
        amount = self.get_argument("amount", strip=True)
        owner = self.get_argument("owner", strip=True)
        signin = self.get_argument("sign", strip=True)

        where = self.request.uri.find("&sign=") 
        src = self.request.uri[:where] + "&platform=boss66"
        sign.update(src)
        signout = sign.hexdigest()
        if signin != signout:
            print signout, signin
            resp = dict()
            resp['code'] =  2
            resp['message'] = "Sign Error" 
            self.write(cjson.encode(resp))
            return

        data = mysql.Create(fuwaid, fuwagid, amount, owner)
        r.srem(owner + "_pack", fuwagid)
        self.write(cjson.encode(data))

class msgHandler(tornado.web.RequestHandler):
    def get(self):
        results = dict()
        result = list()
        userid = self.get_argument("userid", strip=True)
        for row in mysql.QueryMessage(userid):
            result.append({
                "id":       row[0],
                "type":     row[1],
                "nick":     row[2],
                "snap":     row[3],
                "title":    row[4],
                "url":      row[5],
                "content":  row[6],
            })
        results['data'] = result;
        results['code'] = 0;
        results['message'] = 'OK';
        self.write(cjson.encode(results))
        return

class applyHandler(tornado.web.RequestHandler):
    def get(self):
        userid = self.get_argument("userid", strip=True)
        phone = self.get_argument("phone", strip=True)
        name = self.get_argument("name", strip=True)
        number = self.get_argument("number", strip=True)
        purpose = self.get_argument("purpose", strip=True)
        region = self.get_argument("region", strip=True)
        shop = self.get_argument("shop", strip=True)

        if len(userid) < 2 or len(phone) < 2 or len(name) < 2 or len(number) < 1 or len(purpose) < 2 or len(region) < 2:
            resp = dict()
            resp['code'] =  2
            resp['message'] = "Parameter Error" 
            self.write(cjson.encode(resp))
            return
        mysql.Apply(userid, name, phone, number, shop, purpose, region)
        resp = dict()
        resp['code'] =  0
        resp['message'] = "Ok" 
        self.write(cjson.encode(resp))

class moneyHandler(tornado.web.RequestHandler):
    def get(self):
        userid = self.get_argument("userid", strip=True)
        alipay = self.get_argument("alipay", strip=True)
        amount = self.get_argument("amount", strip=True)
        name = self.get_argument("name", strip=True)
        signin = self.get_argument("sign", strip=True)

        if len(name) < 2 or len(userid) < 2 or len(alipay) < 2 or len(amount) < 2 or len(signin) < 5:
            resp = dict()
            resp['code'] =  2
            resp['message'] = "Parameter Error" 
            self.write(cjson.encode(resp))
            return

        sign = hashlib.md5()
        where = self.request.uri.find("&sign=") 
        src = self.request.uri[:where] + "&platform=boss66"
        sign.update(src)
        signout = sign.hexdigest()
        if signin != signout:
            print signout, signin
            resp = dict()
            resp['code'] =  2
            resp['message'] = "Sign Error" 
            self.write(cjson.encode(resp))
            return
        money = float(amount)
        yuhe = mysql.Yuhe(userid)
        if yuhe < money:
            resp = dict()
            resp['code'] =  3
            resp['message'] = "amount's not enough" 
            self.write(cjson.encode(resp))
            return
        mysql.YuheSub(userid, money)
        mysql.Withdraw(userid, alipay, amount, name)
        resp = dict()
        resp['code'] =  0
        resp['message'] = "Ok" 
        self.write(cjson.encode(resp))

class querymoneyHandler(tornado.web.RequestHandler):
    def get(self):
        userid = self.get_argument("userid", strip=True)
        if len(userid) < 2:
            resp = dict()
            resp['code'] =  2
            resp['message'] = "Parameter Error" 
            self.write(cjson.encode(resp))
            return

        resp = dict()
        resp['code'] =  0
        resp['message'] = "Ok" 
        resp['data'] = mysql.Yuhe(userid)
        self.write(cjson.encode(resp))

class CancelsellHandler(tornado.web.RequestHandler):
    def get(self):
        resp = dict()
        orderid = self.get_argument("orderid", strip=True)
        gid = self.get_argument("fuwagid", strip=True)
        userid = self.get_argument("userid", strip=True)

        if len(orderid) < 2 or len(gid) < 3 or len(userid) < 5 :
            resp['code'] =  2
            resp['message'] = "Parameter Error" 
            self.write(cjson.encode(resp))
            return

        mysql.CancelSell(orderid)
        r.sadd(userid + "_pack", gid)

        resp['code'] =  0
        resp['message'] = "OK" 
        self.write(cjson.encode(resp))

class donateHandler(tornado.web.RequestHandler):
    def get(self):
        resp = dict()
        owner = self.get_argument("owner", strip=True)
        buyer = self.get_argument("buyer", strip=True)

        if len(owner) < 2 or len(buyer) < 3:
            resp['code'] =  2
            resp['message'] = "Parameter Error" 
            self.write(cjson.encode(resp))
            return

        mysql.DonateMsg(owner, buyer)
        resp['code'] =  0
        resp['message'] = "OK" 
        self.write(cjson.encode(resp))

application = tornado.web.Application([
    (r"/querysell", QuerysellHandler),
    (r"/querymysell", QuerymysellHandler),
    (r"/cancelsell", CancelsellHandler),
    (r"/notice", NoticeHandler),
    (r"/topup", topupHandler), #充值
    (r"/openredevp", topupHandler), #抢红包
    (r"/submoney", submoneyHandler), #发红包
    (r"/sell", sellHandler),
    (r"/myinfo", msgHandler),
    (r"/apply", applyHandler),
    (r"/money", moneyHandler), #提现
    (r"/querymoney", querymoneyHandler),
    (r"/donatemsg", donateHandler),
])

if __name__ == "__main__":
    application.listen(7777)
    tornado.ioloop.IOLoop.instance().start()

