from typing import List

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import transaction

from libi_sharing.errors import NotExistSharingError
from libi_sharing.models import Sharing, SharingOption, SharingPhoto


def create_sharing(sharing_type: int, area_id: int, title: str, category_id: int, goal_price: int, description: str,
                   option_description: str, option_price: int, photo: List[InMemoryUploadedFile],
                   created_account_id) -> Sharing:
    """
    신규 sharing 을 생성합니다
    :return: 신규 sharing 인스턴스
    :rtype: Sharing
    """
    with transaction.atomic():
        new_sharing = Sharing.objects.create(title=title, description=description, area_id=area_id, category_id=category_id,
                                             created_account=created_account_id, goal_price=goal_price,
                                             sharing_type=sharing_type)
        SharingOption.objects.create(sharing=new_sharing, description=option_description, price=option_price)
        for f in photo:
            SharingPhoto.objects.create(file=f, sharing=new_sharing)
    return new_sharing


def find_sharing(pk: int) -> Sharing:
    """
    이미 존재하는 sharing 찾기
    :return: 찾은 sharing 인스턴스
    :rtype: Sharing
    """
    sharing = Sharing.objects.filter(
        id=pk,
        deleted_at=None
    ).first()
    if not sharing:
        raise NotExistSharingError()

    return sharing
