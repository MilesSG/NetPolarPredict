from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends, WebSocket, WebSocketDisconnect
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import random
import asyncio
import json
from pydantic import BaseModel

router = APIRouter(
    prefix="/monitor",
    tags=["monitor"],
    responses={404: {"description": "Not found"}},
)

# 模拟的连接客户端
connected_clients = set()

class MonitoringSettings(BaseModel):
    update_interval: int = 5  # 更新间隔（秒）
    alert_threshold: float = 0.75  # 警报阈值
    is_active: bool = True  # 监控是否激活

# 全局监控设置
monitoring_settings = MonitoringSettings()

# 模拟的事件数据
current_pi_value = 0.6
alert_history = []
monitoring_events = []

platforms = ["twitter", "facebook", "reddit", "weibo", "youtube"]
event_types = ["极化上升", "极化下降", "达到阈值", "系统重启"]

async def generate_monitoring_data():
    """
    生成模拟的监控数据
    """
    global current_pi_value, alert_history, monitoring_events
    
    # 随机波动极化指数值
    trend = random.choice([-1, 1, 1])  # 稍微偏向上升
    change = random.uniform(0.01, 0.04) * trend
    current_pi_value = max(0.1, min(0.95, current_pi_value + change))
    
    # 获取当前时间
    now = datetime.now()
    
    # 生成监控事件
    if random.random() < 0.2:  # 20%的概率生成一个新事件
        event_type = random.choice(event_types)
        platform = random.choice(platforms)
        monitoring_events.append({
            "event_id": f"evt_{len(monitoring_events) + 1}",
            "timestamp": now,
            "event_type": event_type,
            "platform": platform,
            "pi_value": current_pi_value,
            "description": f"{platform}平台上检测到{event_type}事件"
        })
        
        # 保持事件列表在合理大小
        if len(monitoring_events) > 50:
            monitoring_events = monitoring_events[-50:]
    
    # 检查是否超过警报阈值
    if current_pi_value > monitoring_settings.alert_threshold:
        alert_history.append({
            "alert_id": f"alt_{len(alert_history) + 1}",
            "timestamp": now,
            "pi_value": current_pi_value,
            "threshold": monitoring_settings.alert_threshold,
            "status": "已触发",
            "description": f"极化指数({current_pi_value:.2f})超过警报阈值({monitoring_settings.alert_threshold:.2f})"
        })
        
        # 保持警报历史在合理大小
        if len(alert_history) > 100:
            alert_history = alert_history[-100:]
    
    # 返回当前数据
    return {
        "timestamp": now.isoformat(),
        "pi_value": current_pi_value,
        "is_alert": current_pi_value > monitoring_settings.alert_threshold,
        "latest_events": monitoring_events[-5:] if monitoring_events else [],
        "alert_count": len([a for a in alert_history if (now - a["timestamp"]).total_seconds() < 3600])  # 过去一小时的警报数
    }

async def monitor_task():
    """
    监控任务，定期发送数据给所有连接的客户端
    """
    while True:
        if monitoring_settings.is_active and connected_clients:
            data = await generate_monitoring_data()
            # 发送数据给所有连接的客户端
            disconnected = set()
            for client in connected_clients:
                try:
                    await client.send_json(data)
                except Exception:
                    disconnected.add(client)
            
            # 移除断开连接的客户端
            connected_clients.difference_update(disconnected)
            
        # 根据设置的更新间隔等待
        await asyncio.sleep(monitoring_settings.update_interval)

# 后台任务
background_task = None

@router.on_event("startup")
async def startup_event():
    """
    应用启动时开始监控任务
    """
    global background_task
    background_task = asyncio.create_task(monitor_task())

@router.on_event("shutdown")
async def shutdown_event():
    """
    应用关闭时取消监控任务
    """
    if background_task:
        background_task.cancel()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket连接，用于实时监控数据
    """
    await websocket.accept()
    connected_clients.add(websocket)
    try:
        while True:
            # 接收客户端消息（可选）
            data = await websocket.receive_text()
            # 处理客户端消息（此处简单回显）
            await websocket.send_text(f"收到: {data}")
    except WebSocketDisconnect:
        connected_clients.remove(websocket)

@router.get("/settings")
async def get_monitoring_settings():
    """
    获取当前监控设置
    """
    return monitoring_settings

@router.post("/settings")
async def update_monitoring_settings(settings: MonitoringSettings):
    """
    更新监控设置
    """
    global monitoring_settings
    monitoring_settings = settings
    return {"message": "监控设置已更新", "settings": monitoring_settings}

@router.get("/alerts")
async def get_alert_history(limit: int = 20):
    """
    获取警报历史
    """
    return {"alerts": alert_history[-limit:]}

@router.get("/events")
async def get_monitoring_events(limit: int = 20):
    """
    获取监控事件
    """
    return {"events": monitoring_events[-limit:]}

@router.get("/statistics")
async def get_monitoring_statistics():
    """
    获取监控统计数据
    """
    now = datetime.now()
    one_hour_ago = now - timedelta(hours=1)
    one_day_ago = now - timedelta(days=1)
    
    # 计算统计数据
    hourly_alerts = len([a for a in alert_history if a["timestamp"] >= one_hour_ago])
    daily_alerts = len([a for a in alert_history if a["timestamp"] >= one_day_ago])
    
    # 按平台分类事件
    platform_distribution = {}
    for event in monitoring_events:
        platform = event["platform"]
        if platform in platform_distribution:
            platform_distribution[platform] += 1
        else:
            platform_distribution[platform] = 1
    
    # 计算平均极化指数（最近20个事件）
    recent_events = monitoring_events[-20:]
    avg_pi = sum(event["pi_value"] for event in recent_events) / len(recent_events) if recent_events else 0
    
    return {
        "current_pi": current_pi_value,
        "hourly_alerts": hourly_alerts,
        "daily_alerts": daily_alerts,
        "total_events": len(monitoring_events),
        "average_pi": avg_pi,
        "platform_distribution": platform_distribution
    } 