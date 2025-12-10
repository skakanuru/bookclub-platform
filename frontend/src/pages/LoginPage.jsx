import { useState, useEffect } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { BookOpen } from 'lucide-react'
import { useAuth } from '../contexts/AuthContext'
import Button from '../components/common/Button'
import toast from 'react-hot-toast'
import GoogleLoginButton from '../components/auth/GoogleLoginButton'

const LoginPage = () => {
  const { isAuthenticated, login, register } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const [isRegistering, setIsRegistering] = useState(false)
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    name: ''
  })
  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    if (isAuthenticated) {
      const from = location.state?.from?.pathname || '/'
      navigate(from, { replace: true })
    }
  }, [isAuthenticated, navigate, location])

  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsLoading(true)

    try {
      if (isRegistering) {
        if (!formData.name) {
          toast.error('Please enter your name')
          return
        }
        await register(formData.email, formData.password, formData.name)
        toast.success('Account created successfully!')
      } else {
        await login(formData.email, formData.password)
        toast.success('Welcome back!')
      }
    } catch (error) {
      console.error('Auth error:', error)
      toast.error(error.response?.data?.detail || 'Authentication failed')
    } finally {
      setIsLoading(false)
    }
  }

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  const toggleMode = () => {
    setIsRegistering(!isRegistering)
    setFormData({ email: '', password: '', name: '' })
  }

  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-4">
      <div className="max-w-md w-full">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-primary rounded-full mb-4">
            <BookOpen className="w-8 h-8 text-white" />
          </div>

          <h1 className="text-4xl font-serif font-bold text-text-primary mb-2">
            Bookly
          </h1>

          <p className="text-lg text-text-secondary">
            Discuss books without spoilers
          </p>
        </div>

        <div className="bg-surface rounded-lg shadow-md border border-border p-8">
          <div className="space-y-6">
            <div className="text-center">
              <h2 className="text-xl font-semibold text-text-primary mb-2">
                {isRegistering ? 'Create an account' : 'Welcome back'}
              </h2>
              <p className="text-sm text-text-secondary">
                {isRegistering ? 'Start your reading journey' : 'Sign in to join your reading groups'}
              </p>
            </div>

            <div className="space-y-3">
              <GoogleLoginButton />
              <div className="flex items-center gap-2 text-xs text-text-tertiary">
                <div className="flex-1 h-px bg-border" />
                <span>or use email</span>
                <div className="flex-1 h-px bg-border" />
              </div>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4">
              {isRegistering && (
                <div>
                  <label htmlFor="name" className="block text-sm font-medium text-text-primary mb-1">
                    Full Name
                  </label>
                  <input
                    type="text"
                    id="name"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    required={isRegistering}
                    className="w-full px-4 py-2 bg-background border border-border rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent text-text-primary"
                    placeholder="Enter your name"
                  />
                </div>
              )}

              <div>
                <label htmlFor="email" className="block text-sm font-medium text-text-primary mb-1">
                  Email
                </label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-2 bg-background border border-border rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent text-text-primary"
                  placeholder="Enter your email"
                />
              </div>

              <div>
                <label htmlFor="password" className="block text-sm font-medium text-text-primary mb-1">
                  Password
                </label>
                <input
                  type="password"
                  id="password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  required
                  minLength={6}
                  className="w-full px-4 py-2 bg-background border border-border rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent text-text-primary"
                  placeholder={isRegistering ? "At least 6 characters" : "Enter your password"}
                />
              </div>

              <Button
                type="submit"
                variant="primary"
                className="w-full"
                disabled={isLoading}
              >
                {isLoading ? 'Please wait...' : (isRegistering ? 'Create Account' : 'Sign In')}
              </Button>
            </form>

            <div className="text-center">
              <button
                type="button"
                onClick={toggleMode}
                className="text-sm text-primary hover:underline"
              >
                {isRegistering ? 'Already have an account? Sign in' : "Don't have an account? Sign up"}
              </button>
            </div>

            <div className="pt-6 border-t border-border">
              <div className="space-y-3 text-xs text-text-tertiary">
                <p className="flex items-start gap-2">
                  <span>✓</span>
                  <span>Only see comments from readers at or behind your progress</span>
                </p>
                <p className="flex items-start gap-2">
                  <span>✓</span>
                  <span>Get notified about discussions ahead</span>
                </p>
                <p className="flex items-start gap-2">
                  <span>✓</span>
                  <span>Join groups with a simple invite link</span>
                </p>
              </div>
            </div>
          </div>
        </div>

        <p className="text-center text-xs text-text-tertiary mt-6">
          By signing in, you agree to our Terms of Service and Privacy Policy
        </p>
      </div>
    </div>
  )
}

export default LoginPage
