from django.shortcuts import render
from django.http import StreamingHttpResponse  #文件处理
from django.views.decorators.http import require_http_methods #判断状态
from django.http import JsonResponse #返回JSON
from api_1_0.config import RET,PATH
import json,os,shutil,re

from apps.utls.subprocess_test import runcmd  #封装到的subprocess方法

def code():
    pass

# Create your views here.

# 规范视图
def standard(request):
    """"
    :image_name报警的图片
    :images  要测试的算法镜像
    """
    response = {}
    if request.method == "POST":
        try:
            image_name = request.POST.get("image_name")  #图片名
            images = request.POST.get("images")  # <QueryDict: {'name': ['123']}>
        except Exception as e:
            response["error"] = RET.PARAMERR
            response["status_code"]  = 201
            return  JsonResponse(response)
        if not os.system(f"docker pull {images}"):
            response["list"] = images
        else:
            response["error"] = "镜像名不存在"
            response["status_code"] = 201
            return JsonResponse
        # 生成容器，挂载规范目录
        images_name = images.split(":")[0].split("/")[-1]
        if os.path.exists(os.path.join(PATH.DOCKER_DIR, images_name)):
            os.system(f"rm -rf {os.path.join(PATH.DOCKER_DIR, images_name)}")
        else:
            os.makedirs(os.path.join(PATH.DOCKER_DIR, images_name))
        shutil.copy(os.path.join(PATH.DOCKER_DIR, 'guifan.zip'), os.path.join(PATH.DOCKER_DIR, images_name))
        os.system(f"unzip {os.path.join(os.path.join(PATH.DOCKER_DIR, images_name), 'guifan.zip')} -d {os.path.join(PATH.DOCKER_DIR,images_name)}")
        os.system(f"cp {os.path.join(PATH.TMP_DIR, image_name)} {os.path.join(os.path.join(PATH.DOCKER_DIR, images_name), '1.jpg')}")
        docker_run_cmd = f"docker run -itd --runtime=nvidia --privileged -v /dockerdata/AppData:/data -v {os.path.join(PATH.DOCKER_DIR,images_name)}:/zhengzhong  -e LANG=C.UTF-8 -e NVIDIA_VISIBLE_DEVICES=all {images} "
        if runcmd(docker_id):
            # docker_id = os.popen(docker_run_cmd).read()[:8]
            os.system("docker exec -it %s python3 /zhengzhong/auto_run.py" % (docker_id))
            response["msg"] = "算法规范已完成，请去查看结果"
            response["status_code"] = 200
            os.system(f"tar zcvf {os.path.join(PATH.APPS_DIR, 'res.tar.gz')} {os.path.join(os.path.join(PATH.DOCKER_DIR, images_name),'res_jpg')} {os.path.join(os.path.join(PATH.DOCKER_DIR, images_name), 'dynamiv_res')} {os.path.join(os.path.join(PATH.DOCKER_DIR, images_name),'project_res.txt')}")
            response["下载地址"] = "/api/file_download?file=res.tar.gz"
            return JsonResponse(response)
        else:
            response["启动容器失败"]
            return  JsonResponse(response)

    else:
        response["error"] = "方法不对"
        response["status_code"] = 201
        return JsonResponse(response)


# ias封装视图

def ias(request):

    """
    # 封装ias
    :param algo_image:  接收传入的镜像名称:image_name,
    :port  port:镜像的端口
    :return:
    """
    response = {}
    if request.method == "POST":

        res_datas = request.POST
        port = res_datas.get('port')
        image_name = res_datas.get('image_name')

        # 获取到容器id
        cmd_run_sdk = f"docker run -itd  --runtime=nvidia --privileged -v /home/zheng:/tmp  -e LANG=C.UTF-8 -e NVIDIA_VISIBLE_DEVICES=0 --rm  -p {port}:80 {image_name}"
        contain_id = runcmd(cmd_run_sdk)
        if contain_id:
            pass
        else:
            response["errmsg"] = "端口已使用或其他错误"
            response["error"] =  RET.DATAERR
            return JsonResponse(response)

        data = {
            "images": image_name
        }
        ias_ver = requests.post("http://192.168.1.147:8899/api/opencv/", data=data).json().get("opencv版本")
        if ias_ver == "4.1":
            cmd = f"cp {path}/sdk_package/ias/ias_4.1.tar.gz /home/zheng;tar -xvf /home/zheng/ias_4.1.tar.gz -C /home/zheng"
            res_p = runcmd(cmd)
            if res_p:
                pass
            else:
                response["errno"] = RET.SERVERERR
                response["errmsg"] = "移动文件到挂载目录失败"
                return JsonResponse(res)

        else:
            cmd = f"cp {path}/sdk_package/ias/ias_4.1.tar.gz /home/zheng;tar -xvf /home/zheng/ias_4.1.tar.gz -C /home/zheng"
            res_p = runcmd(cmd)
            if res_p:
                pass
            else:
                response["errno"] = RET.SERVERERR
                response["errmsg"] = "移动文件到挂载目录失败"
                return JsonResponse(res)
        ias_install = f"docker exec  {contain_id} bash /tmp/give_license.sh &"
        runcmd(ias_install)
        response["errno"] = RET.OK
        response["errmsg"] = "封装ias成功"
        response["ias的版本是"] = ias_ver
        return JsonResponse(res)
    else:
        response["errot"] = "方法不对"
        return JsonResponse(response)

#验证opencv版本
def opencv(request):
    """
    :param request: images:镜像
    :return:
    """
    response = {}
    if request.method == "POST":
        images = request.POST.get("images")
        docker_run_cmd = f"docker run -itd --runtime=nvidia --rm --privileged -v /dockerdata/AppData:/data  -v {PATH.OPENCV_DIR}:/zhengzhong -e LANG=C.UTF-8 -e NVIDIA_VISIBLE_DEVICES=all {images} "
        code,docker_id = runcmd(docker_run_cmd)
        if code:
            _,r = runcmd(f"docker exec -it {docker_id} python3 /zhengzhong/opencv.py")
        os.system(f"docker stop {docker_id} &")
        response["opencv版本"] = r
        return  JsonResponse(response)
    else:
        response["errot"] = "方法不对"
        return JsonResponse(response)

#验证图片是否报警
def file_image(request):
    """

    :param request: images:镜像
    :return:   myfile 文件【可多个】
    """
    response ={}
    if request.method == "POST":
        name_list_images = []
        myfiles = request.FILES.getlist('myfile', None)  #接收多个文件
        if not myfiles:
            response["msg"] = "没有文件上传"
            return JsonResponse(response)
        for myfile in myfiles:
            name_list_images.append(myfile.name)
            destination = open(os.path.join(os.path.join(PATH.LIBS_DIR,'tmp'), myfile.name), "wb+")
            for chunk in myfile.chunks():
                destination.write(chunk)
            destination.close()
        images = request.POST.get("images")
        docker_run_cmd = f"docker run -itd --runtime=nvidia --rm --privileged -v /dockerdata/AppData:/data  -v {os.path.join(PATH.LIBS_DIR,'tmp')}:/zhengzhong -e LANG=C.UTF-8 -e NVIDIA_VISIBLE_DEVICES=all {images}"
        docker_id = runcmd(docker_run_cmd)
        if docker_id:
            for name in name_list_images:
                os.system(f"docker exec -it {docker_id} bash /zhengzhong/1.sh {name}")
                with open(os.path.join(os.path.join(PATH.LIBS_DIR,'tmp'),"image_res.txt"),"r") as f:
                    con = f.read().splitlines()
                pattern_xmin = 'json:.\{(.*)\}'
                res_xmins = "{" + re.findall(pattern_xmin, str(con))[0].replace("\\t", "").replace(" ", "").replace("','", "") + "}"
                r = json.loads(res_xmins)
                response[name] = r
            os.system(f"docker stop {docker_id}")
            return JsonResponse(res)
    else:
        response["errot"] = "方法不对"
        return JsonResponse(response)





