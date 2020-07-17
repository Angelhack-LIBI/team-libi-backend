import os

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


class FileMetaMixin(models.Model):
    FILE_UPLOAD_PATH = 'etc'

    file_name = models.CharField(max_length=128, null=True, help_text="첨부파일 이름")
    file_ext = models.CharField(max_length=16, null=True, help_text="첨부파일 확장자")
    file_size = models.PositiveIntegerField(default=0, null=True, help_text="파일 크기")

    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if getattr(self, 'file', None):
            file_name, self.file_ext = os.path.splitext(self.file.file.name)
            self.file_size = int(self.file.file.size)
            if self.file_name:
                if "." in self.file_name:
                    self.file_name = os.path.splitext(self.file_name)[0]
            else:
                self.file_name = file_name
        super(FileMetaMixin, self).save(force_insert=force_insert, force_update=force_update, using=using,
                                        update_fields=update_fields)


class FileMixin(FileMetaMixin):
    file = models.FileField(upload_to=generate_upload_path, null=True, help_text="첨부파일")

    class Meta:
        abstract = True


class ImageMixin(FileMetaMixin):
    file = models.ImageField(upload_to=generate_upload_path, null=True, help_text="첨부이미지")

    class Meta:
        abstract = True
