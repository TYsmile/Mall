from rest_framework import serializers

from goods.models import SKU


class CartSelectAllSerializer(serializers.Serializer):
    """购物车全选序列化器类"""
    selected = serializers.BooleanField(label='全选')


class CartDelSerializer(serializers.Serializer):
    """购物车删除序列化器类"""
    sku_id = serializers.IntegerField(label='商品SKU编号')

    def validate_sku_id(self, value):
        """sku_id对应的商品是否存在"""
        try:
            sku = SKU.objects.get(id=value)
        except SKU.DoesNotExist:
            raise serializers.ValidationError('商品不存在')

        return value


class CartSKUSerializer(serializers.ModelSerializer):
    """购物商品记录显示序列化器类"""
    count = serializers.IntegerField(label='商品数量')
    selected = serializers.BooleanField(label='勾选状态')

    class Meta:
        model = SKU
        fields = ('id', 'name', 'price', 'default_image_url', 'count', 'selected')


class CartSerializer(serializers.Serializer):
    """购物车序列化器类"""
    sku_id = serializers.IntegerField(label='商品SKU编号', min_value=1)
    count = serializers.IntegerField(label='商品数量', min_value=1)
    selected = serializers.BooleanField(label='勾选状态', default=True)

    def validate(self, attrs):
        """sku_id商品是否存在，count是否大于库存"""
        # sku_id商品是否存在
        sku_id = attrs['sku_id']

        try:
            sku = SKU.objects.get(id=sku_id)
        except SKU.DoesNotExist:
            raise serializers.ValidationError('商品不存在')

        # count是否大于库存
        count = attrs['count']
        if count > sku.stock:
            raise serializers.ValidationError('商品库存不足')

        return attrs