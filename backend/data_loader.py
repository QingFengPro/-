"""处理 Excel 数据导入的模块"""
import pandas as pd
from models import Comment, Topic, SessionLocal
import os
from datetime import datetime


def load_data_from_excel(file_path: str):
    """
    从 Excel 文件加载数据到数据库
    假设 Excel 格式：
    - 第1列：评论内容
    - 第2列：情感（正向/负向/中立）
    """
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}")
        return False
    
    try:
        # 读取 Excel 文件
        df = pd.read_excel(file_path)
        print(f"✅ 成功读取 Excel 文件，共 {len(df)} 条数据")
        
        db = SessionLocal()
        
        # 清空现有数据
        db.query(Comment).delete()
        db.commit()
        
        # 插入数据 —— 支持多列标注（多数投票）
        def normalize_label(x: str) -> str:
            if x is None:
                return None
            s = str(x).strip().lower()
            if s in ("正向", "正面", "positive", "pos", "p", "1"):
                return "positive"
            if s in ("负向", "负面", "negative", "neg", "n", "-1"):
                return "negative"
            if s in ("中立", "中性", "neutral", "neu", "0"):
                return "neutral"
            return None

        for idx, row in df.iterrows():
            try:
                content = str(row.iloc[0]) if len(row) > 0 else ""

                # 收集最多三列的标注（如果存在）
                votes = []
                for col_idx in (1, 2, 3):
                    if len(row) > col_idx:
                        lab = normalize_label(row.iloc[col_idx])
                        if lab:
                            votes.append(lab)

                # 如果没有任何标注，尝试使用第二列原始文本（兼容旧文件）
                if not votes and len(row) > 1:
                    fallback = normalize_label(row.iloc[1])
                    if fallback:
                        votes.append(fallback)

                # 多数投票决定最终情感；平局或无票则视为中立
                sentiment = "neutral"
                if votes:
                    from collections import Counter
                    cnt = Counter(votes)
                    most_common, count = cnt.most_common(1)[0]
                    # 若存在平局（多个标签数量相等），则选择 neutral
                    top_counts = [v for v in cnt.values() if v == count]
                    if len(top_counts) == 1:
                        sentiment = most_common
                    else:
                        sentiment = "neutral"

                # 映射为分值
                sentiment_score = 0.8 if sentiment == "positive" else (0.2 if sentiment == "negative" else 0.5)

                comment = Comment(
                    content=content,
                    sentiment=sentiment,
                    sentiment_score=sentiment_score,
                    timestamp=datetime.now()
                )
                db.add(comment)
            except Exception as e:
                print(f"⚠️  第 {idx} 行数据处理失败: {e}")
                continue
        
        db.commit()
        print(f"✅ 成功导入 {len(df)} 条评论数据")
        
        # 生成话题统计
        update_topic_stats(db)
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ 导入数据失败: {e}")
        return False


def update_topic_stats(db):
    """更新话题统计数据"""
    # 获取所有评论
    comments = db.query(Comment).all()
    
    if not comments:
        return
    
    # 统计情感分布
    positive = sum(1 for c in comments if c.sentiment == "positive")
    negative = sum(1 for c in comments if c.sentiment == "negative")
    neutral = sum(1 for c in comments if c.sentiment == "neutral")
    avg_score = sum(c.sentiment_score for c in comments) / len(comments)
    
    # 创建或更新话题
    topic = db.query(Topic).first()
    if not topic:
        topic = Topic(
            title="微博话题总体分析",
            positive_count=positive,
            negative_count=negative,
            neutral_count=neutral,
            avg_sentiment_score=avg_score
        )
        db.add(topic)
    else:
        topic.positive_count = positive
        topic.negative_count = negative
        topic.neutral_count = neutral
        topic.avg_sentiment_score = avg_score
    
    db.commit()
    print(f"📊 话题统计：正向 {positive}, 负向 {negative}, 中立 {neutral}, 平均分 {avg_score:.2f}")
