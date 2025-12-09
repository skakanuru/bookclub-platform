import { useNavigate } from 'react-router-dom'
import { BookOpen, Users, Plus } from 'lucide-react'
import { useAuth } from '../contexts/AuthContext'
import Button from '../components/common/Button'

const HomePage = () => {
  const { user } = useAuth()
  const navigate = useNavigate()

  return (
    <div className="min-h-screen bg-background">
      <div className="max-w-5xl mx-auto px-4 py-8">
        <header className="mb-12 text-center">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-primary rounded-full mb-4">
            <BookOpen className="w-10 h-10 text-white" />
          </div>

          <h1 className="text-5xl font-serif font-bold text-text-primary mb-3">
            Welcome to BookClub
          </h1>

          <p className="text-xl text-text-secondary max-w-2xl mx-auto">
            Discuss books without spoilers. Only see comments from readers at or behind your current progress.
          </p>
        </header>

        <div className="grid md:grid-cols-2 gap-6 mb-12">
          <div className="bg-surface rounded-lg shadow-sm border border-border p-8 hover:shadow-md transition-shadow">
            <div className="w-12 h-12 bg-primary bg-opacity-10 rounded-full flex items-center justify-center mb-4">
              <Users className="w-6 h-6 text-primary" />
            </div>

            <h2 className="text-2xl font-serif font-bold text-text-primary mb-3">
              Your Groups
            </h2>

            <p className="text-text-secondary mb-6">
              View and manage your book clubs. See what everyone's reading and join the discussion.
            </p>

            <Button onClick={() => navigate('/groups')} className="w-full">
              View My Groups
            </Button>
          </div>

          <div className="bg-surface rounded-lg shadow-sm border border-border p-8 hover:shadow-md transition-shadow">
            <div className="w-12 h-12 bg-accent bg-opacity-20 rounded-full flex items-center justify-center mb-4">
              <Plus className="w-6 h-6 text-accent" />
            </div>

            <h2 className="text-2xl font-serif font-bold text-text-primary mb-3">
              Create a Group
            </h2>

            <p className="text-text-secondary mb-6">
              Start your own book club. Invite friends and begin reading together without spoilers.
            </p>

            <Button variant="secondary" onClick={() => navigate('/groups')} className="w-full">
              Get Started
            </Button>
          </div>
        </div>

        <div className="bg-primary bg-opacity-5 rounded-lg p-8 border border-primary border-opacity-20">
          <h2 className="text-2xl font-serif font-bold text-text-primary mb-6 text-center">
            How It Works
          </h2>

          <div className="grid md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="w-12 h-12 bg-primary rounded-full flex items-center justify-center text-white font-bold text-xl mx-auto mb-3">
                1
              </div>
              <h3 className="font-semibold text-text-primary mb-2">
                Join or Create a Group
              </h3>
              <p className="text-sm text-text-secondary">
                Use an invite link or start your own book club
              </p>
            </div>

            <div className="text-center">
              <div className="w-12 h-12 bg-primary rounded-full flex items-center justify-center text-white font-bold text-xl mx-auto mb-3">
                2
              </div>
              <h3 className="font-semibold text-text-primary mb-2">
                Set Your Progress
              </h3>
              <p className="text-sm text-text-secondary">
                Track which page you're on and your edition's page count
              </p>
            </div>

            <div className="text-center">
              <div className="w-12 h-12 bg-primary rounded-full flex items-center justify-center text-white font-bold text-xl mx-auto mb-3">
                3
              </div>
              <h3 className="font-semibold text-text-primary mb-2">
                Discuss Freely
              </h3>
              <p className="text-sm text-text-secondary">
                See only comments from your reading level or behind
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default HomePage
