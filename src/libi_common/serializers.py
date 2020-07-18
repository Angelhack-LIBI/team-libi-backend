from rest_framework import serializers


class StatelessSerializer(serializers.Serializer):

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class APIErrorSerializer(StatelessSerializer):
    detail = serializers.CharField(required=False)
