# coding=utf-8
from django.urls import path, include
from .viewset import BookInfoViewSet
from rest_framework.routers import SimpleRouter
# urlpatterns = [
#     path(r'books/', BookInfoViewSet.as_view(
#         {'get': 'list',  # 这里 get  请求对应 list
#          'post': 'create'  # 这里 post 请求对应 create
#          }
#     )),
#     path(r'books/(?P<pk>\d+)/', BookInfoViewSet.as_view(
#         {'get': 'retrieve',  # 这里 get 请求对应 retrieve
#          'put': 'update',  # 这里 put 请求对应 update
#          'delete': 'destroy'}  # 这里 delete 请求对应 destroy
#     )),
#
# ]
urlpatterns = []

router = SimpleRouter()
router.register('books',BookInfoViewSet,base_name='book')
# urlpatterns += router.urls
print('*'*100)
print(router.urls)
urlpatterns.append(path('',include(router.urls)))
# register(prefix, viewset, base_name)
# prefix 该视图集的路由前缀
# viewset 视图集
# base_name 路由名称的前缀