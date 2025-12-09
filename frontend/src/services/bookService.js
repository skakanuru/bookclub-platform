import api from './api'

export const bookService = {
  async searchBooks(query) {
    const response = await api.get(`/books/search?q=${encodeURIComponent(query)}`)
    return response.data
  },

  async getBook(bookId) {
    const response = await api.get(`/books/${bookId}`)
    return response.data
  },

  async createBook(data) {
    const response = await api.post('/books', data)
    return response.data
  }
}
