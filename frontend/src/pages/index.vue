<template>
  <div class="dashboard">
    <h2>📊 仪表板</h2>
    
    <!-- 统计卡片 -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-value">{{ stats.total_comments }}</div>
        <div class="stat-label">总评论数</div>
      </div>
      <div class="stat-card positive">
        <div class="stat-value">{{ positivePercentage }}%</div>
        <div class="stat-label">正面评论</div>
      </div>
      <div class="stat-card neutral">
        <div class="stat-value">{{ neutralPercentage }}%</div>
        <div class="stat-label">中性评论</div>
      </div>
      <div class="stat-card negative">
        <div class="stat-value">{{ negativePercentage }}%</div>
        <div class="stat-label">负面评论</div>
      </div>
    </div>

    <!-- 情感分布 -->
    <h3>情感分布</h3>
    <div class="pie-chart">
      <div class="pie-item positive" :style="{ width: positivePercentage + '%' }">正 {{ positivePercentage }}%</div>
      <div class="pie-item neutral" :style="{ width: neutralPercentage + '%' }">中 {{ neutralPercentage }}%</div>
      <div class="pie-item negative" :style="{ width: negativePercentage + '%' }">负 {{ negativePercentage }}%</div>
    </div>

    <!-- 评分显示 -->
    <h3>总体评分</h3>
    <div class="score-container">
      <div class="score-display">
        <span class="score">{{ overallScore }}</span>
        <div class="score-bar">
          <div class="score-fill" :style="{ width: scorePercentage + '%' }"></div>
        </div>
        <p class="score-text">分数范围：-1 到 1</p>
      </div>
    </div>

    <!-- 最新评论样本 -->
    <h3>最新评论样本</h3>
    <div class="comments-sample">
      <div v-for="comment in sampleComments" :key="comment.id" class="comment-item" :class="comment.sentiment">
        <div class="comment-header">
          <span class="sentiment-badge" :class="comment.sentiment">{{ sentimentLabel(comment.sentiment) }}</span>
          <span class="comment-date">{{ formatDate(comment.timestamp) }}</span>
        </div>
        <p class="comment-text">{{ comment.content }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useAnalysisStore } from '@/stores/analysisStore';

const analysisStore = useAnalysisStore();
const stats = ref({ total_comments: 0, positive: 0, neutral: 0, negative: 0 });
const comments = ref([]);

const positivePercentage = computed(() => 
  stats.value.total_comments ? Math.round(stats.value.positive / stats.value.total_comments * 100) : 0
);
const neutralPercentage = computed(() => 
  stats.value.total_comments ? Math.round(stats.value.neutral / stats.value.total_comments * 100) : 0
);
const negativePercentage = computed(() => 
  stats.value.total_comments ? Math.round(stats.value.negative / stats.value.total_comments * 100) : 0
);

const overallScore = computed(() => {
  if (stats.value.total_comments === 0) return '0.00';
  const score = (stats.value.positive - stats.value.negative) / stats.value.total_comments;
  return score.toFixed(2);
});

const scorePercentage = computed(() => {
  const score = parseFloat(overallScore.value);
  return ((score + 1) / 2) * 100;
});

const sampleComments = computed(() => comments.value.slice(0, 5));

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

const fetchStats = async () => {
  try {
    const data = await analysisStore.fetchStats();
    if (data) {
      stats.value = data;
    }
  } catch (error) {
    console.error('获取统计数据失败:', error);
  }
};

const fetchComments = async () => {
  try {
    const data = await analysisStore.fetchComments();
    if (data) {
      comments.value = data;
    }
  } catch (error) {
    console.error('获取评论失败:', error);
  }
};

onMounted(async () => {
  await fetchStats();
  await fetchComments();
  setInterval(fetchStats, 10000);
});
</script>

<style scoped>
.dashboard {
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
  margin: 1.5rem 0 1rem;
  color: #333;
}

/* 统计卡片 */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.stat-card.positive {
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
}

.stat-card.negative {
  background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
}

.stat-card.neutral {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.stat-value {
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: 1rem;
  opacity: 0.9;
}

/* 图表容器 */
.pie-chart {
  display: flex;
  height: 40px;
  border-radius: 8px;
  overflow: hidden;
  gap: 2px;
  background: #f5f5f5;
  padding: 2px;
  margin-bottom: 2rem;
}

.pie-item {
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 0.85rem;
  font-weight: bold;
  transition: all 0.3s;
}

.pie-item.positive {
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
}

.pie-item.negative {
  background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
}

.pie-item.neutral {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* 分值显示 */
.score-container {
  background: #f9f9f9;
  padding: 2rem;
  border-radius: 8px;
  margin-bottom: 2rem;
}

.score-display {
  text-align: center;
}

.score {
  font-size: 3rem;
  font-weight: bold;
  color: #667eea;
  display: block;
  margin-bottom: 1rem;
}

.score-bar {
  width: 100%;
  height: 30px;
  background: #e0e0e0;
  border-radius: 15px;
  overflow: hidden;
  margin-bottom: 1rem;
}

.score-fill {
  height: 100%;
  background: linear-gradient(90deg, #11998e 0%, #38ef7d 100%);
  transition: width 0.3s;
}

.score-text {
  font-size: 1.2rem;
  color: #666;
}

/* 评论样本 */
.comments-sample {
  background: #f9f9f9;
  border-radius: 8px;
  padding: 1.5rem;
}

.comment-item {
  padding: 1rem;
  margin-bottom: 1rem;
  background: white;
  border-left: 4px solid #667eea;
  border-radius: 4px;
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
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.sentiment-badge {
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
  font-size: 0.9rem;
  color: #999;
}

.comment-text {
  margin: 0;
  color: #555;
  line-height: 1.5;
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .stat-value {
    font-size: 1.8rem;
  }
}
</style>
