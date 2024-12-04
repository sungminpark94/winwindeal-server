from django.db import models

# Create your models here.
class Car(models.Model):
    name = models.CharField(max_length=100)
    car_type = models.CharField(max_length=100)
    number = models.CharField(max_length=10)
    year = models.IntegerField(default=0)
    is_manual_input = models.BooleanField(default=False)  # 수동입력 여부
    created_at = models.DateTimeField(auto_now_add=True)  # 추가
    
    class Meta:
        # 차량번호와 연식의 조합으로 유일성 보장
        unique_together = ['number', 'year']

class Price(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='prices')
    year = models.IntegerField(null=False, blank=False)
    sell_average = models.IntegerField(null=False, blank=False, default=0)
    buy_average = models.IntegerField(null=False, blank=False, default=0)
    sell_count = models.IntegerField(default=0)
    buy_count = models.IntegerField(default=0)
    manual_price = models.IntegerField(null=True, blank=True)  # 수동입력 가격
    created_at = models.DateTimeField(auto_now_add=True)  # 추가
