# models.py
from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone

class ConsultationRequest(models.Model):
   # 전화번호 검증을 위한 정규표현식
   phone_regex = RegexValidator(
       regex=r'^\d{3}-\d{3,4}-\d{4}$',
       message="전화번호는 '000-0000-0000' 형식으로 입력해주세요."
   )
   
   # 전화번호 필드
   phone_number = models.CharField(
       validators=[phone_regex],
       max_length=13,
       verbose_name='연락처'
   )

   # 방문 희망 날짜 필드
   preferred_date = models.DateField(
       verbose_name='방문 희망 날짜',
       help_text='방문을 원하시는 날짜를 선택해주세요',
       default=timezone.now
   )
   
   # 선호 방문 시간대
   TIME_CHOICES = [
       ('morning', '오전 (09:00-12:00)'),
       ('afternoon', '오후 (12:00-17:00)'),
       ('evening', '저녁 (17:00-19:00)')
   ]
   
   preferred_time = models.CharField(
       max_length=20,
       choices=TIME_CHOICES,
       verbose_name='선호 방문 시간대',
       help_text='원하시는 방문 시간대를 선택해주세요'
   )

   # 방문 가능 지역
   available_location = models.CharField(
       max_length=200,
       verbose_name='방문 가능 지역'
   )

   # 신청 일시 (자동 기록)
   created_at = models.DateTimeField(
       auto_now_add=True,
       verbose_name='신청일시'
   )

   class Meta:
       verbose_name = '상담 신청'
       verbose_name_plural = '상담 신청 목록'

   def __str__(self):
       return f"{self.phone_number} - {self.preferred_date} {self.preferred_time}"

# # admin.py
# from django.contrib import admin
# from .models import ConsultationRequest

# @admin.register(ConsultationRequest)
# class ConsultationRequestAdmin(admin.ModelAdmin):
#    # 목록에 표시할 필드
#    list_display = (
#        'phone_number', 
#        'preferred_date', 
#        'preferred_time', 
#        'available_location', 
#        'created_at'
#    )
   
#    # 필터 옵션
#    list_filter = (
#        'preferred_date', 
#        'preferred_time', 
#        'created_at'
#    )
   
#    # 검색 필드
#    search_fields = (
#        'phone_number', 
#        'available_location'
#    )
   
#    # 날짜 계층구조 네비게이션
#    date_hierarchy = 'preferred_date'