import api from './api'

export const commentService = {
  async getComments(groupId, bookId) {
    const response = await api.get(`/comments/groups/${groupId}/books/${bookId}/comments`)
    return response.data
  },

  async createComment(groupId, bookId, data) {
    // Backend create endpoint lives at /comments/groups/{groupId}/comments; book_id is in payload
    const response = await api.post(`/comments/groups/${groupId}/comments`, data)
    return response.data
  },

  async getCommentsAhead(groupId, bookId) {
    const response = await api.get(`/comments/groups/${groupId}/books/${bookId}/comments/ahead`)
    return response.data
  },

  async likeComment(commentId) {
    const response = await api.post(`/comments/${commentId}/like`)
    return response.data
  },

  async unlikeComment(commentId) {
    const response = await api.delete(`/comments/${commentId}/like`)
    return response.data
  },

  async reportComment(commentId, reason) {
    const response = await api.post(`/comments/${commentId}/report`, { reason })
    return response.data
  }
}
