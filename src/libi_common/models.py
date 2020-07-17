import pendulum
from django.conf import settings
from django.db import models


class SimpleBaseModel(models.Model):
    id = models.AutoField(primary_key=True)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True, help_text="생성 일시")

    class Meta:
        abstract = True


class BaseModel(SimpleBaseModel):
    updated_at = models.DateTimeField(auto_now=True, db_index=True, help_text="수정 일시")
    deleted_at = models.DateTimeField(null=True, db_index=True, help_text="삭제 일시")

    class Meta:
        abstract = True

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None

    def delete(self, using=None, keep_parents=False):
        """완전히 데이터를 제거하는 대신 삭제 플래그만 삽입하여 삭제를 마킹합니다."""
        self.deleted_at = pendulum.now(tz=settings.TIME_ZONE)
        super(BaseModel, self).save()
