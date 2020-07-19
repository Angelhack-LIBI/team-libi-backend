from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class DockerWebhookView(APIView):
    @swagger_auto_schema(
        operation_summary="Docker Hub Webhook",
        responses={
            status.HTTP_200_OK: ''
        }
    )
    def get(self, request: Request) -> Response:
        print(request.query_params)
        print(request.data)
        return Response(
            status=status.HTTP_200_OK
        )
