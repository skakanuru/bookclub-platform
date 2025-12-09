import api from './api'

export const progressService = {
  async getProgress(groupId, bookId) {
    const response = await api.get(`/progress/${groupId}/${bookId}`)
    return response.data
  },

  async updateProgress(groupId, bookId, data) {
    const response = await api.put(`/progress/${groupId}/${bookId}`, data)
    return response.data
  },

  async getAllProgress(groupId, bookId) {
    const response = await api.get(`/progress/${groupId}/${bookId}/all`)
    return response.data
  }
}
