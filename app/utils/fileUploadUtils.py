#!/usr/bin/env python 
# _*_ coding: utf-8 _*_

# FTP操作
import ftplib

#服务器files文件夹

FTP_SERVER_PATH = "/pub/"
FILE_URL = ''

#ftp 地址用户名密码
host = '47.107.103.134'
username = 'ftpu'
password = 'x123456'
#file = '1.txt'

f = ftplib.FTP(host)  # 实例化FTP对象
f.login(username, password)  # 登录


'''
local_path 文件本地路径 d:/files
file_name 文件名 例如 1.jpg
remote_pre_url 上传成功后拼接url的前缀 如 http://dc.blfly.com/files
'''
def ftp_upload( local_path, file_name, remote_pre_url):
    '''以二进制形式上传文件'''

    remote_pre_url = "http://dc.blfly.com/files/"

    # 改变并获取当前路径
    f.cwd("/pub")
    print("FTP当前路径:", f.pwd())

    if(not local_path.endswith('/')):
        local_path = local_path + "/"

    try:
        bufsize = 1024  # 设置缓冲器大小
        fp = open(local_path + file_name, 'rb')
        f.storbinary(FTP_SERVER_PATH + file_name, fp, bufsize)
        FILE_URL = remote_pre_url + file_name
    except Exception as e:
        print(e)
    finally:
        fp.close();
        f.quit();

    return FILE_URL



# 逐行读取ftp文本文件
# f.retrlines('RETR %s' % file)

def ftp_download():
    '''以二进制形式下载文件'''
    file_remote = '1.txt'
    file_local = 'D:\\test_data\\ftp_download.txt'
    bufsize = 1024  # 设置缓冲器大小
    fp = open(file_local, 'wb')
    f.retrbinary('RETR %s' % file_remote, fp.write, bufsize)
    fp.close()


#ftp_download()
#ftp_upload()
#f.quit();