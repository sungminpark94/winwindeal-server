# views.py

import uuid
import json
import requests
import base64
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import login
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.middleware.csrf import get_token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from user.models import CustomUser, SocialProviderChoice
from user.autentication import CookieJWTAuthentication

# 토큰 설정
TOKEN_SETTINGS = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=14),
    "COOKIE_SECURE": True,  # HTTPS에서만 쿠키 전송
    "COOKIE_HTTPONLY": True,  # JavaScript에서 쿠키 접근 불가
    "COOKIE_SAMESITE": "None",
}


def set_token_cookies(response, tokens):
    """토큰을 안전한 쿠키로 설정"""
    response.set_cookie(
        "access_token",
        tokens["access"],
        max_age=TOKEN_SETTINGS["ACCESS_TOKEN_LIFETIME"].total_seconds(),
        httponly=TOKEN_SETTINGS["COOKIE_HTTPONLY"],
        secure=TOKEN_SETTINGS["COOKIE_SECURE"],
        samesite=TOKEN_SETTINGS["COOKIE_SAMESITE"],
    )
    response.set_cookie(
        "refresh_token",
        tokens["refresh"],
        max_age=TOKEN_SETTINGS["REFRESH_TOKEN_LIFETIME"].total_seconds(),
        httponly=TOKEN_SETTINGS["COOKIE_HTTPONLY"],
        secure=TOKEN_SETTINGS["COOKIE_SECURE"],
        samesite=TOKEN_SETTINGS["COOKIE_SAMESITE"],
    )

def delete_token_cookies(response):
    """토큰을 안전한 쿠키로 설정"""
    response.set_cookie(
        "access_token",
        '',
        max_age=-1,
        httponly=TOKEN_SETTINGS["COOKIE_HTTPONLY"],
        secure=TOKEN_SETTINGS["COOKIE_SECURE"],
        samesite=TOKEN_SETTINGS["COOKIE_SAMESITE"],
    )
    response.set_cookie(
        "refresh_token",
        '',
        max_age=-1,
        httponly=TOKEN_SETTINGS["COOKIE_HTTPONLY"],
        secure=TOKEN_SETTINGS["COOKIE_SECURE"],
        samesite=TOKEN_SETTINGS["COOKIE_SAMESITE"],
    )

@api_view(["GET"])
@permission_classes([AllowAny])
def kakao_login_view(request):
    """카카오 로그인 초기화 뷰"""
    csrf_token = get_token(request)
    response = redirect(
        f"https://kauth.kakao.com/oauth/authorize"
        f"?client_id={settings.KAKAO_REST_API}"
        f"&redirect_uri={settings.KAKAO_CALLBACK_URL}"
        f"&response_type=code"
    )
    response.set_cookie("csrf_token", csrf_token, httponly=True, secure=True)
    return response


@api_view(["GET"])
@permission_classes([AllowAny])
def kakao_callback_view(request):
    """카카오 콜백 처리 뷰"""
    try:
        auth_code = request.GET.get("code")
        if not auth_code:
            return JsonResponse({"error": "Authorization code is required"}, status=400)

        # 카카오 토큰 요청
        token_response = requests.post(
            "https://kauth.kakao.com/oauth/token",
            data={
                "grant_type": "authorization_code",
                "client_id": settings.KAKAO_REST_API,
                "redirect_uri": settings.KAKAO_CALLBACK_URL,
                "code": auth_code,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"},
        )

        if not token_response.ok:
            print("Kakao token error:", token_response.text)  # 디버깅 로그 추가
            return JsonResponse({"error": "Failed to obtain Kakao token"}, status=400)

        access_token = token_response.json().get("access_token")

        # 카카오 프로필 정보 요청
        profile_response = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        if not profile_response.ok:
            print("Kakao profile error:", profile_response.text)  # 디버깅 로그 추가
            return JsonResponse({"error": "Failed to get Kakao profile"}, status=400)

        profile_data = profile_response.json()
        print("Kakao profile data:", profile_data)  # 디버깅 로그 추가

        # 사용자 생성 또는 조회
        username = f"k#{profile_data['id']}"
        email = profile_data["kakao_account"].get("email", "")
        nickname = profile_data.get("properties", {}).get("nickname", "")

        user, created = CustomUser.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "password": str(uuid.uuid4()),
                "social_provider": SocialProviderChoice.KAKAO,
                "first_name": nickname,
            },
        )

        # JWT 토큰 생성
        refresh = RefreshToken.for_user(user)
        tokens = {"access": str(refresh.access_token), "refresh": str(refresh)}

        # 프론트엔드로 리다이렉트
        response = redirect(settings.FRONTEND_URL)
        set_token_cookies(response, tokens)

        return response

    except Exception as e:
        print(f"Kakao callback error: {str(e)}")  # 디버깅 로그 추가
        return JsonResponse({"error": str(e)}, status=500)


@api_view(["GET"])
@authentication_classes([CookieJWTAuthentication])
@permission_classes([IsAuthenticated])
def islogin_view(request):
    print(request.COOKIES.get("access_token"))
    print("@@@@@@@@@@@@@@@@@@@@", request.user)
    if request.user:
        return JsonResponse({"success": True})


@api_view(["POST"])
@authentication_classes([CookieJWTAuthentication])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """로그아웃 처리 뷰"""
    try:
        # 리프레시 토큰 무효화
        refresh_token = request.COOKIES.get("refresh_token")
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()

        response = Response({"message": "Successfully logged out"})
        # response.delete_cookie("access_token")
        # response.delete_cookie("refresh_token")
        # response.delete_cookie("csrf_token")  # CSRF 토큰도 삭제
        delete_token_cookies(response)
        return response
    except Exception as e:
        print(f"Logout error: {str(e)}")  # 디버깅 로그 추가
        return JsonResponse({"error": str(e)}, status=400)


@api_view(["GET"])
@permission_classes([AllowAny])
def token_refresh_view(request):
    """토큰 갱신 뷰"""
    try:
        print("hihihi", request.get_full_path)
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return JsonResponse({"error": "Refresh token not found"}, status=400)
        refresh = RefreshToken(refresh_token)
        tokens = {"access": str(refresh.access_token), "refresh": str(refresh)}
        response = JsonResponse({"message": "Token refreshed successfully"})
        set_token_cookies(response, tokens)
        return response
    except Exception as e:
        print(f"Token refresh error: {str(e)}")  # 디버깅 로그 추가
        return JsonResponse({"error": str(e)}, status=400)


@api_view(["GET"])
@authentication_classes([CookieJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    """사용자 프로필 정보 조회"""
    try:
        user = request.user
        profile_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "name": user.first_name,
            "social_provider": user.social_provider,
        }
        return JsonResponse(profile_data)
    except Exception as e:
        print(f"Profile fetch error: {str(e)}")  # 디버깅 로그 추가
        return JsonResponse({"error": str(e)}, status=400)
