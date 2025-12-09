import api from './api'

export const groupService = {
  async createGroup(data) {
    const response = await api.post('/groups', data)
    return response.data
  },

  async getMyGroups() {
    const response = await api.get('/groups/my-groups')
    return response.data
  },

  async getGroup(groupId) {
    const response = await api.get(`/groups/${groupId}`)
    return response.data
  },

  async updateGroup(groupId, data) {
    const response = await api.put(`/groups/${groupId}`, data)
    return response.data
  },

  async joinGroup(inviteCode) {
    const response = await api.post('/groups/join', { invite_code: inviteCode })
    return response.data
  },

  async removeMember(groupId, userId) {
    const response = await api.delete(`/groups/${groupId}/members/${userId}`)
    return response.data
  },

  async getGroupBooks(groupId) {
    const response = await api.get(`/groups/${groupId}/books`)
    return response.data
  },

  async addBookToGroup(groupId, bookId) {
    const response = await api.post(`/groups/${groupId}/books`, { book_id: bookId })
    return response.data
  }
}
