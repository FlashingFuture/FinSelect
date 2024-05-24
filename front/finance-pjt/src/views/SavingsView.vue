<template>
  <div class="h-100 mx-5">
    <div class="d-flex flex-row h-100 w-100">
      <div class="border-end p-3 search-div">
        <h2 class="mb-5">정기적금</h2>
        <form @submit.prevent="searchSavings">
          <p class="mt-1">검색 조건</p>
          <hr class="mb-1">
          <p class="mb-1">은행</p>
          <select name="bank" id="bank" class="mb-1 w-90" v-model="bank">
            <option value="all">전체</option>
            <option value="bankOnly">은행만</option>
            <option v-for="bank in store.bankData"
            :key="bank.id"
            :value="bank.id"
            >{{ bank.name }}</option>
          </select>
          <p class="mb-1">예치금 (최소)</p>
          <input type="text" class="mb-1 w-90" v-model="money">
          <p class="mb-1">예치기간 (최대)</p>
          <select name="bank" id="bank" class="mb-1 w-90" v-model="term">
            <option value="1">1개월</option>
            <option value="3">3개월</option>
            <option value="6">6개월</option>
            <option value="12">12개월</option>
            <option value="24">24개월</option>
            <option value="36">36개월</option>
          </select>
          <button @click="submit" class="btn btn-info w-90">검색</button>
        </form>
      </div>
      <div class="p-3 w-75">
        <SavingsList 
          :sort_base="sort_base"
          :sort_top="sort_top"
        />
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import SavingsList from '@/components/SavingsList.vue'
import { useRoute } from 'vue-router'
import { useStore } from '@/stores/main'

const route = useRoute()
const store = useStore()

const bank = ref(null)
const bankTag = ref(null)
const money = ref(null)
const term = ref(null)
const sort = ref('intr_rate')

const sort_base = () => {
  sort.value = 'intr_rate'
  searchSavings()
}
const sort_top = () => {
  sort.value = 'intr_rate2'
  searchSavings()
}

onMounted(() => {
  store.getBankData()
})

const searchSavings = () => {
  if (bank.value == 'bankOnly') {
    bankTag.value = '은행'
    bank.value = null
  } else if (bank.value == 'all') {
    bank.value = null
  } else {
    bankTag.value = null
  }
  const payload = {
    sort_key: sort.value,
    bank_id: bank.value,
    bank_tag: bankTag.value,
    save_trm: Number(term.value),
    money_mount: Number(money.value),
  }
  console.log(payload)
  store.getSavingsData(payload)
  if (bank.value == null) {
    bank.value = 'all'
  }
}
</script>

<style scoped>
.w-90 {
  width: 90%;
}

.search-div {
  min-width: 160px;
}

input {
  border-radius: 5px;
  height: 30px;
  border: 0.6px solid rgb(77, 77, 77);
}

select {
  border-radius: 5px;
  height: 30px;
  border: 0.6px solid rgb(77, 77, 77);
}
</style>