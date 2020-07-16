import json
from rest_framework import serializers
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpRequest, JsonResponse
from django.shortcuts import redirect
from django.template import loader
from rest_framework.generics import GenericAPIView
# Create your views here.
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.base import View
from rest_framework.response import Response
from rest_framework.views import APIView

from user.serializers import BookInfoSerializer
from .models import BookInfo, HeroInfo


def my_decorator(func):
    def wrapper(request, *args, **kwargs):
        print('自定义装饰器被调用了')
        print(f'请求路径：{request.path}')
        return func(request, *args, **kwargs)

    return wrapper


def my_decorator2(func):
    def wrapper(request, *args, **kwargs):
        print('自定义装饰器被调用了22222')
        print('请求的路径:%s' % request.path)
        return func(request, *args, **kwargs)

    return wrapper


def index(request):
    # template = loader.get_template('index.html')
    context = {
        'citys': '北京',
        'adict': {
            'name': '西游记',
            'author': '吴承恩'
        },
        'alist': [1, 2, 3, 4, 5]
    }
    return render(request, 'index.html', context)


def say(request):
    url = reverse('sayname')
    print(url)
    return HttpResponse('say')


def weather(request, city, year):
    print(f'city:{city}')
    print(f'year:{year}')
    return HttpResponse('OK')


def qs(re):
    a = re.GET.get('a')
    b = re.GET.get('b')
    alist = re.GET.getlist('a')
    # print(a,b,alist)
    return HttpResponse((a, b, alist))


# def get_body(request):
#     a = request.POST.get('a')
#     b = request.POST.get('b')
#     alist = request.POST.getlist('a')
#     print(a)
#     print(b)
#     print(alist)
#     return HttpResponse((a, b, alist),404)


def get_body(request: HttpRequest):
    # print(request.method)
    # print(request.user)
    # print(request.path)
    # print(request.encoding)
    # data = request.body
    # res = json.loads(data)
    # print(request.META)
    # print(res)

    if request.COOKIES.get('demo'):
        response = HttpResponse('ok')
    else:
        response = HttpResponse('false')
        response['demo'] = 'Python'
        response.set_cookie('demo1', 'python3', max_age=3600)

    return response


def set_session(request: HttpRequest):
    request.session['one'] = '1'
    request.session['two'] = '2'
    return HttpResponse('保存session数据成功')


@my_decorator
def get_session(request):
    one = request.session.get('one')
    two = request.session.get('two')
    return HttpResponse(f'one={one},two={two}')


class BaseView(object):
    @classmethod
    def as_view(cls, *args, **kwargs):
        view = super().as_view(*args, **kwargs)
        view = my_decorator(view)
        return view


class Base2View(object):
    @classmethod
    def as_view(cls, *args, **kwargs):
        view = super().as_view(*args, **kwargs)
        view = my_decorator2(view)
        return view


# @method_decorator(my_decorator,name='dispatch')
class UserView(BaseView, Base2View, View):

    # def dispatch(self, request, *args, **kwargs):
    #     return super(UserView, self).dispatch(request, *args, **kwargs)

    # @method_decorator(my_decorator)
    def get(self, request):
        """处理GET请求，返回注册页面"""
        # print(request.path)
        return render(request, 'test.html')

    # @method_decorator(my_decorator)
    def post(self, request):
        """处理POST请求，实现注册逻辑"""
        return HttpResponse('这里实现注册逻辑')


# class BookListView(View):
#     '''
#     查询所有图书,增加图书
#     '''
#
#     def get(self, request):
#         '''
#         查询所有图书
#         路由：GET /books/
#         '''
#
#         # 获取所有的图书信息:
#         queryset = BookInfo.objects.all()
#         # 创建一个新的列表
#         book_list = []
#         # 遍历查询集, 获取每一本书, 并且拼接, 存放到list中
#         for book in queryset:  # 惰性查询
#             book_list.append({
#                 'id': book.id,
#                 'btitle': book.btitle,
#                 'bpub_date': book.bpub_date,
#                 'bread': book.bread,
#                 'bcomment': book.bcomment,
#                 'image': book.image.url if book.image else ''
#             })
#         # 返回json类型数据
#         # 这里 JsonResponse(dict, safe=True)
#         # 默认第一个参数接收dict类型
#         # 如果第一个参数不是字典类型
#         # 需要把 safe=False, 否则报类型错误
#         return JsonResponse(book_list, safe=False)
#
#     def post(self, request):
#         '''
#         新增图书 post /books/  参数json
#         :param request:
#         :return:
#         '''
#         # 获取所有非表单数据，得到bytes
#         data = request.body
#         data_dict = json.loads(data)
#
#         book = BookInfo.objects.create(
#             btitle=data_dict.get('btitle'),
#             bpub_date=data_dict.get('bpub_date')
#         )
#
#         return JsonResponse({
#             'id': book.id,
#             'btitle': book.btitle,
#             'bpub_date': book.bpub_date,
#             'bread': book.bread,
#             'bcomment': book.bcomment,
#             'image': book.image.url if book.image else ''
#         }, status=201)


class BookDetailView(View):

    def get(self, request, pk):
        """
        获取单个图书信息
        路由： GET  /books/<pk>/
        """

        try:
            book = BookInfo.objects.get(pk=pk)
        except BookInfo.DoesNotExist:
            return HttpResponse(status=404)
        return JsonResponse({
            'id': book.id,
            'btitle': book.btitle,
            'bpub_date': book.bpub_date,
            'bread': book.bread,
            'bcomment': book.bcomment,
            'image': book.image.url if book.image else ''
        })

    def put(self, request, pk):

        try:
            book = BookInfo.objects.get(pk=pk)
        except BookInfo.DoesNotExist:
            return HttpResponse(status=404)
        json_bytes = request.body
        print(type(json_bytes))
        book_dict = json.loads(json_bytes)
        # 校验参数
        book.btitle = book_dict.get('btitle')
        book.bpub_date = book_dict.get('bpub_date')
        book.save()
        return JsonResponse({
            'id': book.id,
            'btitle': book.btitle,
            'bpub_date': book.bpub_date,
            'bread': book.bread,
            'bcomment': book.bcomment,
            'image': book.image.url if book.image else ''
        })

    def delete(self, request, pk):
        """
        删除图书
        路由： DELETE /books/<pk>/
        """
        try:
            book = BookInfo.objects.get(pk=pk)
        except BookInfo.DoesNotExist:
            return HttpResponse(status=404)
        # 如果存在,调用delete()函数,删掉对应的内容
        book.delete()

        return HttpResponse(status=204)

# APIView
# class BookListView(APIView):
#
#     def get(self, request):
#         # 获取查询集
#         books = BookInfo.objects.all()
#         # 调用序列化器,对查询集进行序列化处理
#         serializer = BookInfoSerializer(books, many=True)
#         # 处理完成的数据, 再经过 Response 类的处理就会变成 json
#         print(self.authentication_classes)
#         print('-----------')
#         print(self.permission_classes)
#         print('===========')
#         print(self.throttle_classes)
#         return Response(serializer.data)
#
#     def post(self,request):
#         # 反序列化
#         serializer = BookInfoSerializer(data =request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.validated_data)
#
#     def put(self,request):
#         # data = json.loads( request.body)
#         # print(data)
#         print(1)
#         book = BookInfo.objects.get(pk = request.data.get('id'))
#         print(book)
#         serializer = BookInfoSerializer(instance=book,data=request.data)
#         print(2)
#         serializer.is_valid(raise_exception=True)
#         print(3)
#         book = serializer.save()
#         print(book)
#         return Response(serializer.data)


# GenericAPIView
class BookListView(GenericAPIView):
    # 指明当前视图使用BookInfoSerializer
    # 这个序列化器类进行数据序列化
    serializer_class = BookInfoSerializer
    queryset =  BookInfo.objects.all()
    # def get(self,request):
    #     # 获取当前类中定义的序列化器类
    #     className = self.get_serializer_class()
    #     serializerObj  = self.get_serializer()
    #     queryset = self.get_queryset()
    #     object = self.get_object()
    #     print(object)
    #     self.check_object_permissions
    #     return Response('get func')

    def get(self,request):

        # 查询出所有图书信息
        obj = self.get_queryset()

        # 返回所有图书信息
        serializer = self.get_serializer(obj,many=True)

        return Response(serializer.data)

    def post(self,request):
        """新建一本图书信息"""
        serializer:serializers.ModelSerializer = self.get_serializer(data = request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

