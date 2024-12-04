# from django.db import models

# from django.contrib.auth.models import AbstractBaseUser
# # Create your models here.
# class User(AbstractBaseUser):
#     email = models.EmailField(max_length= 100)
#     nickname = models.CharField(max_length=100)
#     phonenumber = models.CharField(max_length=30)

#     USERNAME_FIELD = 'email'


# class UserCar(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     car = models.ForeignKey('car.Car', on_delete=models.CASCADE)

from django.contrib.auth.models import AbstractUser
from django.db import models

class SocialProviderChoice(models.TextChoices):
    KAKAKO = "kakao", "Kakao"

class CustomUser(AbstractUser):
    social_provider = models.CharField(
        choices=SocialProviderChoice.choices, max_length=8, null=True,)
    