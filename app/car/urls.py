from django.urls import path

from . import views

urlpatterns = [
    path('price/search/', views.search_car_price_view),
    path('data/', views.car_data),
 # 새로 추가되는 URL 패턴
    path('update/', views.update_manual_car_info, name='update_manual_car_info'),
    path('info/save/', views.save_car_info, name='save_car_info'),  # 이 줄 추가
]

# from django.urls import path
# from . import views

# urlpatterns = [
#     path('price/search', views.search_car_price_view),
#     path('data', views.car_data),
#     path('update/', views.update_manual_car_info, name='update_manual_car_info'),
#     # 새로 추가되는 URL 패턴
#     path('info/save', views.save_car_info, name='save_car_info'),
# ]