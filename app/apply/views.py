# from django.shortcuts import render

# # Create your views here.

from django.http import JsonResponse

# 회원 목록을 보여주는 기능
def reservation(request):
    if request.method == 'POST':
        return JsonResponse({'message': 'POST 에약 정보가 표시될 거예요'})
    return JsonResponse({'message': '여기에 에약 정보가 표시될 거예요'})