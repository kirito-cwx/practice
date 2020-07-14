from django.test import TestCase

# Create your tests here.
# 测试序列化器

# import os
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'practice.settings')

from rest_framework import serializers


# class User():
#     '''用户类'''
#
#     def __init__(self, username, age):
#         self.username = username
#         self.age = age
#
#
# class UserSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     age = serializers.IntegerField()
#
#
# if __name__ == '__main__':
#     user = User('zs', 18)
#     serializers = UserSerializer(user)
#     print(serializers.data)
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'practice.settings'
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import django
django.setup()


from user.serializers import BookInfoSerializer,HeroInfoSerializer
from user.models import BookInfo,HeroInfo

if __name__ == '__main__':
    # 查询id为1的图书:
    book = BookInfo.objects.get(id=1)

    # 创建序列化器类的对象:
    serializer = BookInfoSerializer(book)

    # 可以通过data查看结果
    print(serializer.data)
    # hero = HeroInfo.objects.get(id=6)
    # serializer = HeroInfoSerializer(hero)
    # print(serializer.data)