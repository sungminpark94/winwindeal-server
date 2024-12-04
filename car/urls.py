from django.urls import path

from . import views

urlpatterns = [
    path('price/search', views.search_car_price_view),
    path('data', views.car_data),
 # 새로 추가되는 URL 패턴
    path('manual-info/update/', views.update_manual_car_info, name='update_manual_car_info'),

]