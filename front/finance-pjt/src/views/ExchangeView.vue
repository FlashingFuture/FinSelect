<template>
  <div class="mx-5">
    <div class="p-3 title-div">
      <p>환율계산기</p>
    </div>
    <div class="p-3">
      <div class="calculator-div mx-auto">
        <div class="d-flex justify-content-around align-items-end text-start">
          <div>
            <p>From</p>
            <select v-model="fromCountry" class="money-select" name="from-money" id="from-money">
              <option value="한국 원" selected>한국 원</option>
              <option v-for="country in countryList" 
              :value="country">{{ country }}</option>
            </select>
          </div>
          <img class="exchange-icon m-2" src="@/assets/images/exchange.svg"  alt="">
          <div>
            <p>To</p>
            <select v-model="toCountry" class="money-select" name="from-money" id="from-money">
              <option value="한국 원" selected>한국 원</option>
              <option v-for="country in countryList" 
              :value="country">{{ country }}</option>
            </select>

          </div>
        </div>
        <hr>
        <div class="show-div">
          <div class="">
            <p>From : {{ fromCountry }}</p>
            <input @input="getExchange" v-model="money" class="exchange-result" type="text" placeholder="여기에 입력해 주세요.">
          </div>
          <hr>
          <div class="">
            <p>To : {{ toCountry }}</p>
            <input v-model="store.exchangedMoney" class="exchange-result" type="text" placeholder="여기에 환전된 값이 나와요." readonly>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useStore } from '@/stores/main'

const store = useStore()

const fromCountry = ref(null)
const toCountry = ref(null)
const money = ref(null)

const countryList = ref(
  [
 '아랍에미리트 디르함',
  
 '호주 달러',
  
 '바레인 디나르',
  
 '브루나이 달러',
  
 '캐나다 달러',
  
 '스위스 프랑',
  
 '위안화',
  
 '덴마크 크로네',
  
 '유로',
  
 '영국 파운드',
  
 '홍콩 달러',
  
 '인도네시아 루피아',
  
 '일본 옌',
  
 '쿠웨이트 디나르',
  
 '말레이지아 링기트',
  
 '노르웨이 크로네',
  
 '뉴질랜드 달러',
  
 '사우디 리얄',
  
 '스웨덴 크로나',
  
 '싱가포르 달러',
  
 '태국 바트',
  
 '미국 달러',
]
)

const getExchange = () => {
  const payload = {
    to_country: toCountry.value,
    from_country: fromCountry.value,
    money: money.value,
  }
  store.getExchange(payload)
}
</script>

<style scoped>

.title-div {
  max-width: 600px;
}

.title-div p {
  font-size: 32px;
}
.calculator-div {
  background-color: #bfefff;
  text-align: center;
  padding: 30px;
  border-radius: 15px;
  max-width: 600px;
}

.exchange-icon {
  width: 20px;
  height: 20px;
}

.money-select {
  width: 100%;
  height: 40px;
  border-radius: 5px;
  border: 1px solid #66A0ff;
}

.show-div {
  background-color: white;
  text-align: start;
  padding: 22px;
}

.exchange-result {
  width: 100%;
  border: 0;
  font-size: 28px; 
}
</style>