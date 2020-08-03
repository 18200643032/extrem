# @Time : 2020/8/1 15:53 
# @modele : opencv
# @Author : zhengzhong
# @Software: PyCharm

import os
res_p = os.popen("ldd /usr/local/ev_sdk/lib/libji.so |grep so.4.1").read()
if res_p is "":
    print(3.4)
else:
    print(4.1)
