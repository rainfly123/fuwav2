#!/usr/bin/env python
#-*- coding: utf-8 -*- 
import redis  
import random
import urllib2
import json
import mysql
import pickle

BASE = "https://api.66boss.com/ucenter/userinfo/info?user_id="
pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0, password="aaa11bbb22")  
r = redis.Redis(connection_pool=pool)  

def getName(userid):
    response = urllib2.urlopen(BASE + userid)
    html = response.read()
    if not html:
        return dict()
    data =  json.loads(html)
    response.close()
    dic = {"name": data['user_name'], "avatar": data['avatar'], "gender": data['sex'],\
           "location":data['district_str'], "signature":data['signature']}
    return dic

def gene(recv, creator, info, total, shop):
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
        temp["owner"] = recv
        idd = random.randint(1,65)
        if idd in [6, 16, 26, 36, 46, 56]:
            idd -= 1
        temp["id"] =  idd        
        temp["creator"] = creator 
        temp["awarded"] = "0" 
        temp["detail"] = "活动赠送" 
        temp["pos"] = "广州珠江纺织城"
        temp["name"] = info['name']
        temp["avatar"] = info['avatar']
        temp["gender"] = info['gender']
        temp["location"] = info['location']
        temp["signature"] = info['signature']
        i=r.hmset(key, temp)
        r.sadd(recv + "_pack", key)

creator  = "100000153"
receiver = ["100000075", "100001038", "100001284", "100001285", "100001287", "100001389", "100001397", "100001433"]

info = getName(creator)

for recv in receiver:
    gene(recv, creator, info, 100, 0)
