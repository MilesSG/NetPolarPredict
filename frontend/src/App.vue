<script setup lang="ts">
import { ref, provide } from 'vue'
import { useLocalStorage } from '@vueuse/core'
import { RouterView } from 'vue-router'

const isDark = useLocalStorage('dark-mode', false)

const toggleDarkMode = () => {
  isDark.value = !isDark.value
  document.documentElement.classList.toggle('dark', isDark.value)
}

// 提供全局的暗黑模式状态
provide('isDark', isDark)
provide('toggleDarkMode', toggleDarkMode)

// 初始化暗黑模式
if (isDark.value) {
  document.documentElement.classList.add('dark')
}
</script>

<template>
  <div class="app min-h-screen transition-colors duration-300" :class="{ 'dark': isDark }">
    <RouterView />
  </div>
</template>

<style>
.app {
  width: 100%;
  height: 100%;
}
</style> 