<template>
  <div class="mx-5">
    <div class="p-3">
      <h1>글쓰기</h1>
    </div>
    <form @submit.prevent="updateArticle">
      <div class="title-div">
        <input type="text" placeholder="제목" v-model.trim="title">
      </div>
      <div class="content-div py-1">
        <textarea type="text" placeholder="내용을 입력해 주세요." v-model.trim="content">
        </textarea>
      </div>
      <div class="article-file-div py-3">
        <label class="mx-2">첨부파일</label>
        <input type="file" @change="getArticleFile">
      </div>
      <button @click="submit" class="btn bg-info-subtle me-3">글쓰기</button>
      <button @click="goBack" class="btn bg-dark-subtle">돌아가기</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useStore } from '@/stores/main'

const route = useRoute()
const router = useRouter()
const store = useStore()

const article = store.articles.find((element) => element.id == route.params.articlePk)


const title = ref(article.title)
const content = ref(article.content)
const articleFile = ref(null)


const updateArticle = () => {
  const payload = {
    title: title.value,
    content: content.value,
    article_id: article.id
  }
  store.updateArticle(payload)
}

const goBack = () => {
  router.go(-1)
}
</script>

<style scoped>
.title-div {
  padding-top: 30px;
  border-top: 1px solid rgb(196, 228, 250);
}

.title-div input {
  width: 100%;
}

.content-div textarea {
  width: 100%;
  height: 400px;
}

.article-file-div {
  background-color: rgb(226, 226, 248);
  border-radius: 5px;
  margin-bottom: 10px;
}
</style>