import { GoogleLogin } from '@react-oauth/google'
import { useAuth } from '../../contexts/AuthContext'
import { useNavigate } from 'react-router-dom'
import toast from 'react-hot-toast'

const GoogleLoginButton = () => {
  const { googleLogin } = useAuth()
  const navigate = useNavigate()

  const handleSuccess = async (credentialResponse) => {
    try {
      await googleLogin(credentialResponse.credential)
      navigate('/')
    } catch (error) {
      console.error('Login error:', error)
      toast.error('Failed to login. Please try again.')
    }
  }

  const handleError = () => {
    toast.error('Login failed. Please try again.')
  }

  return (
    <div className="flex justify-center">
      <GoogleLogin
        onSuccess={handleSuccess}
        onError={handleError}
        useOneTap
        size="large"
        theme="outline"
        text="continue_with"
      />
    </div>
  )
}

export default GoogleLoginButton
