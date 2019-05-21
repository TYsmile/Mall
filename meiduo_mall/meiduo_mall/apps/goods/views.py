from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from drf_haystack.viewsets import HaystackViewSet
from rest_framework_extensions.cache.mixins import ListCacheResponseMixin

from goods import constants
from goods.serializers import SKUSerializer, SKUIndexSerializer
from goods.serializers import ChannelSerializer, CategorySerializer
from goods.models import SKU, GoodsCategory


# Create your views here.


class SKUSearchViewSet(HaystackViewSet):
    """商品搜索视图集"""
    # 指定索引模型类
    index_models = [SKU]

    # 指定搜索结果序列化时所使用的序列化器类
    serializer_class = SKUIndexSerializer


# GET /categories/(?P<category_id>\d+)/skus/?page=<page>&page_size=<page_size>&ordering=<field>
# class SKUListView(GenericAPIView):
class SKUListView(ListAPIView):
    # 指定当前视图所使用的查询集
    # queryset = SKU.objects.filter(category_id=category_id, is_launched=True)
    serializer_class = SKUSerializer

    # 排序
    filter_backends = [OrderingFilter]
    # 指定排序字段
    ordering_fields = ('create_time', 'price', 'sales')

    def get_queryset(self):
        """返回视图使用的查询集"""
        category_id = self.kwargs['category_id']
        return SKU.objects.filter(category_id=category_id, is_launched=True)

    # def get(self, request, category_id):
    #     """
    #     self.kwargs：保存从url地址中提取的所有命名参数
    #     获取分类商品列表信息:
    #     1. 根据`category_id`获取分类下面所有商品的信息
    #     2. 将商品的信息序列化并返回
    #     """
    #     # 1. 根据`category_id`获取分类下面所有商品的信息
    #     skus = self.get_queryset()
    #
    #     # 2. 将商品的信息序列化并返回
    #     serializer = self.get_serializer(skus, many=True)
    #     return Response(serializer.data)


class CategoryView(GenericAPIView):
    """
    类别
    """
    queryset = GoodsCategory.objects.all()

    def get(self, request, pk=None):
        ret = dict(
            cat1='',
            cat2='',
            cat3=''
        )
        category = self.get_object()
        if category.parent is None:
            # 当前类别为一级类别
            ret['cat1'] = ChannelSerializer(category.goodschannel_set.all()[0]).data
        elif category.goodscategory_set.count() == 0:
            # 当前类别为三级
            ret['cat3'] = CategorySerializer(category).data
            cat2 = category.parent
            ret['cat2'] = CategorySerializer(cat2).data
            ret['cat1'] = ChannelSerializer(cat2.parent.goodschannel_set.all()[0]).data
        else:
            # 当前类别为二级
            ret['cat2'] = CategorySerializer(category).data
            ret['cat1'] = ChannelSerializer(category.parent.goodschannel_set.all()[0]).data

        return Response(ret)


class HotSKUListView(ListCacheResponseMixin, ListAPIView):
    """
    热销商品, 使用缓存扩展
    """
    serializer_class = SKUSerializer
    pagination_class = None

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return SKU.objects.filter(category_id=category_id, is_launched=True).order_by('-sales')[0:constants.HOT_SKUS_COUNT_LIMIT]
