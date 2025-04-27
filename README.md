# 🌐 NetPolarPredict - 网络极化预测系统

## 📋 项目介绍

NetPolarPredict是一个基于人工智能的网络极化预测系统，旨在监测、分析和预测社交媒体平台上的极化趋势。通过对多平台社交媒体数据的实时监控，系统可以及时捕捉极化事件，并提供未来趋势预测。

## ✨ 核心功能

- 🔍 **实时监控**：实时追踪多个社交媒体平台的极化指数变化
- 📊 **数据分析**：多维度分析极化事件，包括情感分析、主题分析
- 🔮 **趋势预测**：基于历史数据预测未来极化趋势
- ⚠️ **预警系统**：当极化指数超过阈值时发出警报
- 📱 **多平台支持**：覆盖Twitter、Facebook、Reddit、微博等主流社交平台

## 🛠️ 技术栈

### 前端
- 🖼️ **Vue 3** + **TypeScript**：构建响应式用户界面
- 🎨 **Tailwind CSS**：现代化的UI设计
- 📈 **ECharts**：数据可视化图表
- 🧰 **Pinia**：状态管理
- 🚦 **Vue Router**：路由管理

### 后端
- 🐍 **Python** + **FastAPI**：高性能API服务
- 🔄 **WebSocket**：实现实时数据推送
- 🧠 **机器学习模型**：用于极化指数预测
- 🔒 **JWT认证**：安全的用户认证

## 📸 界面展示

*项目截图将在完成后添加*

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

## 📝 开发计划

- [x] 系统基础架构搭建
- [x] 实时监控模块
- [x] 数据分析模块
- [x] 趋势预测模块
- [ ] 用户权限管理
- [ ] 移动端适配
- [ ] 多语言支持

## 👥 贡献者

- MilesSG - 项目发起人

## �� 许可证

MIT License 