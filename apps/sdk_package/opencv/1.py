import os
res_p = os.popen("ldd /usr/local/ev_sdk/lib/libji.so |grep so.4.1").read()
if res_p is not "":
    print(3.4)
else:
    print(4.1)

