#/bin/bash
export LD_LIBRARY_PATH=/usr/local/cuda-10.0/lib64:/usr/local/nvidia/lib:/usr/local/nvidia/lib64

if [ -e /usr/local/ev_sdk/bin/test ]; then
    cd /usr/local/ev_sdk/bin
    chmod +x ev_license
    ./ev_license -r r.txt
    ./ev_license -l privateKey.pem r.txt license.txt
else
    cp /usr/local/ev_sdk/3rd/license/bin/ev_license /usr/local/ev_sdk/authorization
    cd /usr/local/ev_sdk/authorization
    chmod +x ev_license
    ./ev_license -r r.txt
    ./ev_license -l privateKey.pem r.txt license.txt
    cp /usr/local/ev_sdk/authorization/license.txt  /usr/local/ev_sdk/bin
fi


cd /usr/local/ev_sdk/bin
./test-ji-api -f 1 -i /zhengzhong/$1 2>&1 | tee /zhengzhong/image_res.txt