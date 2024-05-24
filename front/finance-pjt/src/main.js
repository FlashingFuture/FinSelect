import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

import App from './App.vue'
import router from './router'
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'
import { useKakao } from 'vue3-kakao-maps/@utils'

const KAKAOMAP_API_KEY = import.meta.env.VITE_KAKAOMAP_API_KEY

const app = createApp(App)
const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)
useKakao(KAKAOMAP_API_KEY, ['clusterer', 'services', 'drawing']);

app.use(pinia)
app.use(router)

app.mount('#app')
