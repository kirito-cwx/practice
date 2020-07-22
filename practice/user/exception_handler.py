# coding=utf-8
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework import status
from django.db import DatabaseError


# 自定义数据库异常处理
# exc 指的是抛出的异常对象
def dry_exception_handler(exc,context):
    # 先调用rest_framework 默认的异常处理方法
    # 获取到 异常处理对象 response
    response = exception_handler(exc,context)

    # 查看 response 是否等于 None
    # 如果等于 None 则代表是 DRF 框架不能处理的异常
    # 在此处补充自定义的异常处理
    if response is None:
        # 判断错误是否是数据库错误:
        if isinstance(exc, DatabaseError):
            # 打印错误信息
            print('%s' % exc)
            # 返回响应 507:和存储有关的错误
            response = Response({'detail': '服务器内部错误'}, status=status.HTTP_507_INSUFFICIENT_STORAGE)

        # 返回最终的 response 对象
    return response