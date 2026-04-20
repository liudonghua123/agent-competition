import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import './style.css'
import App from './App.vue'
import { useThemeStore } from './stores/theme'

const app = createApp(App)

const pinia = createPinia()
app.use(pinia)

// Initialize theme
const themeStore = useThemeStore(pinia)
themeStore.init()

app.use(router)

app.mount('#app')