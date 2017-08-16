# 藏视频，视频里面关联很多红包， 服务器根据位置下发视频，或视频地图，
# 用户看完视频就可以领取红包 ,(没有线索图片) , 藏视频 可以地图任意选点

# 0 查询周围的地图视频
http://fuwav2.hmg66.com/api/query?geohash=102.2301-33.2827
经度－纬度

```
message: "OK",
code: 0,
data: {
[{
pos: "珠江国际纺织城",
video: "http://x.xx.cx/uuid.mp4",
hider: "100000354",
geo: "113.300937-23.085474",
name: "CHU",
gender: "女",
uuid: "adfadfawwfadd"
avatar: "https://imgcdn.66boss.com/imagesu/avatar/20170515023034206335.jpeg",
signature: "",
location: "广东 广州市"
money: "1" 有红包
}
{
}
]
}
```

# 1 查询周围的视频
http://fuwav2.hmg66.com/api/queryvideo?geohash=102.2301-33.2827
经度－纬度

```
message: "OK",
code: 0,
data: {
[{
pos: "珠江国际纺织城",
video: "http://x.xx.cx/uuid.mp4",
hider: "100000354",
geo: "113.300937-23.085474",
name: "CHU",
gender: "女",
uuid: "adfadfawwfadd"
avatar: "https://imgcdn.66boss.com/imagesu/avatar/20170515023034206335.jpeg",
signature: "",
location: "广东 广州市"
money: "1" 有红包
},
{
pos: "珠江国际纺织城",
video: "http://x.xx.cx/uuid.mp4",
hider: "100000354",
geo: "113.300937-23.085474",
name: "CHU",
gender: "女",
uuid: "bjfadkeab", 
avatar: "https://imgcdn.66boss.com/imagesu/avatar/20170515023034206335.jpeg",
signature: "",
location: "广东 广州市"
money: "0" 无红包
},

]
}
```
# 1.1 打开红包 

http://fuwav2.hmg66.com/api/openmoney?uuid=xxx
```
message: "OK",
code: 0,
data:{ 
result: true/false
msg :"红包已存入你个人余额"/"红包已被领完了"
}
```


# 2 藏视频 

POST http://fuwav2.hmg66.com/api/hide?owner=xx&detail=店内活动&pos=xx&geohash=102.2-33.22&redevpnum=?&redevptotal=?
owner福娃所有者
pos 福娃位置　比如广州珠江纺织城Ａ区
geohash 经纬度
redevpnum 红包数量
redevptotal 红包总金额
视频采用POST name=video

```
图片为file 视频为video
    <form action='upload' enctype="multipart/form-data" method='post'>
    <input type='file' name='file'/><br/>
    <input type='file' name='video'/><br/>
    <input type='submit' value='submit'/>
    </form>
```


# 3 福娃活动介绍
http://fuwav2.hmg66.com/api/huodong?uuid=adfeadfdbbdfw
```
uuid为视频uuid
{
message: "Ok",
code: 0,
data: "抢到本次福娃用户，本店消费全场八折"
}
```


# 4 查询我的消息　(没有更改)
http://fuwav2.hmg66.com/msg/myinfo?userid=
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

# 5 提现申请 (没有更改)
http://fuwa.hmg66.com/msg/money?userid=xx&amount=xx&alipay=xx&name=小啊&sign=xx
http://fuwav2.hmg66.com/msg/money?userid=xx&amount=xx&alipay=xx&name=小啊&sign=xx
userid 用户ID
amount 体现金额
alipay 支付宝帐号
sign 签名
md5(/money?userid=100000076&alipay=22233322x&amount=13&name=%E5%B0%8F%E5%95%8A&platform=boss66)

# 6 查询可用余额 (没有更改) 
http://fuwav2.hmg66.com/msg/querymoney?userid=100000078
http://fuwa.hmg66.com/msg/querymoney?userid=100000078
二个路径应该都可以
userid 用户ID


# 7 增加播放次数 (暂时不做）
http://fuwa.hmg66.com/api/hit?uuid=adfefadfcafda&time=1496313547&sign=
uuid 是视频文件ＭＤ５　校验值。
如果是萌友视频class设置为i
time 是从1970年１月１日凌晨到目前的秒数
sign 是签名


# 8 查询视频入口则为http://fuwav2.hmg66.com/api/queryvideo?geohash=102.2301-33.2827
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
    uuid:"3ea31ba3efg1331a398"
   },
   {,
    name: "CHU",
    userid : "10000023",
    gender: "女",
    avatar: "https://imgcdn.66boss.com/imagesu/avatar/20170515023034206335.jpeg",
    video: "http://wsim.66boss.com/avatar/20170.mp4"
    width:1024
    height:768
    uuid:"3ea31ba3efg1331a398"
    distance: 1000 距离你距离
    },

    ]
}
```
#9 查询自己藏得宝贝

http://fuwav2.hmg66.com/api/querymy?userid=

```
message: "OK",
code: 0,
data: {
[{
pos: "珠江国际纺织城",
video: "http://x.xx.cx/uuid.mp4",
hider: "100000354",
geo: "113.300937-23.085474",
name: "CHU",
gender: "女",
detail: "测试",
uuid: "adfadfawwfadd"
avatar: "https://imgcdn.66boss.com/imagesu/avatar/20170515023034206335.jpeg",
signature: "",
location: "广东 广州市"
money: "true"
},
{
pos: "珠江国际纺织城",
video: "http://x.xx.cx/uuid.mp4",
hider: "100000354",
geo: "113.300937-23.085474",
name: "CHU",
gender: "女",
detail: "测试",
uuid: "bjfadkeab", 
avatar: "https://imgcdn.66boss.com/imagesu/avatar/20170515023034206335.jpeg",
signature: "",
money: "true"
location: "广东 广州市"
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

