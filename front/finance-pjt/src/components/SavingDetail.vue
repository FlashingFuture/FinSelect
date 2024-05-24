<template>
  <div class="mx-5">
    <div class="p-3">
      <h1>{{ saving.name }}</h1>
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
          <p>{{ saving.bank.name }}</p>
          <p>{{ saving.join_deny }}</p>
          <p>{{ saving.join_way }}</p>
          <p>{{ saving.intr_rate }}</p>
          <p>{{ saving.intr_rate2 }}</p>
          <p>{{ saving.save_trm }}</p>
          <p>{{ saving.max_limit }}</p>
          <p>{{ saving.spcl_cnd }}</p>
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
const saving = store.currentDetail


const goBankUrl = () => {
  window.open(saving.bank.bank_url, "_blank")
}


console.log(saving.liked_by_users.includes(saving.id))
const isLiked = ref(saving.liked_by_users.includes(store.currentUserData.pk))

const likeItem = () => {
  store.likeSaving(saving.id)
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