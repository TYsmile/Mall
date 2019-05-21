# 定义索引类
from haystack import indexes

from goods.models import SKU


class SKUIndex(indexes.SearchIndex, indexes.Indexable):
    """
    商品模型索引类:
    索引类名: <模型类>+Index
    """
    # document=True：说明text字段是索引字段
    # use_template=True：说明索引字段中包含哪些内容会在一个文件中进行指定
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        """返回索引类对应模型类"""
        return SKU

    def index_queryset(self, using=None):
        """返回要建立索引数据的查询集"""
        return self.get_model().objects.filter(is_launched=True)