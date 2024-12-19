"""
URL configuration for winwindeal_be project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView  # base에서 import


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),  # /user/ 형태로 주소가 만들어집니다
    path('car/', include('car.urls')),  # /car/ 형태로 주소가 만들어집니다
    path('apply/', include('apply.urls')),
]