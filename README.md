# 🌐 NetPolarPredict - 网络极化预测系统

## 📋 项目介绍

NetPolarPredict是一个基于人工智能的网络极化预测系统，旨在监测、分析和预测社交媒体平台上的极化趋势。通过对多平台社交媒体数据的实时监控，系统可以及时捕捉极化事件，并提供未来趋势预测。
![image](https://github.com/user-attachments/assets/ecf67468-79b0-4cb3-b922-dc662efdf383)

![image](https://github.com/user-attachments/assets/3e63a65d-99d7-49bf-b833-1616ea19ed6d)
![image](https://github.com/user-attachments/assets/d5bf4469-a32b-4f57-b8c4-6aec24f046e6)


## 📢 最新更新

- ✅ **UI宽屏优化**：所有页面已优化为100%宽屏显示，提供更佳的视觉体验
- ✅ **模态框分析功能**：在仪表盘和事件详情页添加"详情分析"功能，通过模态框展示深度分析报告
- ✅ **交互体验优化**：完善按钮点击反馈，增强用户交互体验

## ✨ 核心功能

* 🔍 **实时监控**：实时追踪多个社交媒体平台的极化指数变化
* 📊 **数据分析**：多维度分析极化事件，包括情感分析、主题分析和深度分析报告
* 🔮 **趋势预测**：基于历史数据预测未来极化趋势
* ⚠️ **预警系统**：当极化指数超过阈值时发出警报
* 📱 **多平台支持**：覆盖Twitter、Facebook、Reddit、微博等主流社交平台

## 🛠️ 技术栈

### 前端

* 🖼️ **Vue 3** + **TypeScript**：构建响应式用户界面
* 🎨 **Tailwind CSS**：现代化的UI设计
* 📈 **ECharts** + **echarts-wordcloud**：数据可视化图表
* 🧰 **Pinia**：状态管理
* 🚦 **Vue Router**：路由管理
* 🧩 **Element Plus**：UI组件库

### 后端

* 🐍 **Python** + **FastAPI**：高性能API服务
* 🔄 **WebSocket**：实现实时数据推送
* 🧠 **机器学习模型**：用于极化指数预测
* 🔒 **JWT认证**：安全的用户认证

## 📸 界面展示

### 主要功能界面

* **热点事件列表**：展示热点事件、极化指数、类别分布和评论数量等信息
* **事件详情分析**：提供事件极化趋势图、情感分布图、评论网络图和关键词云图等多维分析
* **实时监控面板**：实时展示极化指数变化、热点事件分布和舆论走势
* **预测趋势分析**：基于历史数据进行极化态势预测与模拟
* **深度分析报告**：通过模态框展示事件的深度分析报告，包括极化原因、发展趋势和干预建议

## 🚀 快速开始

### 前端启动

```bash
cd frontend
npm install
npm run dev
```

### 后端启动

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

## 🧩 依赖项

### 前端依赖

确保安装以下关键依赖：

```bash
npm install echarts echarts-wordcloud @element-plus/icons-vue @vueuse/core
```

### 后端依赖

```bash
pip install fastapi uvicorn sqlalchemy pandas scikit-learn
```

## 🔧 常见问题

### echarts-wordcloud模块问题

如果遇到词云图表无法显示的问题：

```
[plugin:vite:import-analysis] Failed to resolve import "echarts-wordcloud"
```

请确保已正确安装echarts-wordcloud依赖：

```bash
npm install echarts-wordcloud --save
```

### UI显示问题

如果遇到UI组件显示不全或布局错乱问题：

```
请确保正确安装了Element Plus和Tailwind CSS依赖，并在浏览器中强制刷新页面（Ctrl+F5）。
```

## 📝 开发计划

- [x] 系统基础架构搭建
- [x] 热点事件列表展示
- [x] 事件详情分析
- [x] 多维度数据可视化
- [x] 实时监控模块
- [x] UI宽屏优化
- [x] 交互功能增强（详情分析模态框）
- [ ] 趋势预测模块优化
- [ ] 用户权限管理
- [ ] 移动端适配
- [ ] 多语言支持

## 👥 贡献者

* MilesSG - 项目发起人

## �� 许可证

MIT License 
