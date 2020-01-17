#!/usr/bin/python
# coding:utf-8
import datetime
import os
import sys

import commands

"""
author:jimw
date:2020-01-14

支持范围：
1、newWebSite.log.2019-05-14

2、catalina.2019-01-03.out
python zipFile.py /home/webApp/logs
根据月份打包
然后删除历史的数据
zip logging
"""


# 返回需要打包的集合
def loggingFile(filepath):
    # 遍历filepath下所有文件，包括子目录 下个小版本优化
    files = os.listdir(filepath)

    # 这里必须排序，不然无法整合出数据
    files.sort()
    now = datetime.datetime.now()
    # 得到今年的的时间 （年份） 得到的today_year等于2019年

    # 修改一个bug 月份转str是int的
    today_month = str(now.year) + '-' + (str(now.month), '0' + str(now.month))[str(now.month).__len__() >= 1]
    print('today_month:', today_month)
    ###
    data_list_todays = []
    data_list_files = []
    remove_data_list_files = []
    dictName = dict()
    flagName = ''
    os.chdir(filepath)
    for fi in files:

        fi_d = os.path.join(filepath, fi)
        if not os.path.isdir(fi_d):
            varName = os.path.join(filepath, fi_d)
            varName = varName.split('/')[-1]
            # 文件名统计
            if (varName.split('.')[1] == 'log'):
                varFileName = varName.split('.')[0] + '.' + varName.split('.')[1]
            else:
                varFileName = varName.split('.')[0]
            if flagName == '':
                # flagName = varFileName
                print()
            elif flagName != varFileName:
                data_list_todays = []
            flagName = varFileName
            #print('flagName:', flagName)
            data_list_files.append(varFileName)

            # 判断是否重复
            if containsDuplicate(data_list_files):
                data_list_files.remove(varFileName)
                # print(data_list_files)
                # 月份统计
                # print(varFileName)
            try:

                if (varName.split('.')[1] == 'log'):
                    varNameindex = varName.split('.')[2]
                    varNameMonth = varNameindex.split('-')[0] + '-' + varNameindex.split('-')[1]
                else:
                    varNameindex = varName.split('.')[1]
                    varNameMonth = varNameindex.split('-')[0] + '-' + varNameindex.split('-')[1]
                if (varNameMonth == today_month):
                    print('当前月份不压缩')
                    continue
                # print(varNameMonth)
            except(Exception):
                # print(varName)
                continue
            data_list_todays.append(varNameMonth)
            if containsDuplicate(data_list_todays):
                data_list_todays.remove(varNameMonth)
                # pythodata_list_todays.reverse()
            data_list_todays.reverse()
            print(data_list_todays)
            dictName[varFileName] = data_list_todays
            if fi_d.find('.gz')==-1:
                remove_data_list_files.append(str(fi_d))
            else:
                print('not delete:',fi_d)

    return dictName, remove_data_list_files


# 如果返回true 则不新加
def containsDuplicate(nums):
    """

    :type nums: List[int]
    :rtype: bool
    """
    if len(nums) == 0 or len(nums) == 1:
        return False
    d = {}
    for i in nums:
        if i in d:
            return True
        d[i] = 0
    return False


# 执行命令
def execCmd(cmd):
    print(cmd)
    # r = os.popen(cmd)
    (status, output) = commands.getstatusoutput(cmd)
    print("result:", status)
    print("result output:", output)
    text = 'ok'
    return text


# 遍历结果
def zipFile(result):
    print(result)
    for file, valus in result.items():

        # print('不存在则打包')
        # print(file)
        # print(valus)
        for months in valus:
            varZipFile = file + '.' + months + '.tar.gz'
            if os.path.isfile(varZipFile):
                print('varZipFile 已经存在不需要更新:', varZipFile)
                continue
            # 压缩
            cmdval = 'tar -zcvf ./' + varZipFile + ' ' + file + '.' + months + '*'
            print(cmdval)
            execCmd(cmdval)


# 遍历结果 然后删除
def delFile(result):
    print(result)
    for valus in result:
        # 压缩完成后就删除
        os.remove(valus)
        print('delete history file:', valus)


if __name__ == '__main__':
    # 递归遍历/root目录下所有文件
    result = loggingFile(sys.argv[1])
    # result = loggingFile('D://logs')
    zipFile(result[0])
    delFile(result[1])
