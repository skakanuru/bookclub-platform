import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Plus, Users, LogOut } from 'lucide-react'
import { useAuth } from '../contexts/AuthContext'
import { useGroups } from '../hooks/useGroups'
import Button from '../components/common/Button'
import GroupCard from '../components/groups/GroupCard'
import CreateGroupModal from '../components/groups/CreateGroupModal'
import LoadingSpinner from '../components/common/LoadingSpinner'
import Avatar from '../components/common/Avatar'

const GroupsPage = () => {
  const { user, logout } = useAuth()
  const { groups, isLoading, createGroup, isCreating } = useGroups()
  const [showCreateModal, setShowCreateModal] = useState(false)
  const navigate = useNavigate()

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <LoadingSpinner size="lg" />
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background">
      <header className="bg-surface border-b border-border">
        <div className="max-w-5xl mx-auto px-4 py-4 flex items-center justify-between">
          <h1 className="text-2xl font-serif font-bold text-text-primary">
            My Groups
          </h1>

          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2">
              <Avatar src={user?.avatar_url} alt={user?.name} size="sm" />
              <span className="text-sm font-medium text-text-primary hidden sm:block">
                {user?.name}
              </span>
            </div>

            <Button
              variant="ghost"
              size="sm"
              onClick={logout}
              icon={<LogOut className="w-4 h-4" />}
            >
              <span className="hidden sm:inline">Logout</span>
            </Button>
          </div>
        </div>
      </header>

      <div className="max-w-5xl mx-auto px-4 py-8">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-xl font-semibold text-text-primary">
              Your Book Clubs
            </h2>
            <p className="text-sm text-text-secondary mt-1">
              {groups.length} {groups.length === 1 ? 'group' : 'groups'}
            </p>
          </div>

          <Button
            onClick={() => setShowCreateModal(true)}
            icon={<Plus className="w-4 h-4" />}
          >
            Create Group
          </Button>
        </div>

        {groups.length === 0 ? (
          <div className="text-center py-16">
            <Users className="w-16 h-16 text-text-tertiary mx-auto mb-4" />
            <h3 className="text-xl font-serif font-semibold text-text-primary mb-2">
              No groups yet
            </h3>
            <p className="text-text-secondary mb-6 max-w-md mx-auto">
              Create your first book club or ask a friend for an invite link to get started.
            </p>
            <Button
              onClick={() => setShowCreateModal(true)}
              icon={<Plus className="w-4 h-4" />}
            >
              Create Your First Group
            </Button>
          </div>
        ) : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {groups.map((group) => (
              <GroupCard key={group.id} group={group} />
            ))}
          </div>
        )}
      </div>

      <CreateGroupModal
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        onCreate={createGroup}
        onCreated={(group) => navigate(`/groups/${group.id}`)}
        isCreating={isCreating}
      />
    </div>
  )
}

export default GroupsPage
