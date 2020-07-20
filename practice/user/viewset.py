# coding=utf-8
from django.utils.decorators import method_decorator
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.viewsets import ModelViewSet, ViewSet, GenericViewSet, ReadOnlyModelViewSet
from .models import BookInfo
from .serializers import BookInfoSerializer
from rest_framework.mixins import ListModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.decorators import action


class BookInfoViewSet(ModelViewSet):
    # 查询出所有的数据,存放到查询集中(queryset: 查询集)
    queryset = BookInfo.objects.all()
    # 使用序列化器进行序列化:
    serializer_class = BookInfoSerializer
    lookup_url_kwarg = 'hbook'
    filter_fields = ('btitle', 'bread')

    # 给当前视图增加认证: SessionAuthentication--session认证
    # authentication_classes = (SessionAuthentication,)

    # # 给当前视图添加权限: 仅通过认证的用户能够访问该视图
    # permission_classes = (IsAuthenticated,)

    # # 添加限制信息, 但是这里添加的将会覆盖掉全局设置的
    # throttle_classes = (AnonRateThrottle,)

    # 这里的 contacts 指的是 settings.py 中定义的名字
    # throttle_scope = 'contacts'

    @action(methods=['get'], detail=False)
    def latest(self, request):
        '''
        返回最新的图书信息
        :param request:
        :return:
        '''
        book = BookInfo.objects.latest('id')
        serializer = self.get_serializer(book)
        return Response(serializer.data)

    @action(methods=['put'], detail=True, url_path='userss', url_name='reads')
    def read(self, request, pk):
        """
        修改图书的阅读量数据
        """
        book = self.get_object()
        book.bread = request.data.get('read')
        book.save()
        serializer = self.get_serializer(book)
        return Response(serializer.data)


# class BookInfoViewSet(ViewSet):
#     '''
#     ViewSet 继承自 APIView 与 ViewSetMixin
#     作用也与 APIView 基本类似，提供了身份认证、权限校验、流量管理等
#     在ViewSet中，没有提供任何动作(action)方法，需要我们自己实现action方法
#     ViewSet主要通过继承ViewSetMixin来实现对 as_view( ) 中字典({'get':'list'}) 的映射工作
#     '''
#
#     # 无用,等同于APIView,多的只是请求方法对应动作
#     # 内部实现action方法
#     # 这里我只写了一个, 其他的类似:
#     # ListModelMixin功能
#     def list(self, request):
#         # 获取所有的数据:
#         books = BookInfo.objects.all()
#         # 使用序列化器, 多个数据进行解析
#         serializer = BookInfoSerializer(books, many=True)
#         # 返回解析后的结果
#         return Response(serializer.data)


class BookInfoGenericViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = BookInfo.objects.all()
    serializer_class = BookInfoSerializer

    # GenericViewSet无用,等同于GenericAPIView,多的只是请求方法对应动作
    # def get_serializer_class(self):
    #     if self.action == 'create':
    #         return OrderCommitSerializer
    #     else:
    #         return OrderDataSerializer

    # 添加自定义动作。
    def latest(self, request):
        '''
        返回最新的图书信息
        :param request:
        :return:
        '''
        book = BookInfo.objects.latest('id')
        serializer = self.get_serializer(book)
        return Response(serializer.data)

    def read(self, request, pk):
        """
        修改图书的阅读量数据
        """
        book = self.get_object()
        book.bread = request.data.get('read')
        book.save()
        serializer = self.get_serializer(book)
        return Response(serializer.data)
