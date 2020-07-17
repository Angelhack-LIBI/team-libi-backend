from dataclasses import asdict
from typing import Dict

import jwt
import pendulum

from libi_common.utils import now
from libi_common.oauth.models import StatelessAccount, TokenConfig, TokenPayload
from libi_common.oauth.errors import TokenExpiredError, TokenInvalidError


def generate_access_token(
        account: StatelessAccount,
        expire_after: Dict[str, int],
        max_expire_time: pendulum.DateTime
) -> str:
    """
    AccessToken을 생성합니다
    :param account: 계정
    :param expire_after: 토큰 지속 시간
    :param max_expire_time: 토큰 최대 만료 시간
    :return: 생성된 AccessToken
    :rtype: str
    """
    token_expire_at = min(now().add(**expire_after), max_expire_time)
    payload = TokenPayload.factory(account, token_expire_at)
    token = jwt.encode(
        asdict(payload),
        TokenConfig.SECRET_KEY,
        algorithm=TokenConfig.ALGORITHM,
    ).decode('utf-8')
    return token


def extract_access_token(token: str) -> TokenPayload:
    """
    AccessToken을 검증하고, payload를 가져옵니다
    :param token: accesstoken
    :return: Payload 객체
    :rtype: TokenPayload
    """
    try:
        raw_payload = jwt.decode(
            jwt=token,
            key=TokenConfig.SECRET_KEY,
            algorithms=TokenConfig.ALGORITHM,
            issuer=TokenConfig.ISSUER
        )
        raw_account = raw_payload['account']
        del raw_payload['account']
        return TokenPayload(
            account=StatelessAccount(**raw_account),
            **raw_payload
        )

    except jwt.ExpiredSignature:
        raise TokenExpiredError()

    except (
            jwt.DecodeError,
            jwt.MissingRequiredClaimError,
            jwt.ImmatureSignatureError,
            jwt.InvalidAudienceError,
            jwt.InvalidIssuerError,
            jwt.InvalidIssuedAtError,
            jwt.InvalidTokenError,
    ):
        raise TokenInvalidError()
