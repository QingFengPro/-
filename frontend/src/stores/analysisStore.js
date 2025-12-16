import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getStats, getComments } from '../api/index.js'

export const useAnalysisStore = defineStore('analysis', () => {
  // 状态
  const stats = ref(null)
  const comments = ref([])
  const commentsTotal = ref(0)
  const sentimentRatio = ref({ positive: 0, negative: 0, neutral: 0 })
  const loading = ref(false)
  const error = ref(null)

  // 获取统计数据
  const fetchStats = async () => {
    loading.value = true
    error.value = null
    try {
      const data = await getStats()
      // 兼容后端返回字段，映射为前端通用字段名
      if (data) {
        stats.value = {
          total_comments: data.total_comments || (data.positive_count + data.negative_count + data.neutral_count) || 0,
          positive: data.positive_count || 0,
          negative: data.negative_count || 0,
          neutral: data.neutral_count || 0,
          avg_sentiment_score: data.avg_sentiment_score || 0
        }
        // 也保存 ratio 供分页显示使用
        sentimentRatio.value = data.sentiment_ratio || { positive: 0, negative: 0, neutral: 0 }
      }
      return stats.value
    } catch (err) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  // 获取评论（改为加载所有或足够多的条数）
  const fetchComments = async (skip = 0, limit = 10000, sentiment = null) => {
    try {
      const data = await getComments(skip, limit, sentiment)
      comments.value = data.data || []
      commentsTotal.value = data.total || 0
      return data
    } catch (err) {
      error.value = err.message
    }
  }

  return {
    stats,
    comments,
    commentsTotal,
    sentimentRatio,
    loading,
    error,
    fetchStats,
    fetchComments
  }
})
