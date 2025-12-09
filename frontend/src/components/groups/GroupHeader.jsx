import { Users, Settings, Copy, Check } from 'lucide-react'
import { useState } from 'react'
import Button from '../common/Button'
import toast from 'react-hot-toast'

const GroupHeader = ({ group, isAdmin }) => {
  const [copied, setCopied] = useState(false)

  const handleCopyInviteCode = () => {
    const inviteLink = `${window.location.origin}/join/${group.invite_code}`
    navigator.clipboard.writeText(inviteLink)
    setCopied(true)
    toast.success('Invite link copied!')
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="bg-surface border-b border-border p-6">
      <div className="max-w-5xl mx-auto">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <h1 className="text-3xl font-serif font-bold text-text-primary mb-2">
              {group.name}
            </h1>

            {group.description && (
              <p className="text-text-secondary mb-4">{group.description}</p>
            )}

            <div className="flex items-center gap-4 text-sm text-text-tertiary">
              <div className="flex items-center gap-1">
                <Users className="w-4 h-4" />
                <span>{group.member_count || 0} members</span>
              </div>

              <div className="flex items-center gap-2">
                <span className="font-mono text-xs bg-background px-3 py-1 rounded">
                  {group.invite_code}
                </span>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={handleCopyInviteCode}
                  icon={copied ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
                >
                  {copied ? 'Copied!' : 'Copy Invite Link'}
                </Button>
              </div>
            </div>
          </div>

          {isAdmin && (
            <Button variant="ghost" size="sm" icon={<Settings className="w-4 h-4" />}>
              Settings
            </Button>
          )}
        </div>
      </div>
    </div>
  )
}

export default GroupHeader
