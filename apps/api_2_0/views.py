from django.shortcuts import render

# Create your views here.
import os,requests,json,time
from api_1_0.config import PATH

from django.http import JsonResponse


host = 'http://192.168.1.16:31082'
path = r'C:/Users/Administrator/Desktop/tmp/'


def get_git_account(username):
    # login
    url_login = '/api/login'
    headers = {"Content-Type": "application/json"}
    data = {
        'username': 'admin',
        'password': 'a2dj%%^^kd@&^&+',
    }
    data = json.dumps(data)
    # 获取登录的token
    res_login = requests.post(host + url_login, data=data, headers=headers)
    res_token = res_login.json().get('data').get('access_token')
    headers = {'Authorization': 'Bearer %s' % (res_token)}
    url_git_list = '/api/developer-manage/developer/list'
    parmams = {
        "page":1,
        "per_page":10
    }
    a1 = requests.get(host+url_git_list,params=parmams,headers=headers).json().get("data")
    for i in a1:
        name = i.get("username")
        if name == username:
            id_num = i.get("id")
             # 获取git账号
            url_git_account = '/api/instance-manage/instance/info?id=%s' % id_num
            res_git_account = requests.get(host + url_git_account, headers=headers).json()
            return res_git_account
    return False





def upload_code(request):
    response = {}
    if request.method == "POST":
        username = request.POST.get("username")
        user_message = get_git_account(username)
        # '''提交代码到远承仓库'''
        git_user = user_message.get('data').get('gitlab_username')
        git_pwd = user_message.get('data').get('gitlab_password')
        git_train_path = user_message.get('data').get('gitlab_path')[7:]
        git_ev_sdk_path = user_message.get('data').get('encoding_gpu_containers')[7:]
        git_train_dir_name = git_train_path.split('/')[-1]
        git_ev_sdk_dir_name = git_ev_sdk_path.split('/')[-1]
        os.chdir(PATH.TRAIN_DIR) #修改当前工作路径
        os.system("git clone http://%s:%s@%s" % (git_user, git_pwd, git_train_path))
        time.sleep(10)
        os.chdir(PATH.TRAIN_DIR+git_train_dir_name)
        cmd = F"unzip {PATH.TRAIN_DIR}/laoshu_train.zip -d {PATH.TRAIN_DIR+git_train_path}"
        os.system(cmd)
        os.system("git add .")
        os.system("git commit -m 'test'")
        os.system('git push')
        response["msg"] = "上传成功"
        return JsonResponse(response)
    else:
        response["errot"] = "方法不对"
        return JsonResponse(response)



