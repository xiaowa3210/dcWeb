import os
import shutil
import zipfile
# from definitions import ROOT_DIR
ROOT_DIR='D:/web/dcWeb/dcWeb/rootdir'

#打包单个文件
def compress_singlefile(zipName,filename):
    with zipfile.ZipFile(zipName, 'w') as z:
        z.write(filename)


#压缩某个文件夹的所有文件
# zipfilename是压缩包名字，dirname是要打包的目录
def compress_files(zipfilename, dirname):
    if os.path.isfile(dirname):
        with zipfile.ZipFile(zipfilename, 'w') as z:
            z.write(dirname)
    else:
        with zipfile.ZipFile(zipfilename, 'w') as z:
            for root, dirs, files in os.walk(dirname):
                for single_file in files:
                    if single_file != zipfilename:
                        filepath = os.path.join(root, single_file)
                        z.write(filepath)

def addfile(zipfilename, dirname):
    if os.path.isfile(dirname):
        with zipfile.ZipFile(zipfilename, 'a') as z:
            z.write(dirname)
    else:
        with zipfile.ZipFile(zipfilename, 'a') as z:
            for root, dirs, files in os.walk(dirname):
                for single_file in files:
                    if single_file != zipfilename:
                        filepath = os.path.join(root, single_file)
                        z.write(filepath)



#将指定为文件名集合打包成一个压缩包
def compress_listfiles(zipfilename,files):
    cwd = os.getcwd()
    copy(cwd,files)                     #先将文件复制到当前目录
    filenames = [os.path.basename(path) for path in files]
    #打包压缩包
    with zipfile.ZipFile(zipfilename, 'w') as z:
            for single_file in filenames:
                if single_file != zipfilename:
                    z.write(single_file)
    #删除文件
    remove(cwd,filenames)


#将文件复制到某个文件夹
def copy(destRir,files):
    print(destRir)
    for file in files:
        shutil.copy(file,destRir)

#删除某个文件夹下的文件
def remove(dirname,filenames):
    for filename in filenames:
        os.remove(os.path.join(dirname,filename))

if __name__ == '__main__':
    zipName = os.path.join(ROOT_DIR, 'log.zip')
    filename = os.path.join(ROOT_DIR,'info.log')
    dirName = os.path.join(ROOT_DIR,'zip')
    files={os.path.join(ROOT_DIR,'info.log'),
           os.path.join(ROOT_DIR,'info1.log'),
           os.path.join(ROOT_DIR, '总结.pdf'),
           os.path.join(ROOT_DIR, '流浪地球-1.jpg'),
           os.path.join(ROOT_DIR, '高清护眼电脑桌面壁纸.jpg')}
    # files={'info.log','info1.log'}
    # compress_singlefile(zipName,'info1.log')
    # compress_files(zipName,dirName)
    compress_listfiles(zipName,files)
    # addfile(zipName,files)

    # copy(os.path.join(ROOT_DIR,'zip'),files)