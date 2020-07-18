from libi_sharing.errors import NotExistSharingError
from libi_sharing.models import Sharing


def create_sharing(**kwargs) -> Sharing:
    """
    신규 sharing 을 생성합니다
    :return: 신규 sharing 인스턴스
    :rtype: Sharing
    """
    new_sharing = Sharing.create_sharing(**kwargs)
    return new_sharing


def find_sharing(id: int) -> Sharing:
    """
    이미 존재하는 sharing 찾기
    :return: 찾은 sharing 인스턴스
    :rtype: Sharing
    """
    sharing = Sharing.objects.filter(
        id=id,
        deleted_at=None
    ).first()
    if not sharing:
        raise NotExistSharingError()

    return sharing