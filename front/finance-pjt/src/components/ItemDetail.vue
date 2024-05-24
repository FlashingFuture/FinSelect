<template>
  <div class="mx-5">
    <div class="p-3">
      <h1>{{ deposit.name }}</h1>
      <button @click="likeItem" v-if="isLiked" class="btn bg-danger-subtle m-2">찜하기 취소</button>
      <button @click="likeItem" v-else class="btn bg-info m-2">찜하기</button>
      <button @click="goBankUrl()" class="btn bg-info m-2">가입하러가기</button>
    </div>
    <div class="p-3">
      <div class="d-flex flex-row h-100 w-100">
      <div class="me-3 atr-div p-1">
        <p>금융기관명</p>
        <p>가입제한</p>
        <p>가입방법</p>
        <p>기본금리</p>
        <p>최고금리</p>
        <p>가입기간</p>
        <p>최대금액</p>
        <p>우대조건</p>
      </div>
      <div class="w-75 p-1">
        <div>
          <p>{{ deposit.bank.name }}</p>
          <p>{{ deposit.join_deny }}</p>
          <p>{{ deposit.join_way }}</p>
          <p>{{ deposit.intr_rate }}</p>
          <p>{{ deposit.intr_rate2 }}</p>
          <p>{{ deposit.save_trm }}</p>
          <p>{{ deposit.max_limit }}</p>
          <p>{{ deposit.spcl_cnd }}</p>
        </div>
      </div>

    </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue' 
import { useRoute, useRouter } from 'vue-router'
import { useStore } from '@/stores/main';

const route = useRoute()
const router = useRouter()
const store = useStore()
const deposit = store.currentDetail


const goBankUrl = () => {
  window.open(deposit.bank.bank_url, "_blank")
}


console.log(deposit.liked_by_users.includes(deposit.id))
const isLiked = ref(deposit.liked_by_users.includes(store.currentUserData.pk))

const likeItem = () => {
  console.log('아이템디테일')
  store.likeDeposit(deposit.id)
  console.log(isLiked.value)
  isLiked.value = !isLiked.value
  console.log(isLiked.value)
}

console.log(route.params)
</script>

<style scoped>
.atr-div {
  border-right: 0.4px solid rgb(200, 200, 248);
}
</style>