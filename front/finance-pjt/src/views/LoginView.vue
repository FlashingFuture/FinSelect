<template>
  <div class="text-center login">
    <div class="p-3">
    </div>
    <div class="login-card p-3 mx-auto">
      <div class="p-2 py-5">
        <img src="@/assets/images/finSelectLogo.png" alt="Logo" width="256" height="64" class="d-inline-block align-text-top">
      </div>
      <div>
        <p class="login-card-msg">로그인</p>
      </div>
      <form @submit.prevent="login">
        <div class="text-start pt-5 login-max-width mx-auto">
          <p class="mb-1">ID</p>
          <input class="mb-3" type="text" v-model.trim="username">
          <p class="mb-1">Password</p>
          <input class="mb-3" type="password" v-model.trim="password">
          <button @click="submit" class="login-button">로그인</button>
        </div>
      </form>
      <div class="text-start pt-3 login-max-width mx-auto">
        <div>
          <a class="text-decoration-none" @click="goSignin" style="cursor: pointer;">회원가입</a>
        </div>
        <div class="mt-1">
          <a class="text-decoration-none" @click="goHome" style="cursor: pointer;">홈으로 돌아가기</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from '@/stores/main'

const router = useRouter()
const store = useStore()

const goSignin = () => {
  router.push({ name: 'signin' })
}

const goHome = () => {
  router.push({ name: 'home' })
}

const username = ref(null)
const password = ref(null)

const login = () => {
  const payload = {
    username: username.value,
    password: password.value,
  }
  store.login(payload)
}
</script>

<style scoped>
.login {
  background-color: #66DAFF;
  height: 1000px;
}

.login-card {
  background-color: white;
  border-radius: 20px;
  margin: 10px;
  width: 60%;
  margin-left: 20%;
  min-width: 340px;
  max-width: 680px;
}

.login-card-msg {
  font-size: 32px;
}

.login-max-width {
  max-width: 300px;
}

input {
  border-radius: 10px;
  height: 30px;
  border: 0.6px solid rgb(77, 77, 77);
  width: 100%;
}

.login-button {
  border-radius: 10px;
  height: 30px;
  background-color: #66DAFF;
  width: 100%;
  border: 0;
}
</style>