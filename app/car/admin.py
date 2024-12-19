# car/admin.py

from django.contrib import admin
from .models import Car, Price

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    # 목록에서 보여질 필드들
    list_display = ['number', 'name', 'car_type', 'year', 'created_at']
    
    # 검색 가능한 필드들
    search_fields = ['number', 'name']
    
    # 필터 옵션
    list_filter = ['year', 'created_at']
    
    # 각 필드별 정렬 가능
    ordering = ['-created_at']
    
    # 읽기 전용 필드
    readonly_fields = ['created_at']

@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    # 목록에서 보여질 필드들
    list_display = ['car', 'year', 'sell_count', 'sell_average', 'buy_count', 'buy_average', 'created_at']
    
    # 검색 가능한 필드들
    search_fields = ['car__number', 'car__name']  # 차량 번호나 이름으로 검색 가능
    
    # 필터 옵션
    list_filter = ['year', 'created_at']
    
    # 각 필드별 정렬 가능
    ordering = ['-created_at']