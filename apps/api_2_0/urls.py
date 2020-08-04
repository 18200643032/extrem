# @Time : 2020/8/4 14:26 
# @modele : urls
# @Author : zhengzhong
# @Software: PyCharm

from django.urls import re_path
from apps.api_2_0 import views

urlpatterns = [
    re_path("upload_code", views.upload_code), #规范
]