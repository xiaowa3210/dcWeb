#!/usr/bin/env python 
# _*_ coding: utf-8 _*_
import time, os, ftplib

host = '47.107.103.134' #ftp 地址用户名密码
username = 'ftpu'
password = 'x123456'

f = ftplib.FTP(host)  # 实例化FTP对象
f.connect(host, 21)
f.login(username, password)  # 登录
f.set_pasv(0)

'''
从服务器路径上传到ftp
local_path 带斜杠的本地路径如 d:/resources/
file_name 文件名 例如 1.jpg
remote_pre_url 上传成功后拼接url的前缀，带斜杠 如 http://dc.blfly.com/resources/
'''
def ftp_upload( local_path, file_name):

    daystr = time.strftime('%Y%m%d', time.localtime())#年月日 如 20181007
    secStr = time.strftime('%H%M%S', time.localtime())#时分秒 如 092936

    (shotname, extension) = os.path.splitext(file_name)#判断工作路径，路径加上年月日
    if(extension == 'jpg' or extension == 'png' or extension == 'bmp'): # 根据文件后缀决定上传的路径
        ftp_mid = '/pub/images/' + daystr + '/'
        remote_pre_url = 'http://dc.blfly.com/resources/images/' + daystr +'/'
    else:
        ftp_mid = '/pub/' + daystr + '/'
        remote_pre_url = 'http://dc.blfly.com/resources/' + daystr +'/'

    try:
        f.cwd(ftp_mid)  # 改变路径
    except:
        f.mkd(ftp_mid)# 如果没有此路径则创建路径
    finally:
        f.cwd(ftp_mid)  # 改变路径

    print("FTP当前路径:", f.pwd())
    print(f.nlst())#列出当前路径下所有文件
    file_url = ''
    try:
        bufsize = 1024  # 设置缓冲器大小
        fp = open(local_path + file_name, 'rb')
        print(fp)
        f.storbinary('STOR ' + secStr + file_name, fp, bufsize)
        file_url = remote_pre_url + secStr + file_name
    except Exception as e:
        print(e)
    finally:
        fp.close()
        f.quit()
        print(file_url)
        return file_url #返回附件链接

def ftp_download():
    '''以二进制形式下载文件'''
    file_remote = '1.txt'
    file_local = 'D:\\test_data\\ftp_download.txt'
    bufsize = 1024  # 设置缓冲器大小
    fp = open(file_local, 'wb')
    f.retrbinary('RETR %s' % file_remote, fp.write, bufsize)
    fp.close()
    f.quit()

