<template>
  <div class="analysis-page">
    <h2>📈 情感分析</h2>

    <div class="analysis-content">
      <!-- 时间范围选择 -->
      <div class="filters">
        <div class="filter-group">
          <label>筛选条件：</label>
          <select v-model="selectedSentiment" class="filter-select">
            <option value="">全部情感</option>
            <option value="positive">正面</option>
            <option value="neutral">中性</option>
            <option value="negative">负面</option>
          </select>
        </div>
      </div>

      <!-- 统计摘要（使用后端统计，避免受分页影响） -->
      <div class="summary-cards">
        <div class="summary-card">
          <div class="card-label">总评论数</div>
          <div class="card-value">{{ stats?.total_comments || commentsTotal || 0 }}</div>
        </div>
        <div class="summary-card">
          <div class="card-label">正面比例</div>
          <div class="card-value">{{ sentimentRatio?.positive || stats?.sentiment_ratio?.positive || 0 }}%</div>
        </div>
        <div class="summary-card">
          <div class="card-label">中性比例</div>
          <div class="card-value">{{ sentimentRatio?.neutral || stats?.sentiment_ratio?.neutral || 0 }}%</div>
        </div>
        <div class="summary-card">
          <div class="card-label">负面比例</div>
          <div class="card-value">{{ sentimentRatio?.negative || stats?.sentiment_ratio?.negative || 0 }}%</div>
        </div>
      </div>

      <!-- 详细评论列表 -->
      <h3>详细评论</h3>
      <div class="comments-list">
        <div v-for="comment in paginatedComments" :key="comment.id" class="comment-card" :class="comment.sentiment">
          <div class="comment-sentiment">
            <span class="sentiment-label" :class="comment.sentiment">{{ sentimentLabel(comment.sentiment) }}</span>
          </div>
          <div class="comment-body">
            <p class="comment-text">{{ comment.content }}</p>
            <div class="comment-meta">
              <span class="comment-date">{{ formatDate(comment.timestamp) }}</span>
            </div>
          </div>
        </div>
        <div v-if="filteredComments.length === 0" class="no-data">
          <p>暂无评论数据</p>
        </div>
      </div>

      <!-- 分页 -->
      <div class="pagination" v-if="filteredComments.length > 0">
        <button :disabled="currentPage === 1" @click="currentPage--" class="page-btn">上一页</button>
        <span class="page-info">{{ currentPage }} / {{ totalPages }}</span>
        <button :disabled="currentPage === totalPages" @click="currentPage++" class="page-btn">下一页</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useAnalysisStore } from '@/stores/analysisStore';

const analysisStore = useAnalysisStore();
const selectedSentiment = ref('');
const currentPage = ref(1);
const pageSize = 20;

const stats = computed(() => analysisStore.stats || {});
const comments = computed(() => analysisStore.comments || []);
const sentimentRatio = computed(() => analysisStore.sentimentRatio || { positive: 0, negative: 0, neutral: 0 });
const commentsTotal = computed(() => analysisStore.commentsTotal || 0);

const filteredComments = computed(() => {
  if (!selectedSentiment.value) {
    return comments.value;
  }
  return comments.value.filter(c => c.sentiment === selectedSentiment.value);
});

const totalPages = computed(() => Math.ceil(filteredComments.value.length / pageSize) || 1);

const paginatedComments = computed(() => {
  const start = (currentPage.value - 1) * pageSize;
  return filteredComments.value.slice(start, start + pageSize);
});

// 使用后端返回的比率，避免受前端分页影响
const positiveRate = computed(() => sentimentRatio.value?.positive || 0);
const neutralRate = computed(() => sentimentRatio.value?.neutral || 0);
const negativeRate = computed(() => sentimentRatio.value?.negative || 0);

const sentimentLabel = (sentiment) => {
  const labels = { positive: '正面', neutral: '中性', negative: '负面' };
  return labels[sentiment] || sentiment;
};

const formatDate = (dateStr) => {
  try {
    return new Date(dateStr).toLocaleDateString('zh-CN');
  } catch {
    return dateStr;
  }
};

// 加载数据
analysisStore.fetchStats();
analysisStore.fetchComments();
</script>

<style scoped>
.analysis-page {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

h2 {
  margin-bottom: 2rem;
  color: #333;
}

h3 {
  margin: 2rem 0 1rem;
  color: #333;
  font-size: 1.2rem;
}

.analysis-content {
  width: 100%;
}

/* 筛选器 */
.filters {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: #f9f9f9;
  border-radius: 8px;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 1rem;
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

/* 统计摘要 */
.summary-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.summary-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1.5rem;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.card-label {
  font-size: 0.9rem;
  opacity: 0.9;
  margin-bottom: 0.5rem;
}

.card-value {
  font-size: 1.8rem;
  font-weight: bold;
}

/* 评论列表 */
.comments-list {
  background: #f9f9f9;
  border-radius: 8px;
  padding: 1rem;
}

.comment-card {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  margin-bottom: 1rem;
  background: white;
  border-left: 4px solid #667eea;
  border-radius: 4px;
  transition: box-shadow 0.3s;
}

.comment-card:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.comment-card.positive {
  border-left-color: #38ef7d;
}

.comment-card.negative {
  border-left-color: #f45c43;
}

.comment-card.neutral {
  border-left-color: #667eea;
}

.comment-sentiment {
  flex-shrink: 0;
}

.sentiment-label {
  display: inline-block;
  padding: 0.3rem 0.8rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: bold;
  color: white;
}

.sentiment-label.positive {
  background-color: #38ef7d;
}

.sentiment-label.negative {
  background-color: #f45c43;
}

.sentiment-label.neutral {
  background-color: #667eea;
}

.comment-body {
  flex: 1;
}

.comment-text {
  margin: 0 0 0.5rem 0;
  color: #333;
  line-height: 1.6;
  word-wrap: break-word;
}

.comment-meta {
  font-size: 0.85rem;
  color: #999;
}

.comment-date {
  margin-right: 1rem;
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
  margin-top: 2rem;
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

@media (max-width: 768px) {
  .summary-cards {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .comment-card {
    flex-direction: column;
  }
}
</style>
