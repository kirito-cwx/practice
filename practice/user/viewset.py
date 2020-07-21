# coding=utf-8
from django.db.models import Q
from django.utils.decorators import method_decorator
from rest_framework.authentication import SessionAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.viewsets import ModelViewSet, ViewSet, GenericViewSet, ReadOnlyModelViewSet
from .models import BookInfo
from .serializers import BookInfoSerializer
from rest_framework.mixins import ListModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.decorators import action
from django_filters import rest_framework as filters
from django import forms

# class MultiValueCharFilter(filters.CharFilter):
#     def __init__(self, *args, **kwargs):
#         kwargs.setdefault('distinct', True)
#         self.conjoined = kwargs.pop('conjoined', False)
#         self.null_value = kwargs.get('null_value',  'null')
#         super().__init__(*args, **kwargs)
#
#     def get_filter_predicate(self, v):
#         name = self.field_name
#         if name and self.lookup_expr != 'exact':
#             name = '__'.join([name, self.lookup_expr])
#         try:
#             return {name: getattr(v, self.field.to_field_name)}
#         except (AttributeError, TypeError):
#             return {name: v}
#
#     def filter(self, qs, value):
#         print(value)
#         if not value:
#             # Even though not a noop, no point filtering if empty.
#             return qs
#
#         if not self.conjoined:
#             q = Q()
#         for v in value.split(','):
#             if v == self.null_value:
#                 v = None
#             predicate = self.get_filter_predicate(v)
#             if self.conjoined:
#                 qs = self.get_method(qs)(**predicate)
#             else:
#                 q |= Q(**predicate)
#
#         if not self.conjoined:
#             qs = self.get_method(qs)(q)
#
#         return qs.distinct() if self.distinct else qs


# TODO  查询字符串中表示多个选择（例如，“？btitle = a,b”）
# class MultiValueCharFilter(filters.MultipleChoiceFilter):
#     field_class = forms.CharField
#     def filter(self, qs, value):
#         value = value.split(',')
#         return super().filter(qs,value)

class BookInfoFilterSet(filters.FilterSet):
    min_bread = filters.NumberFilter(field_name='bread', lookup_expr='gte')
    max_bread = filters.NumberFilter(field_name='bread', lookup_expr='lte')
    # btitle= filters.MultipleChoiceFilter(field_name='btitle', lookup_expr='contains',choices=(('abou','about django'),))# 查询字符串中表示多个选择（例如，“？btitle = a$btitle=b”）
    # btitle= MultiValueCharFilter(field_name='btitle', lookup_expr='contains',)# 查询字符串中表示多个选择（例如，“？btitle = a,b”）
    btitle= filters.CharFilter(field_name='btitle', lookup_expr='contains')
    # btitles= filters.CharFilter(method='dry_filter_btitle')
    # btitle= filters.CharFilter(method='dry_filter_btitle',lookup_expr='contains') # 使用method时lookup_expr无效

    class Meta:
        model = BookInfo
        fields = ['btitle','max_bread', 'min_bread']

    def dry_filter_btitle(self,queryset,name,value):
        a=0
        print(a)
        print(queryset)
        print(name,value)
        a+=1
        # print(*args,**kwargs)
        return BookInfo.objects.filter(**{
            # f'{name}': value,
            f'btitle__contains': value,
        })
        # return queryset


# 自定义分页器类
class LargeResultsSetPagination(PageNumberPagination):
    # page_size 每页数目
    # page_query_param 前端发送的页数关键字名，默认为 "page"
    # page_size_query_param 前端发送的每页数目关键字名，默认为None
    # max_page_size 前端最多能设置的每页数量
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10000

    # LimitOffsetPagination
    # default_limit 默认限制，默认值与PAGE_SIZE设置一致
    # limit_query_param limit参数名，默认'limit'
    # offset_query_param offset参数名，默认'offset'
    # max_limit 最大limit限制，默认None

class BookInfoViewSet(ModelViewSet):
    # 查询出所有的数据,存放到查询集中(queryset: 查询集)
    queryset = BookInfo.objects.all()
    # 使用序列化器进行序列化:
    serializer_class = BookInfoSerializer
    # pagination_class = None
    pagination_class = LargeResultsSetPagination
    # lookup_url_kwarg = 'hbook'
    # filter_fields = ('btitle', 'bread')
    # filterset_fields = ('btitle', 'bread')
    filterset_class = BookInfoFilterSet  # 不支持将filterset_fields 和 filterset_class一起使用。
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
