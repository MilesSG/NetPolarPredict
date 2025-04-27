from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import json
from app.routers import events, analysis, prediction, monitor

# 创建FastAPI应用
app = FastAPI(
    title="网络热点事件群体极化预测分析系统API",
    description="提供热点事件数据分析、情感分析和极化趋势预测的API",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该限制为前端URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含路由器
app.include_router(events.router, prefix="/api/events", tags=["events"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["analysis"])
app.include_router(prediction.router, prefix="/api/prediction", tags=["prediction"])
app.include_router(monitor.router, prefix="/api/monitor", tags=["monitor"])

@app.get("/")
async def root():
    return {
        "message": "网络热点事件群体极化预测分析系统API",
        "version": "1.0.0",
        "documentation": "/docs"
    }

@app.on_event("startup")
async def startup_event():
    # 确保数据目录存在
    os.makedirs("data/events", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)
    os.makedirs("data/analysis", exist_ok=True)
    
    # 初始化示例数据(如果不存在)
    if not os.path.exists("data/events/events.json"):
        sample_events = [
            {
                "id": 1,
                "title": "某科技公司CEO涉嫌违规交易",
                "category": "科技",
                "date": "2025-04-25",
                "source": "新浪微博",
                "commentCount": 25631,
                "polarizationLevel": 8.7,
                "hotLevel": 9.2,
                "description": "某科技公司CEO被曝出涉嫌内幕交易，引发公众对企业道德和监管制度的激烈讨论。相关话题在社交媒体上迅速发酵，形成明显的群体极化现象，支持者认为这是商业竞争中的正常行为被过度解读，反对者则严厉谴责这种行为并呼吁加强监管。",
                "keywords": ["科技公司", "CEO", "违规交易", "企业道德", "监管"]
            },
            {
                "id": 2,
                "title": "新冠疫苗接种争议",
                "category": "医疗",
                "date": "2025-04-23",
                "source": "知乎",
                "commentCount": 38752,
                "polarizationLevel": 9.2,
                "hotLevel": 9.8,
                "description": "关于新冠疫苗安全性和有效性的争论在社交媒体上持续发酵，形成了支持和反对两个强烈对立的群体。支持者强调疫苗的科学依据和公共健康收益，反对者则关注潜在风险和个人选择权。",
                "keywords": ["新冠疫苗", "接种", "公共健康", "副作用", "个人选择"]
            }
        ]
        with open("data/events/events.json", "w", encoding="utf-8") as f:
            json.dump(sample_events, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 