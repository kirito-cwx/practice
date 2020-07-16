# coding=utf-8
from rest_framework import serializers
from .models import BookInfo, HeroInfo


# 定义序列化器
class BookInfoSerializer(serializers.ModelSerializer):
    class Meta:
        # 序列化数据来源于 BookInfo 模型类
        model = BookInfo
        # 对 BookInfo 中的所有数据都进行序列化:all代表所有
        fields = '__all__'

        # 或者
        # 也可以写成下面的形式, 代表我们只序列化对应的字段:
        # fields = ('id', 'btitle', 'bpub_date')
        extra_kwargs = {
            'bread': {'min_value': 0, 'required': True},
            'bcomment': {'min_value': 0, 'required': True},
        }

class HeroInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroInfo
        fields = '__all__'
        depth = 0
        read_only_fields = ('id', 'bread', 'bcomment')

# class HeroInfoSerializer(serializers.Serializer):
#     """
#     英雄数据序列化器
#     """
#     GENDER_CHOICES = ((0, 'male'), (1, 'female'))
#     id = serializers.IntegerField(label='ID', read_only=True)
#     hname = serializers.CharField(label='名字', max_length=20)
#     hgender = serializers.ChoiceField(choices=GENDER_CHOICES, label='性别')
#     hcomment = serializers.CharField(label='描述信息', max_length=200, required=False, allow_null=True)
#     # 1） PrimaryKeyRelatedField
#     hbook = serializers.PrimaryKeyRelatedField(label='图书', read_only=True)
#     # hbook = serializers.PrimaryKeyRelatedField(label='图书', queryset=BookInfo.objects.all())
#     # 指明字段时需要包含read_only=True或者queryset参数：
#     # 包含read_only=True参数时，该字段将不能用作反序列化使用
#     # 包含queryset参数时，将被用作反序列化时参数校验使用
#
#     # 2)使用关联对象的序列化器
#     # hbook = BookInfoSerializer()
#
#     # 3) StringRelatedField 此字段将被序列化为关联对象的字符串表示方式（即str方法的返回值）
#     # hbook = serializers.StringRelatedField(label='图书')

def btitle_validators(value):
    if 'haha' not in value:
        raise  serializers.ValidationError("反序列化时, 传入的字段中没有haha这个字符串")

# class BookInfoSerializer(serializers.Serializer):
#     '''图书数据序列化器'''
#
#     id = serializers.IntegerField(label='ID', read_only=True)
#     btitle = serializers.CharField(label='名称', max_length=20)
#     # btitle = serializers.CharField(label='名称', max_length=20,validators=[btitle_validators])
#     bpub_date = serializers.DateField(label='发布日期', required=True)
#     bread = serializers.IntegerField(label='阅读量', required=False)
#     bcomment = serializers.IntegerField(label='评论量', required=False)
#     image = serializers.ImageField(label='图片', required=False)
#     # 新增
#     # heroinfo_set = serializers.PrimaryKeyRelatedField(queryset=HeroInfo.objects.all(),many=True)
#     # heroinfo_set = HeroInfoSerializer(many=True)
#
#     # def validate_btitle(self, value):
#     #     if 'haha' not in value:
#     #         raise  serializers.ValidationError("反序列化时, 传入的字段中没有haha这个字符串")
#     #     return value
#     # def validate(self, attrs):
#     #     print(attrs)
#     #     bread = attrs['bread']
#     #     bcomment = attrs['bcomment']
#     #     # 进行验证:
#     #     # if bread < bcomment:
#     #     #     raise serializers.ValidationError('阅读量小于评论量')
#     #     return attrs
#
#     def create(self, validated_data):
#         """新建"""
#         return BookInfo.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         """更新，instance为要更新的对象实例"""
#         print(validated_data)
#         instance.btitle = validated_data.get('btitle',instance.btitle)
#         instance.bpub_date = validated_data.get('bpub_date', instance.bpub_date)
#         instance.bread = validated_data.get('bread', instance.bread)
#         instance.bcomment = validated_data.get('bcomment', instance.bcomment)
#         instance.save()
#         return instance

