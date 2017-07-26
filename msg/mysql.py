#!/usr/bin/env python
#-*- coding: utf-8 -*- 

import MySQLdb
import time
import string
from DBUtils.PooledDB import PooledDB
import dbconfig
from tornado import gen


ERROR = {0:"OK", 1:"Parameter Error", 2:"Database Error", 3:u"您已赞", 4:u"你无权开通直播"}
Default_Snapshot = "http://7xvsyw.com2.z0.glb.qiniucdn.com/n.jpg"

class DbManager():
    def __init__(self):
        kwargs = {}
        kwargs['host'] =  dbconfig.DBConfig.getConfig('database', 'dbhost')
        kwargs['port'] =  int(dbconfig.DBConfig.getConfig('database', 'dbport'))
        kwargs['user'] =  dbconfig.DBConfig.getConfig('database', 'dbuser')
        kwargs['passwd'] =  dbconfig.DBConfig.getConfig('database', 'dbpassword')
        kwargs['db'] =  dbconfig.DBConfig.getConfig('database', 'dbname')
        kwargs['charset'] =  dbconfig.DBConfig.getConfig('database', 'dbcharset')
        self._pool = PooledDB(MySQLdb, mincached=1, maxcached=15, maxshared=10, maxusage=10000, **kwargs)

    def getConn(self):
        return self._pool.connection()

_dbManager = DbManager()

def getConn():
    return _dbManager.getConn()

def Query():
    con = getConn()
    cur =  con.cursor()
    result = list()
    results = dict()

    selling = []
    sql = "select orderid, fuwaid, fuwagid, amount, owner from sell where state = 1"
    cur.execute(sql)
    res = cur.fetchall()

    for channel in res:
        temp = dict()
        temp['orderid'] = channel[0]
        temp['fuwaid'] = channel[1]
        temp['fuwagid'] = channel[2]
        temp['amount'] = channel[3]
        temp['owner'] = channel[4]
        result.append(temp)

    cur.close()
    con.close()
    results['code'] =  0
    results['message'] =  ERROR[0]
    results['data'] =  result
    return results

def Myquery(user):
    con = getConn()
    cur =  con.cursor()
    result = list()
    results = dict()

    selling = []
    sql = "select orderid, fuwaid, fuwagid, amount from sell where state = 1 and owner='%s'" %user
    cur.execute(sql)
    res = cur.fetchall()

    for channel in res:
        temp = dict()
        temp['orderid'] = channel[0]
        temp['fuwaid'] = channel[1]
        temp['fuwagid'] = channel[2]
        temp['amount'] = channel[3]
        result.append(temp)

    cur.close()
    con.close()
    results['code'] =  0
    results['message'] =  ERROR[0]
    results['data'] =  result
    return results

def Delete(orderid):
    con = getConn()
    cur =  con.cursor()

    result = dict()

    sql = "delete from sell where orderid = '{0}' ".format(orderid)
    cur.execute(sql)
    con.commit()

    cur.close()
    con.close()
    result['code'] =  0
    result['message'] =  ERROR[0]
    return result

def Done(orderid, buyer):
    con = getConn()
    cur =  con.cursor()

    result = dict()

    sql = "update sell set state = 2, buyer ='{1}' where orderid = '{0}' ".format(orderid, buyer)
    cur.execute(sql)
    con.commit()
    cur.close()
    con.close()
    sellAferCreateMsg(orderid, buyer)
    result['code'] =  0
    result['message'] =  ERROR[0]
    result['data'] =  ""
    return result

def Topup(userid, amount):
    con = getConn()
    cur =  con.cursor()

    sql = "update money set amount = amount + %s where userid='%s'" %(userid)
    cur.execute(sql)
    con.commit()
    cur.close()
    con.close()

    result = dict()
    result['code'] =  0
    result['message'] =  ERROR[0]
    result['data'] =  ""
    return result

@gen.engine
def sellAferCreateMsg(orderid, buyer):
    """
    交易完成后添加 提醒原持有人的消息
    :param orderid:  订单ID
    :return:
    """
    import datetime
    con = getConn()
    cur = con.cursor()
    sql = "SELECT owner FROM sell WHERE orderid='{0}' ".format(orderid)
    cur.execute(sql)
    res = cur.fetchone()
    owner = res[0]
    user = getUserinfo(buyer)
    now = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    if user.has_key('user_name'):

        title = u"你的福娃被成功购买"
        content = u"{0} 于 {1}　成功购买了你的福娃".format(user['user_name'], now)
        sql = u"insert into message (touser, type, nick, snap, title, content, state) values\
('%s', 0, '%s', '%s', '%s', '%s', 0)" %(owner, user['user_name'], user['avatar'], title, content)
        cur.execute(sql)
        con.commit()

    cur.close()
    con.close()

def getUserinfo(userid):
    import urllib2
    import json
    response = urllib2.urlopen("https://api.66boss.com/ucenter/userinfo/friendlist?user_id=%s" % userid)
    html = response.read()
    if not html:
        return dict()
    users =  json.loads(html)
    response.close()
    for user in users:
        if user['user_id'] == int(userid):
            return user

def Create(fuwaid, fuwagid, amount, owner):
    con = getConn()
    cur =  con.cursor()
    result = dict()

    sql = "insert into sell (fuwaid,fuwagid,amount,owner,state)\
          values ('{0}', '{1}', '{2}', '{3}', 1)".format(fuwaid, fuwagid, amount, owner)

    cur.execute(sql)
    con.commit()
    cur.close()
    con.close()

    result['code'] =  0
    result['message'] =  ERROR[0]
    return result

"""
|  mid     | int(10) unsigned | NO   | PRI | NULL    | auto_increment |
| touser  | varchar(64)      | YES  |     | NULL    |                |
| type    | int(10) unsigned | YES  |     | NULL    |                |
| nick    | varchar(64)      | YES  |     | NULL    |                |
| snap    | varchar(255)     | YES  |     | NULL    |                |
| title   | varchar(255)     | YES  |     | NULL    |                |
| url     | varchar(255)     | YES  |     | NULL    |                |
| content | varchar(255)     | YES  |     | NULL    |                |
| state   | int(11)          | YES  |     | NULL    |                |
"""
def QueryMessage(user):
    con = getConn()
    cur = con.cursor()
    sql = "select mid, type, nick, snap, title, url, content from message WHERE touser='%s' AND state=0" % user
    cur.execute(sql)
    result = cur.fetchall()
    sql = "UPDATE message SET state=1 WHERE touser='%s' AND state=0" % user
    cur.execute(sql)
    con.commit()
    cur.close()
    con.close()
    return  result

def Apply(userid, name, phone, number, shop, purpose, region):

   # name = name.decode('utf-8') 
   # purpose = purpose.decode('utf-8') 
   # region = region.decode('utf-8') 

    con = getConn()
    cur = con.cursor()
    sql = u"insert into application (phone, name, number, shop, purpose, region, state, userid) values\
('%s', '%s', %s, %s, '%s', '%s', 0, '%s')" %(phone, name, number, shop, purpose, region, userid)
    cur.execute(sql)
    con.commit()

    cur.close()
    con.close()

def Withdraw(userid, alipay, amount, name):
    con = getConn()
    cur = con.cursor()
    sql = u"insert into withdraw (userid, alipay, amount,name, state) values ('%s', '%s', %s, '%s', 1)" %(userid, alipay, amount, name)
    cur.execute(sql)
    con.commit()

    cur.close()
    con.close()

def Yuhe(userid):
    con = getConn()
    cur = con.cursor()
    sql = "select amount from money where userid = %s" %(userid)
    cur.execute(sql)
    result = cur.fetchone()

    cur.close()
    con.close()
    return result[0]

def YuheSub(userid, amount):
    con = getConn()
    cur = con.cursor()
    sql = "update money set amount = amount - %s where userid='%s'" %(amount, userid)
    cur.execute(sql)
    con.commit()

    cur.close()
    con.close()

def CancelSell(orderid):
    con = getConn()
    cur = con.cursor()
    sql = "delete from sell where orderid =%s" %(orderid)
    cur.execute(sql)
    con.commit()

    cur.close()
    con.close()

@gen.engine
def DonateMsg(owner, buyer):
    import datetime
    con = getConn()
    cur = con.cursor()
    user = getUserinfo(buyer)
    now = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    if user.has_key('user_name'):
        title = u"你的朋友成功赠送福娃"
        content = u"您于{1}收到 {0} 赠送的福娃".format(user['user_name'], now)
        sql = u"insert into message (touser, type, nick, snap, title, content, state) values\
('%s', 0, '%s', '%s', '%s', '%s', 0)" %(owner, user['user_name'], user['avatar'], title, content)
        cur.execute(sql)
        con.commit()

    cur.close()
    con.close()

if __name__ ==  '__main__':
    import cjson
    #print Myquery("xiechc")
    #a = u"王"
    #b =u"女"
    #ApplyLive("1234", a.encode('utf-8'), b.encode('utf-8'), "133333333333", "afadf.jpg")
    #print  Query()
    #print  Delete(1)
    #print Create(66, "fuwa_33", 100.10, "xiechc")
    #print  Query()
    #print  Done(10, "john")
    #print getUserinfo("100000076")
    #sellAferCreateMsg(57, "100000076")
    for x in range(100):
        Done(57, "100000076")
