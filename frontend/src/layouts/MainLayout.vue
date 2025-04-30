<script setup lang="ts">
import { ref, computed, inject } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { RouterView } from 'vue-router'
import { Moon, Sunny } from '@element-plus/icons-vue'

const isDark = inject('isDark') as any
const toggleDarkMode = inject('toggleDarkMode') as Function

const isCollapse = ref(false)
const route = useRoute()
const router = useRouter()

// 活动菜单项，使用路径而不是名称来匹配
const activeIndex = computed(() => {
  // 如果是事件详情页，激活"events"菜单
  if (route.name === 'EventDetail') {
    return '/events'
  }
  // 返回当前路由的路径
  return route.path
})

const toggleSidebar = () => {
  isCollapse.value = !isCollapse.value
}

// 获取路由菜单项
const menuItems = computed(() => {
  // 过滤掉事件详情页，它不应该出现在菜单中
  return router.options.routes[0].children?.filter(route => 
    route.meta?.title && route.name !== 'EventDetail'
  ) || []
})

// 系统名称
const systemName = '网络热点事件群体极化预测分析系统'
</script>

<template>
  <el-container class="layout-container w-full">
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

        <el-menu-item 
          v-for="item in menuItems" 
          :key="item.name" 
          :index="'/' + item.path" 
          :route="'/' + item.path"
        >
          <el-icon><component :is="item.meta?.icon" /></el-icon>
          <template #title>{{ item.meta?.title }}</template>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <!-- 主内容区 -->
    <el-container class="w-full">
      <!-- 头部导航 -->
      <el-header class="border-b shadow-sm dark:bg-dark-light dark:border-gray-700 flex items-center justify-between w-full">
        <div class="text-xl font-bold">{{ route.meta?.title }}</div>
        <div class="flex items-center gap-4">
          <el-switch
            v-model="isDark"
            @change="toggleDarkMode"
            class="mr-2"
            active-color="#1E293B"
            inactive-color="#F8FAFC"
            inline-prompt
            size="large"
            :active-icon="Moon"
            :inactive-icon="Sunny"
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
      <el-main class="p-6 dark:bg-dark w-full">
        <RouterView v-slot="{ Component }">
          <keep-alive>
            <component :is="Component" />
          </keep-alive>
        </RouterView>
      </el-main>
    </el-container>
  </el-container>
</template>

<style scoped>
.layout-container {
  height: 100vh;
  width: 100%;
}

.el-header {
  height: 64px;
  line-height: 64px;
  width: 100%;
}

.el-main {
  overflow-y: auto;
  padding: 20px !important;
  width: 100%;
}

.el-container {
  width: 100%;
  flex: 1;
}
</style> 