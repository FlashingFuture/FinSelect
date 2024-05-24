<template>
  <div class="mx-5 text-center">
    <QuizCard v-if="quizCount == 1" :quiz="quizes[0]" />
    <QuizCard v-if="quizCount == 2" :quiz="quizes[1]" />
    <QuizCard v-if="quizCount == 3" :quiz="quizes[2]" />
    <div class="skip-div mx-auto" @click="skip()">
      <p class="m-0">질문 건너뛰기</p>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from '@/stores/main'
import QuizCard from '@/components/QuizCard.vue'

const router = useRouter()
const store = useStore()

const quizes = ref([
  {
    id: 1,
    question: '금융기관 선택',
    select: [
      {select:'전체', answer: null},
      {select:'은행(제 1금융권)만', answer: '은행'},
    ],
    select1: '전체',
    select2: '은행(제 1금융권)만',
  },
  {
    id: 2,
    question: '금액 선택',
    select: [
      {select: '5000만 원 이상', answer: 50000000},
      {select: '1000만 원 이상', answer: 10000000},
      {select: '100만 원 이상', answer: 1000000},
      {select: '상관없음', answer: null},
    ],
    select1: '50만 원 이상',
    select2: '50만 원 미만(상관없음)',
  },
  {
    id: 3,
    question: '최대 기간 선택',
    select: [
      {select: '3개월', answer: 3},
      {select: '6개월', answer: 6},
      {select: '12개월', answer: 12},
      {select: '36개월', answer: null},
    ],
  },
])

const quizCount = computed(() => store.quizCount)

const goDepositView = () => {
  store.quizAnswer.value = [null, null, null]
  router.push({ name: 'deposit'})
}

const skip = () => {
  const payload = {
      sort_key: null,
      bank_id: null,
      bank_tag: null,
      save_trm: null,
      money_mount: null,
    }
    store.getDepositData(payload)
    store.quizAnswer.value = [null, null, null]
    goDepositView()
}

watch(quizCount, (newCount) => {
  if (newCount >= 4) {
    const payload = {
      sort_key: null,
      bank_name: null,
      bank_tag: store.quizAnswer[0],
      save_trm: store.quizAnswer[2],
      money_mount: store.quizAnswer[1],
    }
    store.getDepositData(payload)
    store.quizAnswer.value = [null, null, null]
    goDepositView()
  }
})

onMounted(() => {
  store.quizCount = 1
})
</script>

<style scoped>
.question-number {
  background-color: grey;
  width: 40px;
  height: 40px;
  border-radius: 100%;
}

.question-div {
  margin: 60px 0;
}

.question-div p {
  font-size: 32px;
  margin: 0;
}

.skip-div {
  margin-left: 30px;
  max-width: 400px;
}

.skip-div p {
  text-align: start;
  color: rgb(67, 152, 233);
  font-size: 16px;
}
</style>