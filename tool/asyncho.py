#!/usr/bin/env python
#-*- coding: utf-8 -*- 
import json
import os
import tornado
import tornado.ioloop
from tornado.httpclient import AsyncHTTPClient
from tornado import gen
import tornado.web

BASE = "https://api.66boss.com/ucenter/userinfo/info?user_id=100000320"

class GenAsyncHandler(tornado.web.RequestHandler):
    @gen.engine
    def get(self):
        http_client = AsyncHTTPClient()
        http_client.fetch(BASE, callback=self.on_response, user_agent="uuid")

    def on_response(self,response):
        print response.request.headers['User-Agent']
        data =  json.loads(response.body)
        dic = {"name": data['user_name'], "avatar": data['avatar'], "gender": data['sex'],\
               "location":data['district_str'], "signature":data['signature']}

application = tornado.web.Application([
    (r"/app", GenAsyncHandler),
])

if __name__ == "__main__":
    application.listen(55555)
    tornado.ioloop.IOLoop.instance().start()

