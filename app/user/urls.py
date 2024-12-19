# user/urls.py

from django.urls import path
from .views import (
    kakao_login_view,
    kakao_callback_view,
    islogin_view,
    logout_view,
    token_refresh_view,
    get_user_profile,
)

app_name = 'user'

urlpatterns = [
    path('accounts/kakao/login/', kakao_login_view, name='kakao-login'),
    path('accounts/kakao/callback/', kakao_callback_view, name='kakao-callback'),
    path('islogin/', islogin_view, name='islogin-view'),
    path('logout/', logout_view, name='logout'),
    path('token/refresh/', token_refresh_view, name='token-refresh'),
    path('profile/', get_user_profile, name='user-profile'),
]