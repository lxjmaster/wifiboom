# --*--coding:utf-8--*--

__AUTHOR__ = "Master_LXJ"
__DOC__ = "The dream more than endlessly!"

import sys
from datetime import datetime
from utils import *
import re

# f = open("test.txt","a+")
# sys.stdout = ""
# print("world")
# print("sss")
# sys.stdout.flush()
# f.close()
# sys.stdout = f
# sys.stdout.write("cwemwel")
# sys.stdout.flush()
# print("helo")
# f.close()

class __redirection__:
    def __init__(self):
        self.buff = ''
        self.__console__ = sys.stdout

    def write(self, output_stream):
        self.buff += output_stream

    def to_console(self):
        sys.stdout = self.__console__
        for b in self.buff.split():
            t = datetime.now()
            str_time = datetime.strftime(t, "[%m/%d %H:%M:%S]  ")
            print(str_time+b+"\n",end="")

    def to_file(self, file_path):
        f = open(file_path, 'w')
        sys.stdout = f
        for b in self.buff.split():
            t = datetime.now()
            str_time = datetime.strftime(t, "[%m/%d %H:%M:%S]  ")
            print(str_time+b+"\n",end="")
        f.close()

    def flush(self):
        self.buff = ''

    def reset(self):
        sys.stdout = self.__console__


# obj = __redirection__()
# sys.stdout = obj
# print("hec3eo")
# print("hhhhid")
# obj.to_file("test.txt")
# obj.to_console()
# t = datetime.now()
# print(datetime.strftime(t,"[%m/%d %H:%M:%S]"))
# obj.flush()
# obj.reset()
# print("hahah")

# from utils import Password
#
# password = Password()
# f = password.ask_file()
# passwords = password.get_passwords(f)
# for p in passwords:
#     print(p)


status = read_status()
with open(status[0],"r") as f:
    lines = f.readlines()
    if status[2] in lines[status[1]]:
        passwords = lines[status[1]:]
        print(passwords)
        passwords = [(p.split())[0] for p in passwords]
        print(passwords)
        # run(passwords=passwords)
# with open('logs/status.log',"r") as f:
#     d = f.readlines()
#     print(d[0])
    # pattern = r"(?P<time>.+)   当前破解的WIFI: (?P<ssid>.+) 测试密码: (?P<password>.+)"
    # regex = re.compile(pattern)
    # a = re.search(regex,d[-1])
    # print(a)
    # print(a.group("time"))