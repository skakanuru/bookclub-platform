import { useEffect } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { BookOpen } from 'lucide-react'
import { useAuth } from '../contexts/AuthContext'
import GoogleLoginButton from '../components/auth/GoogleLoginButton'

const LoginPage = () => {
  const { isAuthenticated } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()

  useEffect(() => {
    if (isAuthenticated) {
      const from = location.state?.from?.pathname || '/'
      navigate(from, { replace: true })
    }
  }, [isAuthenticated, navigate, location])

  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-4">
      <div className="max-w-md w-full">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-primary rounded-full mb-4">
            <BookOpen className="w-8 h-8 text-white" />
          </div>

          <h1 className="text-4xl font-serif font-bold text-text-primary mb-2">
            BookClub
          </h1>

          <p className="text-lg text-text-secondary">
            Discuss books without spoilers
          </p>
        </div>

        <div className="bg-surface rounded-lg shadow-md border border-border p-8">
          <div className="space-y-6">
            <div className="text-center">
              <h2 className="text-xl font-semibold text-text-primary mb-2">
                Welcome back
              </h2>
              <p className="text-sm text-text-secondary">
                Sign in to join your reading groups
              </p>
            </div>

            <GoogleLoginButton />

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
