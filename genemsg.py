#!/usr/bin/env python
#-*- coding: utf-8 -*- 

import MySQLdb
import time
import string
from DBUtils.PooledDB import PooledDB
import dbconfig


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

def generalmsg(userid):
    """
    交易完成后添加 提醒原持有人的消息
    :param orderid:  订单ID
    :return:
    """
    import datetime
    con = getConn()
    cur = con.cursor()
    now = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')

    title = u"你的福娃被成功购买"
    content = u"{0} 于 {1}　成功购买了你的福娃".format("Rain", now)
    sql = u"insert into message (touser, type, nick, snap, title, content, state) values\
('%s', 0, '%s', '%s', '%s', '%s', 0)" %(userid, 'Rain', 'http://ogcp293hg.bkt.clouddn.com/emopic/0330b6ffe129a0ab4a304e125bd54a00.jpg', title, content)
    cur.execute(sql)
    con.commit()

    cur.close()
    con.close()

def activitiymsg(userid):
    """
    交易完成后添加 提醒原持有人的消息
    :param orderid:  订单ID
    :return:
    """
    import datetime
    con = getConn()
    cur = con.cursor()

    title = u"重大活动公告"
    url = "http://m.66boss.com"
    sql = u"insert into message (touser, type, nick, snap, title, url, state) values\
('%s', 1, '%s', '%s', '%s', '%s', 0)" %(userid, u'嗨萌', 'http://wsimcdn.hmg66.com/hm_logo.png', title, url)
    cur.execute(sql)
    con.commit()

    cur.close()
    con.close()



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
if __name__ ==  '__main__':
    for x in range(100000070, 100000080):
        generalmsg(str(x))
        activitiymsg(str(x))

