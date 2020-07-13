import json

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpRequest, JsonResponse
from django.shortcuts import redirect
from django.template import loader

# Create your views here.
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic.base import View
from .models import BookInfo,HeroInfo


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
    return render(request,'index.html',context)


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
class UserView(BaseView,Base2View,View):

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


class BookListView(View):
    '''
    查询所有图书,增加图书
    '''
    def get(self,request):
        '''
        查询所有图书
        路由：GET /books/
        '''

        # 获取所有的图书信息:
        queryset = BookInfo.objects.all()
        # 创建一个新的列表
        book_list = []
        # 遍历查询集, 获取每一本书, 并且拼接, 存放到list中
        for book in queryset:     # 惰性查询
            book_list.append({
                'id': book.id,
                'btitle': book.btitle,
                'bpub_date': book.bpub_date,
                'bread': book.bread,
                'bcomment': book.bcomment,
                'image': book.image.url if book.image else ''
            })
        # 返回json类型数据
        # 这里 JsonResponse(dict, safe=True)
        # 默认第一个参数接收dict类型
        # 如果第一个参数不是字典类型
        # 需要把 safe=False, 否则报类型错误
        return JsonResponse(book_list,safe=False)





