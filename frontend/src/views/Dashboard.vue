<script setup lang="ts">
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'

interface StatCardProps {
  title: string
  value: number | string
  icon: string
  color: string
}

// 统计卡片数据
const statCards = ref<StatCardProps[]>([
  { title: '监测事件总数', value: 125, icon: 'DataLine', color: 'bg-blue-500' },
  { title: '极化事件数量', value: 43, icon: 'Warning', color: 'bg-red-500' },
  { title: '今日新增评论', value: '12,836', icon: 'ChatDotRound', color: 'bg-green-500' },
  { title: '情感分析准确率', value: '96.7%', icon: 'Histogram', color: 'bg-purple-500' }
])

// 近期热点事件数据
const recentEvents = ref([
  { id: 1, title: '某科技公司CEO涉嫌违规交易', category: '科技', polarizationLevel: 8.7, date: '2025-04-25' },
  { id: 2, title: '新冠疫苗接种争议', category: '医疗', polarizationLevel: 9.2, date: '2025-04-23' },
  { id: 3, title: '国际贸易政策调整', category: '政治', polarizationLevel: 7.5, date: '2025-04-22' },
  { id: 4, title: '教育改革新政策实施', category: '教育', polarizationLevel: 6.8, date: '2025-04-20' },
  { id: 5, title: '环保抗议活动在全国蔓延', category: '环境', polarizationLevel: 8.1, date: '2025-04-18' }
])

// 极化趋势图表
let polarizationTrendChart: echarts.ECharts | null = null
// 情感分布图表
let sentimentDistributionChart: echarts.ECharts | null = null

onMounted(() => {
  initPolarizationTrendChart()
  initSentimentDistributionChart()
  
  window.addEventListener('resize', () => {
    polarizationTrendChart?.resize()
    sentimentDistributionChart?.resize()
  })
})

// 初始化极化趋势图
function initPolarizationTrendChart() {
  const chartDom = document.getElementById('polarization-trend-chart')
  if (!chartDom) return
  
  polarizationTrendChart = echarts.init(chartDom)
  
  const option = {
    title: {
      text: '近30天群体极化趋势',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis'
    },
    xAxis: {
      type: 'category',
      data: Array.from({ length: 30 }, (_, i) => `4/${i + 1}`)
    },
    yAxis: {
      type: 'value',
      name: '极化指数',
      min: 0,
      max: 10
    },
    series: [
      {
        name: '极化指数',
        type: 'line',
        data: Array.from({ length: 30 }, () => +(Math.random() * 4 + 5).toFixed(1)),
        markPoint: {
          data: [
            { type: 'max', name: '最大值' },
            { type: 'min', name: '最小值' }
          ]
        },
        markLine: {
          data: [{ type: 'average', name: '平均值' }]
        },
        itemStyle: {
          color: '#FF6B3D'
        },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(255, 107, 61, 0.8)' },
            { offset: 1, color: 'rgba(255, 107, 61, 0.1)' }
          ])
        }
      }
    ]
  }
  
  polarizationTrendChart.setOption(option)
}

// 初始化情感分布图
function initSentimentDistributionChart() {
  const chartDom = document.getElementById('sentiment-distribution-chart')
  if (!chartDom) return
  
  sentimentDistributionChart = echarts.init(chartDom)
  
  const option = {
    title: {
      text: '热点事件情感分布',
      left: 'center'
    },
    tooltip: {
      trigger: 'item'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        name: '情感分布',
        type: 'pie',
        radius: '65%',
        center: ['50%', '60%'],
        data: [
          { value: 42, name: '积极' },
          { value: 38, name: '消极' },
          { value: 20, name: '中性' }
        ],
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        },
        itemStyle: {
          borderRadius: 8,
          borderColor: '#fff',
          borderWidth: 2
        }
      }
    ]
  }
  
  sentimentDistributionChart.setOption(option)
}
</script>

<template>
  <div class="dashboard">
    <!-- 统计卡片区域 -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <el-card 
        v-for="(card, index) in statCards" 
        :key="index" 
        class="stat-card transition-all hover:shadow-lg hover:-translate-y-1"
        :class="{ 'dark:bg-dark-light': true }"
      >
        <div class="flex items-center">
          <div :class="`${card.color} rounded-lg p-3 mr-4`">
            <el-icon class="text-white text-2xl">
              <component :is="card.icon"></component>
            </el-icon>
          </div>
          <div>
            <div class="text-gray-500 text-sm dark:text-gray-400">{{ card.title }}</div>
            <div class="text-2xl font-bold mt-1 dark:text-white">{{ card.value }}</div>
          </div>
        </div>
      </el-card>
    </div>
    
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
      <!-- 极化趋势图 -->
      <el-card class="chart-card" :class="{ 'dark:bg-dark-light': true }">
        <div id="polarization-trend-chart" class="chart-container"></div>
      </el-card>
      
      <!-- 情感分布图 -->
      <el-card class="chart-card" :class="{ 'dark:bg-dark-light': true }">
        <div id="sentiment-distribution-chart" class="chart-container"></div>
      </el-card>
    </div>
    
    <!-- 近期热点事件 -->
    <el-card class="recent-events-card" :class="{ 'dark:bg-dark-light': true }">
      <template #header>
        <div class="flex justify-between items-center">
          <span class="text-lg font-bold">近期热点事件</span>
          <el-button type="primary" text>查看全部</el-button>
        </div>
      </template>
      
      <el-table :data="recentEvents" style="width: 100%" stripe :class="{ 'dark:bg-dark-light': true }">
        <el-table-column prop="title" label="事件标题" min-width="280">
          <template #default="{ row }">
            <div class="font-medium">{{ row.title }}</div>
          </template>
        </el-table-column>
        <el-table-column prop="category" label="类别" width="120">
          <template #default="{ row }">
            <el-tag>{{ row.category }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="polarizationLevel" label="极化程度" width="120">
          <template #default="{ row }">
            <el-progress 
              :percentage="row.polarizationLevel * 10" 
              :color="row.polarizationLevel > 8 ? '#F56C6C' : row.polarizationLevel > 6 ? '#E6A23C' : '#67C23A'"
            ></el-progress>
          </template>
        </el-table-column>
        <el-table-column prop="date" label="发生日期" width="120"></el-table-column>
        <el-table-column label="操作" width="120">
          <template #default="{ row }">
            <el-button type="primary" link>详情分析</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<style scoped>
.chart-container {
  height: 350px;
}
</style>