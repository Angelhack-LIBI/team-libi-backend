class TokenExpiredError(Exception):
    """
    토큰 만료
    """
    pass


class TokenInvalidError(Exception):
    """
    토큰이 올바르지 않음 (sign key 등)
    """
    pass
