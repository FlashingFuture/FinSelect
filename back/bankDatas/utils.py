from .models import Bank, FixedDeposit, SavingsAccount
from django.conf import settings
from bs4 import BeautifulSoup
from pprint import pprint
import requests


####################오픈API###########################

def get_data_by_openAPI_and_save(want_category, want_DB):
    
    temp_data = {}
    bank_type = ['020000', '030300']  # 오픈 api는 은행, 저축은행 구별하여 요청이 필요함
    api_key = settings.API_KEY
    url = f'http://finlife.fss.or.kr/finlifeapi/{want_category}.json'
    want_DB.objects.all().update(isCheck=False)

    for code in bank_type:
        
        pre_res = requests.get(url=url, params= { 'auth': api_key, 'topFinGrpNo': code, 'pageNo': 1})
        
        if pre_res.status_code == 200:
            pre_data = pre_res.json()
            max_page_number = pre_data.get('result', {}).get('max_page_no', {})
            
            # 페이지 수만큼 순회
            for page in range(1, max_page_number + 1):
                
                res = requests.get(url=url, params= { 'auth': api_key, 'topFinGrpNo': code, 'pageNo': page})
                data = res.json()

                # # 기존 DB 
                # existing_deposits = want_DB.objects.all()
        
                # 금융 상품
                base_list = data.get('result', {}).get('baseList', [])
                
                # 상품 옵션 정보(ex: 12, 24개월 )
                option_list = data.get('result', {}).get('optionList', [])
                
                # 금융 상품과 옵션 정보를 합치기 위해 임시 데이터 저장
                for base in base_list:
                    pin_number = base.get('fin_prdt_cd')            # 은행이 달라도 핀 넘버가 같을때가 있어 bank_code도 같이 넣은 것을 고유 번호로
                    bank_code = base.get('fin_co_no') 
                    temp_data[pin_number + bank_code] = base
                    

                # 금융 상품과 옵션을 pin number로 
                for option in option_list:
                    pin_number = option.get('fin_prdt_cd')                                 # 핀넘버(정기예금 고유번호)
                    bank_code = option.get('fin_co_no')                                    # 금융회사 코드
                    combined_key = pin_number + bank_code
                    # temp_data에서 동일한 fin 넘버의 dict의 자료와 함께 option data를 result_data에 삽입
                    fin_prdt_nm = temp_data[combined_key]['fin_prdt_nm']                   # 정기예금 이름
                    subm_day = temp_data[combined_key]['fin_co_subm_day']                  # 업데이트 날짜
                    join_member = temp_data[combined_key]['join_member']                   # 가입 대상
                    join_deny = content_deny_dict[temp_data[combined_key]['join_deny']]    # 가입 제한
                    join_way = temp_data[combined_key]['join_way']                         # 가입 방법
                    save_trm = option.get('save_trm')                                      # 가입 기간
                    max_limit = temp_data[combined_key]['max_limit']                       # 가입 한도
                    intr_rate = option.get('intr_rate')                                    # 기본 금리
                    intr_rate2 = option.get('intr_rate2')                                  # 최대 금리
                    intr_rate_type = option.get('intr_rate_type_nm')                       # 금리 유형
                    spcl_cnd = temp_data[combined_key]['spcl_cnd']                         # 우대 조건
                    etc_note = temp_data[combined_key]['etc_note']                         # 기타 사항
                    kor_co_nm = temp_data[combined_key]['kor_co_nm']                       # 은행 이름
                    bank_id = bank_name_dict[kor_co_nm]                                    # 은행 id
                    
                    # 복리인 적금은 이름에 표시
                    if intr_rate_type == '복리':
                        fin_prdt_nm += ' (복리)'
                    
                    if intr_rate is None:
                        # 기본 금리가 없는 경우, 오류니 패스
                        continue
                    if intr_rate2 is None:
                        # 기본값 설정 또는 데이터 누락 처리 로직 추가
                        intr_rate2 = intr_rate

                    if max_limit is None:
                        max_limit = 1e10


                    # 위 걸 바로 받아서 해도 되지만 가독성이 더 나은 것 같아 아래와 같이 
                    final = want_DB(
                        name = fin_prdt_nm,
                        updated_at = subm_day,
                        join_member = join_member,
                        join_deny = join_deny,
                        join_way = join_way,
                        save_trm = save_trm,
                        max_limit = max_limit,
                        intr_rate = intr_rate,
                        intr_rate2 = intr_rate2,
                        intr_rate_type  = intr_rate_type,
                        spcl_cnd = spcl_cnd,
                        etc_note = etc_note,
                        bank_id = bank_id,
                        pin_number = pin_number,
                        bank_code = bank_code,
                        isCheck = True,
                        views = 0
                    )
                    if want_category == 'savingProductsSearch':
                        rsrv_type =  option.get('rsrv_type_nm')
                        if rsrv_type == '자유적립식':
                            final.name += ' (자유적립)'
                            fin_prdt_nm += ' (자유적립)'
                                     
                        final.rsrv_type = rsrv_type
                        
                    # 정기예금 새로 갱신된 게 있으면 
                    if want_DB.objects.filter(pin_number=pin_number, name= fin_prdt_nm, bank_code= bank_code, save_trm=save_trm).exists():
                        # 기존 예금 갖고오기
                        existing_instance = want_DB.objects.get(pin_number=pin_number, name= fin_prdt_nm, bank_code= bank_code, save_trm=save_trm)
                        # 아래 제외한 데이터 비교
                        final_data = {k: v for k, v in final.__dict__.items() if k != 'updated_at' and k != '_state' and k != 'id' and k != 'isCheck' and k != 'views'}
                        existing_data = {k: v for k, v in existing_instance.__dict__.items() if k != 'updated_at' and k != '_state' and k != 'id' and k != 'isCheck' and k != 'views'}
                        ## 숫자들의 경우 컴퓨터라 1 과 1도 다르게 봄..
                        # save_trm 필드의 형식을 맞추기
                        if 'save_trm' in final_data and 'save_trm' in existing_data:
                            final_data['save_trm'] = str(final_data['save_trm'])
                            existing_data['save_trm'] = str(existing_data['save_trm'])
                        # intr_rate와 intr_rate2도 필드의 형식을 맞추기
                        if 'intr_rate' in final_data and 'intr_rate' in existing_data:
                            final_data['intr_rate'] = format(final_data['intr_rate'], '.2f')
                            existing_data['intr_rate'] = format(existing_data['intr_rate'], '.2f')
                        if 'intr_rate2' in final_data and 'intr_rate2' in existing_data:
                            final_data['intr_rate2'] = format(final_data['intr_rate2'], '.2f')
                            existing_data['intr_rate2'] = format(existing_data['intr_rate2'], '.2f')
                        
                        # 디버깅용
                        # 데이터가 다른 경우 차이 출력
                        if final_data != existing_data:
                   
                            print("차이가 있는 데이터:")
                            print(want_category )
                            pprint(base)
                            pprint(option)

                            for key in final_data:
                                if final_data[key] != existing_data.get(key):
                                    
                                    print(f"{key}: {final_data[key]} -> {existing_data.get(key)}")
                                    # 조회수의 경우 새 데이터로 이전
                                    if key == 'views':
                                        final['views'] = existing_instance['views']            
                            # 새로운 데이터 저장
                            final.save()      
                            # 기존 데이터 삭제
                            existing_instance.delete()
                        else:    
                            existing_instance.isCheck = True
                            existing_instance.save()
                    else:
                        # 데이터가 존재하지 않는 경우에는 새로운 데이터 저장
                        final.save()            
        else:
            print(res.status_code)
    ################오픈 API로 새 데이터 생성 및 비교 완료###########################
def check_old_and_delete(want_DB):
    want_DB.objects.filter(isCheck=False).delete()



# 나중에 vue로 보낼때 바꿔도 되지만 사용자가 받을때는 최대한 빠르게 보내기 위해 DB에 저장할 때 미리 변환시켜두기 
content_deny_dict= { '1': '제한없음', '2':'서민전용', '3':'일부제한',}

# 받아온 데이터의 은행 이름에 맞게 pk 값을 정기예금과 적금에 넣기 위해 만듬
bank_name_dict ={ 
     "국민은행": 1,
     "신한은행": 2,
     "하나은행": 3,
     "우리은행": 4,
     "농협은행주식회사": 5,
     "중소기업은행": 6,
     "한국산업은행": 7,
     "신협": 8,
     "한국스탠다드차타드은행": 9,
     "우정사업본부": 10,
     "부산은행": 11,
     "대구은행": 12,
     "수협은행": 13,
     "경남은행": 14,
     "주식회사 카카오뱅크": 15,
     "광주은행": 16,
     "토스뱅크 주식회사": 17,
     "전북은행": 18,
     "주식회사 케이뱅크": 19,
     "제주은행": 20,
     "우리종합금융": 21,
     "비엔케이저축은행": 22,
     "CK저축은행": 23,
     "디비저축은행": 24,
     "디에이치저축은행": 25,
     "HB저축은행": 26,
     "아이비케이저축은행": 27,
     "제이티저축은행": 28,
     "제이티친애저축은행": 29,
     "케이비저축은행": 30,
     "엔에이치저축은행": 31,
     "오케이저축은행": 32,
     "오에스비저축은행": 33,
     "에스비아이저축은행": 34,
     "에스앤티저축은행": 35,
     "고려저축은행": 36,
     "국제저축은행": 37,
     "금화저축은행": 38,
     "남양저축은행": 39,
     "다올저축은행": 40,
     "대명상호저축은행": 41,
     "대백저축은행": 42,
     "대신저축은행": 43,
     "대아상호저축은행": 44,
     "대원상호저축은행": 45,
     "대한저축은행": 46,
     "더블저축은행": 47,
     "더케이저축은행": 48,
     "동양저축은행": 49,
     "동원제일저축은행": 50,
     "드림저축은행": 51,
     "라온저축은행": 52,
     "머스트삼일저축은행": 53,
     "모아저축은행": 54,
     "민국저축은행": 55,
     "바로저축은행": 56,
     "부림저축은행": 57,
     "삼정저축은행": 58,
     "삼호저축은행": 59,
     "상상인저축은행": 60,
     "상상인플러스저축은행": 61,
     "세람상호저축은행": 62,
     "센트럴저축은행": 63,
     "솔브레인저축은행": 64,
     "스마트저축은행": 65,
     "스카이저축은행": 66,
     "스타저축은행": 67,
     "신한저축은행": 68,
     "아산저축은행": 69,
     "안국저축은행": 70,
     "안양저축은행": 71,
     "애큐온저축은행": 72,
     "엠에스상호저축은행": 73,
     "영진저축은행": 74,
     "예가람저축은행": 75,
     "오성저축은행": 76,
     "오투저축은행": 77,
     "우리금융저축은행": 78,
     "우리저축은행": 79,
     "웰컴저축은행": 80,
     "유니온상호저축은행": 81,
     "유안타저축은행": 82,
     "융창저축은행": 83,
     "인성저축은행": 84,
     "인천저축은행": 85,
     "조은저축은행": 86,
     "조흥저축은행": 87,
     "진주저축은행": 88,
     "참저축은행": 89,
     "청주저축은행": 90,
     "키움예스저축은행": 91,
     "키움저축은행": 92,
     "페퍼저축은행": 93,
     "평택저축은행": 94,
     "푸른상호저축은행": 95,
     "하나저축은행": 96,
     "한국투자저축은행": 97,
     "한성저축은행": 98,
     "한화저축은행": 99,
     "흥국저축은행": 100,
     "회원수협": 101,
     "새마을금고": 102 }     


####################크롤링###########################


from concurrent.futures import ThreadPoolExecutor
from playwright.sync_api import sync_playwright
from urllib.parse import urlencode
from datetime import datetime

# 도시 구역별 페이지 수 확인, 10개 당 1 페이지임
def getTotal(city_name, city_district):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        params = {
            'r1': city_name,
            'r2': city_district,
            'pageNo': 1
        }
        url = f'https://www.kfcc.co.kr/map/list.do?{urlencode(params)}'
        page = browser.new_page()
        page.set_extra_http_headers(headers)        
        page.goto(url)
        page.wait_for_load_state('networkidle')
        page.set_default_timeout(5000)
        total_count = page.locator('a.btn.small.blueBtn03').count()

        return total_count

# Current datetime for updated_at
updated_at = datetime.now().strftime("%Y-%m-%d")
# 받은 정보들을 통해 지점별 상품들 확인 후 DB 비교
def process_page(city_name, city_district, j, page_no):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            params = {
                'r1': city_name,
                'r2': city_district,
                'pageNo': page_no + 1
            }
            url = f'https://www.kfcc.co.kr/map/list.do?{urlencode(params)}'
            print(city_name, city_district, j, page_no)
            page = browser.new_page()
            page.set_extra_http_headers(headers)        
            page.goto(url)
            page.wait_for_load_state('networkidle')
            page.set_default_timeout(5000)
          

            page.locator('a.btn.small.blueBtn03').nth(j).click()
            page.wait_for_selector("#sub_tab_rate")

            bank_name = page.query_selector('#div1 > div.pop-body.detail > div > div.top > div.title')
            name = bank_name.inner_text()
            element = page.query_selector('#sub_tab_rate')
            
            if element:
                iframe_element = page.frame_locator('iframe[id="rateFrame"][name="rateFrame2"]')
                iframe_element.locator('a.tabw80').nth(1).click()

                # mg정기예금
                try:
                    mg_fixed_rate = iframe_element.locator('table[summary="MG더뱅킹정기예금에 대한 상품명, 계약기간, 기본이율 등의 정보를 나타낸 표"] > tbody > tr > td:nth-child(3)').text_content()
                    mg_fixed_name = f'MG더뱅킹정기예금 ({name})'
                except:
                    mg_fixed_rate = '연0.0%'
                iframe_element.locator('a.tabw80').nth(2).click()

                # 정기적금
                try:
                    mg_saving1_rate = iframe_element.locator('table[summary="정기적금에 대한 상품명, 계약기간, 기본이율 등의 정보를 나타낸 표"] > tbody > tr:nth-child(2) > td:nth-child(2)').first.text_content()
                    mg_saving1_name = f'정기적금 ({name})'
                except:
                    mg_saving1_rate = '연0.0%'
                # mg정기적금
                try: 
                    mg_saving2_rate = iframe_element.locator('table[summary="MG더뱅킹정기적금에 대한 상품명, 계약기간, 기본이율 등의 정보를 나타낸 표"] > tbody > tr:nth-child(2) > td:nth-child(2)').first.text_content()
                    mg_saving2_name = f'MG더뱅킹정기적금 ({bank_name})'
                except:
                    mg_saving2_rate = '연0.0%'
                # 자유적립적금
                try:
                    mg_saving3_rate = iframe_element.locator('table[summary="자유적립적금에 대한 상품명, 계약기간, 기본이율 등의 정보를 나타낸 표"] > tbody > tr:nth-child(4) > td:nth-child(2)').first.text_content()
                    mg_saving3_name = f'MG월복리자유적금 ({bank_name})'
                except:
                    mg_saving3_rate = '연0.0%'
                ####### 상품들 이율 확인 완료 ######
                    
                # 상품이 없으면 이율 없음
                if mg_fixed_name:
                    if FixedDeposit.objects.filter(name = mg_fixed_name).exists():
                        existing_instance = FixedDeposit.objects.get(name = mg_fixed_name)
                        new_intr_rate = mg_fixed_rate.replace("연", "").replace("%", "")
                        if existing_instance.intr_rate != new_intr_rate:
                            existing_instance.intr_rate = new_intr_rate
                            existing_instance.intr_rate2 = new_intr_rate + 0.3
                            existing_instance.isCheck = True
                            existing_instance.save()
                    # 기존 상품이 없으면 추가
                    else:
                        new_product = FixedDeposit(
                        name = mg_fixed_name,
                        updated_at = updated_at,
                        join_member = '만 19세 이상의 실명의 개인',
                        join_deny = '''공동명의예금으로 가입 불가, 
                                양도‧양수 및 계좌분할 불가''',
                        join_way = '스마트뱅킹 “MG더뱅킹” 어플에서만 가입 가능',
                        save_trm = 12,
                        max_limit = 100000000,
                        intr_rate = new_intr_rate,
                        intr_rate2 = new_intr_rate + 0.3,
                        intr_rate_type  = '',
                        spcl_cnd = '''이 예금 가입일부터 만기일 전일까지 MG스마트알림서비스를 가입하고 1회 이상 로그인하는 경우
                                (단, MG스마트알림서비스에 기가입되어 있는 경우 이 예금 가입일부터 만기일 전일까지 1회 이상 로그인 하는 경우)
                                또는 이 예금 가입일부터 만기일 전일까지 MG더뱅킹 어플에서 더뱅킹PUSH알림서비스를 통해 1회 이상 입출금 PUSH알림을 받은 경우 : 연 0.1%
                                이 예금 가입시 만기자동이체를 등록한 경우 : 연 0.1%
                                이 예금 가입일부터 가입시 정한 만기일 전일까지 MG더뱅킹을 이용한 이체거래 실적이 6회 이상 있는 경우 : 연 0.1%''',
                        etc_note = '(해지) 창구, 인터넷(스마트)뱅킹, 만기자동이체 신청 가능',
                        bank_id = 102,
                        pin_number = 119112,
                        bank_code = 119112,
                        isCheck = True,
                        views = 0
                    )   
                        new_product.save()
                # 없어졌는데 기존 DB에 있으면       
                else:
                    if FixedDeposit.objects.filter(name = mg_fixed_name).exists():
                        existing_instance = FixedDeposit.objects.get(name = mg_fixed_name)
                        existing_instance.delete()
                
                if mg_saving1_name:
                    if SavingsAccount.objects.filter(name = mg_saving1_name).exists():
                        existing_instance = SavingsAccount.objects.get(name = mg_saving1_name)
                        new_intr_rate = mg_saving1_rate.replace("연", "").replace("%", "")
                        if existing_instance.intr_rate != new_intr_rate:
                            existing_instance.intr_rate = new_intr_rate
                            existing_instance.intr_rate2 = new_intr_rate
                            existing_instance.isCheck = True
                            existing_instance.save()
                    # 기존 상품이 없으면 추가
                    else:
                        new_product = SavingsAccount(
                        name = mg_saving1_name,
                        updated_at = updated_at,
                        join_member = '제한없음',
                        join_deny = '제한없음',
                        join_way = '지점별 상이',
                        save_trm = 12,
                        max_limit = 100000000,
                        intr_rate = new_intr_rate,
                        intr_rate2 = new_intr_rate,
                        intr_rate_type  = "단리",
                        spcl_cnd = '',
                        etc_note = '',
                        rsrv_type = '정액적립식',
                        bank_id = 102,
                        pin_number = 119113,
                        bank_code = 119112,
                        isCheck = True,
                        views = 0
                    )   
                        new_product.save()
                # 없어졌는데 기존 DB에 있으면       
                else:
                    if SavingsAccount.objects.filter(name = mg_saving1_name).exists():
                        existing_instance = SavingsAccount.objects.get(name = mg_saving1_name)
                        existing_instance.delete()
                
                
                if mg_saving2_name:
                    if SavingsAccount.objects.filter(name = mg_saving2_name).exists():
                        existing_instance = SavingsAccount.objects.get(name = mg_saving2_name)
                        new_intr_rate = mg_saving2_rate.replace("연", "").replace("%", "")
                        if existing_instance.intr_rate != new_intr_rate:
                            existing_instance.intr_rate = new_intr_rate
                            existing_instance.intr_rate2 = new_intr_rate + 0.5
                            existing_instance.isCheck = True
                            existing_instance.save()
                    # 기존 상품이 없으면 추가
                    else:
                        new_product = SavingsAccount(
                        name = mg_saving2_name,
                        updated_at = updated_at,
                        join_member = '만19세 이상의 실명의 개인 (금고별 1인 1계좌)',
                        join_deny = '제한없음',
                        join_way = '(가입) 스마트뱅킹 “MG더뱅킹” 어플에서만 가입 가능',
                        save_trm = 12,
                        max_limit = 1000000,
                        intr_rate = new_intr_rate,
                        intr_rate2 = new_intr_rate + 0.5,
                        intr_rate_type  = "단리",
                        spcl_cnd = '''최고 연 0.5% (모든 우대이율은 만기해지하는 경우에만 적용)

이 예금 가입일부터 만기일 전일까지 MG스마트알림서비스를 가입하고 1회 이상 로그인하는 경우
(단, MG스마트알림서비스에 기가입되어 있는 경우 이 예금 가입일부터 만기일 전일까지 1회 이상 로그인 하는 경우)
또는 이 예금 가입일부터 만기일 전일까지 MG더뱅킹 어플에서 더뱅킹PUSH알림서비스를 통해 1회 이상 입출금 PUSH알림을 받은 경우 : 연 0.2%
이 예금 가입시 만기자동이체를 등록한 경우 : 연 0.1%

새마을금고 요구불예금에서 이 예금 자동이체 시 : 연 0.1%

※ 계약기간 6개월은 3회 이상, 1년은 6회 이상 자동이체로 납입하는 경우

이 예금 가입일로부터 1개월내 이 예금 개설금고 거치식 상품을 추가로 가입하고 해당 상품을 만기해지하거나 이 예금 만기일 현재까지 유지한 경우 : 연 0.1%
                            ''',
                        etc_note = '(해지) 창구, 인터넷(스마트)뱅킹, 만기자동이체 신청 가능',
                        rsrv_type = '정액적립식',
                        bank_id = 102,
                        pin_number = 119114,
                        bank_code = 119112,
                        isCheck = True,
                        views = 0
                    )   
                        new_product.save()
                # 없어졌는데 기존 DB에 있으면       
                else:
                    if SavingsAccount.objects.filter(name = mg_saving2_name).exists():
                        existing_instance = SavingsAccount.objects.get(name = mg_saving2_name)
                        existing_instance.delete()
                if mg_saving3_name:
                    if SavingsAccount.objects.filter(name = mg_saving3_name).exists():
                        existing_instance = SavingsAccount.objects.get(name = mg_saving3_name)
                        new_intr_rate = mg_saving3_rate.replace("연", "").replace("%", "")
                        if existing_instance.intr_rate != new_intr_rate:
                            existing_instance.intr_rate = new_intr_rate
                            existing_instance.intr_rate2 = new_intr_rate + 0.7
                            existing_instance.isCheck = True
                            existing_instance.save()
                    # 기존 상품이 없으면 추가
                    else:
                        new_product = SavingsAccount(
                        name = mg_saving3_name,
                        updated_at = updated_at,
                        join_member = '실명에 의한 개인(1인 1계좌)',
                        join_deny = '실명에 의한 개인(1인 1계좌)',
                        join_way = '지점별 상이',
                        save_trm = 12,
                        max_limit = 30000000,
                        intr_rate = new_intr_rate,
                        intr_rate2 = new_intr_rate + 0.7,
                        intr_rate_type  = "복리",
                        spcl_cnd = '''아래의 우대이율 요건을 충족할 경우 최대 연 0.7%까지 우대이율 지급 다만, 5호의 우대이율의 한도는 0.1% 지급
① 가입일 당시 화수분 또는 화수분II예금 가입자 연 0.1%
② 가입일 기준 3개월 이내에 신규가입 회원 연 0.1%
③ 가입일전 1개월이내 거치식예금을 가입하여 유지하고 있는자 연 0.2%
④ 가입일전 1개월이내 적립식예금을 가입하여 유지하고 있는자 연 0.1%
⑤ 계약기간 내 본인을 포함한 세대구성원 2인 이상이 가입시 연 0.1%
⑥ 가입일 전월말 기준 직전 3개월간 입출금이 자유로운 예금 평잔이 30만원 이상인 경우 연 0.1%
''',
                        etc_note = '',
                        rsrv_type = '자유적립식',
                        bank_id = 102,
                        pin_number = 119115,
                        bank_code = 119112,
                        isCheck = True,
                        views = 0
                    )   
                        new_product.save()
                # 없어졌는데 기존 DB에 있으면       
                else:
                    if SavingsAccount.objects.filter(name = mg_saving3_name).exists():
                        existing_instance = SavingsAccount.objects.get(name = mg_saving3_name)
                        existing_instance.delete()
                
            button2 = page.query_selector('button.grayBtn')
            button2.click()
    except Exception as e:
        print(f'Error processing page {j}: {e}')



# 크롤링을 하는데 비동기식으로 도시 구역별 페이지 돌림
def find_intr(city_name, city_district, city_stores):
    group_size = 10
    with ThreadPoolExecutor(max_workers=30) as executor:
        futures = []
        for i in range(0, city_stores, group_size):  # Assuming 100 as the maximum total_count
            for j in range(i, i + group_size):
                index_page = j // group_size
                if index_page:
                    futures.append(executor.submit(process_page, city_name, city_district, j, index_page))
                else:
                    futures.append(executor.submit(process_page, city_name, city_district, j, 0))
                
                if j == city_stores - 1:
                    break
 

      


