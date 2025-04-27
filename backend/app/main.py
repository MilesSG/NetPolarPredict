from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import events, analysis, prediction, monitor

app = FastAPI(title="网络极化预测系统API")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该限制为特定域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由器
app.include_router(events.router, prefix="/api/events", tags=["events"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["analysis"])
app.include_router(prediction.router, prefix="/api/prediction", tags=["prediction"])
app.include_router(monitor.router, prefix="/api/monitor", tags=["monitor"])

@app.get("/")
async def root():
    return {"message": "网络极化预测系统API"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"} 