import { createContext, useContext, useState, useEffect } from 'react'
import { authService } from '../services/authService'

const AuthContext = createContext(null)

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const initAuth = async () => {
      try {
        if (authService.isAuthenticated()) {
          const storedUser = authService.getStoredUser()
          setUser(storedUser)

          // Verify token is still valid
          try {
            const currentUser = await authService.getCurrentUser()
            setUser(currentUser)
            localStorage.setItem('user', JSON.stringify(currentUser))
          } catch (error) {
            // Token invalid, clear auth
            await logout()
          }
        }
      } catch (error) {
        console.error('Auth initialization error:', error)
      } finally {
        setIsLoading(false)
      }
    }

    initAuth()
  }, [])

  const login = async (email, password) => {
    const { user: newUser } = await authService.emailPasswordLogin(email, password)
    setUser(newUser)
  }

  const googleLogin = async (credential) => {
    const { user: newUser } = await authService.googleLogin(credential)
    setUser(newUser)
  }

  const register = async (email, password, name) => {
    const { user: newUser } = await authService.emailPasswordRegister(email, password, name)
    setUser(newUser)
  }

  const logout = async () => {
    try {
      await authService.logout()
    } catch (error) {
      console.error('Logout error:', error)
    }
    setUser(null)
  }

  const value = {
    user,
    isLoading,
    isAuthenticated: !!user,
    login,
    googleLogin,
    register,
    logout,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}
