from rest_framework import serializers

from libi_sharing.models import Sharing, SharingOption


class SharingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sharing
        fields = '__all__'  # TODO: 명시적으로 fields를 명시해야 함


class SharingOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharingOption
        fields = ['description', 'minimum_price', 'price']


class SharingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sharing
        fields = ['id', 'title', 'category', 'goal_price', 'sharing_type', 'created_account', 'area', 'option']

    option = serializers.SerializerMethodField()

    def get_option(self, obj: Sharing):
        option_object = SharingOption.objects.get(sharing=obj)
        if option_object:
            return SharingOptionSerializer(option_object).data
