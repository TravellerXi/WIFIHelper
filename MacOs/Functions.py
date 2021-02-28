#!/usr/bin/env python3
# coding=utf-8
import rumps
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

class 状态栏及通知(rumps.App):
    def __init__(self):
        super(状态栏及通知, self).__init__("WIFI助手")
        self.menu = []
        #self.quit_button="Quit1"




def Notify(title:str,content:str):
    rumps.notification(title,"",content)


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
class 初始化:
    def 更新plist(self,CurrentDir):
        DefaultPlist = resource_path(os.path.join("res", "Info.plist"))
        copyfile(DefaultPlist,CurrentDir+'/Info.plist')

class 密码机制:
    def __init__(self):
        Username = getpass.getuser()
        ExeFileLocation = "/Users/"+Username+"/Documents/WIFI助手"
        self.ConfigureFile = ExeFileLocation + "/Configure.ini"
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
    def 登陆(self):
        self.用户密码 = 密码机制().read()
        if self.用户密码 != 1:
            if self.用户密码==2:
                Notify(title='第一次使用',content='第一次使用，请在弹出窗口里输入用户名密码')
                time.sleep(2)
                自定义登录界面()
            else:
                (Username, Password) = self.用户密码
                登陆结果=登陆登出.登陆(Username, Password)
                if 登陆结果 != 200:
                    if 登陆结果 == -1:
                        Notify(title='WIFI已断开', content='请手动重连相关WIFI')
                    else:
                        Notify(title='提示',content='用户名密码配置错误，请在弹出窗口里修改')
                        time.sleep(2)
                        自定义登录界面()

        else:
            Notify(title='第一次使用', content='第一次使用，请在弹出窗口里输入用户名密码')
            time.sleep(2)
            自定义登录界面()
    def 检查网络(self):
        try:
            requests.get("https://www.baidu.com")
        except:
            Notify("WIFI状态更新", "认证已失效，正在重新认证")
            self.登陆()
            time.sleep(2)
            Notify("WIFI状态更新", "网络已恢复,已成功认证")
