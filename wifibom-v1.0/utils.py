# --*--coding:utf-8--*--

__AUTHOR__ = "Master_LXJ"
__DOC__ = "The dream more than endlessly!"

import time
import os
import sys
from datetime import datetime
import re


BASE_PATH = os.path.dirname(os.path.abspath(__file__))
logs_dir = os.path.join(BASE_PATH, "logs")
log_file = os.path.join(logs_dir, "logging.log")
status_file = os.path.join(logs_dir, "status.log")

def timer(times, obj):
    """
    一个计时器
    :param times:
    :param obj:
    :return:
    """
    assert type(times) is int
    assert type(obj) is bool
    for t in range(times):
        if obj == True:
            break
        else:
            time.sleep(1)

class Password(object):

    def __init__(self):
        """
        密码类,密码的相关操作
        """
        global FileList
        # self.password_way = ""
        self.password_dir = os.path.join(BASE_PATH, "passwords")
        if os.path.isdir(self.password_dir):
            FileList = os.listdir(self.password_dir)
            if len(FileList) > 0:
                pass
            else:
                print("未检测到密码字典文件,请查询passwords目录下是否有密码字典文件.\n程序将使用默认密码...")
                FileList = None
        else:
            print("未检测到密码字典文件,请查询passwords目录下是否有密码字典文件.\n程序将使用默认密码...")
            FileList = None
        self.password_base_dirs = FileList
        # self.password_full_dirs = [os.path.join(self.password_dir, base) for base in self.password_base_dirs]

    # def ask_file(self):
    #
    #     if not self.password_base_dirs is None:
    #         print("*"*25+"注:A为自动模式,即自动选取所有字典.M为手动模式,即手动选择单个字典."+"*"*25)
    #         ask = input("请选择字典爆破方式(A(自动)/M(手动)) :")
    #         if ask in ["M","m"]:
    #             self.password_way = ask
    #             for index,p in enumerate(self.password_base_dirs):
    #                 print("%-3s | %-10s"%(index+1, p))
    #             way = int(input("请选择一个字典文件的序号 :"))
    #             assert way > 0
    #             file_path = self.password_full_dirs[way-1]
    #
    #             return file_path
    #         elif ask in ["A", "a"]:
    #             self.password_way = ask
    #             print("*"*25+"程序将自动选取所有密码字典"+"*"*25)
    #             files_path = self.password_full_dirs
    #
    #             return files_path
    #         else:
    #             print("*"*25+"输入错误,重新输入"+"*"*25)
    #             return self.ask_file()
    #     else:
    #         passwords = [n*8 for n in range(10)]+["12345678", "password", "abcdefg"]
    #
    #         return passwords

    def ask_file(self):
        """
        字典操作
        :return:
        """
        if not self.password_base_dirs is None:
            password_full_dirs = [os.path.join(self.password_dir, base) for base in self.password_base_dirs]
            for index, p in enumerate(self.password_base_dirs):
                print("%-3s | %-10s"%(index+1, p))
            file_num = eval(input("请选择一个字典文件的序号: "))
            if len(password_full_dirs) > 0:
                assert file_num > 0
            file_path = password_full_dirs[file_num-1]

            return file_path
        else:
            passwords = [str(n)*8 for n in range(10)]+["12345678", "password", "abcdefgh"]
            print("-"*15+"将使用默认密码!"+"-"*15)

            return passwords

    def get_passwords(self, f):
        """
        密码处理
        :param f:
        :return:
        """
        # if len(self.password_way) > 0:
        if not self.password_base_dirs is None:
            assert os.path.isfile(f)
            with open(f, "r") as f:
                passwords = [(p.split())[0] for p in f.readlines()]

            return passwords
        else:
            passwords = f
            return passwords

class Loger(object):

    def __init__(self, *args, **kwargs):
        """
        重写print重定向,直接使用print简单输出一些log,未使用logging库
        :param args:
        :param kwargs:
        """
        self.buff = ''
        self.__console__ = sys.stdout
        if not os.path.exists(logs_dir):
            os.mkdir(logs_dir)
            with open(log_file, "w") as f:
                pass
        else:
            if not os.path.exists(log_file):
                with open(log_file, "w") as f:
                    pass
            else:
                pass
        self.log_file = log_file

    def write(self, output_stream):

        self.buff += output_stream

    def to_console(self):

        sys.stdout = self.__console__
        print(self.buff, end="")

    def to_log(self):

        f = open(self.log_file, 'a+')
        sys.stdout = f
        t = datetime.now()
        str_time = datetime.strftime(t, "[%m/%d %H:%M:%S]   ")
        print(str_time+self.buff, end="")
        f.close()

    def flush(self):

        self.buff = ''

    def reset(self):

        sys.stdout = self.__console__

def loger(strings):
    """
    重定向log
    :param strings:
    :return:
    """
    obj = Loger()
    sys.stdout = obj
    print(strings)
    obj.to_log()
    obj.to_console()

def check_log():
    """
    检测上一次运行记录
    :return:
    """
    if not os.path.exists(log_file):
        return False
    else:
        with open(log_file, "r+") as f:
            logs = f.readlines()
            pattern = r"(?P<time>.+)   当前破解的WIFI: (?P<ssid>.+) 测试密码: (?P<password>.+)"
            regex = re.compile(pattern)
            staus = re.search(regex, logs[-1])
        if staus is None:
            return False
        else:
            return [staus.group("time"), staus.group("ssid"), staus.group("password")]

def write_status(s, m):
    """
    写入破解状态
    :param s:
    :param m:
    :return:
    """
    with open(status_file, m) as f:
        f.write(s)

def read_status():
    """
    读取破解状态
    :return:
    """
    with open(status_file, "r+") as f:
        status = f.readlines()
        pattern = r"<PathFile>(?P<file>.+)</PathFile>\n<index>(?P<index>\d+)</index>\t<password>(?P<password>.+)</password>"
        regex = re.compile(pattern)
        status = re.search(regex, status[0]+status[-1])
    if status is not None:
        return [status.group("file"), int(status.group("index")), status.group("password")]
    else:
        return None

def start_string():
    s = """
--------------------------------------------------------------------------------------------------
| 程序名称:WiFi爆破工具(WiFiboom)                                                                  |
|
| 作者:lxj_Master                                                                                 |
|
| 联系方式:379501669@qq.com////www.dagouzi.cn                                                      |
|
| 功能:暴力破解WiFi                                                                                |
|
| 原理:通过密码字典,不停的对某个WiFi进行密码尝试连接                                                 |
|
| 注意:该程序不能保证100%破解WiFi,能否成功破解WiFi与所用的密码字典有关.详情参考原理!!!                 |
|
| 字典全部存放在程序同目录下的passwords中,如自定义字典,请务必保证文件为txt文本,且每个密码占文件的一行!!!|
 ---------------------------------------------------------------------------------------------------
 可能会出现屏幕信息不动的情况,显示问题,按CTRL+C就可以刷新内容了!!!
 请选择有密码的WiFi进行爆破(无密码程序会报错)!
 
 －－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－－
    """
    print(s)