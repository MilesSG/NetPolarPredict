from fastapi import APIRouter, HTTPException, Path, Query
from typing import Dict, List, Optional
import json
import os
from pydantic import BaseModel
import random

router = APIRouter()

# 数据模型
class AnalysisResult(BaseModel):
    eventId: int
    timestamp: str
    sentimentDistribution: Dict[str, float]
    topicDistribution: Dict[str, float]
    polarizationScore: float
    sentimentTrend: List[Dict[str, float]]

class CommentAnalysis(BaseModel):
    commentId: str
    text: str
    sentiment: str
    topics: List[str]
    polarizationContribution: float

# 工具函数
def load_analysis(event_id: int):
    """加载特定事件的分析结果"""
    try:
        with open(f"data/analysis/results_{event_id}.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def save_analysis(event_id: int, analysis_data: dict):
    """保存分析结果"""
    os.makedirs("data/analysis", exist_ok=True)
    with open(f"data/analysis/results_{event_id}.json", "w", encoding="utf-8") as f:
        json.dump(analysis_data, f, ensure_ascii=False, indent=2)

def generate_mock_analysis(event_id: int):
    """生成模拟分析数据（开发测试用）"""
    # 情感分布
    sentiment_dist = {
        "positive": random.uniform(0.1, 0.5),
        "neutral": random.uniform(0.1, 0.3),
        "negative": random.uniform(0.1, 0.5)
    }
    # 归一化
    total = sum(sentiment_dist.values())
    sentiment_dist = {k: v/total for k, v in sentiment_dist.items()}
    
    # 话题分布
    topics = ["政治", "经济", "社会", "科技", "文化", "教育", "健康", "环境"]
    topic_dist = {t: random.uniform(0, 1) for t in random.sample(topics, 5)}
    total = sum(topic_dist.values())
    topic_dist = {k: v/total for k, v in topic_dist.items()}
    
    # 极化得分
    polar_score = random.uniform(0.1, 0.9)
    
    # 情感趋势（过去7天）
    sentiment_trend = []
    for i in range(7):
        day = {
            "day": i+1,
            "positive": random.uniform(0.1, 0.6),
            "neutral": random.uniform(0.1, 0.3),
            "negative": random.uniform(0.1, 0.6)
        }
        # 归一化
        total = sum(v for k, v in day.items() if k != "day")
        for k in ["positive", "neutral", "negative"]:
            day[k] = day[k] / total
        sentiment_trend.append(day)
    
    analysis = {
        "eventId": event_id,
        "timestamp": "2023-06-01T12:00:00Z",
        "sentimentDistribution": sentiment_dist,
        "topicDistribution": topic_dist,
        "polarizationScore": polar_score,
        "sentimentTrend": sentiment_trend
    }
    
    return analysis

# 路由
@router.get("/events/{event_id}", response_model=AnalysisResult)
async def get_event_analysis(event_id: int = Path(..., description="事件ID")):
    """
    获取特定事件的分析结果
    """
    analysis_data = load_analysis(event_id)
    
    if not analysis_data:
        # 开发/测试期间，如果没有分析数据，生成模拟数据
        analysis_data = generate_mock_analysis(event_id)
        save_analysis(event_id, analysis_data)
    
    return analysis_data

@router.get("/comments/{event_id}", response_model=List[CommentAnalysis])
async def get_comments_analysis(
    event_id: int = Path(..., description="事件ID"),
    limit: int = Query(20, description="返回结果数量限制"),
    sort_by: str = Query("polarization", description="排序方式：polarization, sentiment")
):
    """
    获取事件评论的分析结果
    """
    # 检查评论数据是否存在
    comments_file = f"data/events/comments_{event_id}.json"
    if not os.path.exists(comments_file):
        raise HTTPException(status_code=404, detail=f"Comments for event {event_id} not found")
    
    # 加载评论数据
    with open(comments_file, "r", encoding="utf-8") as f:
        comments = json.load(f)
    
    # 模拟分析结果（实际应用中这部分应该从分析系统获取）
    sentiment_options = ["positive", "neutral", "negative"]
    topic_options = ["政治", "经济", "社会", "科技", "文化", "教育", "健康", "环境"]
    
    analysis_results = []
    for comment in comments[:min(limit*2, len(comments))]:  # 取更多以便后续筛选
        analysis = CommentAnalysis(
            commentId=comment["id"],
            text=comment["content"],
            sentiment=random.choice(sentiment_options),
            topics=random.sample(topic_options, random.randint(1, 3)),
            polarizationContribution=random.uniform(0, 1)
        )
        analysis_results.append(analysis)
    
    # 排序
    if sort_by == "polarization":
        analysis_results.sort(key=lambda x: x.polarizationContribution, reverse=True)
    elif sort_by == "sentiment":
        # 按情感排序（负面->中性->正面）
        sentiment_order = {"negative": 0, "neutral": 1, "positive": 2}
        analysis_results.sort(key=lambda x: sentiment_order[x.sentiment])
    
    return analysis_results[:limit]

@router.get("/related/{event_id}", response_model=Dict)
async def get_related_events(event_id: int = Path(..., description="事件ID")):
    """
    获取与特定事件相关的其他事件
    """
    related_file = f"data/analysis/related_{event_id}.json"
    
    # 如果数据不存在，创建模拟数据
    if not os.path.exists(related_file):
        # 创建随机相关事件ID（1-20范围内）
        related_ids = random.sample(range(1, 21), min(5, 20))
        # 排除当前事件ID
        if event_id in related_ids:
            related_ids.remove(event_id)
        
        related_data = {
            "eventId": event_id,
            "relatedEvents": related_ids,
            "relationStrength": {str(rid): random.uniform(0.5, 1.0) for rid in related_ids}
        }
        
        # 保存数据
        os.makedirs("data/analysis", exist_ok=True)
        with open(related_file, "w", encoding="utf-8") as f:
            json.dump(related_data, f, ensure_ascii=False, indent=2)
    else:
        # 加载已有数据
        with open(related_file, "r", encoding="utf-8") as f:
            related_data = json.load(f)
    
    return related_data

@router.get("/polarization/overview")
async def get_polarization_overview():
    """
    获取总体极化概览数据
    """
    # 这里返回模拟数据，实际应用中应该从分析系统获取
    categories = ["政治", "经济", "社会", "科技", "文化"]
    
    # 按类别的极化程度
    category_polarization = {cat: random.uniform(0.2, 0.8) for cat in categories}
    
    # 近期极化趋势（最近30天）
    polarization_trend = []
    base_value = 0.5
    for i in range(30):
        # 生成波动的趋势数据
        value = base_value + random.uniform(-0.05, 0.05)
        # 确保值在合理范围内
        value = max(0.1, min(0.9, value))
        polarization_trend.append({
            "day": i+1,
            "date": f"2023-05-{(i+1):02d}",
            "value": value
        })
        base_value = value  # 保持连续性
    
    # 极化热点事件
    hot_polarized_events = []
    for i in range(5):
        hot_polarized_events.append({
            "id": random.randint(1, 20),
            "title": f"热点事件 {i+1}",
            "polarizationLevel": random.uniform(0.6, 0.9),
            "category": random.choice(categories)
        })
    
    return {
        "categoryPolarization": category_polarization,
        "polarizationTrend": polarization_trend,
        "hotPolarizedEvents": hot_polarized_events
    } 