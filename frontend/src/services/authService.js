import api from './api'

export const authService = {
  async googleLogin(credential) {
    const response = await api.post('/auth/google', { credential })
    const { access_token, user } = response.data

    localStorage.setItem('accessToken', access_token)
    localStorage.setItem('user', JSON.stringify(user))

    return { token: access_token, user }
  },

  async getCurrentUser() {
    const response = await api.get('/auth/me')
    return response.data
  },

  async logout() {
    await api.post('/auth/logout')
    localStorage.removeItem('accessToken')
    localStorage.removeItem('user')
  },

  getStoredUser() {
    const userStr = localStorage.getItem('user')
    return userStr ? JSON.parse(userStr) : null
  },

  isAuthenticated() {
    return !!localStorage.getItem('accessToken')
  }
}
