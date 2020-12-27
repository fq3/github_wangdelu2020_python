import re
import requests
import json
import urllib
import time
import timeit
import math
import sys
from datetime import datetime
from dateutil import tz
import os


osenviron={}

djj_bark_cookie=''
djj_sever_jiang=''


JD_API_HOST = 'https://daojia.jd.com/client?_jdrandom=1608968590824'
url=''
yuanck=''
cookiesList=[]
yuanckList=[]
urlList=[]
result=''


zyheaders={"Accept": "*/*","Accept-Encoding": "br, gzip, deflate","Accept-Language": "zh-cn","Content-Type": "application/x-www-form-urlencoded;","User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148________appName=jdLocal&platform=iOS&djAppVersion=8.3.0&supportDJSHWK","traceparent": "00-41efefb5fc0ac1984e57912247192866-74f60f509f5e0b12-01","Referer":"https://daojia.jd.com/taroh5/h5dist/"}


djheaders={"Accept": "*/*","Accept-Encoding": "br, gzip, deflate","Accept-Language": "zh-cn","Content-Type": "application/x-www-form-urlencoded;","User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148________appName=jdLocal&platform=iOS&djAppVersion=8.3.0&supportDJSHWK","traceparent": "00-41efefb5fc0ac1984e57912247192866-74f60f509f5e0b12-01","Referer":"https://daojia.jd.com/taroh5/h5dist/"}


def JD_Daojia():
   Daojia_getUserAccountInfo()
   
   showSignInMsgNew()
   tasklist_Daojia()



     
def showSignInMsgNew():
   print('\n showSignInMsgNew')
   try:
     body = {"platform":4,"longitude":1,"latitude":2,"source":"H5"}
     data=json.loads(iosrule('signin%2FshowSignInMsgNew',body).text)
     #print(data)
     data=data['result']['userInfoResponse']
     msg=''
     if data['hasSign']==False:
        sdata=userSigninNew()
        if sdata['msg'].find('重复')>0 or sdata['msg'].find('成功')>0:
           msg='今日已经签到,'
     else:
        msg='今日已经签到,'
     msg+=f'''已经签到{data['alreadySignInDays']}天'''
     loger(msg)
   except Exception as e:
       print(str(e))
       
def userSigninNew():
   print('\n signin_userSigninNew')
   try:
     body = {"channel":"qiandao_baibaoxiang"}
     data=json.loads(iosrule('signin%2FuserSigninNew',body).text)
     print(data['msg'])
     return data
   except Exception as e:
       print(str(e))
       
       
def Daojia_getUserAccountInfo():
   print('\n  Daojia_getUserAccountInfo')
   try:
     
     data=json.loads(requests.get(url,headers=zyheaders).text)
     #print(data)
     accountInfo=data['result']['accountInfo']['infos'][0]
     userBaseInfo=data['result']['userInfo']['userBaseInfo']
     
     msg=f'''{userBaseInfo['userName']}|{userBaseInfo['nickName']}|{userBaseInfo['mobile']}|{accountInfo[0]['accName']}{accountInfo[0]['value']}|{accountInfo[1]['accName']}{accountInfo[1]['value']}|{accountInfo[3]['accName']}{accountInfo[3]['value']}
     '''
     loger(msg)
     
   except Exception as e:
       print(str(e))
       
       
       

def tasklist_Daojia():
   print('\n tasklist_Daojia')
   try:
     body = {"modelId":"M10001","plateCode":1}
     data=json.loads(iosrule('task%2Flist',body).text)
     #print(data)
     print('到家任务列表')
     for itm in data['result']['taskInfoList']:
       if itm['status']==3:
          m='【完成】'
       elif itm['status']==2:
          m='【领奖】'
       else:
          m='【未完成】'+str(itm['status'])
       print(f'''{itm['taskName']}={itm['taskType']}=={m}''')
     print('\n-----------------------')
     kk=0
     for itm in data['result']['taskInfoList']:
       kk+=1
       if itm['status']==3:
         print(f'''任务{len(data['result']['taskInfoList'])}-{str(kk)}: {itm['taskType']} -{itm['taskName']}-{itm['status']}已经完成✌🏻️✌🏻️✌🏻️✌🏻️''')
       if itm['status']!=3:
         print(f'''开始任务{len(data['result']['taskInfoList'])}-{str(kk)}: {itm['taskType']} -{itm['taskName']}-{itm['status']}🎁🎁🎁🎁''')
         if itm['status']==1 or itm['status']==0:
           if itm['taskType']!=506:
            task_received(itm['modelId'],itm['taskId'],itm['taskType'],5)
            time.sleep(2)
            task_finished(itm['modelId'],itm['taskId'],itm['taskType'],5)
            
         if itm['status']==2:
           if itm['taskType']==513:
              task_sendPrize(itm['modelId'],itm['taskId'],itm['taskType'],1,5)
              task_sendPrize(itm['modelId'],itm['taskId'],itm['taskType'],2,5)
              task_sendPrize(itm['modelId'],itm['taskId'],itm['taskType'],3,5)

           else:
           	  task_sendPrize(itm['modelId'],itm['taskId'],itm['taskType'],0,5)
           time.sleep(2)
   except Exception as e:
       print(str(e))

def task_do(taskType):
   print('\n task_do___'+str(taskType))
   try:
      if taskType==401:
         fun='xapp%2FfriendHelp%2Flist'
         body={}
      if taskType==502:
         fun='signin%2FifClickedCouponButton'
         body={}
         
      data=json.loads(iosrule(fun,body).text)
      print(data)
      print(data['msg'])
   except Exception as e:
       print(str(e))
         
         
         
def task_received(modelId,taskId,taskType,plateCode=1):
   print('\n task_received')
   try:
     body = {"modelId":modelId,"taskId":taskId,"taskType":taskType,"plateCode":plateCode}
     data=json.loads(iosrule('task%2Freceived',body).text)
     print(data['msg'])
   except Exception as e:
       print(str(e))
       
def task_sendPrize(modelId,taskId,taskType,subNode=1,plateCode=1):
   print('\n task_sendPrize')
   try:
     body = {"modelId":modelId,"taskId":taskId,"taskType":taskType,"plateCode":plateCode}
     if taskType==513:
       body = {"modelId":modelId,"taskId":taskId,"taskType":taskType,"plateCode":plateCode,"subNode":subNode}
     
     data=json.loads(iosrule('task%2FsendPrize',body).text)
     print(data['msg'])
   except Exception as e:
       print(str(e))
       
       
def task_finished(modelId,taskId,taskType,plateCode=1):
   print('\n task_finished')
   try:
     body = {"modelId":modelId,"taskId":taskId,"taskType":taskType,"plateCode":plateCode}
     data=json.loads(iosrule('task%2Ffinished',body).text)
     print(data['msg'])
   except Exception as e:
       print(str(e))


       
def plantBeans_watering():
   print('\n  plantBeans_watering')
   try:
     body ={"activityId":"23ad8d84d6addad"}
     body=urllib.parse.quote(json.dumps(body))
     data=json.loads(iosrulex('functionId=plantBeans%2Fwatering&isNeedDealError=true&method=POST&body='+body).text)
     print(data)

    
   except Exception as e:
       print(str(e))
       
       
       
def plantBeans_getWater():
   print('\n  plantBeans_getWater')
   try:
     body ={"activityId":"23ad8d84d6addad"}
     body=urllib.parse.quote(json.dumps(body))
     data=json.loads(iosrulex('functionId=plantBeans%2FgetWater&isNeedDealError=true&method=POST&body='+body).text)
     print(data)

    
   except Exception as e:
       print(str(e))



def pigPetAddFood():
   print('\n  pigPetAddFood')
   try:
   	
      body='reqData=%7B%22skuId%22%3A%221001003001%22%2C%22channelLV%22%3A%22%22%2C%22source%22%3A0%2C%22riskDeviceParam%22%3A%22%7B%5C%22macAddress%5C%22%3A%5C%22%5C%22%2C%5C%22imei%5C%22%3A%5C%22%5C%22%2C%5C%22eid%5C%22%3A%5C%227PEOIPEPFSAQTKCFO6D3R7AKUVSCGGCA4CFQT7TY5GJZ2ONFU2DNUVVLDNUDMZ7SS4BF4RLI66RUA3LYLD6SYWXNII%5C%22%2C%5C%22openUUID%5C%22%3A%5C%22%5C%22%2C%5C%22uuid%5C%22%3A%5C%22%5C%22%2C%5C%22traceIp%5C%22%3A%5C%22%5C%22%2C%5C%22os%5C%22%3A%5C%22%5C%22%2C%5C%22osVersion%5C%22%3A%5C%22%5C%22%2C%5C%22appId%5C%22%3A%5C%22%5C%22%2C%5C%22clientVersion%5C%22%3A%5C%22%5C%22%2C%5C%22resolution%5C%22%3A%5C%22%5C%22%2C%5C%22channelInfo%5C%22%3A%5C%22%5C%22%2C%5C%22networkType%5C%22%3A%5C%22%5C%22%2C%5C%22startNo%5C%22%3A42%2C%5C%22openid%5C%22%3A%5C%22%5C%22%2C%5C%22token%5C%22%3A%5C%22CO6NDE35KVOIEKPZJZGHWMHMDHAKDQTIRH4JPO4NPYNJWYOTRGRO5OWBXJNKHH64UCF3MZYJC5JMY%5C%22%2C%5C%22sid%5C%22%3A%5C%22%5C%22%2C%5C%22terminalType%5C%22%3A%5C%22%5C%22%2C%5C%22longtitude%5C%22%3A%5C%22%5C%22%2C%5C%22latitude%5C%22%3A%5C%22%5C%22%2C%5C%22securityData%5C%22%3A%5C%22%5C%22%2C%5C%22jscContent%5C%22%3A%5C%22%5C%22%2C%5C%22fnHttpHead%5C%22%3A%5C%22%5C%22%2C%5C%22receiveRequestTime%5C%22%3A%5C%22%5C%22%2C%5C%22port%5C%22%3A80%2C%5C%22appType%5C%22%3A%5C%22%5C%22%2C%5C%22deviceType%5C%22%3A%5C%22%5C%22%2C%5C%22fp%5C%22%3A%5C%22f0cbd9bc1239226025501e2d34b891d8%5C%22%2C%5C%22ip%5C%22%3A%5C%22%5C%22%2C%5C%22idfa%5C%22%3A%5C%22%5C%22%2C%5C%22sdkToken%5C%22%3A%5C%22%5C%22%7D%22%7D'
      header=headers
      header['Cookie']=Cookiem
      response=requests.post('https://ms.jr.jd.com/gw/generic/uc/h5/m/pigPetAddFood?_=1608957714442',headers=header,data=body)
      print(response.text)

    
   except Exception as e:
       print(str(e))
       
def iosrule(functionId,body={}):
   url=JD_API_HOST+f'''&functionId={functionId}&isNeedDealError=true&body={urllib.parse.quote(json.dumps(body))}&channel=ios&platform=6.6.0&platCode=h5&appVersion=6.6.0&appName=paidaojia&deviceModel=appmodel'''
   try:
      response=requests.get(url,headers=djheaders)
      return response
   except Exception as e:
     print(f'''初始化{functionId}任务:''', str(e))


def iosrulex(body):
   url=JD_API_HOST
   try:
      response=requests.post(url,headers=djheaders,data=body)
      return response
   except Exception as e:
     print(f'''初始化{functionId}任务:''', str(e))
def TotalBean(cookies,checkck):
   print('检验过期')
   signmd5=False
   headers= {
        "Cookie": cookies,
        "Referer": 'https://home.m.jd.com/myJd/newhome.action?',
        "User-Agent": 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.1 Mobile/15E148 Safari/604.1'
      }
   try:
       ckresult= requests.get('https://wq.jd.com/user_new/info/GetJDUserInfoUnion?orgFlag=JD_PinGou_New',headers=headers,timeout=10).json()
       #print(ckresult)
       if ckresult['retcode']==0:
           signmd5=True
           loger(f'''【京东{checkck}】''')
       else:
       	  signmd5=False
       	  msg=f'''【京东账号{checkck}】cookie已失效,请重新登录京东获取'''
       	  print(msg)
          pushmsg(msg)
   except Exception as e:
      signmd5=False
      msg=str(e)
      print(msg)
      pushmsg('京东cookie',msg)
   return signmd5

def check(flag,list):
   vip=''
   global djj_bark_cookie
   global djj_sever_jiang
   if "DJJ_BARK_COOKIE" in os.environ:
     djj_bark_cookie = os.environ["DJJ_BARK_COOKIE"]
   if "DJJ_SEVER_JIANG" in os.environ:
      djj_sever_jiang = os.environ["DJJ_SEVER_JIANG"]
   if flag in os.environ:
      vip = os.environ[flag]
   if flag in osenviron:
      vip = osenviron[flag]
   if vip:
       for line in vip.split('\n'):
         if not line:
            continue 
         list.append(line.strip())
       return list
   else:
       print(f'''【{flag}】 is empty,DTask is over.''')
       exit()

def pushmsg(title,txt,bflag=1,wflag=1):
   txt=urllib.parse.quote(txt)
   title=urllib.parse.quote(title)
   if bflag==1 and djj_bark_cookie.strip():
      print("\n【通知汇总】")
      purl = f'''https://api.day.app/{djj_bark_cookie}/{title}/{txt}'''
      response = requests.post(purl)
      #print(response.text)
   if wflag==1 and djj_sever_jiang.strip():
      print("\n【微信消息】")
      purl = f'''http://sc.ftqq.com/{djj_sever_jiang}.send'''
      headers={
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'
    }
      body=f'''text={txt})&desp={title}'''
      response = requests.post(purl,headers=headers,data=body)
   global result
   print(result)
   result =''
    
def loger(m):
   print(m)
   global result
   result +=m
    
def islogon(j,count):
    JD_islogn=False
    global jd_name
    for i in count.split(';'):
       if i.find('pin=')>=0:
          jd_name=i.strip()[i.find('pin=')+4:len(i)]
          print(f'''>>>>>>>>>【账号{str(j)}开始】{jd_name}''')
    if(TotalBean(count,jd_name)):
        JD_islogn=True
    return JD_islogn
   
def clock(func):
    def clocked(*args, **kwargs):
        t0 = timeit.default_timer()
        result = func(*args, **kwargs)
        elapsed = timeit.default_timer() - t0
        name = func.__name__
        arg_str = ', '.join(repr(arg) for arg in args)
        print('[🔔运行完毕用时%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, result))
        return result
    return clocked
    
@clock
def start():
 

   global djheaders,zyheaders,url,yuanck
   check('DJJ_DAOJIA_COOKIE',cookiesList)
   check('DJJ_DAOJIA_URL',urlList)
   check('DJJ_YUAN_CK',yuanckList)
   j=0
   #for i in range(2):
   for count in cookiesList:
        j+=1
        if j!=1:
          continue
        djheaders['Cookie']=count
        url=urlList[j-1]
        yuanck=yuanckList[j-1]
        zyheaders['Cookie']=yuanck
        JD_Daojia()
     #time.sleep(30)
   pushmsg('JD_DaoJia',result)
if __name__ == '__main__':
       start()