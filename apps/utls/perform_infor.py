# @Time : 2020/8/7 10:22 
# @modele : perform_infor
# @Author : zhengzhong
# @Software: PyCharm


import requests
import subprocess
import datetime
class PerForm_InFor():
    def __init__(self,name):
        self.name = name
    def sdk_subprocess(self,cmd):
        """
        封装 subprocess 用来定制化返回消息
        :param cmd:
        :param msg:
        :return:
        """
        res_p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        stdout, stderr = res_p.communicate()
        returncode = res_p.returncode
        if returncode == 0:
            if stdout.endswith('\n'):
                return True, stdout.replace('\n', '')
            return True, stdout
        else:
            return False, stderr

    def get_total_seconds(self,info_log):
        begin_time = "cat %s |grep event |awk '{print $2}' |head -1" % info_log
        print("begin_time%s" % begin_time)
        status, begin_time = self.sdk_subprocess(begin_time)
        if not status:
            print(f"begin_time:{begin_time}错误")
        end_time = "tac %s |grep event |awk '{print $2}'|head -1" % info_log
        status, end_time = self.sdk_subprocess(end_time)
        if not status:
            print(f"end_time:{end_time}错误")

        run_times = f"cat {info_log} |grep event |wc -l"
        status, run_times = self.sdk_subprocess(run_times)
        if not status:
            print(f"run_times:{run_times}错误")

        begin_time = datetime.datetime.strptime(begin_time, '%H:%M:%S.%f')
        end_time = datetime.datetime.strptime(end_time, '%H:%M:%S.%f')
        use_time = (end_time - begin_time).seconds

        fps = int(int(run_times) / int(use_time))
        return fps, use_time, run_times

    def get_opencv_num(self,image_name):
        """
        获取算法opencv版本
        :param image_name:
        :return:
        """
        flask_url_opencv = "http://192.168.1.147:5000/api/v1.0/sdk_opencv_message"
        data = {
            "image_name": image_name
        }
        res = requests.post(flask_url_opencv, data=data).json().get("errmsg")[-3:]
        return res

    def run_sdk_opencv(self):
        """
        启动cpu算法命令创建算法基础环境
        :return:
        """
        cpu_total = "lscpu |grep CPU\(s\):|awk 'NR==1 {print $2}'"
        mem_total = "free -m |awk 'NR==2 {print $2}'"
        status, res_cpu_total = self.sdk_subprocess(cpu_total)
        if not status:
            print('res_cpu_total命令出现错误------------------')
            print(res_cpu_total)

        status, res_mem_total = self.sdk_subprocess(mem_total)
        if not status:
            print('res_mem_total命令出现错误------------------')
            print(res_mem_total)
        return res_cpu_total, res_mem_total


    def cpunum_set(self,cpuset_nums):
        """
        主要用于cpu总个数计算共有多少个组合
        :param cpuset_nums:
        :return:
        """
        for cpu_num in cpuset_nums:
            cpuset_nums = []
            sdk_num, k = cpu_num
            for s in range(k):
                cpuset_nums.append(s)
            cpuset_nums = tuple(cpuset_nums)
            total_nums = [cpuset_nums]
            for i in range(sdk_num):
                if int(sdk_num) == len(total_nums):

                    yield (sdk_num, total_nums)
                single_nums = []
                for s in total_nums[-1]:
                    s += len(total_nums[-1])
                    single_nums.append(s)
                total_nums.append(tuple(single_nums))

    def opeccv_num_name(self,opencv_num, res_opencv34_dir, res_opencv41_dir, random_num, res_vas_dir,cpus,image):
        """
        :param opencv_num:
        :param res_opencv34_dir:
        :param res_opencv41_dir:
        :param random_num:
        :param res_vas_dir:
        :return:
        """
        if float(opencv_num) == 4.1:
            docker_command_41 = f' docker run -itd --privileged  -v {res_opencv41_dir}:/tmp  -v /data/vas_performance:/data -v vas_{random_num}:/usr/local/vas  --cpuset-cpus="{cpus}" --rm {image}'
            print(docker_command_41)
            status, res_docker_command_41 = self.sdk_subprocess(docker_command_41)
            if not status:
                print('res_docker_command_41命令出现错误------------------')
            print('res_docker_command_41', res_docker_command_41)
            docker_run_conf = f"cp {res_opencv41_dir}/run_3.0.conf {res_vas_dir}/run.conf"
            status, res_docker_run_conf = self.sdk_subprocess(docker_run_conf)
            if not status:
                print('docker_run_conf命令出现错误------------------')
            print('res_docker_run_conf', res_docker_run_conf)
            return res_docker_command_41
        else:
            docker_command_34 = f' docker run -itd --privileged  -v {res_opencv34_dir}:/tmp  -v  vas_{random_num}:/usr/local/vas -v /data/vas_performance:/data  --cpuset-cpus="{cpus}" --rm {image}'
            status, res_docker_command_34 = self.sdk_subprocess(docker_command_34)
            if not status:
                print('res_docker_command_34命令出现错误------------------')
            print(res_docker_command_34)
            docker_run_conf = f"cp {res_opencv34_dir}/run_2.5.conf {res_vas_dir}/run.conf"
            status, res_docker_run_conf = self.sdk_subprocess(docker_run_conf)
            if not status:
                print('docker_run_conf命令出现错误------------------')
            print(res_docker_run_conf)
            return res_docker_command_34

    def docker_run(self,random_num, cpus, image, opencv_num):
        volume_container_num = f"docker volume create vas_{random_num}"
        status, res_volume_container_num = self.sdk_subprocess(volume_container_num)
        if not status:
            print('res_volume_container_num命令出现错误------------------', res_volume_container_num)
        vas_dir = "docker volume inspect  vas_%s|grep Mountpoint|awk '{print $2}'" % random_num
        status, res_vas_dir = self.sdk_subprocess(vas_dir)
        res_vas_dir = res_vas_dir[1:-8]
        opencv34_dir = "docker volume inspect  opencv_34 |grep Mountpoint|awk '{print $2}'"
        _, res_opencv34_dir = self.sdk_subprocess(opencv34_dir)
        res_opencv34_dir = res_opencv34_dir[1:-8]
        opencv41_dir = "docker volume inspect  opencv_41 |grep Mountpoint|awk '{print $2}'"
        _, res_opencv41_dir = self.sdk_subprocess(opencv41_dir)
        res_opencv41_dir = res_opencv41_dir[1:-8]
        self.opeccv_num_name(opencv_num, res_opencv34_dir, res_opencv41_dir, random_num, res_vas_dir,cpus,image)
