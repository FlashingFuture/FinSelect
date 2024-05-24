<template>
  <div class="mx-5">
    <h1 class="text-center">{{ store.currentUserData.username }}</h1>
    <!-- <div class="d-flex justify-content-around">
      <a>개인정보 수정</a>
      <a>개인 포트폴리오</a>

    </div> -->
    <div class="p-3">
      <div class="form-div p-3">
        <form @submit.prevent="update">
          <h3>정보 수정</h3>
          <div class="d-flex flex-row">
            <div class="text-start p-3 border-end atr-div">
              <p>ID</p>
              <p>email</p>
              <p>나이</p>
              <p>성별</p>
            </div>
            <div class="text-start p-3">
              <p>{{ store.currentUserData.username }}</p>
              <input class="my-1" type="text" placeholder="email" name="email" id="email" v-model="email"><br>
              <input class="my-1" type="number" v-model="age" :placeholder="store.currentUserData.age"><br>
              <select class="my-1" v-model.trim="gender" :placeholder="store.currentUserData.gender">
                <option value="M">남성</option>
                <option value="F">여성</option>
                <option value="O">기타</option>
              </select>
            </div>
          </div>
          <button @click="submit" class="m-3 btn btn-info">수정하기</button>
        </form>
      </div>
      <div class="form-div p-3">
        <form @submit.prevent="passwordUpdate">
          <h3>비밀번호 수정</h3>
          <div class="d-flex flex-row">
            <div class="text-start p-3 border-end atr-div">
              <p>현재 비밀번호</p>
              <p>새 비밀번호</p>
              <p>새 비밀번호 확인</p>
            </div>
            <div class="text-start p-3">
              <input class="my-1" type="password" v-model="currentPassword"><br>
              <input class="my-1" type="password" v-model="newPassword1"><br>
              <input class="my-1" type="password" v-model="newPassword2">
            </div>
          </div>
          <button @click="submit" class="m-3 btn btn-info">비밀번호 수정</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import { useStore } from '@/stores/main.js'

const route = useRoute()
const store = useStore()

const email = ref(null)
const age = ref(null)
const gender = ref(null)

const currentPassword = ref(null)
const newPassword1 = ref(null)
const newPassword2 = ref(null)

const update = () => {
  const newData = {
    email: email.value,
    age: age.value.toString(),
    gender: gender.value,
  }
  const payload = {
    userId: store.currentUserData.pk,
    newData: newData,
  }
  store.update(payload)
}

const passwordUpdate = () => {
  const payload = {
    currentPassword: currentPassword.value,
    new_password1: newPassword1.value,
    new_password2: newPassword2.value,
  }
  store.passwordUpdate(payload)
}
</script>

<style scoped>
.form-div {
  border: 1px solid black;
  border-radius: 10px;
  margin-bottom: 10px;
}

.atr-div {
  width: 170px;
}
</style>