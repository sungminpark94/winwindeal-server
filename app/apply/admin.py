from django.contrib import admin
from .models import ConsultationRequest

# 데코레이터나 register 중 하나만 사용
class ConsultationRequestAdmin(admin.ModelAdmin):
    list_display = (
        'phone_number', 
        'preferred_date', 
        'preferred_time', 
        'available_location', 
        'created_at'
    )
    
    list_filter = (
        'preferred_date', 
        'preferred_time', 
        'created_at'
    )
    
    search_fields = (
        'phone_number', 
        'available_location'
    )
    
    date_hierarchy = 'preferred_date'

# 한 번만 등록
admin.site.register(ConsultationRequest, ConsultationRequestAdmin)