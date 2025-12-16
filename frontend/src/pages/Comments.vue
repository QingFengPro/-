<template>
  <div class="comments-page">
    <h2>💬 评论管理</h2>

    <!-- 操作栏 -->
    <div class="controls">
      <div class="filter-group">
        <label>筛选：</label>
        <select v-model="filterSentiment" class="filter-select">
          <option value="">全部评论</option>
          <option value="positive">正面</option>
          <option value="neutral">中性</option>
          <option value="negative">负面</option>
        </select>
      </div>
      <button @click="reloadComments" class="btn btn-primary">🔄 刷新</button>
      <button @click="clearAllComments" class="btn btn-danger">🗑️ 清空所有</button>
    </div>

    <!-- 评论列表 -->
    <div class="comments-list">
      <div v-for="comment in filteredComments" :key="comment.id" class="comment-item" :class="comment.sentiment">
        <div class="comment-header">
          <span class="comment-id">#{{ comment.id }}</span>
          <span class="sentiment-badge" :class="comment.sentiment">{{ sentimentText[comment.sentiment] }}</span>
          <span class="comment-date">{{ formatDate(comment.timestamp) }}</span>
          <button @click="deleteComment(comment.id)" class="btn-delete">删除</button>
        </div>
        <div class="comment-body">
          <p>{{ comment.content }}</p>
        </div>
      </div>
      <div v-if="filteredComments.length === 0" class="no-data">
        <p>暂无评论数据</p>
      </div>
    </div>

    <!-- 分页 -->
    <div class="pagination" v-if="commentsTotal > pageSize">
      <button :disabled="currentPage === 1" @click="currentPage--" class="page-btn">上一页</button>
      <span class="page-info">{{ currentPage }} / {{ totalPages }}</span>
      <button :disabled="currentPage === totalPages" @click="currentPage++" class="page-btn">下一页</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useAnalysisStore } from '@/stores/analysisStore';

const analysisStore = useAnalysisStore();
const filterSentiment = ref('');
const currentPage = ref(1);
const pageSize = 20;

const sentimentText = {
  positive: '正面',
  neutral: '中性',
  negative: '负面'
};

const comments = computed(() => analysisStore.comments || []);
const commentsTotal = computed(() => analysisStore.commentsTotal || 0);

const filteredComments = computed(() => {
  let filtered = comments.value;
  if (filterSentiment.value) {
    filtered = filtered.filter(c => c.sentiment === filterSentiment.value);
  }
  // 分页
  const start = (currentPage.value - 1) * pageSize;
  return filtered.slice(start, start + pageSize);
});

const totalPages = computed(() => {
  const total = filterSentiment.value
    ? comments.value.filter(c => c.sentiment === filterSentiment.value).length
    : commentsTotal.value;
  return Math.ceil(total / pageSize) || 1;
});

const formatDate = (dateStr) => {
  try {
    return new Date(dateStr).toLocaleDateString('zh-CN');
  } catch {
    return dateStr;
  }
};

const deleteComment = async (id) => {
  if (confirm('确定要删除这条评论吗？')) {
    try {
      // 调用删除 API
      const response = await fetch(`http://localhost:8000/api/comments/${id}`, {
        method: 'DELETE'
      });
      if (response.ok) {
        // 重新加载评论
        await analysisStore.fetchComments();
      }
    } catch (error) {
      console.error('删除失败:', error);
      alert('删除失败');
    }
  }
};

const reloadComments = async () => {
  currentPage.value = 1;
  await analysisStore.fetchComments();
};

const clearAllComments = async () => {
  if (confirm('确定要清空所有评论吗？此操作不可恢复！')) {
    try {
      const response = await fetch('http://localhost:8000/api/all', {
        method: 'DELETE'
      });
      if (response.ok) {
        currentPage.value = 1;
        await analysisStore.fetchComments();
        alert('所有评论已清空');
      }
    } catch (error) {
      console.error('清空失败:', error);
      alert('清空失败');
    }
  }
};

// 初始化数据
analysisStore.fetchComments();
</script>

<style scoped>
.comments-page {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

h2 {
  margin-bottom: 2rem;
  color: #333;
}

/* 控制栏 */
.controls {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: #f9f9f9;
  border-radius: 8px;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.filter-group label {
  font-weight: 500;
  color: #333;
}

.filter-select {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
}

.filter-select:hover {
  border-color: #667eea;
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s;
}

.btn-primary {
  background: #667eea;
  color: white;
}

.btn-primary:hover {
  background: #764ba2;
}

.btn-danger {
  background: #f45c43;
  color: white;
}

.btn-danger:hover {
  background: #d63814;
}

/* 评论列表 */
.comments-list {
  background: #f9f9f9;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 2rem;
}

.comment-item {
  background: white;
  padding: 1.5rem;
  margin-bottom: 1rem;
  border-left: 4px solid #667eea;
  border-radius: 4px;
  transition: box-shadow 0.3s;
}

.comment-item:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.comment-item.positive {
  border-left-color: #38ef7d;
}

.comment-item.negative {
  border-left-color: #f45c43;
}

.comment-item.neutral {
  border-left-color: #667eea;
}

.comment-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.comment-id {
  font-weight: bold;
  color: #667eea;
  font-size: 0.9rem;
}

.sentiment-badge {
  display: inline-block;
  padding: 0.3rem 0.8rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: bold;
  color: white;
}

.sentiment-badge.positive {
  background-color: #38ef7d;
}

.sentiment-badge.negative {
  background-color: #f45c43;
}

.sentiment-badge.neutral {
  background-color: #667eea;
}

.comment-date {
  font-size: 0.85rem;
  color: #999;
  margin-left: auto;
}

.btn-delete {
  padding: 0.3rem 0.6rem;
  background: #f45c43;
  color: white;
  border: none;
  border-radius: 3px;
  font-size: 0.8rem;
  cursor: pointer;
  transition: background 0.3s;
}

.btn-delete:hover {
  background: #d63814;
}

.comment-body {
  color: #333;
  line-height: 1.6;
}

.comment-body p {
  margin: 0;
  word-wrap: break-word;
}

.no-data {
  text-align: center;
  padding: 2rem;
  color: #999;
}

/* 分页 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #ddd;
}

.page-btn {
  padding: 0.5rem 1rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.3s;
}

.page-btn:hover:not(:disabled) {
  background: #764ba2;
}

.page-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.page-info {
  font-size: 0.9rem;
  color: #666;
  min-width: 80px;
  text-align: center;
}
</style>
