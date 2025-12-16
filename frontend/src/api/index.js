/**
 * API 调用模块 - 简化版
 */
import http from './http.js'

// ============ 统计数据 ============
export const getStats = () => http.get('/stats')

// ============ 评论管理 ============
export const getComments = (skip = 0, limit = 50, sentiment = null) => {
  return http.get('/comments', { params: { skip, limit, sentiment } })
}

export const getComment = (id) => http.get(`/comments/${id}`)

export const createComment = (content, sentiment = 'neutral') => {
  return http.post('/comments', null, { params: { content, sentiment } })
}

export const deleteComment = (id) => http.delete(`/comments/${id}`)

// ============ 数据管理 ============
export const reloadData = () => http.post('/reload')

export const deleteAllData = () => http.delete('/all')

export default http