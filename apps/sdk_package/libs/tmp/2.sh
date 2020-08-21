#bin/bash
cd /usr/local/ev_sdk/bin
./test-ji-api -f 1 -i /zhengzhong/$1 2>&1 | tee /zhengzhong/image_res.txt
