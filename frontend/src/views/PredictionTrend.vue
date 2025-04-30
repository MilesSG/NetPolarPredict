<script setup lang="ts">
import { ref, reactive, onMounted, watch, nextTick, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import * as echarts from 'echarts'
import { ElMessage } from 'element-plus'

// 添加调试日志
console.log('PredictionTrend组件被加载')

const route = useRoute()

// 预测模型选项
const modelOptions = [
  { value: 'lstm', label: 'LSTM神经网络' },
  { value: 'gru', label: 'GRU循环神经网络' },
  { value: 'transformer', label: 'Transformer注意力模型' },
  { value: 'ensemble', label: '集成学习模型' }
]

// 当前选择的模型
const currentModel = ref('lstm')

// 预测设置表单
const predictionSettings = reactive({
  eventId: '',
  timeWindow: 7,
  includeHistorical: true,
  includeRelatedEvents: true,
  confidenceInterval: 0.95
})

// 事件选项
const eventOptions = [
  { value: '1', label: '某科技公司CEO涉嫌违规交易' },
  { value: '2', label: '新冠疫苗接种争议' },
  { value: '3', label: '国际贸易政策调整' },
  { value: '4', label: '教育改革新政策实施' },
  { value: '5', label: '环保抗议活动在全国蔓延' }
]

// 从URL参数获取事件ID
watch(() => route.query.eventId, (newEventId) => {
  if (newEventId) {
    predictionSettings.eventId = newEventId as string
    // 如果已经加载了页面，可以触发预测
    if (predictionChart) {
      runPrediction()
    }
  }
}, { immediate: true })

// 图表实例
let predictionChart: echarts.ECharts | null = null
let factorsChart: echarts.ECharts | null = null
let uncertaintyChart: echarts.ECharts | null = null
let comparativeChart: echarts.ECharts | null = null

// 预测状态
const isPredicting = ref(false)
const predictionComplete = ref(false)
const predictionProgress = ref(0)

// 预测结果
const predictionResult = reactive({
  baselinePolarization: 8.2,
  predictedPolarization: 9.4,
  trend: 'increasing',
  certainty: 0.87,
  timeToStabilize: 14,
  keyFactors: [
    { name: '媒体报道强度', value: 0.35 },
    { name: '意见领袖影响', value: 0.25 },
    { name: '事件严重性', value: 0.18 },
    { name: '社交媒体讨论热度', value: 0.15 },
    { name: '官方回应', value: 0.07 }
  ]
})

onMounted(() => {
  console.log('PredictionTrend组件已挂载')
  
  // 给DOM一点时间渲染
  setTimeout(() => {
    console.log('开始初始化图表')
    try {
      initPredictionChart()
      initFactorsChart()
      initUncertaintyChart()
      initComparativeChart()
      console.log('图表初始化完成')
    } catch (error) {
      console.error('图表初始化失败:', error)
    }
    
    // 如果URL中有事件ID，自动运行预测
    if (route.query.eventId) {
      console.log('检测到事件ID:', route.query.eventId)
      predictionSettings.eventId = route.query.eventId as string
      runPrediction()
    }
  }, 300)
  
  // 监听窗口大小变化
  window.addEventListener('resize', handleResize)
})

// 单独的resize处理函数
function handleResize() {
  console.log('窗口大小改变，重新调整图表大小')
  if (predictionChart) predictionChart.resize()
  if (factorsChart) factorsChart.resize()
  if (uncertaintyChart) uncertaintyChart.resize()
  if (comparativeChart) comparativeChart.resize()
}

// 初始化预测趋势图
function initPredictionChart() {
  console.log('初始化预测趋势图')
  const chartDom = document.getElementById('prediction-chart')
  if (!chartDom) {
    console.error('找不到prediction-chart元素')
    return
  }
  
  console.log('预测图表DOM元素尺寸:', chartDom.offsetWidth, chartDom.offsetHeight)
  
  if (predictionChart) {
    predictionChart.dispose()
  }
  
  predictionChart = echarts.init(chartDom)
  
  // 生成历史数据和预测数据
  const dates = []
  const historicalData = []
  const predictionData = []
  const confidenceUpper = []
  const confidenceLower = []
  
  // 过去30天的历史数据
  for (let i = 30; i >= 1; i--) {
    const date = new Date()
    date.setDate(date.getDate() - i)
    dates.push(`${date.getMonth() + 1}/${date.getDate()}`)
    
    // 生成波动的历史极化数据
    const baseValue = 6 + Math.sin(i / 5) * 1.5
    const randomNoise = Math.random() * 0.5
    historicalData.push(+(baseValue + randomNoise).toFixed(1))
    
    predictionData.push(null)
    confidenceUpper.push(null)
    confidenceLower.push(null)
  }
  
  // 今天
  const today = new Date()
  dates.push(`${today.getMonth() + 1}/${today.getDate()}`)
  historicalData.push(8.2) // 今天的极化指数
  predictionData.push(8.2)
  confidenceUpper.push(8.2)
  confidenceLower.push(8.2)
  
  // 未来14天的预测数据
  for (let i = 1; i <= 14; i++) {
    const date = new Date()
    date.setDate(date.getDate() + i)
    dates.push(`${date.getMonth() + 1}/${date.getDate()}`)
    
    historicalData.push(null)
    
    // 生成预测数据，呈现上升趋势后平稳
    const predValue = 8.2 + (i <= 7 ? i * 0.17 : 7 * 0.17 + (i - 7) * 0.05)
    const finalValue = Math.min(predValue, 9.4)
    predictionData.push(+finalValue.toFixed(1))
    
    // 生成置信区间，随时间增加变宽
    const confidence = 0.2 + i * 0.05
    confidenceUpper.push(+(finalValue + confidence).toFixed(1))
    confidenceLower.push(+(finalValue - confidence).toFixed(1))
  }
  
  const option = {
    title: {
      text: '群体极化趋势预测',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross'
      }
    },
    legend: {
      data: ['历史数据', '预测趋势', '置信区间'],
      bottom: 10
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: dates,
      axisLabel: {
        rotate: 45,
        interval: 5
      }
    },
    yAxis: {
      type: 'value',
      name: '极化指数',
      min: 5,
      max: 10
    },
    series: [
      {
        name: '历史数据',
        type: 'line',
        data: historicalData,
        symbolSize: 6,
        lineStyle: {
          width: 3
        },
        itemStyle: {
          color: '#5470C6'
        }
      },
      {
        name: '预测趋势',
        type: 'line',
        data: predictionData,
        symbolSize: 6,
        lineStyle: {
          width: 3,
          type: 'dashed'
        },
        itemStyle: {
          color: '#FF6B3D'
        }
      },
      {
        name: '置信区间',
        type: 'line',
        data: confidenceUpper,
        lineStyle: {
          opacity: 0
        },
        stack: 'confidence',
        symbol: 'none'
      },
      {
        name: '置信区间',
        type: 'line',
        data: confidenceLower,
        lineStyle: {
          opacity: 0
        },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(255, 107, 61, 0.3)' },
            { offset: 1, color: 'rgba(255, 107, 61, 0.1)' }
          ])
        },
        stack: 'confidence',
        symbol: 'none'
      }
    ],
    visualMap: {
      show: false,
      type: 'continuous',
      seriesIndex: 1,
      min: 0,
      max: 14,
      inRange: {
        color: ['#FF6B3D', '#e74c3c']
      }
    }
  }
  
  try {
    predictionChart.setOption(option)
    console.log('预测图表设置选项成功')
    setTimeout(() => {
      if (predictionChart) {
        predictionChart.resize()
        console.log('预测图表调整大小完成')
      }
    }, 200)
  } catch (error) {
    console.error('设置预测图表选项失败:', error)
  }
}

// 初始化关键因素图
function initFactorsChart() {
  const chartDom = document.getElementById('factors-chart')
  if (!chartDom) {
    console.error('找不到factors-chart元素')
    return
  }
  
  if (factorsChart) {
    factorsChart.dispose()
  }
  
  factorsChart = echarts.init(chartDom)
  
  const option = {
    title: {
      text: '极化影响因素分析',
      left: 'center'
    },
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    series: [
      {
        name: '影响因素',
        type: 'pie',
        radius: '60%',
        center: ['50%', '60%'],
        data: predictionResult.keyFactors.map(factor => ({
          name: factor.name,
          value: factor.value
        })),
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        },
        label: {
          formatter: '{b}: {d}%'
        }
      }
    ]
  }
  
  factorsChart.setOption(option)
  setTimeout(() => {
    factorsChart.resize()
  }, 200)
}

// 初始化不确定性分析图
function initUncertaintyChart() {
  const chartDom = document.getElementById('uncertainty-chart')
  if (!chartDom) {
    console.error('找不到uncertainty-chart元素')
    return
  }
  
  if (uncertaintyChart) {
    uncertaintyChart.dispose()
  }
  
  uncertaintyChart = echarts.init(chartDom)
  
  const option = {
    title: {
      text: '预测不确定性分析',
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
      data: ['70%', '80%', '90%', '95%', '99%'],
      axisTick: {
        alignWithLabel: true
      }
    },
    yAxis: {
      type: 'value',
      name: '极化指数范围'
    },
    series: [
      {
        name: '置信区间',
        type: 'bar',
        barWidth: '60%',
        data: [
          { value: 0.6, itemStyle: { color: '#91cc75' } },
          { value: 0.8, itemStyle: { color: '#5470c6' } },
          { value: 1.2, itemStyle: { color: '#fac858' } },
          { value: 1.5, itemStyle: { color: '#ee6666' } },
          { value: 2.0, itemStyle: { color: '#73c0de' } }
        ]
      }
    ]
  }
  
  uncertaintyChart.setOption(option)
  setTimeout(() => {
    uncertaintyChart.resize()
  }, 200)
}

// 初始化比较分析图
function initComparativeChart() {
  const chartDom = document.getElementById('comparative-chart')
  if (!chartDom) {
    console.error('找不到comparative-chart元素')
    return
  }
  
  if (comparativeChart) {
    comparativeChart.dispose()
  }
  
  comparativeChart = echarts.init(chartDom)
  
  const option = {
    title: {
      text: '不同事件极化趋势比较',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      data: ['当前事件', '事件A (医疗类)', '事件B (政治类)', '事件C (环境类)'],
      bottom: 10
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: ['第1天', '第3天', '第5天', '第7天', '第9天', '第11天', '第14天']
    },
    yAxis: {
      type: 'value',
      name: '极化指数',
      min: 5,
      max: 10
    },
    series: [
      {
        name: '当前事件',
        type: 'line',
        lineStyle: { width: 3 },
        emphasis: { focus: 'series' },
        data: [8.2, 8.5, 8.8, 9.1, 9.3, 9.4, 9.4]
      },
      {
        name: '事件A (医疗类)',
        type: 'line',
        lineStyle: { width: 2 },
        emphasis: { focus: 'series' },
        data: [7.5, 8.3, 9.0, 9.3, 9.5, 9.6, 9.6]
      },
      {
        name: '事件B (政治类)',
        type: 'line',
        lineStyle: { width: 2 },
        emphasis: { focus: 'series' },
        data: [8.4, 8.6, 8.8, 8.9, 9.0, 9.0, 9.0]
      },
      {
        name: '事件C (环境类)',
        type: 'line',
        lineStyle: { width: 2 },
        emphasis: { focus: 'series' },
        data: [7.0, 7.6, 8.0, 8.2, 8.3, 8.3, 8.2]
      }
    ]
  }
  
  comparativeChart.setOption(option)
  setTimeout(() => {
    comparativeChart.resize()
  }, 200)
}

// 运行预测
function runPrediction() {
  if (!predictionSettings.eventId) {
    // 如果没有选择事件，显示提示
    ElMessage.warning('请先选择要预测的事件')
    return
  }
  
  isPredicting.value = true
  predictionComplete.value = false
  predictionProgress.value = 0
  
  // 模拟预测过程
  const interval = setInterval(() => {
    predictionProgress.value += 10
    if (predictionProgress.value >= 100) {
      clearInterval(interval)
      isPredicting.value = false
      predictionComplete.value = true
      
      // 更新图表数据
      updateCharts()
    }
  }, 300)
}

// 获取趋势标签
function getTrendLabel(trend: string): string {
  switch (trend) {
    case 'increasing':
      return '上升'
    case 'decreasing':
      return '下降'
    case 'stable':
      return '稳定'
    default:
      return '未知'
  }
}

// 更新图表数据
function updateCharts() {
  // 延迟一点执行，确保DOM已经渲染
  setTimeout(() => {
    // 重新初始化图表以显示预测结果
    initPredictionChart()
    initFactorsChart()
    initUncertaintyChart()
    initComparativeChart()
  }, 50)
}

// 组件销毁时清理图表实例
onUnmounted(() => {
  console.log('PredictionTrend组件将卸载，清理资源')
  window.removeEventListener('resize', handleResize)
  
  if (predictionChart) {
    predictionChart.dispose()
    predictionChart = null
  }
  if (factorsChart) {
    factorsChart.dispose()
    factorsChart = null
  }
  if (uncertaintyChart) {
    uncertaintyChart.dispose()
    uncertaintyChart = null
  }
  if (comparativeChart) {
    comparativeChart.dispose()
    comparativeChart = null
  }
})
</script>

<template>
  <div class="prediction-trend-container w-full">
    <div class="prediction-trend">
      <!-- 预测设置区域 -->
      <el-card class="mb-6 settings-card" :class="{ 'dark:bg-dark-light': true }">
        <template #header>
          <div class="flex justify-between items-center">
            <span class="text-lg font-bold">极化趋势预测配置</span>
            <div class="flex items-center">
              <span class="mr-2">预测模型:</span>
              <el-select v-model="currentModel" class="w-60">
                <el-option
                  v-for="option in modelOptions"
                  :key="option.value"
                  :label="option.label"
                  :value="option.value"
                ></el-option>
              </el-select>
            </div>
          </div>
        </template>
        
        <el-form :model="predictionSettings" label-width="120px" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <el-form-item label="事件选择:">
            <el-select v-model="predictionSettings.eventId" placeholder="选择事件" class="w-full">
              <el-option
                v-for="option in eventOptions"
                :key="option.value"
                :label="option.label"
                :value="option.value"
              ></el-option>
            </el-select>
          </el-form-item>
          
          <el-form-item label="预测时间窗口:">
            <div class="slider-with-labels">
              <el-slider
                v-model="predictionSettings.timeWindow"
                :min="3"
                :max="30"
                :step="1"
                :format-tooltip="(val) => `${val}天`"
                show-stops
                :marks="{3: '3天', 7: '7天', 14: '14天', 30: '30天'}"
              ></el-slider>
            </div>
          </el-form-item>
          
          <el-form-item label="置信区间:">
            <el-select v-model="predictionSettings.confidenceInterval" class="w-full">
              <el-option :value="0.9" label="90%"></el-option>
              <el-option :value="0.95" label="95%"></el-option>
              <el-option :value="0.99" label="99%"></el-option>
            </el-select>
          </el-form-item>
          
          <el-form-item label="包含历史数据:">
            <el-switch 
              v-model="predictionSettings.includeHistorical"
              active-text="开启"
              inactive-text="关闭"
              inline-prompt
            ></el-switch>
          </el-form-item>
          
          <el-form-item label="包含相关事件:">
            <el-switch 
              v-model="predictionSettings.includeRelatedEvents"
              active-text="开启"
              inactive-text="关闭"
              inline-prompt
            ></el-switch>
          </el-form-item>
        </el-form>
        
        <div class="flex justify-center mt-6">
          <el-button type="primary" size="large" @click="runPrediction" :loading="isPredicting" class="w-40">
            运行预测
          </el-button>
        </div>
        
        <!-- 预测进度条 -->
        <div v-if="isPredicting" class="mt-4">
          <div class="text-center mb-2">正在运行预测分析...</div>
          <el-progress :percentage="predictionProgress" :format="(p) => `${p}%`" :stroke-width="20"></el-progress>
        </div>
      </el-card>
      
      <!-- 预测结果区域 -->
      <template v-if="predictionComplete">
        <!-- 预测结果概述 -->
        <el-card class="mb-6 result-summary-card" :class="{ 'dark:bg-dark-light': true }">
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div class="result-item">
              <div class="text-gray-500 dark:text-gray-400 mb-1">当前极化指数</div>
              <div class="text-3xl font-bold">{{ predictionResult.baselinePolarization.toFixed(1) }}</div>
            </div>
            
            <div class="result-item">
              <div class="text-gray-500 dark:text-gray-400 mb-1">预测极化峰值</div>
              <div class="text-3xl font-bold text-red-500">{{ predictionResult.predictedPolarization.toFixed(1) }}</div>
            </div>
            
            <div class="result-item">
              <div class="text-gray-500 dark:text-gray-400 mb-1">预测趋势</div>
              <div class="flex items-center">
                <span class="text-xl font-bold mr-2">{{ getTrendLabel(predictionResult.trend) }}</span>
                <el-icon color="#F56C6C" v-if="predictionResult.trend === 'increasing'"><ArrowUp /></el-icon>
                <el-icon color="#67C23A" v-else-if="predictionResult.trend === 'decreasing'"><ArrowDown /></el-icon>
                <el-icon color="#909399" v-else><DArrowRight /></el-icon>
              </div>
            </div>
            
            <div class="result-item">
              <div class="text-gray-500 dark:text-gray-400 mb-1">预计稳定时间</div>
              <div class="text-xl font-bold">{{ predictionResult.timeToStabilize }} 天</div>
            </div>
          </div>
        </el-card>
        
        <!-- 预测图表区域 -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          <!-- 趋势预测图 -->
          <el-card class="chart-card" :class="{ 'dark:bg-dark-light': true }">
            <div id="prediction-chart" class="chart-container"></div>
          </el-card>
          
          <!-- 影响因素图 -->
          <el-card class="chart-card" :class="{ 'dark:bg-dark-light': true }">
            <div id="factors-chart" class="chart-container"></div>
          </el-card>
          
          <!-- 不确定性分析图 -->
          <el-card class="chart-card" :class="{ 'dark:bg-dark-light': true }">
            <div id="uncertainty-chart" class="chart-container"></div>
          </el-card>
          
          <!-- 比较分析图 -->
          <el-card class="chart-card" :class="{ 'dark:bg-dark-light': true }">
            <div id="comparative-chart" class="chart-container"></div>
          </el-card>
        </div>
        
        <!-- 预测分析报告 -->
        <el-card class="prediction-report-card" :class="{ 'dark:bg-dark-light': true }">
          <template #header>
            <div class="flex justify-between items-center">
              <span class="text-lg font-bold">预测分析报告</span>
              <div>
                <el-button type="primary" icon="Printer" plain class="mr-2">打印报告</el-button>
                <el-button type="success" icon="Download" plain>导出数据</el-button>
              </div>
            </div>
          </template>
          
          <div class="report-content">
            <h3 class="text-xl font-bold mb-4">分析结论</h3>
            <p class="mb-6 text-gray-700 dark:text-gray-300">
              根据LSTM神经网络模型的预测结果，该事件的群体极化程度将在未来7天内继续上升，从当前的8.2上升到9.4，并在两周后趋于稳定。预测的可信度为87%，主要影响因素包括媒体报道强度和意见领袖的影响。
            </p>
            
            <h3 class="text-xl font-bold mb-4">风险评估</h3>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              <el-card shadow="hover" class="risk-card bg-red-50 dark:bg-red-900/20">
                <h4 class="text-lg font-bold mb-2 text-red-600 dark:text-red-400">高风险因素</h4>
                <ul class="list-disc pl-5 text-gray-700 dark:text-gray-300">
                  <li>社交媒体持续发酵</li>
                  <li>相关利益方积极介入</li>
                  <li>信息来源高度分化</li>
                </ul>
              </el-card>
              
              <el-card shadow="hover" class="risk-card bg-yellow-50 dark:bg-yellow-900/20">
                <h4 class="text-lg font-bold mb-2 text-yellow-600 dark:text-yellow-400">中度风险因素</h4>
                <ul class="list-disc pl-5 text-gray-700 dark:text-gray-300">
                  <li>事件本身的模糊性</li>
                  <li>官方回应不及时</li>
                  <li>相关政策不明确</li>
                </ul>
              </el-card>
              
              <el-card shadow="hover" class="risk-card bg-green-50 dark:bg-green-900/20">
                <h4 class="text-lg font-bold mb-2 text-green-600 dark:text-green-400">缓解因素</h4>
                <ul class="list-disc pl-5 text-gray-700 dark:text-gray-300">
                  <li>专家解读澄清事实</li>
                  <li>主流媒体客观报道</li>
                  <li>社会关注度逐渐转移</li>
                </ul>
              </el-card>
            </div>
            
            <h3 class="text-xl font-bold mb-4">干预建议</h3>
            <div class="mb-6 text-gray-700 dark:text-gray-300">
              <p class="mb-2">基于预测结果，建议采取以下干预措施来缓解群体极化现象：</p>
              <ol class="list-decimal pl-5">
                <li>加强信息透明度，及时发布官方权威信息</li>
                <li>鼓励多元化讨论，避免信息茧房效应</li>
                <li>邀请专业人士进行客观解读和分析</li>
                <li>密切监控极端言论，及时引导舆论走向</li>
                <li>建立跨平台统一的信息发布机制</li>
              </ol>
            </div>
          </div>
        </el-card>
      </template>
      
      <!-- 显示调试信息 -->
      <el-card v-if="!predictionComplete" class="debug-card mt-4">
        <h3 class="text-lg font-bold mb-2">调试信息</h3>
        <p>请设置参数并点击"运行预测"按钮来查看预测结果</p>
        <p>URL参数: {{ route.query }}</p>
        <p>当前事件ID: {{ predictionSettings.eventId }}</p>
        <p>当前预测状态: {{ isPredicting ? '预测中' : '未预测' }}</p>
      </el-card>
    </div>
  </div>
</template>

<style scoped>
.prediction-trend-container {
  width: 100%;
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 16px;
}

.prediction-trend {
  width: 100%;
}

.settings-card, 
.result-summary-card, 
.chart-card, 
.prediction-report-card,
.debug-card {
  transition: all 0.3s;
  width: 100%;
  margin-bottom: 20px;
}

.result-item {
  padding: 1rem;
  border-radius: 0.5rem;
  background-color: rgba(0, 0, 0, 0.03);
}

.dark .result-item {
  background-color: rgba(255, 255, 255, 0.05);
}

.risk-card {
  transition: all 0.3s;
}

.slider-with-labels {
  padding: 0 8px;
}

/* 修复开关组件的样式 */
.el-switch__label {
  color: var(--el-color-primary) !important;
}

.el-switch.is-checked .el-switch__core {
  border-color: var(--el-color-primary) !important;
  background-color: var(--el-color-primary) !important;
}

/* 确保内容正确显示 */
.chart-container {
  height: 350px;
  width: 100%;
  display: block;
  position: relative;
}

/* 修复居中问题，避免使用全局选择器 */
.el-main {
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* 确保表单元素宽度正确 */
.el-form-item {
  width: 100%;
}

.el-form-item__content {
  width: 100%;
}

/* 确保卡片内容居中 */
.el-card__body {
  width: 100%;
}
</style> 