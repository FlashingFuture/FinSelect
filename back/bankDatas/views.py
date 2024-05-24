from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404, get_list_or_404
from django.http import JsonResponse
from django.conf import settings
from .serializers import FixedDepositListSerializer, FixedDepositSerializer, BankSerializer, SavingsAccountListSerializer, SavingsAccountSerializer
from .models import FixedDeposit, SavingsAccount, Bank
import requests
from datetime import datetime, timedelta

# Create your views here.

@api_view(['GET'])
def bank_list(request):
    banks = get_list_or_404(Bank)
    serializer = BankSerializer(banks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def fixed_deposit_list(request):
    
    sort_key = request.query_params.get('sort_key')  # 'intr_rate'가 기본값
    bank_id = request.query_params.get('bank_id')
    bank_tag = request.query_params.get('bank_tag')
    save_trm = request.query_params.get('save_trm')
    money_mount = request.query_params.get('money_mount')
    # 정렬할 필드를 동적으로 결정
    if sort_key not in ['intr_rate2', 'intr_rate']:
        sort_key = 'intr_rate'  # 유효하지 않은 값이 들어온 경우 기본값 사용
    sort_key = '-' + sort_key
   
    fixed_deposits = FixedDeposit.objects.all()
    if bank_id:
        fixed_deposits = fixed_deposits.filter(bank__id=bank_id)

    if bank_tag:
        fixed_deposits = fixed_deposits.filter(bank__bank_tag=bank_tag)
    
    if save_trm:
        fixed_deposits = fixed_deposits.filter(save_trm__lt=save_trm)
    
    if money_mount:
        money_mount = float(money_mount)
        fixed_deposits = fixed_deposits.filter(max_limit__gte=money_mount)
    fixed_deposits = fixed_deposits.order_by(sort_key)[:30]
    serializer = FixedDepositListSerializer(fixed_deposits, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# 조회수 up    
@api_view(['POST'])
def fixed_deposit(request, fixed_pk):
    fixed_deposit = get_object_or_404(FixedDeposit, pk= fixed_pk)
    fixed_deposit.views += 1
    fixed_deposit.save()
    serializer = FixedDepositSerializer(fixed_deposit)
    return Response(serializer.data, status=status.HTTP_200_OK)


# 좋아용
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_fixed_deposit(request, fixed_pk):

    fixed_deposit = get_object_or_404(FixedDeposit, id= fixed_pk)
    
 
    if fixed_deposit.liked_by_users.filter(id=request.user.id).exists():

        fixed_deposit.liked_by_users.remove(request.user)
        message = 'Fixed_deposit unliked successfully.'
    else:
      
        fixed_deposit.liked_by_users.add(request.user)
        message = 'Fixed_deposit liked successfully.'


    serializer = FixedDepositSerializer(fixed_deposit)
    return Response({'message': message, 'data': serializer.data}, status=status.HTTP_200_OK)







@api_view(['GET'])
def saving_account_list(request):
    
    sort_key = request.query_params.get('sort_key')  # 'intr_rate'가 기본값
    bank_id = request.query_params.get('bank_id')
    bank_tag = request.query_params.get('bank_tag')
    save_trm = request.query_params.get('save_trm')
    money_mount = request.query_params.get('money_mount')
    # 정렬할 필드를 동적으로 결정
    if sort_key not in ['intr_rate2', 'intr_rate']:
        sort_key = 'intr_rate'  # 유효하지 않은 값이 들어온 경우 기본값 사용
    sort_key = '-' + sort_key
   
    saving_accounts = SavingsAccount.objects.all()
    if bank_id:
        saving_accounts = saving_accounts.filter(bank__id=bank_id)
   
    if bank_tag:
        saving_accounts = saving_accounts.filter(bank__bank_tag=bank_tag)
    
    if save_trm:
        saving_accounts = saving_accounts.filter(save_trm__lt=save_trm)
    
    if money_mount:
        money_mount = float(money_mount)
        saving_accounts = saving_accounts.filter(max_limit__gte=money_mount)
    saving_accounts = saving_accounts.order_by(sort_key)[:30]
    serializer = SavingsAccountListSerializer(saving_accounts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['POST'])
def saving_account(request, saved_pk):
    saving_account = get_object_or_404(SavingsAccount, id= saved_pk)
    saving_account.views += 1
    saving_account.save()
    serializer = SavingsAccountSerializer(saving_account)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_saving_account(request, saved_pk):
    # 해당 적금 객체 가져오기
    saving_account = get_object_or_404(SavingsAccount, id=saved_pk)
    
    # 사용자가 해당 적금을 이미 찜하고 있는지 확인
    if saving_account.liked_by_users.filter(id=request.user.id).exists():
        # 이미 찜하고 있는 경우, 찜을 해제
        saving_account.liked_by_users.remove(request.user)
        message = 'Savings account unliked successfully.'
    else:
        # 찜하지 않은 경우, 찜을 추가
        saving_account.liked_by_users.add(request.user)
        message = 'Savings account liked successfully.'

    # 변경된 적금 객체를 시리얼라이즈하여 반환
    serializer = SavingsAccountSerializer(saving_account)
    return Response({'message': message, 'data': serializer.data}, status=status.HTTP_200_OK)





## 환율 계산
def is_business_day(date):
    weekday = date.weekday()
    return weekday < 5

def get_previous_business_day(date):
    date -= timedelta(days=1)
    while not is_business_day(date):
        date -= timedelta(days=1)
    return date

@api_view(['GET'])
def exchange(request):
    to_country = request.query_params.get('to_country')
    from_country = request.query_params.get('from_country')
    money = request.query_params.get('money')
    
    if not to_country or not from_country or not money:
        return JsonResponse({'error': 'Missing query parameters'}, status=400)
    
    try:
        money = float(money)
    except ValueError:
        return JsonResponse({'error': 'Invalid money value'}, status=400)
    
    date = datetime.now()
    date_str = date.strftime('%Y%m%d')

    url = 'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON'
    api_key = settings.EXCHANGE_KEY
    data_info = 'AP01'

    res = requests.get(url, params={'data': data_info, 'searchdate': date_str, 'authkey': api_key})


    
    if res.status_code == 200:
        while res.json() == []:
            date_str = int(date_str) - 1
            print('error')
            res = requests.get(url, params={'data': data_info, 'searchdate': date_str, 'authkey': api_key})

        data = res.json()

        exchange_from = next((item for item in data if item['cur_nm'] == from_country), None)
        exchange_to = next((item for item in data if item['cur_nm'] == to_country), None)
        
        if exchange_from and exchange_to:
            if '100' in exchange_from['cur_unit'] and '100' not in exchange_to['cur_unit']:
                money *= 100
            elif '100' not in exchange_from['cur_unit'] and '100' in exchange_to['cur_unit']:
                money *= 100

            if to_country != '한국 원' and from_country != '한국 원' and to_country != from_country:
                from_rate = float(exchange_from['deal_bas_r'].replace(',', ''))
                to_rate = float(exchange_to['deal_bas_r'].replace(',', ''))
                result = (money / to_rate) * from_rate
            elif to_country == from_country:
                result = money
            elif to_country == '한국 원':
                exchange_rate = float(exchange_from['deal_bas_r'].replace(',', ''))
                result = money * exchange_rate
            elif from_country == '한국 원':
                exchange_rate = float(exchange_to['deal_bas_r'].replace(',', ''))
                result = money / exchange_rate

            return JsonResponse({'result': result}, status=200)
        else:
            return JsonResponse({'error': 'Invalid currency names'}, status=400)
    else:
        return JsonResponse({'error': 'Failed to fetch data from the API'}, status=res.status_code)
    



