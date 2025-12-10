import api from './api'

export const progressService = {
  async getProgress(groupId, bookId) {
    try {
      const response = await api.get(`/progress/groups/${groupId}/books/${bookId}`)
      return response.data
    } catch (error) {
      // No progress yet is a valid state
      if (error.response?.status === 404) {
        return null
      }
      throw error
    }
  },

  async updateProgress(groupId, bookId, data) {
    const response = await api.post('/progress', {
      group_id: groupId,
      book_id: bookId,
      ...data,
    })
    return response.data
  },

  async getAllProgress(groupId, bookId) {
    const response = await api.get(`/progress/groups/${groupId}/books/${bookId}/all`)
    return response.data
  }
}
