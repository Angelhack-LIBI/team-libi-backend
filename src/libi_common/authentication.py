from rest_framework.authentication import BaseAuthentication, SessionAuthentication

from libi_common.oauth.errors import TokenExpiredError, TokenInvalidError
from libi_common.oauth.utils import extract_access_token


class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        access_token = request.META.get('HTTP_X_AUTHORIZATION', None)
        request.access_token = access_token

        if not access_token:
            return None

        try:
            payload = extract_access_token(access_token)
            return payload.account, access_token

        except (TokenExpiredError, TokenInvalidError):
            return None


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening
