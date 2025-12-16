# 🚀 微博情感分析系统 - 启动说明

## ✨ 系统简介

- **后端**: FastAPI（Python）
- **前端**: Vue 3（JavaScript）
- **数据库**: SQLite（自动创建）
- **数据源**: Excel 文件（自动导入）

---

## 📋 启动步骤

### 方式一：直接运行（推荐）

#### 后端启动
```bash
cd backend
pip install -r requirements.txt
python app.py
```

**访问地址:**
- API 接口: http://localhost:8000
- 交互文档: http://localhost:8000/docs

#### 前端启动（在新终端）
```bash
cd frontend
npm install
npm run dev
```

**访问地址:** http://localhost:5173

---

## 📊 核心功能

### 三个主要页面

1. **首页** (`/`)
   - 统计卡片：总评论数、正向、负向、中立
   - 情感分布比例图
   - 平均情感分值

2. **分析** (`/analysis`)
   - 情感分布分析
   - 样本评论展示
   - 趋势分析

3. **评论** (`/comments`)
   - 完整评论列表
   - 按情感筛选
   - 删除/新增评论

---

## 🔗 API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/stats` | GET | 获取统计数据 |
| `/api/comments` | GET | 获取评论列表（支持分页、筛选） |
| `/api/comments` | POST | 添加新评论 |
| `/api/comments/{id}` | DELETE | 删除评论 |
| `/api/reload` | POST | 重新加载 Excel 数据 |
| `/api/all` | DELETE | 清空所有数据 |

### 请求示例

```bash
# 获取统计数据
curl http://localhost:8000/api/stats

# 获取评论列表（分页）
curl "http://localhost:8000/api/comments?skip=0&limit=20"

# 按情感筛选
curl "http://localhost:8000/api/comments?sentiment=positive"

# 添加评论
curl -X POST "http://localhost:8000/api/comments?content=这是一条评论&sentiment=positive"

# 删除评论
curl -X DELETE "http://localhost:8000/api/comments/1"
```

---

## 📁 项目结构

```
backend/
  ├── app.py              # ⭐ 主应用入口（运行这个）
  ├── models.py           # 数据模型定义
  ├── data_loader.py      # Excel 数据加载
  ├── .env               # 配置文件
  ├── requirements.txt    # Python 依赖
  └── weibo_sentiment.db # SQLite 数据库（自动创建）

frontend/
  ├── src/
  │   ├── pages/         # 页面组件
  │   │   ├── Dashboard.vue   # 首页
  │   │   ├── Analysis.vue    # 分析页
  │   │   └── Comments.vue    # 评论页
  │   ├── api/           # API 调用
  │   └── router/        # 路由配置
  ├── package.json
  └── vite.config.js
```

---

## 📊 数据格式

Excel 文件应包含：
- **第1列**: 评论内容
- **第2列**: 情感（`正向`/`负向`/`中立`）

**默认路径:** `C:\Users\asus\Desktop\评论与情感.xlsx`

修改 `backend/.env` 中的 `DATA_FILE_PATH` 可改变路径。

---

## ⚙️ 配置文件 (.env)

```env
# 数据库
DATABASE_URL=sqlite:///./weibo_sentiment.db

# 数据文件路径
DATA_FILE_PATH=C:\Users\asus\Desktop\评论与情感.xlsx

# FastAPI 配置
APP_NAME=Weibo Sentiment Analysis System
DEBUG=True
SECRET_KEY=your-secret-key
```

---

## 🐛 常见问题

| 问题 | 解决 |
|------|------|
| 后端启动失败 | 检查 Python 3.8+ 是否安装，运行 `python --version` |
| 未找到数据文件 | 确保 Excel 文件在 `.env` 指定的路径 |
| 前端无法连接后端 | 确保后端运行在 `localhost:8000`，检查防火墙 |
| npm install 失败 | 尝试 `npm install --legacy-peer-deps` |

---

## 🎯 快速命令

```bash
# 后端启动（在 backend 目录）
python app.py

# 前端启动（在 frontend 目录）
npm run dev

# 构建前端
npm run build

# API 文档（后端运行中）
http://localhost:8000/docs
```

---

## 📝 更新日志

**v1.0.0 (2025-12-15)**
- ✅ 简化版本发布
- ✅ 支持 Excel 数据导入
- ✅ 实现情感分析 API
- ✅ 前端三个核心页面

---

**问题反馈:** 查看后端控制台输出或前端浏览器控制台
