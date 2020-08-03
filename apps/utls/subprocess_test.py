# @Time : 2020/8/1 15:23 
# @modele : subprocess_test
# @Author : zhengzhong
# @Software: PyCharm
import subprocess

def runcmd(command):
    # res_p = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding="UTF-8")
    # if res_p.stderr.readline() is not "" or res_p.poll() != 0:
    #     return False
    # else:
    #     if res_p.stdout.readline()[0:8] != '':
    #         return res_p.stdout.readline()[0:8].replace(" ","").replace('\n','')
    #     else:
    #         return True

    res_p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    stdout, stderr = res_p.communicate()
    returncode = res_p.returncode
    if returncode == 0:
        if stdout.endswith('\n'):
            return True, stdout.replace('\n', '')
        return True, stdout
    else:
        return False, stderr