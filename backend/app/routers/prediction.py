from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import random
import numpy as np
from pydantic import BaseModel

router = APIRouter(
    prefix="/prediction",
    tags=["prediction"],
    responses={404: {"description": "Not found"}},
)

class PredictionRequest(BaseModel):
    event_id: str
    prediction_horizon: int = 24  # 预测时间范围，默认24小时
    confidence_level: float = 0.95  # 置信水平

class PredictionResponse(BaseModel):
    event_id: str
    predicted_pi: float  # 预测的极化指数
    confidence_interval: List[float]  # 置信区间 [下限, 上限]
    prediction_time: datetime
    predicted_values: List[Dict[str, Any]]  # 预测的时间序列数据

class TimeSeriesPoint(BaseModel):
    timestamp: datetime
    value: float
    lower_bound: Optional[float] = None
    upper_bound: Optional[float] = None

# 模拟极化指数预测的函数
def predict_polarization_index(event_id: str, horizon: int, confidence: float) -> Dict[str, Any]:
    """
    模拟极化指数预测
    """
    now = datetime.now()
    
    # 基础趋势：生成一个有轻微上升趋势的时间序列
    base_pi = 0.65  # 基础极化指数
    noise_level = 0.05  # 噪声水平
    trend_factor = 0.01  # 趋势因子
    
    # 生成预测时间序列
    predicted_series = []
    for i in range(horizon + 1):
        # 添加趋势和随机噪声
        time_point = now + timedelta(hours=i)
        trend = trend_factor * i
        noise = random.uniform(-noise_level, noise_level)
        value = min(0.95, base_pi + trend + noise)  # 限制最大值
        
        # 计算置信区间
        ci_range = noise_level * 1.5  # 置信区间范围
        lower = max(0, value - ci_range)
        upper = min(1, value + ci_range)
        
        predicted_series.append({
            "timestamp": time_point,
            "value": value,
            "lower_bound": lower,
            "upper_bound": upper
        })
    
    # 最终预测值（最后一个时间点的值）
    final_prediction = predicted_series[-1]["value"]
    
    # 置信区间
    confidence_interval = [
        predicted_series[-1]["lower_bound"],
        predicted_series[-1]["upper_bound"]
    ]
    
    return {
        "event_id": event_id,
        "predicted_pi": final_prediction,
        "confidence_interval": confidence_interval,
        "prediction_time": now,
        "predicted_values": predicted_series
    }

@router.post("/polarization-index", response_model=PredictionResponse)
async def predict_pi(request: PredictionRequest):
    """
    预测事件的极化指数
    """
    try:
        prediction_result = predict_polarization_index(
            request.event_id, 
            request.prediction_horizon,
            request.confidence_level
        )
        return prediction_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"预测失败: {str(e)}")

@router.get("/trends/{event_id}")
async def get_prediction_trends(event_id: str, days: int = 7):
    """
    获取事件的预测趋势
    """
    now = datetime.now()
    
    # 生成过去七天的预测准确率趋势
    accuracy_trend = []
    for i in range(days):
        date = now - timedelta(days=days-i-1)
        # 模拟每天的预测准确率（70%-90%之间）
        accuracy = random.uniform(0.7, 0.9)
        accuracy_trend.append({
            "date": date.strftime("%Y-%m-%d"),
            "accuracy": accuracy
        })
    
    # 生成主题极化趋势
    polarization_trend = []
    base_pi = 0.5
    for i in range(days):
        date = now - timedelta(days=days-i-1)
        # 模拟每天的极化指数（有上升趋势）
        pi = base_pi + (i * 0.03) + random.uniform(-0.05, 0.05)
        pi = min(0.95, max(0.1, pi))  # 限制在合理范围内
        polarization_trend.append({
            "date": date.strftime("%Y-%m-%d"),
            "pi_value": pi
        })
    
    return {
        "event_id": event_id,
        "accuracy_trend": accuracy_trend,
        "polarization_trend": polarization_trend
    } 