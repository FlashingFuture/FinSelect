<template>
  <div class="article-align mx-5">
    <div class="p-3">
      <h1>게시판</h1>
    </div>
    <div>
      <RouterView class="p-3"/>
    </div>
    <div class="p-3">
      <ArticleList />
    </div>
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
import ArticleList from '@/components/ArticleList.vue'
</script>

<style scoped>
.article-align {
  text-align: start;
}
</style>