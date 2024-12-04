# from django.shortcuts import render

# # Create your views here.
import requests
from django.conf import settings
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.urls import reverse

# from user.forms import UserSignUpForm

# # 회원 목록을 보여주는 기능
# def user_login(request): 
#     return JsonResponse({'message': '카카오로그인 구현 예정'})
# def user_logout(request):
#     return JsonResponse({'message': '카카오 로그아웃 구현 예정'})
# def user_mypage(request):
#     return JsonResponse({'message': '마이페이지 구현 예정'})

def kakao_log_in_view(request):
    if request.method == 'GET':
        return redirect(
            f"https://kauth.kakao.com/oauth/authorize"
            f"?client_id={settings.KAKAO_REST_API}"
            f"&redirect_uri={settings.KAKAO_CALLBACK_URL}"
            f"&response_type=code"
        )
    
def kakao_callback_view(request):
    if request.method == 'GET':
        auth_code = request.GET.get("code")

        #카카오에 access token 요청
        requests.post(
           "https://kauth.kakao.com/oauth/token",
           data = {
               "grant_type": "authorization_code",
               "client_id": settings.KAKAO_REST_API,
               "redirect_uri": settings.KAKAO_CALLBACK_URL,
               "code": auth_code,
           },
           headers={
               "Content-Type": "application/x-www-form-urlencoded:charset=UTF-8",
           },
    )