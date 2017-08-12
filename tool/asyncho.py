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
        response = http_client.fetch(BASE, callback=self.on_response)
        print (response)
        self.finish()
    def on_response(self,response):
        print response.headers
        print response.body

application = tornado.web.Application([
    (r"/app", GenAsyncHandler),
])

if __name__ == "__main__":
    application.listen(55555)
    tornado.ioloop.IOLoop.instance().start()

