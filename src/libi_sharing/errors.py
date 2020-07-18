from rest_framework import status
from rest_framework.exceptions import APIException


class NotExistSharingError(APIException):
    """
    sharing 없음 오류
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'sharing id 가 존재하지 않습니다'
    default_code = 'not_exist'

