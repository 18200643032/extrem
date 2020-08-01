# @Time : 2020/8/1 15:53 
# @modele : opencv
# @Author : zhengzhong
# @Software: PyCharm

import subprocess
res_p = subprocess.Popen("ldd /usr/local/ev_sdk/lib/libji.so |grep so.4.1",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding="UTF-8")
if res_p.stdout.readlines() == []:
    print(3.4)
else:
    print(4.1)
