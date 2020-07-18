from rest_framework import serializers

from libi_common.serializers import StatelessSerializer
from libi_sharing.models import Sharing, SharingOption


class SharingListFilterSerializer(StatelessSerializer):
    area_id = serializers.IntegerField(required=True)
    keyword = serializers.CharField(required=False)


class SharingOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharingOption
        fields = ('id', 'description', 'minimum_price', 'price')


class SharingListItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sharing
        fields = ('id', 'title', 'sharing_type', 'goal_price', 'thumbnail_url', 'option',)
        read_only_fields = ('id', 'title', 'sharing_type', 'goal_price', 'thumbnail_url', 'option',)

    thumbnail_url = serializers.SerializerMethodField(read_only=True)
    option = serializers.SerializerMethodField(read_only=True)

    def get_thumbnail_url(self, obj: Sharing) -> str:
        pass

    def get_option(self, obj: Sharing) -> SharingOptionSerializer:
        pass
