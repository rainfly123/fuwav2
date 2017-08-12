# fuwa

# 1 查询周围的福娃
http://fuwa.hmg66.com/api/queryv2?geohash=102.2301-33.2827&radius=10000&biggest=0
经度－纬度
查询自己周围radius半径远的福娃，单位m
第一次调用biggest = 0
后续调用　取返回near中福娃gid 最后一个数值，比如fuwa_i_2323 则biggest=2323 依次类推

```
message: "OK",
code: 0,
data: {
"far":[ {
geo: "113.300937-23.085474",
pic: "http://wsim.66boss.com/fuwa/brciqydlwvmtnxz.jpg",
pos: "世界纺织博览中心B坐",
video: "",
hider: "100000354",
number: 64,  此处福娃数量
distance: 808.3202,
name: "CHU",
gender: "女",
detail: "测试",
avatar: "https://imgcdn.66boss.com/imagesu/avatar/20170515023034206335.jpeg",
signature: "",
location: "广东 广州市"
}
{
geo: "113.320937-23.185474",
pic: "http://wsim.66boss.com/fuwa/brciqydlwvmtnxz.jpg",
pos: "世界纺织博览中心A坐",
video: "",
hider: "100000354",
number: 22,  此处福娃数量
distance: 808.3202,
name: "CHU",
gender: "女",
detail: "测试",
avatar: "https://imgcdn.66boss.com/imagesu/avatar/20170515023034206335.jpeg",
signature: "",
location: "广东 广州市"
}

]
"near":[{
pic: "http://wsim.66boss.com/fuwa/brciqydlwvmtnxz.jpg",
pos: "珠江国际纺织城",
video: "",
hider: "100000354",
geo: "113.300937-23.085474",
id: "6",
distance: 808.3202,
name: "CHU",
gender: "女",
detail: "测试",
gid: "fuwa_i_2353", ##2353 递减分页每页最多１００个，请求提交最大值，服务器返回数据都比提交的最大值小
avatar: "https://imgcdn.66boss.com/imagesu/avatar/20170515023034206335.jpeg",
signature: "",
location: "广东 广州市"
},

pic: "http://wsim.66boss.com/fuwa/brciqydlwvmtnxz.jpg",
pos: "珠江国际纺织城",
video: "",
hider: "100000354",
geo: "113.300937-23.085474",
id: "64",
distance: 808.3202,
name: "CHU",
gender: "女",
detail: "测试",
gid: "fuwa_i_2349", 
avatar: "https://imgcdn.66boss.com/imagesu/avatar/20170515023034206335.jpeg",
signature: "",
location: "广东 广州市"
},

]
}
}
```
# 5 藏福娃 

POST http://fuwa.hmg66.com/api/hidev2?owner=xx&detail=店内活动&pos=xx&geohash=102.2-33.22&validtime=1/2/3/4&number=xxx&type=1/0&class=1
owner福娃所有者
pos 福娃位置　比如广州珠江纺织城Ａ区
geohash 经纬度
福娃线索图片采用POST name=file
视频采用POST name=video
detail 福娃活动详情
type=1福娃，０缘分
number 藏福娃数量 （不能多于可用福娃数量,仅申请的福娃可以藏）
class 分类，美食、女装，男装，鞋帽，娱乐，用１，２，３，4，5
如果type=0藏缘分福娃，那么class 设置成i

```
图片为file 视频为video
    <form action='upload' enctype="multipart/form-data" method='post'>
    <input type='file' name='file'/><br/>
    <input type='file' name='video'/><br/>
    <input type='submit' value='submit'/>
    </form>
```


# 7.1 福娃活动介绍
http://fuwa.hmg66.com/api/huodong?fuwagid=fuwa_i_110
```
{
message: "Ok",
code: 0,
data: "抢到本次福娃用户，本店消费全场八折"
}
```


# 11 查询我的消息　
http://fuwa.hmg66.com/msg/myinfo?userid=
```
{
    "message": "Ok",
    "code": 0,
    "data": [
   {
     "id"  :   3
     "type": 1   #代表活动推广 ,有url无content 
     "nick": "港棉纺织",
     "snap": "http://a.b.c.d/a.jpg",
     "title": "庆十一友情回馈",
     "url":  "http://a.b.c.d/ina.html"
     "content":  "",
    },
    {
     "id"  :   4
     "type": 0   #代表系统通知 ,有content 无url
     "nick": "我最摔",
     "snap": "http://a.b.c.d/a.jpg",
     "title": "系统通知",
     "content":  "你的福娃被抓取",
     "url": "";
    }

     ]
}
```

# 16 提现申请
http://fuwa.hmg66.com/msg/money?userid=xx&amount=xx&alipay=xx&name=小啊&sign=xx
userid 用户ID
amount 体现金额
alipay 支付宝帐号
sign 签名
md5(/money?userid=100000076&alipay=22233322x&amount=13&name=%E5%B0%8F%E5%95%8A&platform=boss66)

# 17 查询可用余额
http://fuwa.hmg66.com/msg/querymoney?userid=100000078
userid 用户ID


# 18 增加播放次数
http://fuwa.hmg66.com/api/hit?filemd5=adfefadfcafda&class=1&time=1496313547&sign=
filemd5 是视频文件ＭＤ５　校验值。
class 是视频分类1,2,3,4,5, 美食，女装，男装，鞋帽，玩乐，
如果是萌友视频class设置为i
time 是从1970年１月１日凌晨到目前的秒数
sign 是签名


# 19 查询福娃视频入口则为http://fuwa.hmg66.com/api/queryvideo?geohash=102.2301-33.2827&class=1
class 是分类1,2,3,4,,,,
geohash 是当前经纬度

```
{
   code : 0
   message: "OK",
   data:[
   {
    name: "CHU",
    userid : "10000023",
    gender: "女",
    avatar: "https://imgcdn.66boss.com/imagesu/avatar/20170515023034206335.jpeg",
    video: "http://wsim.66boss.com/avatar/20170.mp4"
    width:1024
    height:768
    filemd5:"3ea31ba3efg1331a398"
    distance: 1000 距离你距离
   },
   {,
    name: "CHU",
    userid : "10000023",
    gender: "女",
    avatar: "https://imgcdn.66boss.com/imagesu/avatar/20170515023034206335.jpeg",
    video: "http://wsim.66boss.com/avatar/20170.mp4"
    width:1024
    height:768
    filemd5:"3ea31ba3efg1331a398"
    distance: 1000 距离你距离
    },

    ]
}
```

# 关于签名 
只对抓福娃ＵＲＬ　签名，其余不要求
每个url后面都有 sign=xxx 签名计算方法是对uri&platform=boss66 进行md5
uri 是这个地址串 不含sign=
举个例子：
http://localhost:1688/capture?user=john&gid=fuwa_6&sign=7ad54cafb52668e4264320c3145c6422
md5(/capture?user=john&gid=fuwa_6&platform=boss66)
结果：
7ad54cafb52668e4264320c3145c6422

## 二维码格式
第一种       fuwa:fuwa:fuwa_c_123                      
第二种       fuwa:user:AEjOkadJMKaGK 
                        
前边是福娃的二维码， 后面是福娃赠送接收用户口令二维码

