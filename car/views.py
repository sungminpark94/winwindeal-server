from django.shortcuts import render
from django.http import JsonResponse
from car.car_selenium import search_car_by_number
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Car, Price

# 회원 목록을 보여주는 기능
# /car/price/search?number=12가1234
def search_car_price_view(request):
    car_number = request.GET.get('number')
    search_car_by_number(car_number)
    return JsonResponse(
        {'message': car_number}
    )

def car_data(request):
        return JsonResponse({'message': '고객이 입력한 차량 정보'})

# 새로 추가되는 수동 입력을 위한 API view
@api_view(['POST'])
def update_manual_car_info(request):
    car_id = request.data.get('car_id')
    try:
        car = Car.objects.get(id=car_id)
        
        # 차량 정보 업데이트
        car.name = request.data.get('name', car.name)
        car.car_type = request.data.get('car_type', car.car_type)
        car.year = request.data.get('year', car.year)
        car.is_manual_input = True
        car.save()

        # 가격 정보 생성/업데이트
        Price.objects.create(
            car=car,
            year=car.year,
            manual_price=request.data.get('price', 0),
            sell_count=0,
            buy_count=0
        )

        return Response({
            'success': True,
            'message': '차량 정보가 성공적으로 업데이트되었습니다.'
        })

    except Car.DoesNotExist:
        return Response({
            'success': False,
            'message': '차량을 찾을 수 없습니다.'
        }, status=status.HTTP_404_NOT_FOUND)