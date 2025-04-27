import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import { createRouter, createWebHistory } from 'vue-router'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import App from './App.vue'
import routes from './router'
import 'element-plus/dist/index.css'
import './style.css'

// 创建Vue应用
const app = createApp(App)

// 配置Pinia状态管理
const pinia = createPinia()
app.use(pinia)

// 配置Vue Router
const router = createRouter({
  history: createWebHistory(),
  routes
})
app.use(router)

// 配置Element Plus
app.use(ElementPlus)
// 注册所有Element Plus图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

// 挂载应用
app.mount('#app')
