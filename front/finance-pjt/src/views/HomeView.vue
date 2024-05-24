<template>
  <div>
    <div class="text-center mx-auto max-768">
      <div class="p-3">
        <img src="@/assets/images/finSelectLogo.png" alt="Logo" width="256" height="64" class="d-inline-block align-text-top">
      </div>
      <div style="height: 300px;">
        <div id="carouselExampleAutoplaying" class="carousel slide h-100" data-bs-ride="carousel">
          <div class="carousel-inner h-100">
            <div class="carousel-item active h-100">
              <div class="bg-danger-subtle h-100 d-flex flex-row align-items-center justify-content-between">
                <div class="align-items-start text-start">
                  <h3 class="m-3 ms-5">예적금 추천</h3>
                  <p class="m-3 ms-5">최적의 예금 / 적금을 찾아 보세요.</p>
                  <button @click="goDeposit" class="btn my-red-button ms-5 px-4">예금 찾기</button>
                  <button @click="goSavings" class="btn my-orange-button ms-1 px-4">적금 찾기</button>
                </div>
                <div> 
                  <div class="img-div m-3 me-5">
                    <img class="img" src="@/assets/images/money.png" alt="...">
                  </div>
                </div>
              </div>
            </div>
            <div class="carousel-item h-100">
              <div class="bg-success-subtle h-100 d-flex flex-row align-items-center justify-content-between">
                <div class="align-items-start text-start">
                  <h3 class="m-3 ms-5">환율 계산기</h3>
                  <p class="m-3 ms-5">빠르게 환율 계산 결과를 확인해 보세요.</p>
                  <button @click="goExchange" class="btn my-green-button ms-5 px-4">환율 계산하기</button>
                </div>
                <div>
                  <div class="img-div m-3 me-5">
                    <img class="img" src="@/assets/images/calculator.png" alt="...">
                  </div>
                </div>
              </div>
            </div>
            <div class="carousel-item h-100">
              <div class="bg-info h-100 d-flex flex-row align-items-center justify-content-between">
                <div class="align-items-start text-start">
                  <h3 class="m-3 ms-5">근처 은행 찾기</h3>
                  <p class="m-3 ms-5">주변 은행을 찾아 드려요.</p>
                  <button @click="goFindBank" class="btn my-blue-button ms-5">은행 찾기</button>
                </div>
                <div>
                  <div class="img-div m-3 me-5">
                    <img class="img" src="@/assets/images/location.png" alt="...">
                  </div>
                </div>
              </div>
            </div>
          </div>
          <button class="carousel-control-prev my-carousel-btn" type="button" data-bs-target="#carouselExampleAutoplaying" data-bs-slide="prev">
            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Previous</span>
          </button>
          <button class="carousel-control-next my-carousel-btn" type="button" data-bs-target="#carouselExampleAutoplaying" data-bs-slide="next">
            <span class="carousel-control-next-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Next</span>
          </button>
        </div>
      </div>
      <div class="text-start p-3 bg-light">
        <h3 class="mb-4">빠른 예금 / 적금 추천</h3>
        <p>고객님의 상황에 기반한 금융상품을 추천해 드려요.</p>
        <button @click="goDeposit" class="btn bg-info me-2 mb-2">지금 정기예금 추천받기</button>
        <button @click="goSavings" class="btn bg-primary-subtle me-2 mb-2">지금 정기적금 추천받기</button>
      </div>
      <div class="text-start p-3">
        <h3 class="mb-4">환율계산기와 함께하는 신혼여행</h3>
        <p>기초적인 환율계산기에요.</p>
        <button @click="goExchange" class="btn bg-success-subtle">환율계산기 바로가기</button>
      </div>
      <div class="text-start p-3 bg-light">
        <h3 class="mb-4">근처 은행 찾기</h3>
        <p>카카오 맵 api와 은행 정보를 통해 주변 은행을 찾아 드려요.</p>
        <button class="btn bg-warning" @click="goFindBank">근처 은행 바로 찾기</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()

const goDeposit = () => {
  router.push({ name: 'depositQuiz' })
}
const goSavings = () => {
  router.push({ name: 'savingsQuiz'})
}

const goExchange = () => {
  router.push({ name: 'exchange' })
}

const goFindBank = () => {
  router.push({ name: 'findBank' })
}
</script>

<style scoped>

.max-768 {
  max-width: 768px;
}
.img-div {
  height: 150px;
}

.img {
  height: 100%;
}

.my-red-button {
  background-color: rgb(148, 65, 76);
  color: white;
}

.my-orange-button {
  background-color: rgb(202, 146, 43);
  color: white;
}

.my-green-button {
  background-color: rgb(67, 146, 14);
  color: white;
}

.my-blue-button {
  background-color: rgb(42, 56, 189);
  color: white;
}

.my-carousel-btn {
  margin: 0;
  padding: 0;
  width: 5%;
}

</style>