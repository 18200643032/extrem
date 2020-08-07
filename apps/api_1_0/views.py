from django.shortcuts import render
from django.http import StreamingHttpResponse  #文件处理
from django.views.decorators.http import require_http_methods #判断状态
from django.http import JsonResponse #返回JSON
from api_1_0.config import RET,PATH
import json,os,shutil,re

from apps.utls.subprocess_test import runcmd  #封装到的subprocess方法
from apps.utls.perform_infor import PerForm_InFor

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
        response["opencv版本"] = r
        os.system(f"docker stop {docker_id} &")
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



#性能测试
def get_performance_information(request):

    """
        运行算法得到算法占用信息
        :return:
        """
    image_name = request.POST.get("images_name")
    zhengzhong = PerForm_InFor("zhengzhong")
    res_cpu_total, res_mem_total = zhengzhong.run_sdk_opencv()
    image_dir = image_name.split('/')[-1].split(":")[0]
    res_image_data = os.path.join(PATH.SDK_PACKAGE_DIR, f'res_data')
    opencv_num = zhengzhong.get_opencv_num(image_name)
    cpu_list = [(i, j) for i in range(1, 50) for j in range(2, 5) if i * j <= int(res_cpu_total)]
    opencv34_dir = "docker volume inspect  opencv_34 |grep Mountpoint|awk '{print $2}'"
    _, res_opencv34_dir = zhengzhong.sdk_subprocess(opencv34_dir)
    res_opencv34_dir = res_opencv34_dir[1:-8]
    opencv41_dir = "docker volume inspect  opencv_41 |grep Mountpoint|awk '{print $2}'"
    _, res_opencv41_dir = zhengzhong.sdk_subprocess(opencv41_dir)
    res_opencv41_dir = res_opencv41_dir[1:-8]

    for sdk_num, cpu_set_nums in zhengzhong.cpunum_set(cpu_list):
        container_list = []
        for cpu_set_num in cpu_set_nums:
            print(sdk_num, cpu_set_num)
            random_num = ''.join([each for each in str(uuid.uuid1()).split('-')])
            # 封装vas
            if float(opencv_num) == 3.4:
                docker_vas = f"docker build -t {image_name}_test --build-arg IMAGE_NAME={image_name} -f {res_opencv34_dir}/Dockerfile ."
            else:
                docker_vas = f"docker build -t {image_name}_test --build-arg IMAGE_NAME={image_name} -f {res_opencv41_dir}/Dockerfile ."
            status, res_docker_vas = sdk_subprocess(docker_vas)
            if not status:
                print('docker_vas命令出现错误------------------')
            image_name_test = image_name + "_test"
            cpuset_cpus = str(cpu_set_num).replace(" ", '')[1:-1]
            container_id = zhengzhong.docker_run(random_num, cpuset_cpus, image_name_test, opencv_num)
            docker_auth = f"docker exec {container_id} bash /tmp/authorization.sh"
            subprocess.Popen(docker_auth, shell=True)
            # 等待算法运行300秒, 在统计资源占用
            time.sleep(20)
            container_id = container_id[:12]
            container_list.append(container_id)
            print("container_list", container_list)
        for container_id, cpu_set_num in zip(container_list, cpu_set_nums):
            cpuset_cpus = str(cpu_set_num).replace(" ", '')[1:-1]
            cpu_mem_used = "docker stats --no-stream |grep  %s |awk '{print $3$4}'" % container_id
            cpu_list = []
            mem_list = []
            for i in range(10):
                status, cpu_mem_used_res = zhengzhong.sdk_subprocess(cpu_mem_used)
                time.sleep(1)
                if not status:
                    print('cpu_mem_used_res命令出现错误------------------')
                cpu_used, mem_used = cpu_mem_used_res.split('%')
                cpu_list.append(cpu_used)
                mem_list.append(mem_used[:-3])
            mem_used = max(mem_list)
            cpu_min = min(cpu_list)
            cpu_max = max(cpu_list)
            vas = f"/data/vas_performance/{container_id}/vas_data/log"
            vas_info = "ls %s |awk '{print $1}'" % vas
            info_log = os.popen(vas_info).read()
            vas_info = info_log.split('\n')[-3]
            fps, use_time, run_times = zhengzhong.get_total_seconds(os.path.join(vas, vas_info))
            with open(os.path.join(res_image_data, f'{image_dir}.txt'), 'a+', encoding='utf-8') as f:
                f.write(f"容器:{container_id}, 当前算法共运行路数:{sdk_num}, 当前指定CPU核数{cpuset_cpus}, 指定的CPU核数为:{len(cpu_set_num)}, 服务器总的CPU核数为{res_cpu_total}\n")
                f.write(f'当前算法cpu占用:{cpu_min}%~{cpu_max}%, 内存占用:{mem_used}MiB, 当前算法运行总时间:{use_time}S,运行总帧数:{run_times} FPS:{fps}\n\n')
        print("--------------------------------------------完成验证")
        os.popen("systemctl restart docker")







