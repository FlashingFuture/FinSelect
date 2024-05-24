import sys
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from bankDatas.utils import get_data_by_openAPI_and_save, check_old_and_delete, getTotal, find_intr 
from bankDatas.models import Bank, FixedDeposit, SavingsAccount
from apscheduler.triggers.interval import IntervalTrigger
from concurrent.futures import ThreadPoolExecutor
from playwright.sync_api import sync_playwright
from urllib.parse import urlencode
from datetime import datetime



scheduler = BackgroundScheduler()

def my_scheduled_task():
    # 도시별, 지점별 총 페이지 수를 구하고 정기예금, 적금 상품들을 크롤링하여 기존 DB와 비교하여 업데이트한다.
    get_data_by_openAPI_and_save('depositProductsSearch', FixedDeposit)
    get_data_by_openAPI_and_save('savingProductsSearch', SavingsAccount)
    
    for city in city_info:
        for district in city_info[city]:
            total_store = getTotal(city, district)
            find_intr(city, district, total_store)
    
    check_old_and_delete(FixedDeposit)
    check_old_and_delete(SavingsAccount)
    sys.stdout.write('Successfully fetched and saved data.\n')

# '0 3 * * *' means every day at 3:00 AM.
scheduler.add_job(my_scheduled_task, trigger=CronTrigger(hour=3, minute=0))

city_info = {
    '인천': ['강화군', '서구', '동구', '중구', '미추홀구', '연수구', '계양구', '부평구', '남동구', '옹진군'], 
    '서울': ['도봉구', '마포구', '관악구', '강북구', '용산구', '서초구', '노원구', '성동구', '강남구', '성북구', '광진구', '송파구', '은평구', 
           '강서구', '강동구', '종로구', '양천구', '중랑구', '영등포구', '서대문구', '구로구', '동대문구', '동작구', '중구', '금천구'], 
    '강원': ['철원군', '화천군', '양구군', '춘천시', '인제군', '고성군', '속초시', '양양군', '홍천군', '강릉시', '원주시', '횡성군', '평창군', '영월군', '정선군', '동해시', '삼척시', '태백시'], 
    '경기': ['김포시', '파주시', '연천군', '고양시', '양주시', '동두천시', '포천시', '의정부시', '남양주시', '구리시', '가평군', '하남시', '부천시', '광명시', '시흥시', '안산시', '안양시', 
           '과천시', '군포시', '의왕시', '성남시', '광주시', '양평군', '화성시', '수원시', '오산시', '용인시', '이천시', '여주시', '평택시', '안성시'], 
    '충북': ['청주시', '진천군', '음성군', '충주시', '제천시', '괴산군', '단양군', '보은군', '옥천군', '영동군', '증평군'], 
    '충남': ['태안군', '서산시', '당진시', '홍성군', '예산군', '아산시', '천안시', '보령시', '청양군', '공주시', '서천군', '부여군', '논산시', '금산군', '계룡시'], 
    '대전': ['유성구', '대덕구', '서구', '중구', '동구'], 
    '경북': ['문경시', '예천군', '영주시', '봉화군', '울진군', '상주시', '의성군', '안동시', '영양군', '김천시', '구미시', '청송군', '영덕군', '성주군', '칠곡군', 
           '영천시', '포항시', '고령군', '경산시', '경주시', '청도군', '울릉군'], 
    '대구': ['서구', '북구', '동구', '달서구', '중구', '남구', '수성구', '달성군', '군위군'], 
    '전북': ['군산시', '익산시', '부안군', '김제시', '완주군', '전주시', '고창군', '정읍시', '순창군', '임실군', '진안군', '무주군', '남원시', '장수군'], 
    '울산': ['울주군', '북구', '중구', '남구', '동구'], 
    '광주': ['광산구', '북구', '서구', '남구', '동구'], 
    '경남': ['함양군', '거창군', '산청군', '합천군', '하동군', '진주시', '의령군', '함안군', '창녕군', '남해군', '사천시', '고성군', '창원시', '밀양시', '통영시', '거제시', '김해시', '양산시'], 
    '부산': ['강서구', '북구', '금정구', '기장군', '사상구', '부산진구', '연제구', '동래구', '사하구', '서구', '중구', '동구', '남구', '수영구', '해운대구', '영도구'], 
    '전남': ['영광군', '장성군', '담양군', '함평군', '신안군', '무안군', '나주시', '화순군', '곡성군', '구례군', '목포시', 
           '영암군', '진도군', '해남군', '강진군', '장흥군', '보성군', '순천시', '완도군', '고흥군', '여수시', '광양시'], 
    '제주': ['제주시', '서귀포시'],
    '세종': ['세종시']
}

