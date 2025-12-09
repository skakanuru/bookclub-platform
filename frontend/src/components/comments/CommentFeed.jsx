import CommentCard from './CommentCard'
import LoadingSpinner from '../common/LoadingSpinner'
import { MessageSquare } from 'lucide-react'

const CommentFeed = ({ comments, isLoading, onLike, onReport, currentUserId }) => {
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

  return (
    <div className="space-y-4">
      {comments.map((comment) => (
        <CommentCard
          key={comment.id}
          comment={comment}
          onLike={onLike}
          onReport={onReport}
          currentUserId={currentUserId}
        />
      ))}
    </div>
  )
}

export default CommentFeed
