import os

from django.db import models


# Create your models here.
class CCTV(models.Model):
    """CCTV Model Description

    Fields
        name (CharField) : 모델명
        region (CharField) : 설치 지역
        description (TextField) : 상세 주소 및 추가 설명
    """

    class Meta:
        verbose_name_plural = "CCTV 관리"

    name = models.CharField(
        max_length=50,
        verbose_name="모델명",
    )
    region = models.CharField(
        max_length=50,
        verbose_name="감시 지역",
    )
    description = models.TextField(
        verbose_name="상세 주소 / 추가 설명",
        blank=True,
    )

    def __str__(self) -> str:
        if len(self.description) > 15:
            return f"{self.region} / {self.description[:15]}..."
        else:
            return f"{self.region} / {self.description}"


def custom_upload_to(instance, filename):
    return os.path.join(instance.cctv, filename)


class Video(models.Model):
    """Video Model Description

    Field:
        video (FileField) : 동영상을 받는 필드. 딥러닝 모델을 거쳐 위반 이미지만 db에 저장할 예정
        cctv (ForeignKey) : 해당 비디오를 찍은 cctv
    """

    # 임시 함수. 후에 딥러닝 모델과 결합 후 위치,내용 재정의

    video = models.FileField(upload_to=custom_upload_to, max_length=100)
    cctv = models.ForeignKey(
        "cctvs.CCTV",
        verbose_name="cctv",
        on_delete=models.SET_NULL,
        related_name="videos",
        null=True,
    )
