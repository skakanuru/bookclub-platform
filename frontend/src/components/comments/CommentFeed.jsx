import { useMemo } from 'react'
import { useState } from 'react'
import CommentCard from './CommentCard'
import LoadingSpinner from '../common/LoadingSpinner'
import { MessageSquare, ChevronDown, ChevronRight } from 'lucide-react'

const CommentThread = ({ comment, replies, onLike, onReport, onReply, currentUserId, currentProgress, depth = 0 }) => {
  const [showReplies, setShowReplies] = useState(true)
  const hasReplies = replies && replies.length > 0

  return (
    <div className="space-y-2">
      <CommentCard
        comment={comment}
        onLike={onLike}
        onReport={onReport}
        onReply={onReply}
        currentUserId={currentUserId}
        currentProgress={currentProgress}
        depth={depth}
      />

      {hasReplies && (
        <div className={`ml-4 sm:ml-8 border-l border-border pl-3 sm:pl-4 space-y-2`}>
          <button
            type="button"
            className="flex items-center gap-2 text-xs text-text-tertiary hover:text-text-primary transition-colors"
            onClick={() => setShowReplies((prev) => !prev)}
          >
            {showReplies ? <ChevronDown className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
            <span>{replies.length} {replies.length === 1 ? 'reply' : 'replies'}</span>
          </button>

          {showReplies && (
            <div className="space-y-2">
              {replies.map((child) => (
                <CommentThread
                  key={child.id}
                  comment={child}
                  replies={child.replies || []}
                  onLike={onLike}
                  onReport={onReport}
                  onReply={onReply}
                  currentUserId={currentUserId}
                  currentProgress={currentProgress}
                  depth={depth + 1}
                />
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  )
}

const CommentFeed = ({ comments, isLoading, onLike, onReport, onReply, currentUserId, currentProgress }) => {
  if (isLoading) {
    return (
      <div className="flex justify-center py-12">
        <LoadingSpinner size="lg" />
      </div>
    )
  }

  if (!comments || comments.length === 0) {
    return (
      <div className="text-center py-12">
        <MessageSquare className="w-12 h-12 text-text-tertiary mx-auto mb-3" />
        <p className="text-text-secondary">No comments yet. Be the first to share your thoughts!</p>
      </div>
    )
  }

  const threaded = useMemo(() => {
    const map = new Map()
    comments.forEach((c) => map.set(c.id, { ...c, replies: [] }))
    const roots = []
    map.forEach((c) => {
      if (c.parent_comment_id && map.has(c.parent_comment_id)) {
        map.get(c.parent_comment_id).replies.push(c)
      } else {
        roots.push(c)
      }
    })
    return roots
  }, [comments])

  return (
    <div className="space-y-4">
      {threaded.map((comment) => (
        <CommentThread
          key={comment.id}
          comment={comment}
          replies={comment.replies}
          onLike={onLike}
          onReport={onReport}
          onReply={onReply}
          currentUserId={currentUserId}
          currentProgress={currentProgress}
        />
      ))}
    </div>
  )
}

export default CommentFeed
