import { useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { BookOpen, Loader2 } from 'lucide-react'
import { useAuth } from '../contexts/AuthContext'
import { useGroups } from '../hooks/useGroups'
import Button from '../components/common/Button'
import GoogleLoginButton from '../components/auth/GoogleLoginButton'

const JoinGroupPage = () => {
  const { inviteCode } = useParams()
  const navigate = useNavigate()
  const { isAuthenticated, isLoading: authLoading } = useAuth()
  const { joinGroup, isJoining } = useGroups()

  useEffect(() => {
    if (isAuthenticated && inviteCode && !isJoining) {
      joinGroup(inviteCode, {
        onSuccess: (group) => {
          navigate(`/groups/${group.id}`)
        },
      })
    }
  }, [isAuthenticated, inviteCode, joinGroup, isJoining, navigate])

  if (authLoading || (isAuthenticated && isJoining)) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="w-12 h-12 animate-spin text-primary mx-auto mb-4" />
          <p className="text-lg text-text-secondary">
            {isAuthenticated ? 'Joining group...' : 'Loading...'}
          </p>
        </div>
      </div>
    )
  }

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center p-4">
        <div className="max-w-md w-full">
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-primary rounded-full mb-4">
              <BookOpen className="w-8 h-8 text-white" />
            </div>

            <h1 className="text-4xl font-serif font-bold text-text-primary mb-2">
              You're Invited!
            </h1>

            <p className="text-lg text-text-secondary">
              Sign in to join this book club
            </p>
          </div>

          <div className="bg-surface rounded-lg shadow-md border border-border p-8">
            <div className="space-y-6">
              <div className="text-center">
                <p className="text-sm text-text-secondary mb-6">
                  You've been invited to join a book discussion group. Sign in with Google to continue.
                </p>
              </div>

              <GoogleLoginButton />

              <div className="pt-6 border-t border-border">
                <p className="text-xs text-text-tertiary text-center">
                  After signing in, you'll automatically join the group and can start discussing books without spoilers.
                </p>
              </div>
            </div>
          </div>

          <div className="text-center mt-6">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => navigate('/')}
            >
              Go to Homepage
            </Button>
          </div>
        </div>
      </div>
    )
  }

  return null
}

export default JoinGroupPage
