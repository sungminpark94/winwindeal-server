# from django.shortcuts import render, redirect
# from django.http import JsonResponse
# from car.car_selenium import search_car_by_number
# from rest_framework import status
# from rest_framework.response import Response
# from .models import Car, Price
# from rest_framework.decorators import (
#     api_view,
#     permission_classes,
#     authentication_classes,
# )
# from user.autentication import CookieJWTAuthentication
# from rest_framework.permissions import IsAuthenticated
# # 회원 목록을 보여주는 기능
# # /car/price/search?number=12가1234
# @api_view(["GET"])
# @authentication_classes([CookieJWTAuthentication])
# @permission_classes([IsAuthenticated])
# def search_car_price_view(request):
#     # if not request.user.is_authenticated:
#     #     return redirect("user:kakao-log-in")
#     if not request.user.is_authenticated:
#         return JsonResponse({'error': 'Login required'}, status=401)
#     car_number = request.GET.get('number')
#     car_data = search_car_by_number(car_number)

#     if not car_data or not car_data['exist'] :
#         #빈 데이터로 차량 정보만 저장
#         car, created = Car.objects.get_or_create(
#             number=car_number,
#             defaults={
#                  'name': '미등록 차량',
#                  'car_type': '정보없음',
#                  'year': 0,
#                  'is_manual_input': True  # 수동입력 필요 표시
#             }
#         )

#         return JsonResponse( 
#             {'message': '조회안됨',
#              'exist': False,
#              'car_id': car.id
#              }
#         )
    
#     result = {
#          'min_price': 999999999,
#          'name' : car_data['datas'][0]['name'],
#          'prices': []
#     }
# # search_result['datas']에 있는 각각의 차량 정보를 순회
#     for car_info in car_data['datas']:
#         # 1. 차량 정보 저장
#         car, created = Car.objects.update_or_create(
#             number=car_number,
#             year=car_info['year'],
#             defaults={
#                 'name' : car_info['name'],
#                 'car_type': car_info['car_type']    
#             }
#         )
        
#         # 2. 최소값 비교
#         if car_info['sell_average'] < result['min_price']:
#             result['min_price'] = car_info['sell_average']
        
#         # 3. 연식별 데이터 추가
#         year_data = {
#             'year': car_info['year'],
#             'price': car_info['sell_average'],
#             'car_id': car.id,
#             'sell_count': car_info['sell_count'],
#             'buy_count': car_info['buy_count'],
#             'buy_average': car_info['buy_average']
#         }
#         result['prices'].append(year_data)
    
#     # 최종 결과 반환
#     return JsonResponse({
#         'message': '조회성공',
#         'exist': True,
#         'data': result
#     })

#     return JsonResponse(result)

# def car_data(request):
#         return JsonResponse({'message': '고객이 입력한 차량 정보'})

# # 새로 추가되는 수동 입력을 위한 API view
# @api_view(['POST'])
# def update_manual_car_info(request):
#     car_id = request.data.get('car_id')
#     try:
#         car = Car.objects.get(id=car_id)
        
#         # 차량 정보 업데이트
#         car.name = request.data.get('name', car.name)
#         car.car_type = request.data.get('car_type', car.car_type)
#         car.year = request.data.get('year', car.year)
#         car.is_manual_input = True
#         car.save()

#         # 가격 정보 생성/업데이트
#         Price.objects.create(
#             car=car,
#             year=car.year,
#             manual_price=request.data.get('price', 0),
#             sell_count=0,
#             buy_count=0
#         )

#         return Response({
#             'success': True,
#             'message': '차량 정보가 성공적으로 업데이트되었습니다.'
#         })

#     except Car.DoesNotExist:
#         return Response({
#             'success': False,
#             'message': '차량을 찾을 수 없습니다.'
#         }, status=status.HTTP_404_NOT_FOUND)

# # # 새로 추가되는 코드
# @api_view(['POST'])
# @authentication_classes([CookieJWTAuthentication])
# @permission_classes([IsAuthenticated])
# def save_car_info(request):
#     try:
#         # 프론트엔드에서 보내는 데이터 받기
#         vehicle_number = request.data.get('vehicleNumber')
#         year = request.data.get('year')
#         name = request.data.get('name')

#         # Car 모델 생성 또는 업데이트
#         car, created = Car.objects.update_or_create(
#             number=vehicle_number,
#             defaults={
#                 'name': name,
#                 'year': year,
#                 'car_type': '확인불가',
#                 'is_manual_input': True
#             }
#         )

#         # Price 모델 생성
#         Price.objects.create(
#             car=car,
#             year=year,
#             sell_average=0,
#             buy_average=0,
#             sell_count=0,
#             buy_count=0,
#             manual_price=None
#         )

#         return Response({
#             'success': True,
#             'message': '차량 정보가 성공적으로 저장되었습니다.'
#         })

#     except Exception as e:
#         return Response({
#             'success': False,
#             'message': '차량 정보 저장에 실패했습니다.'
#         }, status=status.HTTP_400_BAD_REQUEST)

from django.shortcuts import render, redirect
from django.http import JsonResponse
from car.car_selenium import search_car_by_number
from rest_framework import status
from rest_framework.response import Response
from .models import Car, Price
from rest_framework.decorators import (
   api_view,
   permission_classes,
   authentication_classes,
)
from user.autentication import CookieJWTAuthentication
from rest_framework.permissions import IsAuthenticated
# 회원 목록을 보여주는 기능
# /car/price/search?number=12가1234
@api_view(["GET"])
@authentication_classes([CookieJWTAuthentication])
@permission_classes([IsAuthenticated])
def search_car_price_view(request):
   # if not request.user.is_authenticated:
   #     return redirect("user:kakao-log-in")
   if not request.user.is_authenticated:
       return JsonResponse({'error': 'Login required'}, status=401)
   car_number = request.GET.get('number')
   car_data = search_car_by_number(car_number)

   if not car_data or not car_data['exist'] :
       #빈 데이터로 차량 정보만 저장
       car, created = Car.objects.get_or_create(
           number=car_number,
           defaults={
                'name': '미등록 차량',
                'car_type': '정보없음',
                'year': 0,
                'is_manual_input': True  # 수동입력 필요 표시
           }
       )

       return JsonResponse( 
           {'message': '조회안됨',
            'exist': False,
            'car_id': car.id
            }
       )
   
   result = {
        'min_price': 999999999,
        'name' : car_data['datas'][0]['name'],
        'prices': []
   }
# search_result['datas']에 있는 각각의 차량 정보를 순회
   for car_info in car_data['datas']:
       # 1. 차량 정보 저장
       car, created = Car.objects.update_or_create(
           number=car_number,
           year=car_info['year'],
           defaults={
               'name' : car_info['name'],
               'car_type': car_info['car_type']    
           }
       )
       
       # 2. 최소값 비교
       if car_info['sell_average'] < result['min_price']:
           result['min_price'] = car_info['sell_average']
       
       # 3. 연식별 데이터 추가
       year_data = {
           'year': car_info['year'],
           'price': car_info['sell_average'],
           'car_id': car.id,
           'sell_count': car_info['sell_count'],
           'buy_count': car_info['buy_count'],
           'buy_average': car_info['buy_average']
       }
       result['prices'].append(year_data)
   
   # 최종 결과 반환
   return JsonResponse({
       'message': '조회성공',
       'exist': True,
       'data': result
   })

   return JsonResponse(result)

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

# # 새로 추가되는 코드
@api_view(['POST'])
@authentication_classes([CookieJWTAuthentication])
@permission_classes([IsAuthenticated])
def save_car_info(request):
    try:
        print("받은 데이터:", request.data)

        # 필수 필드 검사
        required_fields = ['vehicleNumber', 'year', 'name']
        for field in required_fields:
            if not request.data.get(field):
                return Response({
                    'success': False,
                    'message': f'{field} 필드는 필수입니다.'
                }, status=status.HTTP_400_BAD_REQUEST)

        # 데이터 가져오기
        vehicle_number = request.data.get('vehicleNumber')
        year = request.data.get('year')
        name = request.data.get('name')
        
        # year가 숫자인지 확인
        try:
            year = int(year)
        except (TypeError, ValueError):
            return Response({
                'success': False,
                'message': '연식은 숫자여야 합니다.'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Car 모델 생성 또는 업데이트
        car, created = Car.objects.update_or_create(
            number=vehicle_number,
            defaults={
                'name': name,
                'year': year,
                'car_type': '확인불가',
                'is_manual_input': True
            }
        )

        # Price 모델 생성
        Price.objects.create(
            car=car,
            year=year,
            sell_average=0,
            buy_average=0,
            sell_count=0,
            buy_count=0,
            manual_price=None
        )

        return Response({
            'success': True,
            'message': '차량 정보가 성공적으로 저장되었습니다.'
        })

    except Exception as e:
        print(f"차량 정보 저장 중 오류 발생: {str(e)}")  # 에러 로깅 추가
        return Response({
            'success': False,
            'message': '차량 정보 저장에 실패했습니다.'
        }, status=status.HTTP_400_BAD_REQUEST)