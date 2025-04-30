<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import * as echarts from 'echarts'
// 引入词云图扩展
import 'echarts-wordcloud'
import { DataAnalysis, TrendCharts, AlarmClock, Share, View, Pointer } from '@element-plus/icons-vue'

const route = useRoute()
const eventId = computed(() => Number(route.params.id))

// 深度分析模态框
const analysisDialogVisible = ref(false)
const analysisLoading = ref(false)
const analysisResult = ref('')

// 事件详情数据
const eventDetail = ref({
  id: 1,
  title: '某科技公司CEO涉嫌违规交易',
  category: '科技',
  date: '2025-04-25',
  source: '新浪微博',
  commentCount: 25631,
  polarizationLevel: 8.7,
  hotLevel: 9.2,
  description: '某科技公司CEO被曝出涉嫌内幕交易，引发公众对企业道德和监管制度的激烈讨论。相关话题在社交媒体上迅速发酵，形成明显的群体极化现象，支持者认为这是商业竞争中的正常行为被过度解读，反对者则严厉谴责这种行为并呼吁加强监管。',
  keywords: ['科技公司', 'CEO', '违规交易', '企业道德', '监管']
})

// 深度分析函数
function handleDeepAnalysis() {
  analysisDialogVisible.value = true
  analysisLoading.value = true
  
  // 模拟API请求延迟
  setTimeout(() => {
    analysisLoading.value = false
    analysisResult.value = `
      <h3 class="text-xl font-bold mb-4">事件深度分析报告</h3>
      
      <div class="mb-4">
        <p class="font-bold">事件概述：</p>
        <p>某科技公司CEO涉嫌违规交易事件在社交媒体上引起广泛讨论，形成明显的群体极化现象。</p>
      </div>
      
      <div class="mb-4">
        <p class="font-bold">极化指数分析：</p>
        <p>该事件极化指数为8.7（满分10分），属于高度极化事件。主要表现为支持与反对意见明显对立，缺乏中间立场的讨论。</p>
      </div>
      
      <div class="mb-4">
        <p class="font-bold">极化原因：</p>
        <ul class="list-disc pl-5">
          <li>信息不对称：公众对内幕交易相关法规了解有限</li>
          <li>价值观冲突：对商业道德与个人利益的不同理解</li>
          <li>回音室效应：社交媒体算法推荐相似观点，加剧立场固化</li>
          <li>意见领袖影响：知名财经分析师对事件的截然不同解读</li>
        </ul>
      </div>
      
      <div class="mb-4">
        <p class="font-bold">发展趋势预测：</p>
        <p>根据历史相似案例分析，该事件极化程度预计将在未来3-5天达到峰值，随后随着官方调查结果公布可能出现观点收敛。</p>
      </div>
      
      <div>
        <p class="font-bold">干预建议：</p>
        <ul class="list-disc pl-5">
          <li>发布权威解读，澄清事实与法规边界</li>
          <li>鼓励多元观点表达，打破信息茧房</li>
          <li>引导理性讨论，降低情绪化表达</li>
        </ul>
      </div>
    `
  }, 1500)
}

// 评论数据
const commentsData = ref([
  { id: 1, content: '这明显是违法行为，应该严惩不贷！', sentiment: -0.8, date: '2025-04-25 09:12:34', likes: 256 },
  { id: 2, content: '媒体又在炒作，根本没有实际证据。', sentiment: -0.5, date: '2025-04-25 09:15:21', likes: 123 },
  { id: 3, content: '这种行为严重影响了市场公平，应该加强监管。', sentiment: -0.7, date: '2025-04-25 09:18:56', likes: 189 },
  { id: 4, content: '看看竞争对手背后有没有推动这个消息。', sentiment: -0.4, date: '2025-04-25 09:22:13', likes: 87 },
  { id: 5, content: '这家公司的产品我一直很喜欢，希望不是真的。', sentiment: 0.2, date: '2025-04-25 09:35:42', likes: 156 }
])

// 图表实例
let polarizationTrendChart: echarts.ECharts | null = null
let sentimentDistributionChart: echarts.ECharts | null = null
let commentNetworkChart: echarts.ECharts | null = null
let keywordCloudChart: echarts.ECharts | null = null

onMounted(() => {
  // 根据ID加载对应事件数据
  if (eventId.value !== 1) {
    // 这里应该调用API获取真实数据，现在我们模拟一下
    eventDetail.value.id = eventId.value
    eventDetail.value.title = `事件ID: ${eventId.value} 的详情`
  }
  
  // 初始化各图表
  initPolarizationTrendChart()
  initSentimentDistributionChart()
  initCommentNetworkChart()
  initKeywordCloudChart()
  
  // 监听窗口大小变化，调整图表尺寸
  window.addEventListener('resize', () => {
    polarizationTrendChart?.resize()
    sentimentDistributionChart?.resize()
    commentNetworkChart?.resize()
    keywordCloudChart?.resize()
  })
})

// 初始化极化趋势图
function initPolarizationTrendChart() {
  const chartDom = document.getElementById('polarization-trend-chart')
  if (!chartDom) return
  
  polarizationTrendChart = echarts.init(chartDom)
  
  const dates = Array.from({ length: 7 }, (_, i) => {
    const date = new Date('2025-04-25')
    date.setDate(date.getDate() - i)
    return `${date.getMonth() + 1}/${date.getDate()}`
  }).reverse()
  
  const option = {
    title: {
      text: '事件极化趋势',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    legend: {
      data: ['支持观点', '反对观点', '极化指数'],
      bottom: 10
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',
      top: '15%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: dates
    },
    yAxis: [
      {
        type: 'value',
        name: '评论数',
        min: 0,
        max: 12000
      },
      {
        type: 'value',
        name: '极化指数',
        min: 0,
        max: 10,
        splitLine: {
          show: false
        }
      }
    ],
    series: [
      {
        name: '支持观点',
        type: 'bar',
        stack: 'viewpoint',
        emphasis: {
          focus: 'series'
        },
        data: [2500, 3100, 5200, 7800, 9400, 8200, 7500]
      },
      {
        name: '反对观点',
        type: 'bar',
        stack: 'viewpoint',
        emphasis: {
          focus: 'series'
        },
        data: [1800, 2200, 4800, 6500, 8600, 7400, 6800]
      },
      {
        name: '极化指数',
        type: 'line',
        yAxisIndex: 1,
        smooth: true,
        lineStyle: {
          width: 3,
          color: '#FF6B3D'
        },
        itemStyle: {
          color: '#FF6B3D'
        },
        data: [5.2, 5.8, 6.7, 7.5, 8.3, 8.7, 8.5]
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
      text: '评论情感分布',
      left: 'center'
    },
    tooltip: {
      trigger: 'item'
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      top: 'center'
    },
    series: [
      {
        name: '情感倾向',
        type: 'pie',
        radius: ['40%', '70%'],
        center: ['50%', '60%'],
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
        data: [
          { value: 39, name: '积极', itemStyle: { color: '#67C23A' } },
          { value: 48, name: '消极', itemStyle: { color: '#F56C6C' } },
          { value: 13, name: '中性', itemStyle: { color: '#909399' } }
        ]
      }
    ]
  }
  
  sentimentDistributionChart.setOption(option)
}

// 初始化评论网络图
function initCommentNetworkChart() {
  const chartDom = document.getElementById('comment-network-chart')
  if (!chartDom) return
  
  commentNetworkChart = echarts.init(chartDom)
  
  // 生成模拟的网络数据
  const nodes = []
  const links = []
  const categories = ['支持', '反对', '中立']
  
  // 添加节点
  for (let i = 0; i < 50; i++) {
    const category = Math.floor(Math.random() * 3)
    nodes.push({
      id: i,
      name: `用户${i}`,
      symbolSize: Math.random() * 20 + 10,
      category,
      value: Math.floor(Math.random() * 100)
    })
  }
  
  // 添加连接
  for (let i = 0; i < 80; i++) {
    const source = Math.floor(Math.random() * 50)
    let target = Math.floor(Math.random() * 50)
    while (target === source) {
      target = Math.floor(Math.random() * 50)
    }
    links.push({
      source,
      target
    })
  }
  
  const option = {
    title: {
      text: '评论互动网络',
      left: 'center'
    },
    tooltip: {},
    legend: [
      {
        data: categories.map(name => ({ name })),
        bottom: 10
      }
    ],
    animationDuration: 1500,
    series: [
      {
        name: '评论网络',
        type: 'graph',
        layout: 'force',
        data: nodes,
        links: links,
        categories: categories.map(name => ({ name })),
        roam: true,
        label: {
          show: false,
          position: 'right'
        },
        force: {
          repulsion: 100,
          edgeLength: 30
        },
        lineStyle: {
          color: 'source',
          curveness: 0.3
        },
        emphasis: {
          focus: 'adjacency',
          lineStyle: {
            width: 4
          }
        }
      }
    ]
  }
  
  commentNetworkChart.setOption(option)
}

// 初始化关键词云图
function initKeywordCloudChart() {
  const chartDom = document.getElementById('keyword-cloud-chart')
  if (!chartDom) return
  
  keywordCloudChart = echarts.init(chartDom)
  
  const keywords = [
    { name: '违规交易', value: 100 },
    { name: '科技公司', value: 85 },
    { name: 'CEO', value: 80 },
    { name: '监管', value: 75 },
    { name: '股价', value: 70 },
    { name: '内幕消息', value: 65 },
    { name: '投资者', value: 60 },
    { name: '企业责任', value: 55 },
    { name: '商业道德', value: 50 },
    { name: '市场反应', value: 45 },
    { name: '媒体报道', value: 40 },
    { name: '法律制裁', value: 35 },
    { name: '公众舆论', value: 30 },
    { name: '股东利益', value: 25 },
    { name: '信息披露', value: 20 }
  ]
  
  const option = {
    title: {
      text: '事件关键词云',
      left: 'center'
    },
    tooltip: {
      show: true
    },
    series: [
      {
        type: 'wordCloud',
        shape: 'circle',
        left: 'center',
        top: 'center',
        width: '90%',
        height: '80%',
        right: null,
        bottom: null,
        sizeRange: [12, 60],
        rotationRange: [-90, 90],
        rotationStep: 45,
        gridSize: 8,
        drawOutOfBound: false,
        textStyle: {
          fontFamily: 'sans-serif',
          fontWeight: 'bold',
          color: function () {
            return 'rgb(' + [
              Math.round(Math.random() * 160 + 80),
              Math.round(Math.random() * 160 + 80),
              Math.round(Math.random() * 160 + 80)
            ].join(',') + ')'
          }
        },
        emphasis: {
          focus: 'self',
          textStyle: {
            shadowBlur: 10,
            shadowColor: '#333'
          }
        },
        data: keywords
      }
    ]
  }
  
  keywordCloudChart.setOption(option)
}

// 获取极化程度标签颜色
function getPolarizationColor(level: number): string {
  if (level >= 8) return 'danger'
  if (level >= 6) return 'warning'
  return 'success'
}

// 获取情感倾向颜色
function getSentimentColor(sentiment: number): string {
  if (sentiment >= 0.3) return 'success'
  if (sentiment <= -0.3) return 'danger'
  return 'info'
}
</script>

<template>
  <div class="event-detail-container w-full">
    <!-- 事件概况 -->
    <el-card class="mb-6" :class="{ 'dark:bg-dark-light': true }">
      <div class="flex flex-col lg:flex-row justify-between">
        <div class="event-info flex-1">
          <div class="flex items-center mb-4">
            <h1 class="text-2xl font-bold mr-4">{{ eventDetail.title }}</h1>
            <el-tag class="mr-2">{{ eventDetail.category }}</el-tag>
            <el-tag 
              :type="getPolarizationColor(eventDetail.polarizationLevel)" 
              effect="dark"
              class="flex items-center"
            >
              极化指数: {{ eventDetail.polarizationLevel.toFixed(1) }}
            </el-tag>
          </div>
          
          <div class="mb-4 text-gray-700 dark:text-gray-300">
            <div><strong>发生时间:</strong> {{ eventDetail.date }}</div>
            <div><strong>数据来源:</strong> {{ eventDetail.source }}</div>
            <div><strong>评论数量:</strong> {{ eventDetail.commentCount.toLocaleString() }}</div>
          </div>
          
          <div class="mb-4">
            <div class="text-gray-700 dark:text-gray-300">{{ eventDetail.description }}</div>
          </div>
          
          <div class="flex flex-wrap">
            <el-tag 
              v-for="(keyword, index) in eventDetail.keywords" 
              :key="index"
              class="mr-2 mb-2"
              effect="plain"
            >
              {{ keyword }}
            </el-tag>
          </div>
        </div>
        
        <div class="action-panel mt-4 lg:mt-0 lg:ml-6 flex flex-col lg:flex-row lg:flex-col justify-center gap-3">
          <el-button type="primary" size="large" @click="handleDeepAnalysis">
            <el-icon><DataAnalysis /></el-icon>深度分析
          </el-button>
          <el-button type="success" size="large">
            <el-icon><TrendCharts /></el-icon>预测趋势
          </el-button>
          <el-button type="warning" size="large">
            <el-icon><AlarmClock /></el-icon>设置监控
          </el-button>
          <el-button size="large">
            <el-icon><Share /></el-icon>分享
          </el-button>
        </div>
      </div>
    </el-card>
    
    <!-- 分析图表区域 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
      <!-- 极化趋势图 -->
      <el-card class="chart-card" :class="{ 'dark:bg-dark-light': true }">
        <div id="polarization-trend-chart" class="chart-container"></div>
      </el-card>
      
      <!-- 情感分布图 -->
      <el-card class="chart-card" :class="{ 'dark:bg-dark-light': true }">
        <div id="sentiment-distribution-chart" class="chart-container"></div>
      </el-card>
      
      <!-- 评论网络图 -->
      <el-card class="chart-card" :class="{ 'dark:bg-dark-light': true }">
        <div id="comment-network-chart" class="chart-container"></div>
      </el-card>
      
      <!-- 关键词云图 -->
      <el-card class="chart-card" :class="{ 'dark:bg-dark-light': true }">
        <div id="keyword-cloud-chart" class="chart-container"></div>
      </el-card>
    </div>
    
    <!-- 评论列表 -->
    <el-card class="comments-card" :class="{ 'dark:bg-dark-light': true }">
      <template #header>
        <div class="flex justify-between items-center">
          <span class="text-lg font-bold">热门评论</span>
          <el-button type="primary" text>
            <el-icon><View /></el-icon>查看全部评论
          </el-button>
        </div>
      </template>
      
      <div class="comments-list">
        <div 
          v-for="comment in commentsData" 
          :key="comment.id"
          class="comment-item p-4 border-b dark:border-gray-700 last:border-0"
        >
          <div class="flex justify-between items-start mb-2">
            <div class="flex items-center">
              <el-avatar size="small" class="mr-2">用户</el-avatar>
              <span class="text-gray-500 dark:text-gray-400 text-sm">{{ comment.date }}</span>
            </div>
            <el-tag :type="getSentimentColor(comment.sentiment)" size="small">
              情感值: {{ comment.sentiment.toFixed(1) }}
            </el-tag>
          </div>
          <div class="comment-content mb-2">{{ comment.content }}</div>
          <div class="flex items-center text-gray-500 dark:text-gray-400 text-sm">
            <el-icon class="mr-1"><Pointer /></el-icon>
            <span>{{ comment.likes }}</span>
          </div>
        </div>
      </div>
    </el-card>

    <!-- 深度分析模态框 -->
    <el-dialog
      v-model="analysisDialogVisible"
      title="事件深度分析"
      width="650px"
      :destroy-on-close="true"
      class="analysis-dialog"
    >
      <div v-if="analysisLoading" class="flex justify-center items-center py-10">
        <el-loading :fullscreen="false" />
        <div class="mt-3 text-center text-gray-600">分析中，请稍候...</div>
      </div>
      <div v-else class="analysis-content" v-html="analysisResult"></div>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="analysisDialogVisible = false">关闭</el-button>
          <el-button type="primary" @click="analysisDialogVisible = false">
            导出报告
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.event-detail-container {
  width: 100%;
}

.chart-container {
  height: 350px;
}

.action-panel {
  min-width: 160px;
}

/* 修复按钮图标间距 */
.el-button .el-icon {
  margin-right: 4px;
}

/* 深度分析模态框样式 */
.analysis-dialog {
  max-width: 90vw;
}

.analysis-content {
  max-height: 60vh;
  overflow-y: auto;
  padding: 0 10px;
}

:deep(.analysis-content ul) {
  margin-bottom: 10px;
}

:deep(.analysis-content li) {
  margin-bottom: 5px;
}
</style> 