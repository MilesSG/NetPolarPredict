<script setup lang="ts">
import { ref, computed, inject } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { RouterView } from 'vue-router'

const isDark = inject('isDark') as any
const toggleDarkMode = inject('toggleDarkMode') as Function

const isCollapse = ref(false)
const route = useRoute()
const router = useRouter()

const activeIndex = computed(() => route.name as string)

const toggleSidebar = () => {
  isCollapse.value = !isCollapse.value
}

// 获取路由菜单项
const menuItems = computed(() => {
  return router.options.routes[0].children?.filter(route => route.meta?.title) || []
})

// 系统名称
const systemName = '网络热点事件群体极化预测分析系统'
</script>

<template>
  <el-container class="layout-container">
    <!-- 侧边栏 -->
    <el-aside :width="isCollapse ? '64px' : '220px'" class="transition-all duration-300">
      <el-menu
        :default-active="activeIndex"
        class="h-screen"
        :collapse="isCollapse"
        :collapse-transition="false"
        router
        :class="{ 'dark:bg-dark dark:text-white dark:border-gray-700': isDark }"
      >
        <div class="flex items-center justify-between p-4 mb-4" :class="{ 'justify-center': isCollapse }">
          <h2 class="text-lg font-bold truncate" v-if="!isCollapse">{{ systemName }}</h2>
          <el-icon @click="toggleSidebar" class="cursor-pointer">
            <component :is="isCollapse ? 'Expand' : 'Fold'" />
          </el-icon>
        </div>

        <el-menu-item v-for="item in menuItems" :key="item.name" :index="item.name" :route="item.path">
          <el-icon><component :is="item.meta?.icon" /></el-icon>
          <template #title>{{ item.meta?.title }}</template>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <!-- 主内容区 -->
    <el-container>
      <!-- 头部导航 -->
      <el-header class="border-b shadow-sm dark:bg-dark-light dark:border-gray-700 flex items-center justify-between">
        <div class="text-xl font-bold">{{ route.meta?.title }}</div>
        <div class="flex items-center gap-4">
          <el-switch
            v-model="isDark"
            @change="toggleDarkMode"
            class="mr-2"
            :active-icon="'Moon'"
            :inactive-icon="'Sunny'"
          />
          <el-dropdown>
            <span class="flex items-center cursor-pointer">
              <el-avatar :size="32" src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png" />
              <span class="ml-2">管理员</span>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item>个人资料</el-dropdown-item>
                <el-dropdown-item>设置</el-dropdown-item>
                <el-dropdown-item divided>退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <!-- 内容区域 -->
      <el-main class="p-6 dark:bg-dark">
        <RouterView />
      </el-main>
    </el-container>
  </el-container>
</template>

<style scoped>
.layout-container {
  height: 100vh;
}

.el-header {
  height: 64px;
  line-height: 64px;
}
</style> 