<template>
  <div>
    <div class="article-div">
      <div class="article-title">
        <p>{{ article.title }}</p>
      </div>
      <div class="article-content">
        <p>{{ article.content }}</p>
      </div>
    </div>
    <div class="py-1">
      <button @click="goUpdateArticle" class="me-2 btn bg-primary-subtle">글 수정</button>
      <button @click="deleteArticle(article.id)" class="btn bg-danger-subtle me-1">글 삭제</button>
    </div>
    <div class="comment-div">
      <div>
        <p>댓글 [{{ store.comments.length }}]</p>
      </div>
      <div>
        <hr>
        <div v-for="comment in store.comments"
          :key="comment.id">
          <span v-if="onUpdate !== comment.id" class="me-1">{{ comment.user.username }} | {{ comment.content }}</span>
          <input v-else type="text" v-model="updateContent" class="me-1 comment-update" @keyup.enter="updateComment(article.id, comment.id)">
          <button v-if="onUpdate !== comment.id" class="me-2 comment-change" @click="tryUpdate(comment.id, comment.user.id)">수정</button>
          <button v-else class="me-2 comment-change" @click="updateComment(article.id, comment.id)">수정</button>
          <button @click="deleteComment(article.id, comment.id)" class="comment-change">삭제</button>
          <hr>
        </div>
      </div>
    </div>
    <div class="comment-div">
      <div>
        <p>댓글 쓰기</p>
      </div>
      <div>
        <form @submit.prevent="createComment">
          <input @keyup.enter="submit" class="comment-input" v-model.trim="content">
          <button @click="submit" class="comment-submit">제출</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useStore } from '@/stores/main'

const route = useRoute()
const router = useRouter()
const store = useStore()

const article = ref(store.articles.find((element) => element.id == route.params.articlePk))
console.log(article.value)
const content = ref(null)
const updateContent = ref(null)
const onUpdate = ref(0)

const goUpdateArticle = () => {
  if (article.value.user.id == store.currentUserData.pk) {
    router.push({ name: 'articleUpdate'})
  } else {
    window.alert('권한이 없어요.')
  }
}

const deleteArticle = (article_id) => {
  store.deleteArticle(article_id)
}

const createComment = () => {
  const payload = {
    content: content.value,
    article_pk: route.params.articlePk
  }
  store.createComment(payload)
  content.value = null
}

const tryUpdate = (commentId, commentUserId) => {
  if (commentUserId == store.currentUserData.pk) {
    if (onUpdate.value) {
      window.alert('한 번에 하나의 댓글만 수정할 수 있습니다.')
    } else {
      updateContent.value = store.comments.find(comment => comment.id == commentId).content
      onUpdate.value = commentId
    }
  } else {
    window.alert('권한이 없습니다.')
  }
}

const updateComment = (articleId, commentId) => {
  const payload = {
    content: updateContent.value,
    article_pk: articleId,
    comment_pk: commentId,
  }
  store.updateComment(payload)
  onUpdate.value = 0
}

const deleteComment = (article_id, comment_id) => {
  store.deleteComment(article_id, comment_id)
}

watch(() => route.params.articlePk, (to, from) => {
  console.log(to)
  store.getArticle(to)
  store.getComments(to)
  article.value = store.articles.find((element) => element.id == to)
})

onMounted(() => {
  store.getComments(route.params.articlePk)
  console.log(store.comments)
})
</script>

<style scoped>
.article-div {
  min-height: 500px;
}

.article-title {
  border-bottom: 1px solid rgb(196, 228, 250);
}

.article-title p {
  font-size: 20px;
}

.article-content {
  padding: 30px;
}

.comment-div {
  background-color: rgb(228, 233, 255);
  padding: 10px;
}

.comment-input {
  width: 100%;
  height: 30px;
  margin-bottom: 10px;
}

.comment-submit {
  width: 100%;
  border: 1px solid rgb(206, 206, 255);
  background-color: rgb(206, 206, 255);
}

.comment-change {
  border: 1px solid rgb(201, 215, 231);
  background-color: rgb(201, 215, 231);
}

.comment-update {
  width: 60%;
}
</style>