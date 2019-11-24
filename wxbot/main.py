# -*- coding: utf-8 -*-
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import itchat
import time
from itchat.content import *
from wxbot import dataprocess
from wxbot import gvariable as gl
from apscheduler.schedulers.background import BackgroundScheduler

# 群聊名称
groupnamelist=[]
# 为了每次唯一确定一个group
groupnametransfer = {}
#群聊指定关键词
groupkeys = {}
#每10分钟进行一次存储
msgfromGroup =[]


# 获取群成员聊天记录。
@itchat.msg_register(TEXT, isGroupChat=True)
def text_record(msg):
    global msgfromGroup
    # 格式为#群聊名#用户昵称#信息内容#时间   这里要注意群聊中的用户昵称会改变，同时要判断自己的昵称···\
    try:
        gname = groupnametransfer[msg['FromUserName']]
        if gname == u'我':
            gname = groupnametransfer[msg['ToUserName']]
    except KeyError:
            gname = u'无关群聊'
    if gname == u'无关群聊':
        return
    msg.text=msg.text.replace('\n', '')
    formatmsg = gname+'\t'+msg.actualNickName+'\t'+msg.text+'\t' + \
                time.strftime(u"%Y-%m-%d %H:%M:%S", time.localtime())

    msgfromGroup.append(formatmsg)
    print(msgfromGroup[-1])

# 通过群名称获取群成员列表，放入统计字典里。  要考虑两个群会有相同的成员，所以要区别对待··· 这里写入文件里
def getchatroom_friendlist(chatroomNamelist):

    filename = gl.CHAT_DATA_PATH + gl.FRIENDLIST_TFILE
    file = open(filename, 'w',encoding='UTF-8')
    itchat.get_chatrooms(update=True)
    for chatroomName in chatroomNamelist:
        chatrooms = itchat.search_chatrooms(name=chatroomName)
        # print(chatrooms)
        if chatrooms:  # 这里是有bug的··· 改成 if chatrooms 就好了，再改了一下逻辑。
            chatroom = itchat.update_chatroom(chatrooms[0]['UserName'])
            # print(chatroom['UserName'])
            # print(chatroom)
            file.write(u'-----------' + chatroomName + u'------------' + '\n')
            for friend in chatroom['MemberList']:
                file.write(friend['NickName'] + '\n')
        else:
            print(u'没有找到群聊：' + chatroomName)


# 作为定时运行函数，定时向群内发送任务,接受参数消息内容和群聊名称
def send_msg(msgcontent, groupname):
    print('schedule execute' + groupname)
    itchat.get_chatrooms(update=True)
    uname = dataprocess.get_key(groupnametransfer, groupname)
    itchat.update_chatroom(uname[0])
    itchat.send(msgcontent, uname[0])

# 转换群名到username，每次登陆username都不同
def getgname(namelist):
    global groupnametransfer
    for gname in namelist:
        itchat.get_chatrooms(update=True)
        chatrooms = itchat.search_chatrooms(name=gname)
        if chatrooms:
            chatroom = itchat.update_chatroom(chatrooms[0]['UserName'])
            groupnametransfer.setdefault(chatroom['UserName'], gname)

    # 在这里将自己的username加进去s
    myusername=itchat.search_friends()
    groupnametransfer.setdefault(myusername['UserName'], '我')


# 定时存储聊天记录
def store():
    global msgfromGroup
    dataprocess.storetofile(msgfromGroup)
    #对聊天记录进行排序，存入到暂时的文件，每隔一段时间进行一次统计
    msgfromGroup.sort()
    dataprocess.storetotempfile(msgfromGroup)
    msgfromGroup.clear()
    dataprocess.statictempfile()

def sendtomyself():
    itchat.send('Hello, filehelper', toUserName='filehelper')

def sendtomaps():
    mps = itchat.get_mps()
    userName = mps[0]['UserName']
    itchat.send("hello", toUserName=userName)

#读取配置文件对程序进行初始化
def readconfigure():
    fname=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+ gl.PATH_SEPARATOR+'configure.txt'
    file = open(fname, 'r',encoding ='UTF-8')
    global groupnamelist
    global groupkeys
    # 根据类型
    for line in file.readlines():
        line = line.strip('\n')
        typetag = line.split('#', 1)
        if typetag[0] == '1':
            getname = typetag[1].split('#', 1)
            if len(getname) == 1:
                groupnamelist.append(getname[0])
                groupkeys.setdefault(getname[0], [])
            else:
                groupnamelist.append(getname[0])
                groupkeys.setdefault(getname[0], getname[1].split('#'))
        if typetag[0] == '2':
             getname= typetag[1].split('#')
             scheduler.add_job(send_msg, 'cron', day='*', hour=getname[1], minute=getname[2], second=getname[3],
                               args=(getname[4], getname[0]))

# 登陆后运行
def after_login():
    readconfigure()
    gl.GROUP_NAMELIST = groupnamelist
    gl.GROUP_KEYS = groupkeys
    dataprocess.createdatadir()  # 创建文件存储目录
    getgname(groupnamelist)  # 获取群聊中人员信息
    scheduler.add_job(store, 'cron', day='*', hour='*', minute='*/2', second=0)  # 只能传函数本身，so？
    scheduler.add_job(sendtomyself, 'cron', day='*', hour='*', minute='*/10', second=0)
    scheduler.add_job(sendtomaps, 'cron', day='*', hour='*', minute='*/10', second=0)
    scheduler.start()

# 注销后运行，手机端推出网页微信或断网··!!!!终止程序不会触发
def after_logout():
    scheduler.shutdown()
    dataprocess.storetofile(msgfromGroup)
    print('logout')


if __name__ == '__main__':
 
    scheduler = BackgroundScheduler()
    itchat.auto_login(hotReload=True, loginCallback=after_login, exitCallback=after_logout)
    getchatroom_friendlist(groupnamelist)
    itchat.run()
