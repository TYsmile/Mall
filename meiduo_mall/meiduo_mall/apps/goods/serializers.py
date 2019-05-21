from rest_framework import serializers
from drf_haystack.serializers import HaystackSerializer

from goods.models import SKU, GoodsCategory, GoodsChannel
from goods.search_indexes import SKUIndex


class SKUSerializer(serializers.ModelSerializer):
    """商品序列化器类"""
    class Meta:
        model = SKU
        fields = ('id', 'name', 'price', 'default_image_url', 'comments')


class SKUIndexSerializer(HaystackSerializer):
    """
    商品搜索结果序列化器类
    """
    object = SKUSerializer(read_only=True)

    class Meta:
        # 指定模型索引类
        index_classes = [SKUIndex]
        fields = ('text', 'object')


class CategorySerializer(serializers.ModelSerializer):
    """
    类别序列化器
    """
    class Meta:
        model = GoodsCategory
        fields = ('id', 'name')


class ChannelSerializer(serializers.ModelSerializer):
    """
    频道序列化器
    """
    category = CategorySerializer()

    class Meta:
        model = GoodsChannel
        fields = ('category', 'url')
