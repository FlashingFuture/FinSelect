<template>
  <div class="text-center signin">
    <div class="p-3">
    </div>
    <div class="signin-card p-3 mx-auto">
      <div class="p-2 py-5">
        <img src="@/assets/images/finSelectLogo.png" alt="Logo" width="256" height="64" class="d-inline-block align-text-top">
      </div>
      <div>
        <p class="signin-card-msg">회원가입</p>
      </div>
      <form @submit.prevent="signin">
        <div class="text-start pt-5 signin-max-width mx-auto">
          <p class="mb-1">ID</p>
          <input class="mb-3" type="text" v-model.trim="username">
          <p class="mb-1">비밀번호</p>
          <input class="mb-3" type="password" v-model.trim="password1">
          <p class="mb-1">비밀번호 확인</p>
          <input class="mb-3" type="password" v-model.trim="password2">
          <p class="mb-1">이메일</p>
          <input class="mb-3 email-id" type="email" v-model.trim="emailName" placeholder="email_id@email_domain">
       
          <p class="mb-1">나이</p>
          <input class="mb-3 small-input" type="number" v-model="age">
          <p class="mb-1">성별</p>
          <select class="mb-3 small-input" v-model.trim="gender">
            <option value="M">남성</option>
            <option value="F">여성</option>
            <option value="O">기타</option>
          </select>
          <button @click="submit" class="signin-button">회원가입</button>
        </div>
      </form>
      <div class="text-start pt-2 signin-max-width mx-auto">
        <a class="text-decoration-none" @click="goHome" style="cursor: pointer;">홈으로 돌아가기</a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useStore } from '@/stores/main.js'
import { useRouter } from 'vue-router';

const store = useStore()
const router = useRouter()

const goHome = () => {
  router.push({ name: 'home' })
}

const username = ref(null)
const password1 = ref(null)
const password2 = ref(null)
const emailName = ref(null)
const age = ref(null)
const gender = ref(null)

const signin = () => {
  const payload = {
    username: username.value,
    password1: password1.value,
    password2: password2.value,
    email: emailName.value,
    age: age.value.toString(),
    gender: gender.value,
  }
  store.signin(payload)
}
// const 

// watch(emailDom, (newDom) => {
//   if (newDom !== 'input'){
//     emailDom.value = 
//   } 
// })
</script>

<style scoped>
.signin {
  background-color: #66DAFF;
  height: 1000px;
}

.signin-card {
  background-color: white;
  border-radius: 20px;
  margin: 10px;
  width: 80%;
  margin-left: 10%;
  min-width: 340px;
  max-width: 680px;
}

.signin-card-msg {
  font-size: 32px;
}

.signin-max-width {
  max-width: 300px;
}



select {
  border-radius: 10px;
  height: 30px;
  border: 0.6px solid rgb(77, 77, 77);
  width: 100%;
}

input {
  border-radius: 10px;
  height: 30px;
  border: 0.6px solid rgb(77, 77, 77);
  width: 100%;
}

.input-email {
  width: 50%;
}

.small-input {
  width: 100px;
}

.signin-button {
  border-radius: 10px;
  height: 30px;
  background-color: #66DAFF;
  width: 100%;
  border: 0;
}
</style>