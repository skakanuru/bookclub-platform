import { Heart, Flag } from 'lucide-react'
import { formatDistanceToNow } from 'date-fns'
import { useState } from 'react'
import Avatar from '../common/Avatar'
import Button from '../common/Button'
import Modal from '../common/Modal'

const CommentCard = ({ comment, onLike, onReport, onReply, currentUserId, currentProgress, depth = 0 }) => {
  const [showReportModal, setShowReportModal] = useState(false)
  const [reportReason, setReportReason] = useState('')
  const [showReply, setShowReply] = useState(false)
  const [replyText, setReplyText] = useState('')

  const handleReport = () => {
    onReport({ commentId: comment.id, reason: reportReason })
    setShowReportModal(false)
    setReportReason('')
  }

  const isOwnComment = comment.user_id === currentUserId
  const progressPct = Number(comment.progress_percentage || 0)
  const createdDate = (() => {
    if (!comment.created_at) return new Date()
    const str = comment.created_at
    const hasTZ = /[Zz]|[+-]\d{2}:?\d{2}$/.test(str)
    return new Date(hasTZ ? str : `${str}Z`)
  })()

  const containerClasses = depth > 0
    ? 'bg-surface border border-border rounded-lg p-3 ml-4 sm:ml-8'
    : 'bg-surface border border-border rounded-lg p-4'

  return (
    <>
      <div className={containerClasses}>
        <div className="flex gap-3">
          <Avatar src={comment.user_avatar_url} alt={comment.user_name} size="md" />

          <div className="flex-1">
            <div className="flex items-start justify-between mb-2">
              <div>
                <p className="font-semibold text-text-primary">{comment.user_name}</p>
                <div className="flex items-center gap-2 text-xs text-text-tertiary">
                  <span className="font-mono bg-background px-2 py-0.5 rounded">
                    Page {comment.progress_page} · {progressPct.toFixed(0)}%
                  </span>
                  <span>·</span>
                  <span>
                    {formatDistanceToNow(createdDate, { addSuffix: true })}
                  </span>
                </div>
              </div>
            </div>

            <p className="comment-content text-text-primary mb-3 whitespace-pre-wrap">
              {comment.content}
            </p>

            <div className="flex items-center gap-3">
              <button
                onClick={() => onLike({ commentId: comment.id, liked: !!comment.user_has_liked })}
                className={`flex items-center gap-1 text-sm transition-colors ${
                  comment.user_has_liked
                    ? 'text-danger'
                    : 'text-text-tertiary hover:text-danger'
                }`}
              >
                <Heart
                  className="w-4 h-4"
                  fill={comment.user_has_liked ? 'currentColor' : 'none'}
                />
                <span>{comment.like_count || 0}</span>
              </button>

              {onReply && currentProgress && (
                <button
                  onClick={() => setShowReply((prev) => !prev)}
                  className="flex items-center gap-1 text-sm text-text-tertiary hover:text-primary transition-colors"
                >
                  Reply
                </button>
              )}

              {!isOwnComment && (
                <button
                  onClick={() => setShowReportModal(true)}
                  className="flex items-center gap-1 text-sm text-text-tertiary hover:text-danger transition-colors"
                >
                  <Flag className="w-4 h-4" />
                  <span>Report</span>
                </button>
              )}
            </div>

            {showReply && currentProgress && (
              <div className="mt-3 space-y-2">
                <textarea
                  value={replyText}
                  onChange={(e) => setReplyText(e.target.value)}
                  rows={3}
                  className="w-full px-3 py-2 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent text-sm"
                  placeholder="Write a reply..."
                />
                <div className="flex gap-2 justify-end">
                  <Button variant="ghost" size="sm" onClick={() => { setShowReply(false); setReplyText('') }}>
                    Cancel
                  </Button>
                  <Button
                    size="sm"
                    disabled={!replyText.trim()}
                    onClick={() => {
                      onReply({
                        content: replyText.trim(),
                        parent_comment_id: comment.id,
                        progress_page: currentProgress.current_page,
                        progress_total_pages: currentProgress.total_pages,
                        book_id: comment.book_id,
                      }, {
                        onSuccess: () => {
                          setReplyText('')
                          setShowReply(false)
                        }
                      })
                    }}
                  >
                    Reply
                  </Button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      <Modal
        isOpen={showReportModal}
        onClose={() => setShowReportModal(false)}
        title="Report Comment"
        footer={
          <>
            <Button variant="ghost" onClick={() => setShowReportModal(false)}>
              Cancel
            </Button>
            <Button
              variant="danger"
              onClick={handleReport}
              disabled={!reportReason.trim()}
            >
              Submit Report
            </Button>
          </>
        }
      >
        <div className="space-y-4">
          <p className="text-sm text-text-secondary">
            Please tell us why you're reporting this comment. We take spoilers seriously.
          </p>

          <textarea
            value={reportReason}
            onChange={(e) => setReportReason(e.target.value)}
            placeholder="This comment contains spoilers about..."
            rows={4}
            className="w-full px-4 py-2 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all resize-none"
            required
          />
        </div>
      </Modal>
    </>
  )
}

export default CommentCard
