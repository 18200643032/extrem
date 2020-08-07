#/bin/bash
export LD_LIBRARY_PATH=/usr/local/cuda-10.0/lib64:/usr/local/nvidia/lib:/usr/local/nvidia/lib64
chmod +x install
if [ -e vas_3.4.gz ]; then
    ./install vas_3.4.gz &
else
    ./install vas_4.1.gz &
fi

if [ -e /usr/local/ev_sdk/bin/test ]; then
    cd /usr/local/ev_sdk/bin
    chmod +x ev_license
    ./ev_license -r r.txt
    ./ev_license -l privateKey.pem r.txt license.txt
    cp /usr/local/ev_sdk/bin/license.txt /usr/local/vas/license.txt
	a=`cat license.txt|sed 's/{"license":"\(.*\)","version":7}/\1/g'`
	sed -i "s/license=/license=$a/g" local.conf
	sed  -i 's/version=/version=7/g' local.conf
else
    cp /usr/local/ev_sdk/3rd/license/bin/ev_license /usr/local/ev_sdk/authorization
    cd /usr/local/ev_sdk/authorization
    chmod +x ev_license
    ./ev_license -r r.txt
    ./ev_license -l privateKey.pem r.txt license.txt
    cp /usr/local/ev_sdk/authorization/license.txt /usr/local/vas/license.txt
	a=`cat license.txt|sed 's/{"license":"\(.*\)","version":7}/\1/g'`
	sed -i "s/license=/license=$a/g" local.conf
	sed -i 's/version=/version=7/g' local.conf
fi
bash /usr/local/vas/vas_stop.sh
bash /usr/local/vas/vas_start.sh  &