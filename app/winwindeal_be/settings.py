from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv
import os

load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'skphw(ps)4g2$6u(=xbwd60e9+7klc8_tc5!58*u-)707w0-v&')

# SECURITY WARNING: don't run with debug turned on in production!
DEV = True if os.getenv('DEV', False) else False
DEBUG = DEV

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "winwindeal.shop",
    "api.winwindeal.shop",
    "3.38.230.69"
]

# Application definition
INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'apply',
    'car',
    'user',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'winwindeal_be.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'winwindeal_be.wsgi.application'

# DB연결 정보
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "3306"),
        "NAME": os.getenv("DB_NAME", "winwindeal"),
        "USER": os.getenv("DB_USER", "root"),
        "PASSWORD": os.getenv("DB_PASSWORD", "ozcoding"),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}
# Auth user model
AUTH_USER_MODEL = "user.CustomUser"

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    # "http://winwindeal.shop",
    "https://winwindeal.shop",
    # "http://api.winwindeal.shop",
    "https://api.winwindeal.shop",
    # "http://www.winwindeal.shop",
    "https://www.winwindeal.shop"
]
CORS_ORIGIN_WHITELIST = CORS_ALLOWED_ORIGINS
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
]
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "cache-control",
    "pragma"
]
CORS_EXPOSE_HEADERS = [
    'Content-Type',
    'X-CSRFToken',
]

# CSRF
CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS
CSRF_COOKIE_SAMESITE = os.getenv('CSRF_COOKIE_SAMESITE')
CSRF_COOKIE_SECURE = bool(os.getenv('CSRF_COOKIE_SECURE'))
CSRF_COOKIE_HTTPONLY = bool(os.getenv('CSRF_COOKIE_HTTPONLY'))

# secure
SECURE_BROWSER_XSS_FILTER = bool(os.getenv('SECURE_BROWSER_XSS_FILTER'))
SECURE_CONTENT_TYPE_NOSNIFF = bool(os.getenv('SECURE_CONTENT_TYPE_NOSNIFF'))
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = bool(os.getenv('SESSION_COOKIE_SECURE'))
SESSION_COOKIE_SAMESITE = os.getenv('SESSION_COOKIE_SAMESITE')

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# Kakao OAuth settings
KAKAO_REST_API = os.getenv('KAKAO_REST_API')
KAKAO_CALLBACK_URL = os.getenv('KAKAO_CALLBACK_URL',"http://127.0.0.1:8000/user/accounts/kakao/callback/")
FRONTEND_URL = os.getenv('FRONTEND_URL',"http://localhost:3000")

# Login URLs
LOGIN_URL = os.getenv('LOGIN_URL', '')
LOGIN_REDIRECT_URL = os.getenv('LOGIN_REDIRECT_URL','')
LOGOUT_REDIRECT_URL = os.getenv('LOGOUT_REDIRECT_URL','')