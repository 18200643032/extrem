# @Time : 2020/8/1 10:30 
# @modele : urls
# @Author : zhengzhong
# @Software: PyCharm


from django.urls import re_path
from apps.api_1_0 import views

urlpatterns = [
    re_path("standard", views.standard), #规范
    re_path("ias",views.ias),
    re_path("opencv",views.opencv),
    re_path("file_image",views.file_image)
]