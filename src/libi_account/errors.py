from rest_framework import status
from rest_framework.exceptions import APIException


class DuplicateAccountError(APIException):
    """
    중복 계정 오류 (휴대전화번호 중복 등)
    """
    status_code = status.HTTP_409_CONFLICT
    default_detail = '이미 가입된 휴대전화번호입니다'
    default_code = 'duplicate'


class NotExistAccountError(APIException):
    """
    계정 없음 오류
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '입력하신 휴대전화번호 또는 비밀번호가 올바르지 않습니다'
    default_code = 'not_eixst'


class NotExistTokenError(APIException):
    """
    토큰 없음 오류
    """
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = '세션이 만료되었습니다. 다시 로그인하여주십시오'
    default_code = 'not_eixst'

