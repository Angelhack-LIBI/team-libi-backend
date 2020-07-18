from rest_framework import mixins, permissions
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.viewsets import GenericViewSet

from libi_sharing.models import Sharing
from libi_sharing.serializers import SharingSerializer, SharingListSerializer


class SharingView(GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin,
                  mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class = SharingListSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Sharing.objects

    def get_serializer_class(self):
        if self.action == 'list':
            return SharingListSerializer

        return SharingSerializer

    @action(methods=['POST'], detail=True, url_path='apply')
    def apply(self, request: Request, *args, **kwargs):
        pass
