from django.contrib import admin
from .models import BookInfo, HeroInfo


admin.site.site_header = '传智书城'
admin.site.site_title = '传智书城MIS'
admin.site.index_title = '欢迎使用传智书城MIS'
# 类型InlineModelAdmin：表示在模型的编辑页面嵌入关联模型的编辑。
# 子类TabularInline：以表格的形式嵌入。
# 子类StackedInline：以块的形式嵌入。
class HeroInfoStackInline(admin.TabularInline):
    model = HeroInfo  # 要编辑的对象
    extra = 1  # 附加编辑的数量

# 装饰器注册
@admin.register(BookInfo)
class BookInfoAdmin(admin.ModelAdmin):
    # 该字段决定每页展示行数的多少
    list_per_page = 2

    # 决定列表页展示的内容:
    list_display = ['id', 'btitle', 'pub_date','bpub_date', 'bread', 'bcomment']
    # fields = ('btitle',)
    # fields与fieldsets两者选一使用。
    # 分组显示
    fieldsets = (
        ('基本',{'fields':['btitle','bpub_date','image']}),
        ('高级',{'fields':('bread','bcomment'),
               'classes':('collapse',)})# 是否折叠显示
    )
    # inlines = [HeroInfoStackInline]

@admin.register(HeroInfo)
class HeroInfoAdmin(admin.ModelAdmin):
    # 把上面定义的函数名添加到列表中:
    list_display = ['id', 'hname', 'hbook', 'read']
    # 该字段决定了右侧是否有过滤器, 以及按照哪些内容进行过滤:
    list_filter =  ['hbook','hgender']
    # 可以在当前页面的最上方添加一个搜索框 ,设置搜索栏范围，如果有外键，要注明外键的哪个字段，双下划线
    search_fields = ['hbook__btitle']
    list_display_links = ('hname',)  # 设置页面上哪个字段可单击进入详细页面
    fields = ('hname',)  # 设置添加/修改详细信息时，哪些字段显示，在这里 remark 字段将不显示



# admin.site.register(BookInfo,BookInfoAdmin) # 参数注册
# admin.site.register(HeroInfo)
