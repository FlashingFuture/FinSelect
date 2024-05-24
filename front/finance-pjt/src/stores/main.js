import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useStore = defineStore('main', () => {
  const router = useRouter()
  const token = ref(null)
  const isAuth = computed(() => {
    return token.value !== null
  })
  const currentUserData = ref(null)

  const bankData = ref([])
  const depositData = ref([])
  const savingsData = ref([])
  const currentDetail = ref(null)

  const quizCount = ref(1)
  const quizAnswer = ref(
    [null, null, null]
  )
  // 지피티에게 채팅 보내기
  const currentGptResponse = ref(null)

  const giveGptChat = (message) => {
    console.log(typeof(message))
    console.log(message)
    axios({
      method: 'post',
      url: 'http://127.0.0.1:8000/get_recommendations/',
      data: {
        message,
      }
    })
    .then((response) => {
      currentGptResponse.value = response.data.choices[0].message.content
    })
    .catch((error) => {
      console.log(error)
      if (currentGptResponse.value == '에러 발생. 다시 시도해 주세요...') {
      currentGptResponse.value = '에러 발생. 다시 시도해 주세요.'
      } else {
        currentGptResponse.value = '에러 발생. 다시 시도해 주세요...'
      }
  })
  }


  // 금융상품 관련 기능
  const getBankData = () => {
    axios({
      method: 'get',
      url: 'http://127.0.0.1:8000/api/v1/banks/'
    })
    .then((response) => {
      bankData.value = response.data
    })
    .catch((error) => console.log(error))
  }

  const getDepositData = (payload) => {
    let { sort_key, bank_id, bank_tag, save_trm, money_mount } = payload
    if (save_trm == 0) save_trm = null
    if (money_mount == 0) money_mount = null
    axios({
      method: 'get',
      url: 'http://127.0.0.1:8000/api/v1/fixedDeposits/',
      params: {
        sort_key,
        bank_id,
        bank_tag,
        save_trm,
        money_mount,
      }
    })
    .then((response) => {
      depositData.value = response.data
    })
    .catch((error) => console.log(error))
  }

  const getDepositDetail = (deposit_pk) => {
    axios({
      method: 'post',
      url: `http://127.0.0.1:8000/api/v1/fixedDeposits/${deposit_pk}/`,

    })
    .then((response) => {
      currentDetail.value = response.data
      router.push({ name: 'itemDetail', params: { itemPk: deposit_pk }})
    })
    .catch(error => console.log(error))
  }

  
  const likeDeposit = (deposit_pk) => {
    axios({
      method: 'post',
      url: `http://127.0.0.1:8000/api/v1/fixedDeposits/${deposit_pk}/like/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
    .then((response) => {
      getDepositDetail(deposit_pk)
    })
    .catch((error) => console.log(error))
  }

  const getSavingsData = (payload) => {
    let { sort_key, bank_id, bank_tag, save_trm, money_mount } = payload
    if (save_trm == 0) save_trm = null
    if (money_mount == 0) money_mount = null
    axios({
      method: 'get',
      url: 'http://127.0.0.1:8000/api/v1/SavingAccounts/',
      params: {
        sort_key,
        bank_id,
        bank_tag,
        save_trm,
        money_mount
      }
    })
    .then((response) => {
      savingsData.value = response.data
    })
    .catch((error) => console.log(error))
  }

  const getSavingDetail = (saving_pk) => {
    axios({
      method: 'post',
      url: `http://127.0.0.1:8000/api/v1/SavingAccounts/${saving_pk}/`,

    })
    .then((response) => {
      currentDetail.value = response.data
      router.push({ name: 'savingDetail', params: { itemPk: saving_pk }})
    })
    .catch(error => console.log(error))
  }

  const likeSaving = (saving_pk) => {
    axios({
      method: 'post',
      url: `http://127.0.0.1:8000/api/v1/SavingAccounts/${saving_pk}/like/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
    .then((response) => {
      getSavingDetail(saving_pk)
    })
  }

  const exchangedMoney = ref(null)

  const getExchange = ({ to_country, from_country, money }) => {
    console.log(to_country)
    axios({
      method: 'get',
      url: `http://127.0.0.1:8000/api/v1/exchange/`,
      params: {
        to_country,
        from_country,
        money,
      }
    })
    .then((result) => {
      exchangedMoney.value = result.data.result
    })
    .catch((error) => {
      exchangedMoney.value = null
    })
  }


  // 로그인, 유저 기능
  const signin = (payload) => {
    const { username, password1, password2, email, age, gender } = payload
    axios({
      method: 'post',
      url: 'http://127.0.0.1:8000/accounts/signup/',
      data: {
        username,
        password1,
        password2,
        email,
        age,
        gender
      }
    })
    .then((response) => {
      token.value = response.data.key
      router.push({ name: 'login' })
    })
    .catch(error => window.alert('400 BAD REQUEST'))
  }

  const getUser = () => {
    axios({
      method: 'get',
      url: 'http://127.0.0.1:8000/accounts/user/',
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
    .then((response) => {
      currentUserData.value = response.data
    })
    .catch(error => {console.log(error)})
  }


  const login = (payload) => {
    const { username, password } = payload

    axios({
      method: 'post',
      url: 'http://127.0.0.1:8000/accounts/login/',
      data: {
        username,
        password
      }
    })
    .then((response) => {
      token.value = response.data.key
      getUser()
      router.push({ name: 'home' })
    })
    .catch((error) => {
      window.alert('틀렸습니다!')
    })
  }

  const logout = () => {
    axios({
      method: 'post',
      url: 'http://127.0.0.1:8000/accounts/logout/',
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
    .then((response) => {
      token.value = null
      currentUserData.value = null
      router.push({ name: 'home' })
    })
    .catch((error) => {
      window.alert('로그아웃 실패. 다시 로그인 해 주세요.')
      token.value = null
      currentUserData.value = null
    })
  }

  const update = (payload) => {
    const { userId, newData } = payload
    axios({
      method: 'patch',
      url: `http://127.0.0.1:8000/accounts/user/`,
      data: newData,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
    .then((response) => {
    })
    .catch(error => console.log(error))
  }

  const passwordUpdate = (payload) => {
    const { currentPassword, new_password1, new_password2 } = payload
    axios({
      method: 'post',
      url: 'http://127.0.0.1:8000/accounts/password/change/',
      data: {
        currentPassword,
        new_password1,
        new_password2,
      },
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
  }

  // 게시판 기능
  const articles = ref(null)

  const getArticles = () => {
    axios({
      method: 'get',
      url: 'http://127.0.0.1:8000/api/v2/articles/',
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
    .then((response) => {
      articles.value = response.data.slice().reverse()
    })
    .catch(error => console.log(error))
  }

  const getArticle = (article_pk) => {
    axios({
      method: 'post',
      url: `http://127.0.0.1:8000/api/v2/articles/${article_pk}/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
    .then((response) => {
      console.log('게시글 detail')
    router.push({ name: 'articleDetail', params: { articlePk: article_pk } })
    })
  }

  const createArticle = ({ title, content, article_file }) => {
    axios({
      method: 'post',
      url: 'http://127.0.0.1:8000/api/v2/articles/',
      headers: {
        Authorization: `Token ${token.value}`
      },
      data: {
        title,
        content,
        article_file,
      }
    })
    .then((response) => {
      console.log(response.data.id)
      router.push({ name: 'articles' })
    })
    .catch(error => console.log(error))
  }

  const updateArticle = ({ title, content, article_id }) => {
    axios({
      method: 'put',
      url: `http://127.0.0.1:8000/api/v2/articles/${article_id}/`,
      headers: {
        Authorization: `Token ${token.value}`
      },
      data: {
        title,
        content,
        article_file: null,
      }
    })
    .then((response) => {
      getArticles()
      router.push({ name: 'articleDetail', params: { articlePk: article_id}})
    })
    .catch((error) => {
      window.alert('문제가 발생했습니다.')
      router.push({ name: 'articles' })
  })
  }

  const deleteArticle = (article_id) => {
    axios({
      method: 'delete',
      url: `http://127.0.0.1:8000/api/v2/articles/${article_id}/`,
      headers: {
        Authorization: `Token ${token.value}`
      },
    })
    .then((response) => {
      getArticles()
      router.push({ name: 'articles' })
    })
    .catch(error => window.alert('권한 없음'))
  }

  const comments = ref([])

  const getComments = (article_pk) => {
    axios({
      method: 'get',
      url: `http://127.0.0.1:8000/api/v2/comments/`,
      headers: {
        Authorization: `Token ${token.value}`
      },
    })
    .then((response) => {
      console.log(response.data)
      if (response.data) {
        if (comments.value) {
          comments.value.splice(0, comments.value.length)
        }
        for (const comment of response.data) {
          if (article_pk == comment.article.id) {
            comments.value.push(comment)
          }
        }
      } else {
        comments.value = []
      }
    })
    .catch(error => console.log(error))
  }

  const createComment = ({ content, article_pk }) => {
    axios({
      method: 'post',
      url: `http://127.0.0.1:8000/api/v2/articles/${article_pk}/comments/`,
      headers: {
        Authorization: `Token ${token.value}`
      },
      data: {
        content,
      }
    })
    .then((response) => {
      getComments(article_pk)
    })
    .catch(error => console.log(error))
  }

  const deleteComment = (article_pk, comment_pk) => {
    axios({
      method: 'delete',
      url: `http://127.0.0.1:8000/api/v2/comments/${comment_pk}/`,
      headers: {
        Authorization: `Token ${token.value}`
      },
    })
    .then((response) => {
      getComments(article_pk)
    })
    .catch((error) => {
      window.alert('권한이 없습니다!')
    })
  }

  const updateComment = ({content, article_pk, comment_pk}) => {
    axios({
      method: 'put',
      url: `http://127.0.0.1:8000/api/v2/comments/${comment_pk}/`,
      headers: {
        Authorization: `Token ${token.value}`
      },
      data: {
        content,
      }
    })
    .then((response) => {
      getComments(article_pk)
    })
    .catch((error) => {
      window.alert('수정 실패. 게시판으로 돌아갑니다.')
      router.push({ name: 'articles' })
    })
  }

  return { token, isAuth, currentUserData,
          bankData, depositData, savingsData,
          quizCount, quizAnswer, 
          getBankData, getDepositData, getDepositDetail, likeDeposit,
          getSavingsData, getSavingDetail, currentDetail, likeSaving,
          exchangedMoney, getExchange,
          signin, login, logout, update, passwordUpdate,
          articles, getArticles, getArticle, createArticle, deleteArticle, updateArticle,
          comments, getComments, createComment, deleteComment, updateComment,
          giveGptChat, currentGptResponse,
        }
}, { persist: true })
