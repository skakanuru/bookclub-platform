import { Bell, ChevronRight } from 'lucide-react'
import { useState } from 'react'
import { formatDistanceToNow } from 'date-fns'
import Button from '../common/Button'
import Modal from '../common/Modal'
import Card from '../common/Card'

const AheadNotifications = ({ commentsAhead }) => {
  const [showModal, setShowModal] = useState(false)

  if (!commentsAhead || commentsAhead.length === 0) {
    return null
  }

  return (
    <>
      <Card
        className="bg-accent bg-opacity-10 border-accent cursor-pointer hover:bg-opacity-20 transition-colors"
        onClick={() => setShowModal(true)}
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-accent rounded-full">
              <Bell className="w-5 h-5 text-white" />
            </div>
            <div>
              <p className="font-semibold text-text-primary">
                {commentsAhead.length} {commentsAhead.length === 1 ? 'comment' : 'comments'} ahead
              </p>
              <p className="text-sm text-text-secondary">
                Keep reading to unlock these discussions
              </p>
            </div>
          </div>
          <ChevronRight className="w-5 h-5 text-text-tertiary" />
        </div>
      </Card>

      <Modal
        isOpen={showModal}
        onClose={() => setShowModal(false)}
        title="Comments Ahead"
        size="md"
      >
        <div className="space-y-4">
          <p className="text-sm text-text-secondary mb-4">
            These comments are from readers ahead of your current progress. Keep reading to unlock them!
          </p>

          <div className="space-y-3 max-h-96 overflow-y-auto custom-scrollbar">
            {commentsAhead.map((comment) => (
              <div
                key={comment.id}
                className="p-4 border border-border rounded-lg bg-background"
              >
                <div className="flex items-start justify-between mb-2">
                  <div>
                    <p className="font-semibold text-text-primary">
                      {comment.user_name}
                    </p>
                    <p className="text-xs text-text-tertiary">
                      {formatDistanceToNow(new Date(comment.created_at), { addSuffix: true })}
                    </p>
                  </div>
                  <span className="text-xs font-mono bg-primary bg-opacity-10 text-primary px-2 py-1 rounded">
                    Page {comment.progress_page} · {comment.progress_percentage?.toFixed(0)}%
                  </span>
                </div>

                <div className="flex items-center gap-2 text-sm text-text-secondary">
                  <span>💬</span>
                  <span>Comment hidden until you reach this point</span>
                </div>
              </div>
            ))}
          </div>

          <div className="pt-4 border-t border-border">
            <Button variant="primary" onClick={() => setShowModal(false)} className="w-full">
              Continue Reading
            </Button>
          </div>
        </div>
      </Modal>
    </>
  )
}

export default AheadNotifications
