from django.urls import path

from user import views

urlpatterns = [
    # path("accounts/", include("django.contrib.auth.urls")),
    # path("accounts/sign-up/", sign_up_view, name="sign-up"),
    path('accounts/kakao/login/', views.kakao_log_in_view, name='kakao-log-in'),
    path('accounts/kakao/callback/', views.kakao_callback_view, name='kakao-callcack'),
    # path("home/", home_view, name="home"),
]