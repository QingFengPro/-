import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getStats } from '../api/index.js'

export const useTopicStore = defineStore('topic', () => {
  // 状态
  const stats = ref(null)
  const loading = ref(false)
  const error = ref(null)

  // 获取统计数据
  const fetchStats = async () => {
    loading.value = true
    error.value = null
    try {
      const data = await getStats()
      stats.value = data
      return data
    } catch (err) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  return {
    stats,
    loading,
    error,
    fetchStats
  }
})
