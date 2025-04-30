<script setup lang="ts">
import { ref, reactive, onMounted, onBeforeUnmount } from 'vue'
import * as echarts from 'echarts'

// 监控状态
const monitoringActive = ref(true)
const updateInterval = ref(5) // 更新间隔，单位为秒
const alertThreshold = ref(8.0) // 极化指数报警阈值

// 实时数据
const realTimeData = reactive({
  activeEvents: 12,
  totalComments: 0,
  polarizationIndex: 0,
  alertCount: 0,
  recentAlerts: []
})

// 图表实例
let realTimeChart: echarts.ECharts | null = null
let eventDistributionChart: echarts.ECharts | null = null
let alertsTimelineChart: echarts.ECharts | null = null
let platformDistributionChart: echarts.ECharts | null = null

// 模拟数据更新定时器
let dataUpdateTimer: number | null = null

// 监控事件列表
const monitoringEvents = ref([
  { 
    id: 1, 
    title: '某科技公司CEO涉嫌违规交易', 
    category: '科技', 
    polarizationIndex: 8.7, 
    trend: 'up', 
    alertLevel: 'high', 
    lastUpdate: '2025-04-27 12:05:26' 
  },
  { 
    id: 2, 
    title: '新冠疫苗接种争议', 
    category: '医疗', 
    polarizationIndex: 9.2, 
    trend: 'up', 
    alertLevel: 'high', 
    lastUpdate: '2025-04-27 12:04:18' 
  },
  { 
    id: 3, 
    title: '国际贸易政策调整', 
    category: '政治', 
    polarizationIndex: 7.5, 
    trend: 'stable', 
    alertLevel: 'medium', 
    lastUpdate: '2025-04-27 12:03:45' 
  },
  { 
    id: 4, 
    title: '教育改革新政策实施', 
    category: '教育', 
    polarizationIndex: 6.8, 
    trend: 'down', 
    alertLevel: 'medium', 
    lastUpdate: '2025-04-27 12:02:30' 
  },
  { 
    id: 5, 
    title: '环保抗议活动在全国蔓延', 
    category: '环境', 
    polarizationIndex: 8.1, 
    trend: 'up', 
    alertLevel: 'high', 
    lastUpdate: '2025-04-27 12:01:52' 
  }
])

// 报警历史
const alertHistory = ref([
  { 
    id: 1, 
    eventId: 2, 
    title: '新冠疫苗接种争议', 
    timestamp: '2025-04-27 11:55:12', 
    polarizationIndex: 9.2, 
    message: '极化指数超过警戒阈值，短时间内增长迅速' 
  },
  { 
    id: 2, 
    eventId: 1, 
    title: '某科技公司CEO涉嫌违规交易', 
    timestamp: '2025-04-27 11:48:36', 
    polarizationIndex: 8.7, 
    message: '极化指数超过警戒阈值，舆论对立明显' 
  },
  { 
    id: 3, 
    eventId: 5, 
    title: '环保抗议活动在全国蔓延', 
    timestamp: '2025-04-27 11:42:19', 
    polarizationIndex: 8.1, 
    message: '极化指数超过警戒阈值，关注人群增加' 
  }
])

onMounted(() => {
  // 初始化图表
  initRealTimeChart()
  initEventDistributionChart()
  initAlertsTimelineChart()
  initPlatformDistributionChart()
  
  // 启动模拟数据更新
  startDataUpdate()
  
  // 窗口大小变化时重新调整图表
  window.addEventListener('resize', handleResize)
})

onBeforeUnmount(() => {
  // 清理定时器和事件监听器
  if (dataUpdateTimer) {
    clearInterval(dataUpdateTimer)
  }
  window.removeEventListener('resize', handleResize)
})

// 处理窗口大小变化
function handleResize() {
  realTimeChart?.resize()
  eventDistributionChart?.resize()
  alertsTimelineChart?.resize()
  platformDistributionChart?.resize()
}

// 启动数据更新定时器
function startDataUpdate() {
  // 初始化实时数据
  updateRealTimeData()
  
  // 设置定时器，模拟实时数据更新
  dataUpdateTimer = setInterval(() => {
    if (monitoringActive.value) {
      updateRealTimeData()
    }
  }, updateInterval.value * 1000) as unknown as number
}

// 更新实时数据
function updateRealTimeData() {
  // 模拟评论总数增加
  realTimeData.totalComments += Math.floor(Math.random() * 200) + 50
  
  // 模拟极化指数变化
  const randomChange = (Math.random() - 0.5) * 0.4
  realTimeData.polarizationIndex = parseFloat((Math.random() * 2 + 7 + randomChange).toFixed(1))
  
  // 更新监控事件列表
  monitoringEvents.value.forEach(event => {
    // 模拟极化指数变化
    const change = (Math.random() - 0.45) * 0.3
    event.polarizationIndex = parseFloat((event.polarizationIndex + change).toFixed(1))
    
    // 更新趋势
    if (change > 0.1) {
      event.trend = 'up'
    } else if (change < -0.1) {
      event.trend = 'down'
    } else {
      event.trend = 'stable'
    }
    
    // 更新警报级别
    if (event.polarizationIndex >= 8.5) {
      event.alertLevel = 'high'
    } else if (event.polarizationIndex >= 7) {
      event.alertLevel = 'medium'
    } else {
      event.alertLevel = 'low'
    }
    
    // 更新最后更新时间
    const now = new Date()
    event.lastUpdate = `${now.getFullYear()}-${(now.getMonth()+1).toString().padStart(2, '0')}-${now.getDate().toString().padStart(2, '0')} ${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}`
  })
  
  // 检查是否需要添加新警报
  const highAlertEvents = monitoringEvents.value.filter(e => e.polarizationIndex > alertThreshold.value)
  if (highAlertEvents.length > 0 && Math.random() > 0.7) {
    // 随机选择一个高警报事件添加到警报历史
    const randomEvent = highAlertEvents[Math.floor(Math.random() * highAlertEvents.length)]
    const now = new Date()
    const timestamp = `${now.getFullYear()}-${(now.getMonth()+1).toString().padStart(2, '0')}-${now.getDate().toString().padStart(2, '0')} ${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}`
    
    alertHistory.value.unshift({
      id: alertHistory.value.length + 1,
      eventId: randomEvent.id,
      title: randomEvent.title,
      timestamp,
      polarizationIndex: randomEvent.polarizationIndex,
      message: `极化指数达到${randomEvent.polarizationIndex.toFixed(1)}，超过警戒阈值`
    })
    
    // 保持警报历史最多10条
    if (alertHistory.value.length > 10) {
      alertHistory.value.pop()
    }
    
    // 更新警报计数
    realTimeData.alertCount++
  }
  
  // 更新实时图表数据
  updateRealTimeChart()
}

// 初始化实时监控图表
function initRealTimeChart() {
  const chartDom = document.getElementById('real-time-chart')
  if (!chartDom) return
  
  realTimeChart = echarts.init(chartDom)
  
  const option = {
    title: {
      text: '实时极化指数监控',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross',
        label: {
          backgroundColor: '#6a7985'
        }
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: Array(60).fill(0).map((_, i) => i.toString())
    },
    yAxis: {
      type: 'value',
      name: '极化指数',
      min: 0,
      max: 10
    },
    series: [
      {
        name: '整体极化指数',
        type: 'line',
        stack: 'Total',
        smooth: true,
        lineStyle: {
          width: 3
        },
        showSymbol: false,
        areaStyle: {
          opacity: 0.3,
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgb(255, 158, 68)' },
            { offset: 1, color: 'rgb(255, 70, 131)' }
          ])
        },
        data: Array(60).fill(0)
      }
    ],
    visualMap: {
      show: false,
      dimension: 1,
      pieces: [
        { lt: 6, color: '#67C23A' },
        { gte: 6, lt: 8, color: '#E6A23C' },
        { gte: 8, color: '#F56C6C' }
      ]
    }
  }
  
  realTimeChart.setOption(option)
}

// 更新实时图表数据
function updateRealTimeChart() {
  if (!realTimeChart) return
  
  const option = realTimeChart.getOption()
  if (!option.series || !option.series[0] || !option.series[0].data) return
  
  // 添加新的数据点
  const data = [...(option.series[0].data as number[])]
  data.shift()
  data.push(realTimeData.polarizationIndex)
  
  realTimeChart.setOption({
    series: [
      {
        data
      }
    ]
  })
}

// 初始化事件分布图表
function initEventDistributionChart() {
  const chartDom = document.getElementById('event-distribution-chart')
  if (!chartDom) return
  
  eventDistributionChart = echarts.init(chartDom)
  
  const categories = ['科技', '医疗', '政治', '教育', '环境', '娱乐', '体育', '经济']
  const data = categories.map(category => ({ 
    name: category, 
    value: Math.floor(Math.random() * 20) + 5
  }))
  
  const option = {
    title: {
      text: '热点事件类别分布',
      left: 'center'
    },
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 10,
      top: 'center',
      data: categories
    },
    series: [
      {
        name: '事件类别',
        type: 'pie',
        radius: ['50%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 20,
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: false
        },
        data
      }
    ]
  }
  
  eventDistributionChart.setOption(option)
}

// 初始化警报时间线图表
function initAlertsTimelineChart() {
  const chartDom = document.getElementById('alerts-timeline-chart')
  if (!chartDom) return
  
  alertsTimelineChart = echarts.init(chartDom)
  
  // 创建过去24小时的时间点
  const hours = []
  for (let i = 23; i >= 0; i--) {
    const now = new Date()
    now.setHours(now.getHours() - i)
    hours.push(`${now.getHours().toString().padStart(2, '0')}:00`)
  }
  
  // 随机生成各时段的警报数据
  const alertData = hours.map(() => Math.floor(Math.random() * 5))
  
  const option = {
    title: {
      text: '24小时警报趋势',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: hours,
      axisLabel: {
        interval: 3,
        rotate: 45
      }
    },
    yAxis: {
      type: 'value',
      name: '警报数量'
    },
    series: [
      {
        name: '警报数量',
        type: 'bar',
        data: alertData,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#f56c6c' },
            { offset: 1, color: '#fac858' }
          ])
        },
        emphasis: {
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: '#e64c4c' },
              { offset: 1, color: '#e6a23c' }
            ])
          }
        }
      }
    ]
  }
  
  alertsTimelineChart.setOption(option)
}

// 初始化平台分布图表
function initPlatformDistributionChart() {
  const chartDom = document.getElementById('platform-distribution-chart')
  if (!chartDom) return
  
  platformDistributionChart = echarts.init(chartDom)
  
  const platforms = ['微博', '微信', '知乎', '抖音', '小红书', 'B站', '今日头条']
  const data = platforms.map(platform => ({ 
    name: platform, 
    value: Math.floor(Math.random() * 100) + 50 
  }))
  
  const option = {
    title: {
      text: '平台活跃度分布',
      left: 'center'
    },
    tooltip: {
      trigger: 'item'
    },
    radar: {
      indicator: platforms.map(platform => ({ name: platform, max: 150 }))
    },
    series: [
      {
        name: '平台活跃度',
        type: 'radar',
        data: [
          {
            value: data.map(item => item.value),
            name: '评论数量',
            areaStyle: {
              color: new echarts.graphic.RadialGradient(0.5, 0.5, 1, [
                { offset: 0, color: 'rgba(54, 162, 235, 0.8)' },
                { offset: 1, color: 'rgba(54, 162, 235, 0.2)' }
              ])
            }
          }
        ]
      }
    ]
  }
  
  platformDistributionChart.setOption(option)
}

// 获取警报级别样式
function getAlertLevelClass(level: string): string {
  switch (level) {
    case 'high':
      return 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400'
    case 'medium':
      return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400'
    case 'low':
      return 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400'
    default:
      return 'bg-gray-100 text-gray-800 dark:bg-gray-900/30 dark:text-gray-400'
  }
}

// 获取趋势图标
function getTrendIcon(trend: string): string {
  switch (trend) {
    case 'up':
      return 'ArrowUp'
    case 'down':
      return 'ArrowDown'
    case 'stable':
      return 'DArrowRight'
    default:
      return 'More'
  }
}

// 获取趋势颜色
function getTrendColor(trend: string): string {
  switch (trend) {
    case 'up':
      return 'text-red-500 dark:text-red-400'
    case 'down':
      return 'text-green-500 dark:text-green-400'
    case 'stable':
      return 'text-gray-500 dark:text-gray-400'
    default:
      return 'text-gray-500 dark:text-gray-400'
  }
}

// 暂停或恢复监控
function toggleMonitoring() {
  monitoringActive.value = !monitoringActive.value
}

// 更新监控设置
function updateMonitoringSettings() {
  // 这里可以添加更新监控设置的逻辑
  if (dataUpdateTimer) {
    clearInterval(dataUpdateTimer)
  }
  
  startDataUpdate()
}
</script>

<template>
  <div class="real-time-monitor-container w-full">
    <!-- 控制面板 -->
    <el-card class="mb-6 control-panel" :class="{ 'dark:bg-dark-light': true }">
      <div class="flex flex-col md:flex-row justify-between items-center">
        <div class="flex items-center mb-4 md:mb-0">
          <div 
            class="flex items-center px-4 py-2 rounded-lg mr-4"
            :class="monitoringActive ? 'bg-green-100 dark:bg-green-900/30' : 'bg-red-100 dark:bg-red-900/30'"
          >
            <div 
              class="w-3 h-3 rounded-full mr-2 animate-pulse"
              :class="monitoringActive ? 'bg-green-500' : 'bg-red-500'"
            ></div>
            <span 
              class="font-medium"
              :class="monitoringActive ? 'text-green-700 dark:text-green-400' : 'text-red-700 dark:text-red-400'"
            >
              {{ monitoringActive ? '监控中' : '已暂停' }}
            </span>
          </div>
          
          <el-button 
            :type="monitoringActive ? 'danger' : 'success'" 
            @click="toggleMonitoring"
          >
            {{ monitoringActive ? '暂停监控' : '恢复监控' }}
          </el-button>
        </div>
        
        <div class="flex items-center">
          <div class="mr-6">
            <span class="text-gray-500 dark:text-gray-400 mr-2">更新间隔:</span>
            <el-select v-model="updateInterval" size="small" class="w-24">
              <el-option :value="1" label="1秒"></el-option>
              <el-option :value="5" label="5秒"></el-option>
              <el-option :value="10" label="10秒"></el-option>
              <el-option :value="30" label="30秒"></el-option>
            </el-select>
          </div>
          
          <div class="mr-6">
            <span class="text-gray-500 dark:text-gray-400 mr-2">警报阈值:</span>
            <el-select v-model="alertThreshold" size="small" class="w-24">
              <el-option :value="7.0" label="7.0"></el-option>
              <el-option :value="7.5" label="7.5"></el-option>
              <el-option :value="8.0" label="8.0"></el-option>
              <el-option :value="8.5" label="8.5"></el-option>
            </el-select>
          </div>
          
          <el-button type="primary" size="small" @click="updateMonitoringSettings">
            应用设置
          </el-button>
        </div>
      </div>
    </el-card>
    
    <!-- 指标卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
      <el-card shadow="hover" class="metric-card" :class="{ 'dark:bg-dark-light': true }">
        <div class="flex items-center">
          <div class="bg-blue-500 rounded-lg p-3 mr-4">
            <el-icon class="text-white text-2xl"><Monitor /></el-icon>
          </div>
          <div>
            <div class="text-gray-500 dark:text-gray-400 text-sm">监控事件数</div>
            <div class="text-2xl font-bold mt-1 dark:text-white">{{ monitoringEvents.length }}</div>
          </div>
        </div>
      </el-card>
      
      <el-card shadow="hover" class="metric-card" :class="{ 'dark:bg-dark-light': true }">
        <div class="flex items-center">
          <div class="bg-green-500 rounded-lg p-3 mr-4">
            <el-icon class="text-white text-2xl"><ChatDotRound /></el-icon>
          </div>
          <div>
            <div class="text-gray-500 dark:text-gray-400 text-sm">评论总数</div>
            <div class="text-2xl font-bold mt-1 dark:text-white">{{ realTimeData.totalComments.toLocaleString() }}</div>
          </div>
        </div>
      </el-card>
      
      <el-card shadow="hover" class="metric-card" :class="{ 'dark:bg-dark-light': true }">
        <div class="flex items-center">
          <div 
            class="rounded-lg p-3 mr-4"
            :class="realTimeData.polarizationIndex >= 8 ? 'bg-red-500' : (realTimeData.polarizationIndex >= 6 ? 'bg-yellow-500' : 'bg-green-500')"
          >
            <el-icon class="text-white text-2xl"><DataAnalysis /></el-icon>
          </div>
          <div>
            <div class="text-gray-500 dark:text-gray-400 text-sm">当前极化指数</div>
            <div 
              class="text-2xl font-bold mt-1"
              :class="realTimeData.polarizationIndex >= 8 ? 'text-red-500' : (realTimeData.polarizationIndex >= 6 ? 'text-yellow-500' : 'text-green-500')"
            >
              {{ realTimeData.polarizationIndex.toFixed(1) }}
            </div>
          </div>
        </div>
      </el-card>
      
      <el-card shadow="hover" class="metric-card" :class="{ 'dark:bg-dark-light': true }">
        <div class="flex items-center">
          <div class="bg-red-500 rounded-lg p-3 mr-4">
            <el-icon class="text-white text-2xl"><Warning /></el-icon>
          </div>
          <div>
            <div class="text-gray-500 dark:text-gray-400 text-sm">今日警报数</div>
            <div class="text-2xl font-bold mt-1 text-red-500">{{ realTimeData.alertCount }}</div>
          </div>
        </div>
      </el-card>
    </div>
    
    <!-- 图表区域 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
      <!-- 实时极化指数图表 -->
      <el-card class="chart-card" :class="{ 'dark:bg-dark-light': true }">
        <div id="real-time-chart" class="chart-container"></div>
      </el-card>
      
      <!-- 事件分布图表 -->
      <el-card class="chart-card" :class="{ 'dark:bg-dark-light': true }">
        <div id="event-distribution-chart" class="chart-container"></div>
      </el-card>
      
      <!-- 警报时间线图表 -->
      <el-card class="chart-card" :class="{ 'dark:bg-dark-light': true }">
        <div id="alerts-timeline-chart" class="chart-container"></div>
      </el-card>
      
      <!-- 平台分布图表 -->
      <el-card class="chart-card" :class="{ 'dark:bg-dark-light': true }">
        <div id="platform-distribution-chart" class="chart-container"></div>
      </el-card>
    </div>
    
    <!-- 监控事件列表 -->
    <el-card class="mb-6 monitoring-events-card" :class="{ 'dark:bg-dark-light': true }">
      <template #header>
        <div class="flex justify-between items-center">
          <span class="text-lg font-bold">实时监控事件</span>
          <el-button type="primary" size="small">添加监控事件</el-button>
        </div>
      </template>
      
      <el-table :data="monitoringEvents" style="width: 100%" stripe>
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        
        <el-table-column prop="title" label="事件标题" min-width="250">
          <template #default="{ row }">
            <div class="font-medium">{{ row.title }}</div>
          </template>
        </el-table-column>
        
        <el-table-column prop="category" label="类别" width="100">
          <template #default="{ row }">
            <el-tag>{{ row.category }}</el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="polarizationIndex" label="极化指数" width="120">
          <template #default="{ row }">
            <div class="flex items-center">
              <span 
                class="mr-2"
                :class="row.polarizationIndex >= 8 ? 'text-red-500' : (row.polarizationIndex >= 6 ? 'text-yellow-500' : 'text-green-500')"
              >
                {{ row.polarizationIndex.toFixed(1) }}
              </span>
              <el-icon :class="getTrendColor(row.trend)">
                <component :is="getTrendIcon(row.trend)"></component>
              </el-icon>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column prop="alertLevel" label="警报级别" width="120">
          <template #default="{ row }">
            <span 
              class="px-2 py-1 rounded text-xs font-medium"
              :class="getAlertLevelClass(row.alertLevel)"
            >
              {{ 
                row.alertLevel === 'high' ? '高危' : 
                row.alertLevel === 'medium' ? '中等' : '低危' 
              }}
            </span>
          </template>
        </el-table-column>
        
        <el-table-column prop="lastUpdate" label="最后更新" width="180"></el-table-column>
        
        <el-table-column label="操作" width="180">
          <template #default="{ row }">
            <el-button type="primary" size="small" link>详情</el-button>
            <el-button type="success" size="small" link>预测</el-button>
            <el-button type="danger" size="small" link>取消监控</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <!-- 警报历史 -->
    <el-card class="alert-history-card" :class="{ 'dark:bg-dark-light': true }">
      <template #header>
        <div class="flex justify-between items-center">
          <span class="text-lg font-bold">警报历史</span>
          <el-button type="primary" text>查看所有警报</el-button>
        </div>
      </template>
      
      <div class="alert-timeline">
        <div 
          v-for="alert in alertHistory" 
          :key="alert.id"
          class="alert-item flex mb-4 pb-4 border-b dark:border-gray-700 last:border-0 last:mb-0 last:pb-0"
        >
          <div class="alert-icon mr-4 relative">
            <div class="w-10 h-10 rounded-full flex items-center justify-center bg-red-100 dark:bg-red-900/30">
              <el-icon class="text-red-500"><Warning /></el-icon>
            </div>
            <div class="absolute top-10 bottom-0 left-1/2 transform -translate-x-1/2 w-0.5 bg-gray-200 dark:bg-gray-700" v-if="alert.id !== alertHistory[alertHistory.length - 1].id"></div>
          </div>
          
          <div class="alert-content flex-1">
            <div class="flex justify-between items-start mb-1">
              <span class="font-medium text-red-500 dark:text-red-400">【警报】{{ alert.title }}</span>
              <span class="text-gray-500 dark:text-gray-400 text-sm">{{ alert.timestamp }}</span>
            </div>
            <div class="mb-2 text-gray-700 dark:text-gray-300">{{ alert.message }}</div>
            <div class="flex justify-between items-center">
              <div>
                <span class="text-gray-500 dark:text-gray-400 text-sm mr-2">极化指数:</span>
                <span class="font-medium text-red-500">{{ alert.polarizationIndex.toFixed(1) }}</span>
              </div>
              <div>
                <el-button type="primary" size="small" link>查看事件</el-button>
                <el-button type="success" size="small" link>处理</el-button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<style scoped>
.real-time-monitor-container {
  width: 100%;
}

.chart-container {
  height: 350px;
}

.metric-card {
  transition: all 0.3s;
}

.chart-card,
.monitoring-events-card,
.alert-history-card {
  transition: all 0.3s;
}
</style> 