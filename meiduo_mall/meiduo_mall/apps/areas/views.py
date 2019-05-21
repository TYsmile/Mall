from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from areas.models import Area
from areas.serializers import AreaSerializer, SubAreaSerializer
# Create your views here.


class AreasViewSet(CacheResponseMixin, ReadOnlyModelViewSet):
    """地区视图集"""
    # 关闭分页
    pagination_class = None

    def get_serializer_class(self):
        if self.action == 'list':
            return AreaSerializer
        else:
            return SubAreaSerializer

    def get_queryset(self):
        if self.action == 'list':
            return Area.objects.filter(parent=None)
        else:
            return Area.objects.all()


# GET /areas/(?P<pk>\d+)/
# class SubAreasView(GenericAPIView):
# class SubAreasView(RetrieveAPIView):
#     queryset = Area.objects.all()
#     serializer_class = SubAreaSerializer
#
#     # def get(self, request, pk):
#     #     """
#     #     获取指定的地区的信息:
#     #     1. 根据pk获取指定的地区信息
#     #     2. 将地区序列化并返回(注: 将地区下级地区嵌套进行序列化)
#     #     """
#     #     # 1. 根据pk获取指定的地区信息
#     #     area = self.get_object()
#     #
#     #     # 2. 将地区序列化并返回(注: 将地区下级地区嵌套进行序列化)
#     #     serializer = self.get_serializer(area)
#     #     return Response(serializer.data)


# GET /areas/
# class AreasView(GenericAPIView):
# class AreasView(ListAPIView):
#     # 指定当前视图所使用的查询集
#     queryset = Area.objects.filter(parent=None)
#     serializer_class = AreaSerializer
#
#     # def get(self, request):
#     #     """
#     #     获取所有省级地区的信息:
#     #     1. 查询所有省级地区的信息
#     #     2. 将省级地区的信息序列化并返回
#     #     """
#     #     # 1. 查询所有省级地区的信息
#     #     areas = self.get_queryset()
#     #
#     #     # 2. 将省级地区的信息序列化并返回
#     #     serializer = self.get_serializer(areas, many=True)
#     #     return Response(serializer.data)
