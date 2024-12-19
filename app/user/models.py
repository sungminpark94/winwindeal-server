from django.db import models
from django.contrib.auth.models import AbstractUser

class SocialProviderChoice(models.TextChoices):
    KAKAO = 'KAKAO', 'Kakao'
    # 다른 소셜 로그인 옵션들을 추가할 수 있습니다
    # GOOGLE = 'GOOGLE', 'Google'
    # NAVER = 'NAVER', 'Naver'

class CustomUser(AbstractUser):
    social_provider = models.CharField(
        max_length=20,
        choices=SocialProviderChoice.choices,
        null=True,
        blank=True
    )
    