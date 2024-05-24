<template>
  <div class="max-500 mx-auto">
    <div class="p-3">
      <p>({{ quiz.id }} / 3)</p>
      <div class="d-flex justify-content-around">
        <div v-if="quiz.id == 1" class="question-number"></div>
        <div v-else class="question-number-not"></div>
        <div v-if="quiz.id == 2" class="question-number"></div>
        <div v-else class="question-number-not"></div>
        <div v-if="quiz.id == 3" class="question-number"></div>
        <div v-else class="question-number-not"></div>
      </div>
    </div>
    <div class="p-3 question-div">
      <p class="">{{ quiz.question }}</p>
    </div>
    <div class="p-3">
      <div v-for="select in quiz.select" @click="getAnswer(select.answer)" class="ans-div">
        <p class="m-0">{{ select.select }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useStore } from '@/stores/main'

const store = useStore()

const props = defineProps({
  quiz: Object,
})

const getAnswer = (answer) => {
  console.log('answer!!')
  store.quizCount++
  store.quizAnswer[props.quiz.id - 1] = answer
}
</script>

<style scoped>
.question-number-not {
  background-color: grey;
  width: 40px;
  height: 40px;
  border-radius: 100%;
}

.question-number {
  background-color: grey;
  width: 80px;
  height: 40px;
  border-radius: 20px;
}

.question-div {
  margin: 60px 0;
}

.question-div p {
  font-size: 32px;
  margin: 0;
}

.ans-div {
  background-color: rgb(233, 233, 233);
  padding: 30px;
  margin: 10px;
}

.ans-div p {
  text-align: start;
  font-size: 24px;
}

.max-500 {
  max-width: 500px;
}
</style>