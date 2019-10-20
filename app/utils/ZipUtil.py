import os
import shutil
import zipfile
# from definitions import ROOT_DIR
ROOT_DIR='../../resources/pics'

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
    files={os.path.join(ROOT_DIR,'0a5850f8762011e9a52d185680cf589a.png'),
           os.path.join(ROOT_DIR,'0c6ed04aee4f11e9b1cfacde48001122.png'),
           os.path.join(ROOT_DIR,'1d498c40762011e99d6a185680cf589a.png'),
           os.path.join(ROOT_DIR,'1e5187aedc1a11e988baacde48001122.png'),
           os.path.join(ROOT_DIR,'2aa392a2ef6311e9a924f45c89b10987.jpg'),

           os.path.join(ROOT_DIR,'20190920230723.png'),
           os.path.join(ROOT_DIR,'20190920230811.png'),
           os.path.join(ROOT_DIR,'20190920232213.png'),
           os.path.join(ROOT_DIR,'20190920232228.png'),
           os.path.join(ROOT_DIR,'20190922221359.png'),

           os.path.join(ROOT_DIR,'20191015181036.png'),
           os.path.join(ROOT_DIR,'20191015181341.png'),
           os.path.join(ROOT_DIR,'20191015182912.png'),
           os.path.join(ROOT_DIR,'20191015183013.png'),
           os.path.join(ROOT_DIR,'20191015183111.png'),}
    compress_listfiles(zipName,files)