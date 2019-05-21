from rest_framework import serializers

from areas.models import Area


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ('id', 'name')


class SubAreaSerializer(serializers.ModelSerializer):
    # 使用指定的序列化器进行序列化
    subs = AreaSerializer(many=True)

    class Meta:
        model = Area
        fields = ('id', 'name', 'subs')
