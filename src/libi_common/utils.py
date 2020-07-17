import datetime

import pendulum
from django.conf import settings


def now() -> pendulum.DateTime:
    """
    현재 시간 pendulum instance를 반환합니다
    :return: 현재 시간
    """
    return pendulum.now(tz=settings.TIME_ZONE)


def datetime_to_pendulum(dt: datetime.datetime) -> pendulum.DateTime:
    """
    datetime instance를 pendulum으로 변환합니다
    :param dt: 변환할 datetime instance
    :return: 변환된 pendulum instance
    """
    return pendulum.instance(dt).in_tz(settings.TIME_ZONE)
