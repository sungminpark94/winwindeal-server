# authentication.py
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import PermissionDenied, NotAuthenticated

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        raw_token = request.COOKIES.get('access_token', None)  # 여기서 'access'가 쿠키 이름입니다
        refresh_token = request.COOKIES.get('refresh_token', None)
        if not refresh_token:
            raise PermissionDenied({'error': "no token"})
        if not raw_token:
            raise NotAuthenticated({'error': "no token"})

        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token