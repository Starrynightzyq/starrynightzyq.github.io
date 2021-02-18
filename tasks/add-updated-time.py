'''
Author: your name
Date: 2021-02-18 18:03:25
LastEditTime: 2021-02-18 18:45:01
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: /Starrynightzyq.bak/tasks/update-post-timestamps-old.py
'''
import glob
import os
import re
import time
import datetime

def get_MdFile():
    _posts_dir = os.path.relpath(os.path.join(os.path.split(os.path.abspath(__file__))[0], '../source/_posts/*.md'))
    md_files = glob.glob(_posts_dir)
    return md_files

'''把时间戳转化为时间: 1479264792 to 2016-11-16 10:53:12'''
def TimeStampToTime(timestamp):
    timeStruct = time.localtime(int(timestamp))
    return time.strftime('%Y-%m-%d %H:%M:%S',timeStruct)

def get_FileModifyTime_FromGitLog(filePath):
    filePath = str(filePath)
    ModifyTime = os.popen("git log --pretty=format:%at -- {0} | sort | tail -n 1".format(filePath)).read()
    return TimeStampToTime(ModifyTime)

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
            if i == 5 and re.match(old_str, line) == None:
                file_data += new_str
                print("add modify time for: ", file, new_str)
            file_data += line
    with open(file,"w",encoding="utf-8") as f:
        f.write(file_data)


if __name__ == "__main__":
    md_files = get_MdFile()
    # print(md_files)
    for f in md_files:
        ModifyTime = get_FileModifyTime_FromGitLog(f)
        # print(f, "ModifyTime: ",ModifyTime)
        alter(f, r'updated: (\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2})', 'updated: '+ModifyTime+'\r')
        
