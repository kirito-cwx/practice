# coding=utf-8
from rest_framework.viewsets import ModelViewSet
from .models import BookInfo
from .serializers import BookInfoSerializer


class BookInfoViewSet(ModelViewSet):
    # 查询出所有的数据,存放到查询集中(queryset: 查询集)
    queryset = BookInfo.objects.all()
    # 使用序列化器进行序列化:
    serializer_class = BookInfoSerializer