from django.shortcuts import render
from django.conf import settings
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import User
from articles.models import Article, Comment
from bankDatas.models import SavingsAccount, FixedDeposit

@csrf_exempt
def chatgpt_response(request):
    if request.method == 'POST':
        print(request)
        user_message = request.POST.get('message')
        print(request.POST.get('message'))
        # OpenAI API 요청
        api_key = settings.GPT_KEY
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        payload = {
            'model': 'gpt-4',
            'messages': [{'role': 'user', 'content': user_message}]
        }
        response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=payload)
        response_data = response.json()

        print(response_data)
        return JsonResponse(response_data)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


import requests
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count


def get_product_data(message):
    if '적금' in message and '정기예금' not in message:
        savings_accounts = SavingsAccount.objects.order_by('-views')[:10]  # 적금 상품 중에서 조회수가 가장 많은 것 최대 10개까지 반환
        most_liked_products = SavingsAccount.objects.annotate(like_count=Count('liked_by_users')).order_by('-like_count')[:10]  # 적금 상품 중에서 좋아요가 가장 많은 것 최대 10개까지 반환
        product_type = SavingsAccount._meta.verbose_name_plural.capitalize()  # 적금 모델의 verbose_name_plural을 가져옴
        combined_products = savings_accounts | most_liked_products         # 둘을 합치고 중복제거
        combined_products = combined_products.distinct()
        fields_info = ", ".join([field.verbose_name.capitalize() for field in SavingsAccount._meta.fields])    
        return {product_type: {"fields": fields_info, "items": list(combined_products.values())}}
    
    elif '정기예금' in message and '적금' not in message:
        fixed_deposits = FixedDeposit.objects.order_by('-views')[:10]
        most_liked_products = FixedDeposit.objects.annotate(like_count=Count('liked_by_users')).order_by('-like_count')[:10]
        product_type = FixedDeposit._meta.verbose_name_plural.capitalize()  
        combined_products = fixed_deposits | most_liked_products         
        combined_products = combined_products.distinct()
        fields_info = ", ".join([field.verbose_name.capitalize() for field in FixedDeposit._meta.fields])
        return {product_type: {"fields": fields_info, "items": list(combined_products.values())}}
    
    else:
        # 메시지에 '적금' 또는 '정기예금'이 없는 경우 모든 상품을 반환합니다.
        fixed_deposits = FixedDeposit.objects.order_by('-views')[:10]  # 정기예금 상품 중에서 최대 5개까지 반환
        fixed_deposits_most_liked_products = FixedDeposit.objects.annotate(like_count=Count('liked_by_users')).order_by('-like_count')[:10]
        fixed_deposit_combined_products = fixed_deposits | fixed_deposits_most_liked_products         
        fixed_deposit_combined_products = fixed_deposit_combined_products.distinct()
        fixed_deposit_type = FixedDeposit._meta.verbose_name_plural.capitalize()  
        fixed_deposit_fields_info = ", ".join([field.verbose_name.capitalize() for field in FixedDeposit._meta.fields])
        
        savings_accounts = SavingsAccount.objects.order_by('-views')[:10] 
        savings_accounts_most_liked_products = SavingsAccount.objects.annotate(like_count=Count('liked_by_users')).order_by('-like_count')[:10]
        savings_account_combined_products = savings_accounts | savings_accounts_most_liked_products         
        savings_account_combined_products = savings_account_combined_products.distinct()    
        savings_account_type = SavingsAccount._meta.verbose_name_plural.capitalize()  
        savings_account_fields_info = ", ".join([field.verbose_name.capitalize() for field in SavingsAccount._meta.fields])

        return {
            fixed_deposit_type: {"fields": fixed_deposit_fields_info, "items": list(savings_account_combined_products.values())},
            savings_account_type: {"fields": savings_account_fields_info, "items": list(fixed_deposit_combined_products.values())}
        }

def get_chatgpt_response(user_message, user_data, product_data):
    headers = {
        'Authorization': f'Bearer {settings.GPT_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'model': 'gpt-4o',
        'messages': [
            {'role': 'user', 'content': f'{user_message}'},  
            {'role': 'system', 'content': '너는 금융상품 추천 매니저야. 고객의 메세지와 같이 보내주는 User data과 Products가 기반이야.'},
            {'role': 'system', 'content': '고객이 원하는 내용만 보내줘'},
            {'role': 'system', 'content': '작은 화면에서 고객에게 출력해 줄 거니까 40글자가 넘어가면 줄 바꿈을 해주면 좋을 것 같아'},
            {'role': 'user', 'content': f'User data: {user_data}, Products: {product_data}. Recommend suitable financial products for the user.'}
        ],
    }
    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)

    return response
from pprint import pprint
@csrf_exempt
def get_recommendations(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get('message', '')
        print(message)
        print('#############################')
        print()
        # 사용자 데이터와 상품 데이터 가져오기
        all_users_data = list(User.objects.values('username', 'gender', 'age'))

        product_data = get_product_data(message)
        pprint(product_data)
        # ChatGPT API 호출
        response = get_chatgpt_response(message, product_data, all_users_data)


        # JSON 응답 생성
        return JsonResponse(response.json())
        
    
    return JsonResponse({"error": "Invalid request"}, status=400)
