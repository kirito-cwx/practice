from django.db import models


# Create your models here.

class BookInfo(models.Model):
    btitle = models.CharField(max_length=20, verbose_name='名称')
    bpub_date = models.DateField(verbose_name='发布日期')
    bread = models.IntegerField(default=0, verbose_name='阅读量')
    bcomment = models.IntegerField(default=0, verbose_name='评论量')
    image = models.ImageField(upload_to='booktest', verbose_name='图片', null=True)
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'tb_books'  # 数据库表名
        verbose_name = '图书'
        verbose_name_plural = verbose_name

    def pub_date(self):
        return self.bpub_date.strftime('%Y年%m月%d日'.encode('unicode_escape').decode('utf8')).encode().decode(
            'unicode_escape')

    # 包含了中文，中文没有转化为unicode编码失败的。解决方法先转为uncode编码执行，执行完后转为utf-8显示
    # 2.解决方法: 修改语言符号 locale.setlocale(locale.LC_CTYPE,'chinese')
    # 3.格式化输出 time.strftime('%Y{y}%m{m}%d{d} %H{h}%M{f}%S{s}').format(y='年', m='月', d='日', h='时', f='分', s='秒')
    pub_date.short_description = '发布日期'
    pub_date.admin_order_field = 'bpub_date'

    def __str__(self):
        return self.btitle


class HeroInfo(models.Model):
    GENDER_CHOICES = (
        (0, 'male'),
        (1, 'female')
    )
    hname = models.CharField(max_length=20, verbose_name='名称')
    hgender = models.SmallIntegerField(choices=GENDER_CHOICES, verbose_name='性别')
    hcomment = models.CharField(max_length=200, null=True, verbose_name='描述信息')
    hbook = models.ForeignKey(BookInfo, on_delete=models.CASCADE, verbose_name='图书')

    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'tb_heros'
        verbose_name = '英雄'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.hname

    def read(self):
        return self.hbook.bread

    read.short_description = '图书阅读量'
