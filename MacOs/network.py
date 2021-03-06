#!/usr/bin/env python3
# coding=utf-8
from Functions import *
import multiprocessing
from multiprocessing import Process
import sys
def ShowIcon():
    状态栏及通知().run()
def AlwaysCheck(pid):
    开始登陆=执行()
    开始登陆.登陆()
    while 1:
        开始登陆.检查网络()
        time.sleep(3)
        pid=int(pid)
        if CheckProcess(pid) is False:
            os._exit(0)

def CheckProcess(pid):
    try:
        os.kill(pid,0)
    except:
        return False
    else:
        return True
if __name__=="__main__":
    CurrentPath = os.path.dirname(sys.argv[0])
    初始化().更新plist(CurrentPath)
    #初始化().test()
    multiprocessing.freeze_support()
    ProcessIcon=Process(target=ShowIcon,args=())
    ProcessIcon.start()
    ProcessID = ProcessIcon.pid
    #print(int(ProcessID))
    ProcessAlwaysCheck = Process(target=AlwaysCheck,args=(str(ProcessID),))
    ProcessAlwaysCheck.start()
    ProcessIcon.join()
    ProcessAlwaysCheck.join()
