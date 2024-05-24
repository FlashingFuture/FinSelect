<template>
  <div class="app-div">
    <div v-if="needNavbar" class="sticky-top">
      <nav class="navbar navbar-expand bg-body flex-row justify-content-between w-100">
        <RouterLink :to="{ name: 'home' }" class="navbar-brand px-2" href="#">
          <img src="@/assets/images/finSelectLogo.png" alt="Logo" width="128" height="32" class="d-inline-block align-text-top">
        </RouterLink>
        <div v-if="store.currentUserData" class="navbar-nav flex-row">
          <RouterLink :to="{ name: 'profile', params: { username: store.currentUserData.username } }" class="nav-link px-4 mx-2">{{ store.currentUserData.username }}</RouterLink>
          <a class="nav-link px-4 mx-2" @click="store.logout">로그아웃</a>
        </div>
        <div v-else class="navbar-nav flex-row">
          <RouterLink :to="{ name: 'signin' }" class="nav-link px-4 mx-2" href="#">회원가입</RouterLink>
          <RouterLink :to="{ name: 'login' }" class="nav-link px-4 mx-2" href="#">로그인</RouterLink>
        </div>
      </nav>

      <nav class="navbar navbar-expand-sm bg-body">
      <div class="container-fluid p-0">

        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span>바로가기</span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav w-100">
            <li class="nav-item">
              <RouterLink :class="{'on-route': isDeposit}" :to="{ name: 'depositQuiz' }" class="nav-link px-3" href="#">정기예금</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink :class="{'on-route': isSavings}" :to="{ name: 'savingsQuiz' }" class="nav-link px-3" href="#">정기적금</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink :class="{'on-route': isExchange}" :to="{ name: 'exchange' }" class="nav-link px-3" href="#">환율계산기</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink :class="{'on-route': isFindBank}" :to="{ name: 'findBank' }" class="nav-link px-3" href="#">가까운 은행</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink :class="{'on-route': isArticle}" :to="{ name: 'articles' }" class="nav-link px-3" href="#">게시판</RouterLink>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </div>


  <div v-if="needNavbar" class="chatbot-explain" @click="toggleChat">
    <p>GPT에게 상품 추천받기</p>
  </div>
  <div v-if="needNavbar" class="chatbot-icon" @click="toggleChat">
    💬
  </div>
  <div v-if="isChatOpen && needNavbar" class="chatbot-window">
    <div class="chatbot-header">
      <span>FinSelect GPT</span>
      <button @click="toggleChat">✖</button>
    </div>
    <div class="chatbot-body">
      <div class="d-flex flex-column justify-content-between h-100">
        <div>
          <div v-for="chat in chatLog">
            <div v-if="chat.chatBy == 'gpt'" class="gpt-chat mb-3">
              <div>
                <p>GPT</p>
              </div>
              <pre>{{ chat.content }}</pre>
            </div>
            <div v-else class="user-chat mb-3">
              <pre>{{ chat.content }}</pre>
              <div>
                <p>나</p>
              </div>
            </div>
          </div>
        </div>
        <div>
          <hr>
          <div>
            <input @keyup.enter="userChatPush" v-model="userChat" class="chatbot-input" type="text">
            <button @click="userChatPush" class="btn bg-info-subtle chatbot-input-btn">검색</button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <RouterView class="" />
  <div v-if="needNavbar" class="gap-for-footer">
  </div>
  <footer v-if="needNavbar" class="footer-div">
    <div class="p-3">
      <p>2024 SSAFY 11기 서울 3반 관통프로젝트 8팀</p>
    </div>
  </footer>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { RouterLink, RouterView, useRoute } from 'vue-router'
import { useStore } from '@/stores/main.js'

const route = useRoute()
const store = useStore()

const needNavbar = computed(() => {
  return !(route.name === 'login' || route.name === 'signin')
})

const chatLog = ref([
  {chatBy: 'gpt', content: '안녕하세요, finSelect GPT 챗봇입니다. 원하는 내용을 입력해 주시면 상품을 추천해 드려요.'},
])

console.log(chatLog.value)

const isChatOpen = ref(false)
const toggleChat = () => {
  isChatOpen.value = !isChatOpen.value
}

const userChat = ref(null)
const userChatPush = () => {
  const newChat = {
    chatBy: 'user',
    content: userChat.value
  }
  chatLog.value.push(newChat)
  store.giveGptChat(userChat.value)
  userChat.value = null
}

const currentGptResponse = computed(() => store.currentGptResponse)

watch(currentGptResponse, (newValue, oldValue) => {
  const gptNewChat = {
    chatBy: 'gpt',
    content: newValue,
  }
  chatLog.value.push(gptNewChat)
})

const isDeposit = ref(false)
const isSavings = ref(false)
const isExchange = ref(false)
const isFindBank = ref(false)
const isArticle = ref(false)

watch(route, () => {
  if (route.name == 'depositQuiz' || route.name == 'deposit' || route.name == 'itemDetail') {
    isDeposit.value = true
  } else { isDeposit.value = false }

  if (route.name == 'savingsQuiz' || route.name == 'savings' || route.name == 'savingDetail') {
    isSavings.value = true
  } else { isSavings.value = false }

  if (route.name == 'exchange') {
    isExchange.value = true
  } else { isExchange.value = false }

  if (route.name == 'findBank') {
    isFindBank.value = true
  } else { isFindBank.value = false }

  if (route.name == 'articles' || route.name == 'articleCreate' || route.name == 'articleDetail' || route.name == 'articleUpdate') {
    isArticle.value = true
  } else { isArticle.value = false }
})

onMounted(() => {
  chatLog.value = [
  {chatBy: 'gpt', content: '안녕하세요, finSelect GPT 챗봇입니다.\n원하는 내용을 입력해 주시면 상품을 추천해 드려요.'},
]
})
</script>

<style scoped>

.navbar-custom {
  background-color: white;
}

.app-div {
  position: relative;
  min-height: 1200px;
  min-width: 576px;
}

.nav-link {
  font-size: 18px;
}

.on-route {
  background-color: #e4e4e4;
  font-weight: bolder;
}

.gap-for-footer {
  height: 80px;
}

.footer-div {
  position: absolute;
  display: flex;
  height: 80px;
  width: 100%;
  bottom: 0px;
  justify-content: center;
  align-items: center;
  background-color: rgb(88, 88, 88);
}

.footer-div div p {
  color: rgb(115, 221, 248);
}

@media (max-width: 576px) {
  .navbar-nav {
    flex-direction: column;
  }

  .navbar-nav .nav-item {
    margin-bottom: 10px;
  }
}

@media (min-width: 576px) {
  .navbar-nav {
    display: flex;
    justify-content: start;
  }
}

/* @font-face {
  font-family: 'NotoSansKR';
  src: url('@/assets/fonts/NotoSansKR-Regular.ttf');
  font-weight: 400;
} */

/* 챗봇 */

.gpt-chat {
  display: flex;
  border-right: 1px solid #66DAFF;
  border-bottom: 1px solid #66DAFF;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  width: 90%;
}

.gpt-chat div {
  width: 10%;
  margin: 0;
  margin-right: 15px;
}

.user-chat {
  display: flex;
  border-left: 1px solid grey;
  border-top: 1px solid grey;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  width: 90%;
  margin-left: 10%;
  margin-bottom: 15px;
}
.user-chat div {
  width: 10%;
  margin: 0;
  margin-left: 15px;
}
.user-chat p {
  width: 80%;
  margin: 0;
  font-size: 14px;
}
.chatbot-icon {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 50px;
  height: 50px;
  background-color: #66DAFF;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 24px;
  cursor: pointer;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  z-index: 1020;
}

.chatbot-explain {
  position: fixed;
  bottom: 20px;
  right: 30px;
  width: 225px;
  height: 50px;
  background-color: #c7f1ff;
  border-radius: 15px;
  display: flex;
  align-items: center;
  justify-content: start;
  color: white;
  font-size: 24px;
  cursor: pointer;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  z-index: 1020;
}

.chatbot-explain p {
  color: rgb(0, 0, 0);
  font-size: 16px;
  text-align: start;
  align-content: center;
  font-weight: bolder;
  padding: 10px;
  margin: 0;
}

.chatbot-window {
  position: fixed;
  bottom: 80px;
  right: 20px;
  width: 540px;
  height: 600px;
  background-color: white;
  border: 1px solid #ddd;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  z-index: 1020;
}
.chatbot-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  background-color: #66DAFF;
  color: white;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
}
.chatbot-body {
  flex: 1;
  padding: 10px;
  overflow-y: auto;
}
.chatbot-header button {
  background: none;
  border: none;
  color: white;
  font-size: 20px;
  cursor: pointer;
}

.chatbot-input {
  height: 36px;
  margin: 0;
  width: 70%;
  border: 0.6px solid rgb(197, 197, 197);
}

.chatbot-input-btn {
  height: 35px;
  margin: 0;
  margin-bottom: 5px;
  width: 30%;
  
}
</style>
