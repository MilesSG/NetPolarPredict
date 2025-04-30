<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Search, RefreshRight, Plus, View, TrendCharts } from '@element-plus/icons-vue'

const router = useRouter()

interface Event {
  id: number
  title: string
  category: string
  date: string
  source: string
  commentCount: number
  polarizationLevel: number
  hotLevel: number
}

// 事件列表数据
const eventsList = ref<Event[]>([
  { 
    id: 1, 
    title: '某科技公司CEO涉嫌违规交易', 
    category: '科技', 
    date: '2025-04-25', 
    source: '新浪微博', 
    commentCount: 25631,
    polarizationLevel: 8.7, 
    hotLevel: 9.2
  },
  { 
    id: 2, 
    title: '新冠疫苗接种争议', 
    category: '医疗', 
    date: '2025-04-23', 
    source: '知乎', 
    commentCount: 38752,
    polarizationLevel: 9.2, 
    hotLevel: 9.8
  },
  { 
    id: 3, 
    title: '国际贸易政策调整', 
    category: '政治', 
    date: '2025-04-22', 
    source: '微信', 
    commentCount: 15329,
    polarizationLevel: 7.5, 
    hotLevel: 7.8
  },
  { 
    id: 4, 
    title: '教育改革新政策实施', 
    category: '教育', 
    date: '2025-04-20', 
    source: '抖音', 
    commentCount: 22436,
    polarizationLevel: 6.8, 
    hotLevel: 8.3
  },
  { 
    id: 5, 
    title: '环保抗议活动在全国蔓延', 
    category: '环境', 
    date: '2025-04-18', 
    source: '微博', 
    commentCount: 19827,
    polarizationLevel: 8.1, 
    hotLevel: 8.7
  },
  { 
    id: 6, 
    title: '某演员不当言论引发争议', 
    category: '娱乐', 
    date: '2025-04-16', 
    source: '微博', 
    commentCount: 52431,
    polarizationLevel: 8.9, 
    hotLevel: 9.5
  },
  { 
    id: 7, 
    title: '体育赛事裁判争议判罚', 
    category: '体育', 
    date: '2025-04-15', 
    source: '微博', 
    commentCount: 31276,
    polarizationLevel: 7.8, 
    hotLevel: 8.5
  },
  { 
    id: 8, 
    title: '新型智能手机发布会', 
    category: '科技', 
    date: '2025-04-12', 
    source: '微信', 
    commentCount: 18432,
    polarizationLevel: 5.6, 
    hotLevel: 8.2
  },
  { 
    id: 9, 
    title: '房地产市场调控政策', 
    category: '经济', 
    date: '2025-04-10', 
    source: '知乎', 
    commentCount: 27893,
    polarizationLevel: 7.3, 
    hotLevel: 8.0
  },
  { 
    id: 10, 
    title: '大型音乐节安全事故', 
    category: '文化', 
    date: '2025-04-08', 
    source: '抖音', 
    commentCount: 41583,
    polarizationLevel: 8.3, 
    hotLevel: 9.1
  }
])

// 获取颜色
function getPolarizationColor(level: number): string {
  if (level >= 8) return 'danger'
  if (level >= 6) return 'warning'
  return 'success'
}

function getHotLevelColor(level: number): string {
  if (level >= 9) return '#F56C6C'
  if (level >= 7) return '#E6A23C'
  return '#67C23A'
}

// 搜索表单
const searchForm = reactive({
  keyword: '',
  category: '',
  dateRange: null,
  polarizationLevel: [0, 10]
})

// 分类选项
const categoryOptions = [
  { value: '', label: '全部' },
  { value: '科技', label: '科技' },
  { value: '医疗', label: '医疗' },
  { value: '政治', label: '政治' },
  { value: '教育', label: '教育' },
  { value: '环境', label: '环境' },
  { value: '娱乐', label: '娱乐' },
  { value: '体育', label: '体育' },
  { value: '经济', label: '经济' },
  { value: '文化', label: '文化' }
]

// 查看事件详情
function viewEventDetail(eventId: number) {
  router.push(`/events/${eventId}`)
}

// 查看预测趋势
function viewPredictionTrend(eventId: number) {
  router.push({
    path: '/prediction',
    query: { eventId: eventId.toString() }
  })
}

// 添加新事件
function addNewEvent() {
  ElMessage.success('添加事件功能将在未来版本推出')
}

// 搜索事件
function searchEvents() {
  ElMessage.info('正在搜索匹配的事件...')
}

// 重置搜索
function resetSearch() {
  searchForm.keyword = ''
  searchForm.category = ''
  searchForm.dateRange = null
  searchForm.polarizationLevel = [0, 10]
  ElMessage.info('已重置搜索条件')
}

// 分页
const currentPage = ref(1)
const pageSize = ref(10)
</script>

<template>
  <div class="events-list-container w-full">
    <!-- 搜索区域 -->
    <el-card class="mb-6 search-card" :class="{ 'dark:bg-dark-light': true }">
      <el-form :model="searchForm" label-width="100px" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <el-form-item label="关键词:">
          <el-input v-model="searchForm.keyword" placeholder="搜索事件标题"></el-input>
        </el-form-item>
        
        <el-form-item label="分类:">
          <el-select v-model="searchForm.category" placeholder="选择分类" class="w-full">
            <el-option v-for="item in categoryOptions" :key="item.value" :label="item.label" :value="item.value"></el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="时间范围:">
          <el-date-picker 
            v-model="searchForm.dateRange" 
            type="daterange" 
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            class="w-full"
          ></el-date-picker>
        </el-form-item>
        
        <el-form-item label="极化程度:">
          <el-slider v-model="searchForm.polarizationLevel" range :min="0" :max="10" :step="0.1"></el-slider>
        </el-form-item>
      </el-form>
      
      <div class="flex justify-center mt-4">
        <el-button type="primary" class="w-32 mr-4" @click="searchEvents">
          <el-icon class="mr-1"><Search /></el-icon>搜索
        </el-button>
        <el-button class="w-32" @click="resetSearch">
          <el-icon class="mr-1"><RefreshRight /></el-icon>重置
        </el-button>
      </div>
    </el-card>
    
    <!-- 事件列表 -->
    <el-card class="events-table-card" :class="{ 'dark:bg-dark-light': true }">
      <template #header>
        <div class="flex justify-between items-center">
          <span class="text-lg font-bold">热点事件列表</span>
          <el-button type="primary" @click="addNewEvent">
            <el-icon class="mr-1"><Plus /></el-icon>添加事件
          </el-button>
        </div>
      </template>
      
      <el-table :data="eventsList" style="width: 100%" stripe :class="{ 'dark:bg-dark-light': true }">
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
        
        <el-table-column prop="date" label="发生日期" width="120"></el-table-column>
        
        <el-table-column prop="source" label="数据源" width="100"></el-table-column>
        
        <el-table-column prop="commentCount" label="评论数" width="110">
          <template #default="{ row }">
            {{ row.commentCount.toLocaleString() }}
          </template>
        </el-table-column>
        
        <el-table-column prop="polarizationLevel" label="极化程度" width="120">
          <template #default="{ row }">
            <el-tag :type="getPolarizationColor(row.polarizationLevel)" effect="dark">
              {{ row.polarizationLevel.toFixed(1) }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="hotLevel" label="热度指数" width="120">
          <template #default="{ row }">
            <el-progress 
              :percentage="row.hotLevel * 10" 
              :color="getHotLevelColor(row.hotLevel)"
              :format="(p) => (p/10).toFixed(1)"
            ></el-progress>
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="viewEventDetail(row.id)">
              <el-icon class="mr-1"><View /></el-icon>详情
            </el-button>
            <el-button type="success" size="small" @click="viewPredictionTrend(row.id)">
              <el-icon class="mr-1"><TrendCharts /></el-icon>预测
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="mt-4 flex justify-end">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          background
          layout="total, sizes, prev, pager, next, jumper"
          :total="eventsList.length"
        />
      </div>
    </el-card>
  </div>
</template>

<style scoped>
.events-list-container {
  width: 100%;
}

.search-card {
  transition: all 0.3s;
}

.el-button .el-icon {
  margin-right: 4px;
}

/* 确保操作按钮中的文本可见 */
.el-table-column--fixed-right .el-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.el-table-column--fixed-right .el-button .el-icon {
  margin-right: 4px;
}

.el-table-column--fixed-right .el-button span {
  color: inherit;
  display: inline-block;
}

/* 增强操作列按钮样式，解决文本不显示问题 */
:deep(.el-table .el-button) {
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  min-width: 70px;
  margin: 0 2px;
}

:deep(.el-table .el-button span) {
  display: inline-block !important;
  color: inherit !important;
  position: relative !important;
  z-index: 2;
  margin-left: 2px;
}

:deep(.el-button--primary),
:deep(.el-button--success) {
  font-weight: normal !important;
  white-space: nowrap;
}

/* 修复暗模式下的按钮文本颜色 */
.dark :deep(.el-button--primary) span,
.dark :deep(.el-button--success) span {
  color: #ffffff !important;
}
</style> 