#!/usr/bin/env python 
# _*_ coding: utf-8 _*_
import ftplib # FTP操作


host = '47.107.103.134' #ftp 地址用户名密码
username = 'ftpu'
password = 'x123456'

f = ftplib.FTP(host)  # 实例化FTP对象
f.connect(host, 21)
f.login(username, password)  # 登录
f.set_pasv(0)

'''
从服务器路径上传到ftp
local_path 文件本地路径 d:/files
file_name 文件名 例如 1.jpg
remote_pre_url 上传成功后拼接url的前缀 如 http://dc.blfly.com/files
'''
def ftp_upload( local_path, file_name, remote_pre_url, ftp_mid):

    try:
        f.cwd(ftp_mid)  # 改变路径
    except:
        f.mkd(ftp_mid)# 如果没有此路径则创建路径
    finally:
        f.cwd(ftp_mid)  # 再改变路径

    print("FTP当前路径:", f.pwd())
    print(f.nlst())#列出当前路径下所有文件
    file_url = ''
    try:
        bufsize = 1024  # 设置缓冲器大小
        fp = open(local_path + file_name, 'rb')
        print(fp)
        f.storbinary('STOR ' + file_name, fp, bufsize)
        file_url = remote_pre_url + file_name
    except Exception as e:
        print(e)
    finally:
        fp.close()
        f.quit()
        print(file_url)
        return file_url




def ftp_download():
    '''以二进制形式下载文件'''
    file_remote = '1.txt'
    file_local = 'D:\\test_data\\ftp_download.txt'
    bufsize = 1024  # 设置缓冲器大小
    fp = open(file_local, 'wb')
    f.retrbinary('RETR %s' % file_remote, fp.write, bufsize)
    fp.close()
    f.quit()

