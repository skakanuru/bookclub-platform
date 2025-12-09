import { useState } from 'react'
import { Copy, Check, Share2 } from 'lucide-react'
import Button from '../common/Button'
import Card from '../common/Card'
import toast from 'react-hot-toast'

const InviteCodeDisplay = ({ inviteCode, groupName }) => {
  const [copied, setCopied] = useState(false)
  const inviteLink = `${window.location.origin}/join/${inviteCode}`

  const handleCopy = () => {
    navigator.clipboard.writeText(inviteLink)
    setCopied(true)
    toast.success('Invite link copied!')
    setTimeout(() => setCopied(false), 2000)
  }

  const handleShare = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: `Join ${groupName}`,
          text: `You've been invited to join ${groupName} on BookClub!`,
          url: inviteLink,
        })
      } catch (error) {
        if (error.name !== 'AbortError') {
          console.error('Share error:', error)
        }
      }
    } else {
      handleCopy()
    }
  }

  return (
    <Card>
      <div className="space-y-4">
        <div>
          <h3 className="text-lg font-semibold text-text-primary mb-1">
            Invite Members
          </h3>
          <p className="text-sm text-text-secondary">
            Share this link to invite people to your group
          </p>
        </div>

        <div className="flex items-center gap-2">
          <div className="flex-1 bg-background px-4 py-2 rounded-lg font-mono text-sm break-all">
            {inviteLink}
          </div>

          <Button
            variant="outline"
            size="sm"
            onClick={handleCopy}
            icon={copied ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
          >
            {copied ? 'Copied' : 'Copy'}
          </Button>

          {navigator.share && (
            <Button
              variant="outline"
              size="sm"
              onClick={handleShare}
              icon={<Share2 className="w-4 h-4" />}
            >
              Share
            </Button>
          )}
        </div>

        <div className="pt-2 border-t border-border">
          <p className="text-xs text-text-tertiary">
            Invite code: <span className="font-mono">{inviteCode}</span>
          </p>
        </div>
      </div>
    </Card>
  )
}

export default InviteCodeDisplay
