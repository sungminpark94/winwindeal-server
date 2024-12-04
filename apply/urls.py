from django.urls import path

from . import views

urlpatterns = [
    path('reservation/result', views.reservation_result),
]

