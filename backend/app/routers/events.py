from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
import json
import os
from pydantic import BaseModel

router = APIRouter()

# 数据模型
class EventKeyword(BaseModel):
    name: str
    weight: Optional[float] = None

class Event(BaseModel):
    id: int
    title: str
    category: str
    date: str
    source: str
    commentCount: int
    polarizationLevel: float
    hotLevel: float
    description: Optional[str] = None
    keywords: Optional[List[str]] = None

class EventDetail(Event):
    comments: Optional[List[dict]] = None
    relatedEvents: Optional[List[int]] = None
    analysisResults: Optional[dict] = None

class EventCreate(BaseModel):
    title: str
    category: str
    date: str
    source: str
    description: Optional[str] = None
    keywords: Optional[List[str]] = None

# 工具函数
def load_events():
    """加载所有事件数据"""
    try:
        with open("data/events/events.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_events(events):
    """保存事件数据"""
    os.makedirs("data/events", exist_ok=True)
    with open("data/events/events.json", "w", encoding="utf-8") as f:
        json.dump(events, f, ensure_ascii=False, indent=2)

# 路由
@router.get("/", response_model=List[Event])
async def get_events(
    category: Optional[str] = None,
    min_polarization: Optional[float] = None,
    max_polarization: Optional[float] = None,
    keyword: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
):
    """
    获取事件列表，支持分类筛选、极化程度筛选和关键词搜索
    """
    events = load_events()
    
    # 应用筛选
    if category:
        events = [e for e in events if e["category"] == category]
    
    if min_polarization is not None:
        events = [e for e in events if e["polarizationLevel"] >= min_polarization]
    
    if max_polarization is not None:
        events = [e for e in events if e["polarizationLevel"] <= max_polarization]
    
    if keyword:
        filtered_events = []
        for event in events:
            if (keyword.lower() in event["title"].lower() or 
                (event.get("description") and keyword.lower() in event["description"].lower()) or
                any(keyword.lower() in kw.lower() for kw in event.get("keywords", []))):
                filtered_events.append(event)
        events = filtered_events
    
    # 应用分页
    return events[skip:skip + limit]

@router.get("/{event_id}", response_model=EventDetail)
async def get_event(event_id: int):
    """
    获取单个事件的详细信息
    """
    events = load_events()
    for event in events:
        if event["id"] == event_id:
            # 加载评论数据
            comments = []
            comments_file = f"data/events/comments_{event_id}.json"
            if os.path.exists(comments_file):
                try:
                    with open(comments_file, "r", encoding="utf-8") as f:
                        comments = json.load(f)
                except json.JSONDecodeError:
                    pass
            
            # 加载相关事件
            related_events = []
            related_file = f"data/analysis/related_{event_id}.json"
            if os.path.exists(related_file):
                try:
                    with open(related_file, "r", encoding="utf-8") as f:
                        related_data = json.load(f)
                        related_events = related_data.get("relatedEvents", [])
                except json.JSONDecodeError:
                    pass
            
            # 加载分析结果
            analysis_results = {}
            analysis_file = f"data/analysis/results_{event_id}.json"
            if os.path.exists(analysis_file):
                try:
                    with open(analysis_file, "r", encoding="utf-8") as f:
                        analysis_results = json.load(f)
                except json.JSONDecodeError:
                    pass
            
            # 构建详细信息
            event_detail = dict(event)
            event_detail["comments"] = comments
            event_detail["relatedEvents"] = related_events
            event_detail["analysisResults"] = analysis_results
            
            return event_detail
    
    raise HTTPException(status_code=404, detail=f"Event with id {event_id} not found")

@router.post("/", response_model=Event)
async def create_event(event: EventCreate):
    """
    创建新事件
    """
    events = load_events()
    
    # 生成新ID
    new_id = 1
    if events:
        new_id = max(e["id"] for e in events) + 1
    
    # 创建新事件
    new_event = event.dict()
    new_event["id"] = new_id
    new_event["commentCount"] = 0
    new_event["polarizationLevel"] = 0.0
    new_event["hotLevel"] = 0.0
    
    events.append(new_event)
    save_events(events)
    
    return new_event

@router.put("/{event_id}", response_model=Event)
async def update_event(event_id: int, event_update: EventCreate):
    """
    更新事件信息
    """
    events = load_events()
    
    for i, event in enumerate(events):
        if event["id"] == event_id:
            # 更新事件信息
            updated_event = event.copy()
            updated_event.update(event_update.dict(exclude_unset=True))
            events[i] = updated_event
            save_events(events)
            return updated_event
    
    raise HTTPException(status_code=404, detail=f"Event with id {event_id} not found")

@router.delete("/{event_id}")
async def delete_event(event_id: int):
    """
    删除事件
    """
    events = load_events()
    initial_count = len(events)
    
    events = [e for e in events if e["id"] != event_id]
    
    if len(events) < initial_count:
        save_events(events)
        return {"message": f"Event with id {event_id} successfully deleted"}
    
    raise HTTPException(status_code=404, detail=f"Event with id {event_id} not found")

@router.get("/categories/all")
async def get_categories():
    """
    获取所有事件分类
    """
    events = load_events()
    categories = set(e["category"] for e in events)
    return {"categories": list(categories)}

@router.get("/keywords/top")
async def get_top_keywords(limit: int = 20):
    """
    获取热门关键词
    """
    events = load_events()
    
    # 统计关键词出现次数
    keyword_counts = {}
    for event in events:
        for keyword in event.get("keywords", []):
            if keyword in keyword_counts:
                keyword_counts[keyword] += 1
            else:
                keyword_counts[keyword] = 1
    
    # 排序并返回前N个
    sorted_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)
    top_keywords = [{"name": k, "count": c} for k, c in sorted_keywords[:limit]]
    
    return {"keywords": top_keywords} 