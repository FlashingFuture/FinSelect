<template>
  <div class="min-480">
    <div class="d-flex justify-content-between">
      <h2 class="mb-5">검색 결과</h2>
      <p class="updated-date m-0">Updated : {{ yesterday.slice(0, 15) }}</p>
    </div>
    <table class="table">
      <thead>
        <tr>
          <th scope="col" @click="sort_base">금리(기본)</th>
          <th scope="col" class="hide-md" @click="sort_top">금리(최고)</th>
          <th scope="col" class="hide-sm">상품명</th>
          <th scope="col">금융기관명</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="deposit in store.depositData" class="item" @click="goItemDetail(deposit.id)">
          <td class="deposit-intr-rate " scope="row">{{ deposit.intr_rate }}</td>
          <td class="deposit-intr-rate hide-md">{{ deposit.intr_rate2 }}</td>
          <td><p class="deposit-name">{{ deposit.name }}</p></td>
          <td class="bank d-flex align-item-center">
            <img class="me-1 bank-logo" :src="`http://127.0.0.1:8000${ deposit.bank.bank_image }`" alt="loading">
            <p>{{ deposit.bank.name }}</p>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useStore } from '@/stores/main.js'
import { useRouter } from 'vue-router'

const props = defineProps({
  sort_base: Function,
  sort_top: Function,
})

const router = useRouter()
const store = useStore()

const goItemDetail = (itemPk) => {
  if (store.currentUserData) {
  store.getDepositDetail(itemPk)
  } else {
    window.alert('상세정보를 확인하려면 로그인해 주세요.')
    router.push({ name: 'login' })
  }
}

const today = new Date()
const yesterday = String(new Date(today.setDate(today.getDate() - 1)))
</script>

<style scoped>
.item:hover {
  background-color: rgb(0, 0, 0);
  opacity: 0.5;
}

.active-sort {
  background-color: rgb(206, 245, 245);
}

.min-480 {
  min-width: 480px;
}
.deposit-intr-rate {
  min-width: 100px;
}
.deposit-name {
  text-wrap: nowrap;
  width: 200px;
  overflow: hidden;
}

.bank {
  text-wrap: nowrap;
  width: 160px;
  overflow: hidden;
}
.bank-logo {
  height: 24px;
}

.updated-date {
  font-size: 14px;
}

@media (max-width: 768px) {
  .hide-md {
    display: none;
  }
}

@media (max-width: 576px) {
  .hide-sm {
    display: none;
  }
}
</style>