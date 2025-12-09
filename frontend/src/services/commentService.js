import api from './api'

export const commentService = {
  async getComments(groupId, bookId) {
    const response = await api.get(`/groups/${groupId}/books/${bookId}/comments`)
    return response.data
  },

  async createComment(groupId, bookId, data) {
    const response = await api.post(`/groups/${groupId}/books/${bookId}/comments`, data)
    return response.data
  },

  async getCommentsAhead(groupId, bookId) {
    const response = await api.get(`/groups/${groupId}/books/${bookId}/comments/ahead`)
    return response.data
  },

  async likeComment(commentId) {
    const response = await api.post(`/comments/${commentId}/like`)
    return response.data
  },

  async reportComment(commentId, reason) {
    const response = await api.post(`/comments/${commentId}/report`, { reason })
    return response.data
  }
}
