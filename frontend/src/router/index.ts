import { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('../layouts/MainLayout.vue'),
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: () => import('../views/Dashboard.vue'),
        meta: {
          title: '仪表盘',
          icon: 'DataAnalysis'
        }
      },
      {
        path: 'events',
        name: 'Events',
        component: () => import('../views/EventsList.vue'),
        meta: {
          title: '热点事件总览',
          icon: 'List'
        }
      },
      {
        path: 'monitor',
        name: 'RealTimeMonitor',
        component: () => import('../views/RealTimeMonitor.vue'),
        meta: {
          title: '实时监控',
          icon: 'Monitor'
        }
      },
      {
        path: 'prediction',
        name: 'PredictionTrend',
        component: () => import('../views/PredictionTrend.vue'),
        meta: {
          title: '极化趋势预测',
          icon: 'TrendCharts'
        }
      },
      {
        path: 'events/:id',
        name: 'EventDetail',
        component: () => import('../views/EventDetail.vue'),
        meta: {
          title: '事件详情分析',
          icon: 'InfoFilled'
        }
      }
    ]
  }
]

export default routes 