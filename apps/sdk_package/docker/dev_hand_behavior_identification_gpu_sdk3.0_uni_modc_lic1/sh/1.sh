#/bin/bash
source /etc/profile
source /root/.bashrc
if [ -e /usr/local/ev_sdk/bin/test-ji-api ]; then
    cp /usr/local/ev_sdk/3rd/license/bin/ev_license /usr/local/ev_sdk/authorization
    cd /usr/local/ev_sdk/authorization
    chmod +x ev_license
    ./ev_license -r r.txt
    ./ev_license -l privateKey.pem r.txt license.txt
    cp license.txt /usr/local/ev_sdk/bin
    cp /usr/local/ev_sdk/config/algo_config.json /zhengzhong/config
fi

