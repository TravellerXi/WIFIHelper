#!/usr/bin/env python3
# coding=utf-8
# pip install pywin32 requests, pythonping

from win32api import *
from win32gui import *
import win32con
import sys, os, getpass, configparser, re, requests, tkinter, time
from shutil import copyfile
from tkinter import messagebox
from pythonping import ping

#生成资源文件目录访问路径
def resource_path(relative_path):
    if getattr(sys, 'frozen', False): #是否Bundle Resource
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class WindowsBalloonTip:
    def __init__(self, software_name:str):
        self.software_name=software_name
        message_map = {
            win32con.WM_DESTROY: self.OnDestroy,
        }
        # Register the Window class.
        wc = WNDCLASS()
        hinst = wc.hInstance = GetModuleHandle(None)
        wc.lpszClassName = "PythonTaskbar"
        wc.lpfnWndProc = message_map  # could also specify a wndproc.
        classAtom = RegisterClass(wc)
        # Create the Window.
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = CreateWindow(classAtom, "Taskbar", style, \
                                 0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, \
                                 0, 0, hinst, None)
        UpdateWindow(self.hwnd)
        #iconPathName = os.path.abspath(os.path.join(os.getcwd(), "ico.ico"))
        iconPathName = resource_path(os.path.join("res", "ico.ico"))
        icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
        try:
            self.hicon = LoadImage(hinst, iconPathName, \
                              win32con.IMAGE_ICON, 0, 0, icon_flags)
        except:
            self.hicon = LoadIcon(0, win32con.IDI_APPLICATION)
        flags = NIF_ICON | NIF_MESSAGE | NIF_TIP
        self.nid = (self.hwnd, 0, flags, win32con.WM_USER + 20, self.hicon, software_name)
        Shell_NotifyIcon(NIM_ADD, self.nid)

    def Notify(self,title:str,msg:str):
        Shell_NotifyIcon(NIM_MODIFY, \
                         (self.hwnd, 0, NIF_INFO, win32con.WM_USER + 20, \
                          self.hicon, "Balloon  tooltip", msg, 200, title))
        # self.show_balloon(title, msg)

    def destroy(self):
        DestroyWindow(self.hwnd)

    def OnDestroy(self):
        nid = (self.hwnd, 0)
        Shell_NotifyIcon(NIM_DELETE, nid)
        PostQuitMessage(0)  # Terminate the app.

class 登陆登出():
    def 登陆(username: str, password: str):
        '''
            发送纯文本信息
            UserId：String
            Content:String
        '''
        params = {
            "username": username,  # input标签下的name
            "password": password,  # input标签下的name
            "RedirectUrl": "",  # input标签下的name
            "anonymous": "DISABLE",
            "anonymousurl": "",
            "accesscode": "",
            "accesscode1": "DISABLE",
            "checkbox": "on",
            "checkbox1": "on"

        }
        try:
            StatusInfo = requests.post("http://172.31.31.31:8080/cn/login", data=params)
            return StatusInfo.status_code
        except:
            return -1
    def 登出(self):
        try:
            requests.post("http://172.31.31.31:8080/cn/logout")
        except:
            return -1



class 自定义登录界面:
    def __init__(self):
        self.top = tkinter.Tk()
        self.top.geometry('400x170+350+150')
        self.top.wm_title('WIFI认证')
        label1 = tkinter.Label(self.top, text='用户名:', font=('宋体', '18'))
        label1.grid(row=0, column=0)
        label2 = tkinter.Label(self.top, text='密码:', font=('宋体', '18'))  # 集合为另一种形式的字典
        label2.grid(row=1, column=0)
        v = tkinter.StringVar()
        self.entry1 = tkinter.Entry(self.top, font=('宋体', '18'), textvariable=v, \
                               validate='focusout', validatecommand=self.validateText)

        self.entry1.grid(row=0, column=1)
        self.entry1.focus_force()
        self.entry2 = tkinter.Entry(self.top, font=('宋体', '18'), show='*')

        self.entry2.grid(row=1, column=1)
        button1 = tkinter.Button(self.top, text='登陆', font=('宋体', '18'), \
                                 command=self.anw_button)
        button1.grid(row=2, column=0, padx=50, pady=10)
        button2 = tkinter.Button(self.top, text='退出', font=('宋体', '18'), \
                                 command=sys.exit)

        button2.grid(row=2, column=1, padx=80, pady=10)
        self.label3 = tkinter.Label(self.top, text='信息提示区', font=('华文新魏', '16'), \
                               relief='ridge', width=30)
        self.label3.grid(row=3, column=0, padx=10, pady=10, columnspan=2, sticky='s')
        self.top.mainloop()

    def validateText(self):
        val = self.entry1.get()
        if re.findall('^[0-9a-zA-Z_]{1,}$', str(val)):
            return True
        else:
            self.label3['text'] = '用户名只能包含字母、数字、下划线'
            return False

    def anw_button(self):
        username=str(self.entry1.get())
        password=str(self.entry2.get())
        #print(username,password,登陆登出.登陆(username,password))
        if 登陆登出.登陆(username,password)==200:
            密码机制().write(username, password)
            self.label3['text'] = '登陆成功，自动转为后台守护'
            tkinter.messagebox.showinfo(title='WIFI认证成功', message='点此后台守护网络')
            #time.sleep(1)
            self.top.destroy()
            #self.top.quit()
        else:
            self.label3['text'] = '用户名或密码错误，请重新输入！'
        #if str.upper(self.entry1.get()) == "123456" and str.upper(self.entry2.get()) == '123456':
        #    self.label3['text'] = '登陆成功'
        #else:
        #    self.label3['text'] = '用户名或密码错误，请重新输入！'

class 密码机制:
    def __init__(self):
        windows_username = getpass.getuser()
        ExeFileLocation = r"C:\\Users\\" + windows_username + "\\Documents\\WIFI助手"
        self.ConfigureFile = ExeFileLocation + "\\Configure.ini"
        self.config = configparser.ConfigParser()
        self.config.read(self.ConfigureFile, encoding='utf-8')
        if not os.path.exists(ExeFileLocation):
            os.mkdir(ExeFileLocation)
            DefaultConfigure = resource_path(os.path.join("res", "Configure.ini"))
            copyfile(DefaultConfigure, self.ConfigureFile)
        if not os.path.isfile(self.ConfigureFile):
            DefaultConfigure = resource_path(os.path.join("res", "Configure.ini"))
            copyfile(DefaultConfigure, self.ConfigureFile)

    def read(self):
        """
        根本没有文件或者没有section，return 1
        用户名密码定义为空, return 2
        :return:
        """
        try:
            Username = self.config.get('AccountInfo', 'Username')
            Password = self.config.get('AccountInfo', 'Password')
            if Username=='' and Password=='':
                return 2
            return (Username,Password)
        except:
            return 1


    def write(self,username,password):
        self.config.set("AccountInfo","Username",username)
        self.config.set("AccountInfo","Password",password)
        with open(self.ConfigureFile,'w') as f:
            self.config.write(f)


class 执行:
    def __init__(self):
        登陆登出().登出()
        self.ThisWindows = WindowsBalloonTip(software_name='WIFI助手')
        self.OfflineCount=0
    def 登陆(self):
        self.用户密码 = 密码机制().read()
        if self.用户密码 != 1:
            if self.用户密码==2:
                self.ThisWindows.Notify(title='第一次使用', msg='第一次使用，请在弹出窗口里输入用户名密码')
                time.sleep(2)
                自定义登录界面()
            else:
                (Username, Password) = self.用户密码
                登陆结果=登陆登出.登陆(Username, Password)
                if 登陆结果 != 200:
                    if 登陆结果 == -1:
                        self.ThisWindows.Notify(title='WIFI已断开', msg='请手动重连相关WIFI')
                    else:
                        self.ThisWindows.Notify(title='提示', msg='用户名密码配置错误，请在弹出窗口里修改')
                        time.sleep(2)
                        自定义登录界面()

        else:
            self.ThisWindows.Notify(title='第一次使用', msg='第一次使用，请在弹出窗口里输入用户名密码')
            time.sleep(2)
            自定义登录界面()
    def 检查网络(self):
        try:
            if not (ping('baidu.com', count=1).success()):
                self.OfflineCount+=1
                if self.OfflineCount <3:
                    self.ThisWindows.Notify("WIFI状态更新", "认证已失效，正在重新认证")
                else:
                    if self.OfflineCount==3:
                        self.ThisWindows.Notify("WIFI故障", "此WIFI目前存在故障，暂时屏蔽通知。待WIFI网络恢复，将再次通知")
                self.登陆()
                time.sleep(2)
                if ping('baidu.com', count=1).success():
                    self.ThisWindows.Notify("WIFI状态更新", "网络已恢复,已成功认证")
            else:
                if self.OfflineCount>= 3:
                    self.ThisWindows.Notify("WIFI故障恢复","WIFI故障已恢复，已成功认证")
                self.OfflineCount=0
        except:
            self.ThisWindows.Notify(title='WIFI已断开', msg='请手动重连相关WIFI')
