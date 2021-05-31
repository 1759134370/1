import parser
import bs4
from bs4 import BeautifulSoup  
import re
import urllib
import urllib.request,urllib.error   
import requests
import lxml
from urllib import request, parse
import urllib.request
from urllib import request
from prettytable import PrettyTable
import smtplib    #邮箱
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.header import Header
import pandas as pd
from texttable import Texttable





'''
xuenian = input("请输入学年 例如(2020-2021)")
xueqi = input ("请输入第几学期")
'''

loginurl = '学校教务网地址'

headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'DNT': '1',
        'Host': 'jw1.hustwenhua.net',
        'Origin': 'http://jw1.hustwenhua.net',
        'Referer': '学校教务网地址',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.66',
       }
paramss = {
    'gnmkdm':'N121613',
    }
params = {
    '__EVENTTARGET':'', 
    '__EVENTARGUMENT':'',
    'hidLanguage': '',
    'ddlXN': '2020-2021',
    'ddlXQ': '1',
    'ddl_kcxz': '',
    'btn_xn': '',
    }
headerss = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'DNT': '1',
    'Host': 'jw1.hustwenhua.net',
    'Origin': 'http://jw1.hustwenhua.net',
    'Referer': 'http://jw1.hustwenhua.net/(s5su4a45ptsokz45r2uz022y)/default2.aspx',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.66',
    }
denglu = requests.get(loginurl,headers=headers)


url = '在network看到的url地址'
req = requests.get(url,data=paramss,headers=headers)


#获取__VIEWSTATE
html = req.content.decode('gb2312')
viewstate = re.search('<input type="hidden" name="__VIEWSTATE" value="(.+?)"',html)
params['__VIEWSTATE'] = viewstate.group(1)
#传参登录
red = requests.post(url,data=params,headers=headerss)

soup = BeautifulSoup(red.content.decode('gb2312'),'html.parser')
[s.extract() for s in soup(['a '])]
html = soup.find('table',class_='datelist')
#注：也可以用pandas做具体方法参考下面课程表
print('你的所有成绩如下：')
#指定要输出的列，原网页的表格列下标从0开始
outColumn = [1,2,3,4,6,7,8,9]
#用于标记是否是遍历第一行
flag = True
#根据DOM解析所要数据，首位的each是NavigatableString对象，其余为Tag对象
#遍历行
for each in html:
    columnCounter = 0
    column = []
    if(type(each) == bs4.element.NavigableString):
        pass
    else:
        #遍历列
        for item in each.contents:
            if(item != '\n'):
                if columnCounter in outColumn:
                    #要使用str转换，不然陷入copy与deepcopy的无限递归
                    column.append(str(item.contents[0]).strip())
                columnCounter += 1
        if flag:
            table = PrettyTable(column)
            flag = False
        else:
            table.add_row(column)
print(table)
f = open('你的txt保存地址','a',encoding='utf-8')
f.write(str(table))
f.close()


#发送邮件
file = '你的txt保存地址'
host = 'smtp.qq.com'
port = 465
#qq邮箱和授权码
username = 'qq邮箱'
password = '授权码'
#发送账户
to_addr = '你要发送的邮箱'

message = MIMEMultipart()
message['From'] = Header("实验", 'utf-8')
message['To'] =  Header("测试", 'utf-8')
subject = '你的期末成绩'
message['Subject'] = Header(subject, 'utf-8')
message.attach(MIMEText('这是你当前出来的成绩','plain','utf-8'))  #邮件内容
msg1 = MIMEText(open(file,'rb').read(),'base64', 'utf-8')  #邮件附件
msg1["Content-Type"] = 'application/octet-stream'
msg1["Content-Disposition"] = 'attachment;filename="chengji.txt"'
message.attach(msg1)
server = smtplib.SMTP_SSL(host,)
server.connect(host,port)
server.login(username,password)    #登录smtp服务
server.sendmail(username,to_addr,message.as_string())
server.quit()
print("发送成功")


#爬取课程表
data = {
    'gnmkdm': 'N121602',
    }
urlkecheng = '在network看到的url地址'
kecheng = requests.get(urlkecheng,data= data,headers=headers)  #登录
kebiao = BeautifulSoup(kecheng.content.decode('gb2312'),'html.parser')

htmls = kebiao.find('table',class_='blacktab')


fp = open('文件保存地址','w',encoding='utf-8')
fp.write(str(kebiao))
fp.close
pd.set_option('display.unicode.ambiguous_as_wide', True)  #设置pd表格参数
pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)
df_data = pd.read_html('文件保存地址')
print(df_data)
'''
注：将课程表以cvs的形式保存到本地！！！未做完！！！
for i in df_data:
    table_data = pd.DataFrame(i)
    table_data.to_csv('table_.csv')
'''
