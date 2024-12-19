from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # UserAdmin의 기본 필드에 social_provider 추가
    list_display = ('username', 'email', 'social_provider', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'social_provider')
    
    # social_provider 필드를 기존 UserAdmin의 fieldsets에 추가
    fieldsets = UserAdmin.fieldsets + (
        ('Social Login Info', {'fields': ('social_provider',)}),
    )
    
    # 사용자 생성 시 보여줄 필드 설정
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Social Login Info', {'fields': ('social_provider',)}),
    )