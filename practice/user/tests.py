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
# from rest_framework.renderers import
from user.serializers import BookInfoSerializer, HeroInfoSerializer
from user.models import BookInfo, HeroInfo
from rest_framework.response import Response
# from .viewseturls import

if __name__ == '__main__':
    # 查询id为1的图书:
    # book = BookInfo.objects.all()
    # print(book)
    #
    # # 创建序列化器类的对象:
    # serializer = BookInfoSerializer(book)
    #
    # # 可以通过data查看结果
    # print(serializer.data)
    # hero = HeroInfo.objects.get(id=6)
    # serializer = HeroInfoSerializer(hero)
    # print(serializer.data)
    # data =  {'btitle': 'about djangos', 'bread': 10, 'bcomment': 20,'bpub_date':'2021-05-10'}
    # serializer = BookInfoSerializer(data=data, context={'request': 1})
    # print(serializer.context)
    # # print(serializer.id)
    # print(serializer.is_valid())
    # print(serializer.errors)
    # print(serializer.validated_data)
    # book = serializer.save()
    # print(book)
    # books = BookInfo.objects.all()
    # print(books)
    # book = BookInfo.objects.get(id=2)
    # data = {'btitle': '倚天剑2'}
    # serializer = BookInfoSerializer(book, data=data,partial=True)
    # serializer.is_valid(raise_exception=True)  # True
    # serializer.save(owner='cwx')  # <BookInfo: 倚天剑>
    # print(book.btitle)  # '倚天剑'
    # books = BookInfo.objects.all()
    # print(books)
    # data = {'btitle': 'about django', 'bread': 10, 'bcomment': 20,"bpub_date":'2020-10-10'}
    # # 传入数据, 进行检测:
    # serializer = BookInfoSerializer(data=data)
    #
    # print(serializer.is_valid())
    # print(serializer.errors)
    # print(serializer.validated_data)
    #
    # # 进行保存:
    # book = serializer.save()
    # # 查看是否保存成功:
    # print(book)
    book = BookInfo.objects.last()
    print(book)


