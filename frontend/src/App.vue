<script setup lang="ts">
import { ref, provide, onMounted } from 'vue'
import { useLocalStorage } from '@vueuse/core'
import { RouterView } from 'vue-router'

// 使用localStorage持久化暗黑模式设置
const isDark = useLocalStorage('dark-mode', false)

// 切换暗黑模式
const toggleDarkMode = () => {
  isDark.value = !isDark.value
  // 在文档根元素上切换dark类名
  if (isDark.value) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
}

// 提供全局的暗黑模式状态和切换函数
provide('isDark', isDark)
provide('toggleDarkMode', toggleDarkMode)

// 初始化暗黑模式
onMounted(() => {
  // 从localStorage读取设置并应用
  if (isDark.value) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
})
</script>

<template>
  <div class="app min-h-screen w-full transition-colors duration-300">
    <RouterView />
  </div>
</template>

<style>
.app {
  width: 100%;
  height: 100%;
}

/* 修复布局问题 */
body {
  margin: 0;
  padding: 0;
  display: block !important; /* 覆盖默认样式 */
  min-height: 100vh;
  width: 100%;
  overflow-x: hidden;
}

html {
  width: 100%;
  overflow-x: hidden;
}

#app {
  max-width: 100% !important; /* 覆盖默认样式 */
  width: 100% !important;
  margin: 0 !important;
  padding: 0 !important;
  text-align: left !important;
}
</style> 