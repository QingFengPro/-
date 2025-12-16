"""
简化版微博情感分析系统 - FastAPI 应用入口
直接运行: python app.py
"""
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import uvicorn
import os
from dotenv import load_dotenv
from datetime import datetime

# 加载环境变量
load_dotenv()

# 导入模型和数据加载器
from models import init_db, get_db, Comment, Topic
from data_loader import load_data_from_excel

# 创建 FastAPI 应用
app = FastAPI(
    title="微博情感分析系统",
    description="简化版本 - 核心接口",
    version="1.0.0"
)

# CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============ 初始化接口 ============

@app.on_event("startup")
async def startup():
    """启动时初始化数据库"""
    print("🚀 应用启动中...")
    init_db()
    
    # 自动从 xlsx 文件加载数据
    excel_path = os.getenv("DATA_FILE_PATH", "C:\\Users\\asus\\Desktop\\评论与情感.xlsx")
    if os.path.exists(excel_path):
        print(f"📂 检测到数据文件: {excel_path}")
        load_data_from_excel(excel_path)
    else:
        print(f"⚠️  未找到数据文件: {excel_path}")
    
    print("✅ 应用启动成功")


@app.get("/")
def index():
    """应用首页"""
    return {
        "message": "欢迎使用微博情感分析系统",
        "docs": "http://localhost:8000/docs",
        "api_list": [
            "GET /api/stats - 获取统计数据",
            "GET /api/comments - 获取所有评论",
            "GET /api/comments/{id} - 获取单个评论",
            "POST /api/comments - 添加新评论",
            "DELETE /api/comments/{id} - 删除评论",
            "POST /api/reload - 重新加载 Excel 数据"
        ]
    }


# ============ 统计接口 ============

@app.get("/api/stats")
def get_stats(db: Session = Depends(get_db)):
    """获取统计数据"""
    topic = db.query(Topic).first()
    
    if not topic:
        return {
            "total_comments": 0,
            "positive_count": 0,
            "negative_count": 0,
            "neutral_count": 0,
            "avg_sentiment_score": 0.0,
            "sentiment_ratio": {
                "positive": 0,
                "negative": 0,
                "neutral": 0
            }
        }
    
    total = topic.positive_count + topic.negative_count + topic.neutral_count
    total = max(total, 1)  # 避免除以零
    
    return {
        "total_comments": total,
        "positive_count": topic.positive_count,
        "negative_count": topic.negative_count,
        "neutral_count": topic.neutral_count,
        "avg_sentiment_score": round(topic.avg_sentiment_score, 2),
        "sentiment_ratio": {
            "positive": round(topic.positive_count / total * 100, 2),
            "negative": round(topic.negative_count / total * 100, 2),
            "neutral": round(topic.neutral_count / total * 100, 2)
        }
    }


# ============ 评论接口 ============

@app.get("/api/comments")
def get_comments(skip: int = 0, limit: int = 50, sentiment: str = None, db: Session = Depends(get_db)):
    """获取评论列表"""
    query = db.query(Comment)
    
    # 按情感过滤
    if sentiment and sentiment in ["positive", "negative", "neutral"]:
        query = query.filter(Comment.sentiment == sentiment)
    
    # 分页
    total = query.count()
    comments = query.offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": [
            {
                "id": c.id,
                "content": c.content,
                "sentiment": c.sentiment,
                "sentiment_score": c.sentiment_score,
                "timestamp": c.timestamp.isoformat() if c.timestamp else None
            }
            for c in comments
        ]
    }


@app.get("/api/comments/{comment_id}")
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    """获取单个评论"""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    
    if not comment:
        return JSONResponse(status_code=404, content={"error": "评论不存在"})
    
    return {
        "id": comment.id,
        "content": comment.content,
        "sentiment": comment.sentiment,
        "sentiment_score": comment.sentiment_score,
        "timestamp": comment.timestamp.isoformat() if comment.timestamp else None
    }


@app.post("/api/comments")
def create_comment(
    content: str,
    sentiment: str = "neutral",
    db: Session = Depends(get_db)
):
    """添加新评论"""
    # 简单的情感分值计算
    sentiment_map = {
        "positive": 0.8,
        "negative": 0.2,
        "neutral": 0.5
    }
    sentiment_score = sentiment_map.get(sentiment, 0.5)
    
    comment = Comment(
        content=content,
        sentiment=sentiment,
        sentiment_score=sentiment_score,
        timestamp=datetime.now()
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    
    # 更新话题统计
    from data_loader import update_topic_stats
    update_topic_stats(db)
    
    return {
        "id": comment.id,
        "content": comment.content,
        "sentiment": comment.sentiment,
        "sentiment_score": comment.sentiment_score,
        "message": "✅ 评论添加成功"
    }


@app.delete("/api/comments/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    """删除评论"""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    
    if not comment:
        return JSONResponse(status_code=404, content={"error": "评论不存在"})
    
    db.delete(comment)
    db.commit()
    
    # 更新话题统计
    from data_loader import update_topic_stats
    update_topic_stats(db)
    
    return {"message": "✅ 评论删除成功"}


# ============ 数据管理接口 ============

@app.post("/api/reload")
def reload_data(db: Session = Depends(get_db)):
    """重新加载 Excel 数据"""
    excel_path = os.getenv("DATA_FILE_PATH", "C:\\Users\\asus\\Desktop\\评论与情感.xlsx")
    
    if not os.path.exists(excel_path):
        return JSONResponse(
            status_code=400,
            content={"error": f"文件不存在: {excel_path}"}
        )
    
    # 清空现有数据
    db.query(Comment).delete()
    db.query(Topic).delete()
    db.commit()
    
    # 重新加载
    success = load_data_from_excel(excel_path)
    
    if success:
        return {
            "message": "✅ 数据重新加载成功",
            "file": excel_path
        }
    else:
        return JSONResponse(
            status_code=500,
            content={"error": "数据加载失败"}
        )


@app.delete("/api/all")
def delete_all_data(db: Session = Depends(get_db)):
    """删除所有数据"""
    count = db.query(Comment).delete()
    db.query(Topic).delete()
    db.commit()
    
    return {
        "message": "✅ 所有数据已删除",
        "deleted_comments": count
    }


# ============ 启动脚本 ============

if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════╗
    ║    微博情感分析系统 - FastAPI 服务启动    ║
    ╚════════════════════════════════════════════╝
    """)
    
    # 启动服务
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # 开发模式自动重载
        log_level="info"
    )
