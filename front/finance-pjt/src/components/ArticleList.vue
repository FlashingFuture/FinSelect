<template>
  <div>
    <div>
      <button @click="goArticleCreate" class="btn bg-info-subtle">글쓰기</button>
    </div>
    <table class="table article-table">
      <thead>
        <tr>
          <th scope="col">작성자</th>
          <th scope="col">작성 시간</th>
          <th scope="col">제목</th>
          <th scope="col">조회수</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="article in store.articles" class="item" :key="article.id"
         @click="goArticleDetail(article.id)">
          <td>{{ article.user.username }}</td>
          <td>{{ article.created_at.slice(5, 10) }} {{ article.created_at.slice(11, 16) }}</td>
          <td>{{ article.title }}</td>
          <td>{{ article.views }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { onMounted } from 'vue'
import { useStore } from '@/stores/main'

const router = useRouter()
const store = useStore()

const goArticleDetail = (articlePk) => {
  store.getArticle(articlePk)
}

const goArticleCreate = () => {
  router.push({ name: 'articleCreate' })
}

onMounted(() => {
  store.getArticles()
})
</script>

<style scoped>
.item:hover {
  background-color: rgb(0, 0, 0);
  opacity: 0.5;
}

.article-table {
  min-width: 400px;
}
</style>