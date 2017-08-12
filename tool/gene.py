#!/usr/bin/env python
#-*- coding: utf-8 -*- 
import redis  
import random
import urllib2
import json

BASE = "https://api.66boss.com/ucenter/userinfo/info?user_id="
pool = redis.ConnectionPool(host='127.0.0.1', port=6379)  
r = redis.Redis(connection_pool=pool)  

def getName(userid):
    response = urllib2.urlopen(BASE + userid)
    html = response.read()
    if not html:
        return dict()
    info =  json.loads(html)
    response.close()
    return info['user_name']
    

def gene(userid, name, total, shop):
    gid = r.get("globalid")
    start = int(gid)
    for i in range (total):
        r.incr("globalid")
        fid = str(start + i)
        if shop :
            key ="fuwa_c_%s"%fid
        else:
            key ="fuwa_i_%s"%fid
        temp = dict()
        temp["owner"] = userid
        temp["id"] = random.randint(1,66)
        temp["creator"] = userid
        temp["awarded"] = "0" 
        temp["pos"] = "广州大酒店"
        temp["name"] = name
        i=r.hmset(key, temp)
        r.sadd(userid + "_pack", key)

def Create(userid, total, shop):
    name = getName(userid)
    gene(userid, name, total, shop)

Create("100000100", 10, True)
Create("100000100", 10, False)
