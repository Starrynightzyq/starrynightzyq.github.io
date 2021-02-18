'''
Author: your name
Date: 2021-02-18 16:12:09
LastEditTime: 2021-02-18 18:23:57
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: /Starrynightzyq.bak/tasks/update-post-timestamps.py
'''
import os
import re
import time
import datetime

'''把时间戳转化为时间: 1479264792 to 2016-11-16 10:53:12'''
def TimeStampToTime(timestamp):
    timeStruct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S',timeStruct)

'''获取文件的大小,结果保留两位小数，单位为MB'''
def get_FileSize(filePath):
    filePath = str(filePath)
    fsize = os.path.getsize(filePath)
    fsize = fsize/float(1024*1024)
    return round(fsize,2)

'''获取文件的访问时间'''
def get_FileAccessTime(filePath):
    filePath = str(filePath)
    t = os.path.getatime(filePath)
    return TimeStampToTime(t)

'''获取文件的创建时间'''
def get_FileCreateTime(filePath):
    filePath = str(filePath)
    t = os.path.getctime(filePath)
    return TimeStampToTime(t)

'''获取文件的修改时间'''
def get_FileModifyTime(filePath):
    filePath = str(filePath)
    t = os.path.getmtime(filePath)
    return TimeStampToTime(t)

def alter(file,old_str,new_str):
    """
    替换文件中的字符串
    :param file:文件名
    :param old_str:就字符串
    :param new_str:新字符串
    :return:
    
    """
    file_data = ""
    with open(file, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i < 10:
                line = re.sub(old_str, new_str, line)
            file_data += line
    with open(file,"w",encoding="utf-8") as f:
        f.write(file_data)

def update_FileModifyTime():
    diff_files = os.popen('git diff --staged --name-only').read().splitlines()
    md_files = [f for f in diff_files if os.path.splitext(f)[-1] == '.md']
    print(md_files)

    for f_md in md_files:
        ModifyTime = get_FileModifyTime(f_md)
        alter(f_md, r'updated: (\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2})', 'updated: '+ModifyTime)
        os.system(r'git add ' + f_md)

if __name__ == "__main__":
    TMP_FILE = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'tmp')
    update_FileModifyTime()