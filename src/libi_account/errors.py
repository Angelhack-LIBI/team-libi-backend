from rest_framework import status
from rest_framework.exceptions import APIException


class DuplicateAccountError(APIException):
    """
    중복 계정 오류 (휴대전화번호 중복 등)
    """
    status_code = status.HTTP_409_CONFLICT
    default_detail = '이미 가입된 휴대전화번호입니다'
    default_code = 'duplicate'
