from django.urls import path, re_path
from .import views
from .viewset import BookInfoViewSet
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path(r'index/', views.index),
    path(r'say/', views.say),
    path(r'qs/', views.qs),
    path(r'qb/', views.get_body),
    path(r'set_session/', views.set_session),
    path(r'get_session/', views.get_session),
    path(r'qb/', views.get_body),
    path(r'register/', views.UserView.as_view()),
    # path(r'books/', views.BookListView.as_view()),
    # re_path(r'books/(\d+)/', views.BookDetailView.as_view()),
    re_path(r'weather/([a-z]+)/(\d{4})/', views.weather),
]

# 创建一个默认的路由对象
router = DefaultRouter()

# 使用路由对象,注册路由信息:
# 'books'指的是:上面的路由路径,即:该视图集的路由前缀
# viewset.BookInfoViewSet指的是上面定义的用于处理数据序列化的视图集
# base_name = 'books'指的是路由名称前缀
router.register('books',viewset=BookInfoViewSet,base_name='books')

# 将生成的配置项, 放入到urlpatterns列表里.
urlpatterns += router.urls
