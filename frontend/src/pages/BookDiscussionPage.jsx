import { useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { ArrowLeft, Edit } from 'lucide-react'
import { useAuth } from '../contexts/AuthContext'
import { useProgress } from '../hooks/useProgress'
import { useComments } from '../hooks/useComments'
import { useQuery } from '@tanstack/react-query'
import { bookService } from '../services/bookService'
import Button from '../components/common/Button'
import BookCover from '../components/books/BookCover'
import ProgressIndicator from '../components/progress/ProgressIndicator'
import UpdateProgressModal from '../components/progress/UpdateProgressModal'
import CommentFeed from '../components/comments/CommentFeed'
import CommentInput from '../components/comments/CommentInput'
import AheadNotifications from '../components/comments/AheadNotifications'
import LoadingSpinner from '../components/common/LoadingSpinner'
import Card from '../components/common/Card'

const BookDiscussionPage = () => {
  const { groupId, bookId } = useParams()
  const navigate = useNavigate()
  const { user } = useAuth()
  const [showProgressModal, setShowProgressModal] = useState(false)

  const { data: book, isLoading: bookLoading } = useQuery({
    queryKey: ['book', bookId],
    queryFn: () => bookService.getBook(bookId),
  })

  const { progress, updateProgress, isUpdating } = useProgress(groupId, bookId)
  const {
    comments,
    commentsAhead,
    isLoading: commentsLoading,
    createComment,
    likeComment,
    reportComment,
    isCreatingComment,
  } = useComments(groupId, bookId)

  if (bookLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <LoadingSpinner size="lg" />
      </div>
    )
  }

  if (!book) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-center">
          <h2 className="text-2xl font-serif font-bold text-text-primary mb-2">
            Book not found
          </h2>
          <Button onClick={() => navigate(`/groups/${groupId}`)}>
            Back to Group
          </Button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background">
      <header className="bg-surface border-b border-border">
        <div className="max-w-5xl mx-auto px-4 py-4">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => navigate(`/groups/${groupId}`)}
            icon={<ArrowLeft className="w-4 h-4" />}
          >
            Back to Group
          </Button>
        </div>
      </header>

      <div className="max-w-5xl mx-auto px-4 py-8">
        <div className="grid lg:grid-cols-3 gap-8">
          {/* Book Info & Progress Sidebar */}
          <div className="lg:col-span-1 space-y-6">
            <Card>
              <div className="flex flex-col items-center text-center">
                <BookCover
                  src={book.cover_url}
                  alt={book.title}
                  size="xl"
                  className="mb-4"
                />

                <h1 className="text-2xl font-serif font-bold text-text-primary mb-2">
                  {book.title}
                </h1>

                <p className="text-lg text-text-secondary mb-4">
                  by {book.author}
                </p>

                {book.isbn && (
                  <p className="text-xs text-text-tertiary font-mono">
                    ISBN: {book.isbn}
                  </p>
                )}
              </div>
            </Card>

            <Card>
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-text-primary">
                  Your Progress
                </h3>
                {progress && (
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setShowProgressModal(true)}
                    icon={<Edit className="w-4 h-4" />}
                  >
                    Update
                  </Button>
                )}
              </div>

              {progress ? (
                <ProgressIndicator
                  currentPage={progress.current_page}
                  totalPages={progress.total_pages}
                  percentage={progress.progress_percentage}
                />
              ) : (
                <div className="text-center py-6">
                  <p className="text-text-secondary mb-4">
                    Set your reading progress to start commenting and see discussions.
                  </p>
                  <Button onClick={() => setShowProgressModal(true)}>
                    Set Progress
                  </Button>
                </div>
              )}
            </Card>
          </div>

          {/* Discussion Feed */}
          <div className="lg:col-span-2 space-y-6">
            <div>
              <h2 className="text-2xl font-serif font-bold text-text-primary mb-2">
                Discussion
              </h2>
              <p className="text-sm text-text-secondary">
                {progress
                  ? `Showing comments up to page ${progress.current_page} (${Number(progress.progress_percentage || 0).toFixed(1)}%)`
                  : 'Set your progress to see comments'}
              </p>
            </div>

            {commentsAhead && commentsAhead.length > 0 && (
              <AheadNotifications commentsAhead={commentsAhead} />
            )}

            <CommentInput
              onSubmit={createComment}
              isSubmitting={isCreatingComment}
              currentProgress={progress}
              bookId={bookId}
            />

            <CommentFeed
              comments={comments}
              isLoading={commentsLoading}
              onLike={likeComment}
              onReport={reportComment}
              onReply={createComment}
              currentUserId={user?.id}
              currentProgress={progress}
            />
          </div>
        </div>
      </div>

      <UpdateProgressModal
        isOpen={showProgressModal}
        onClose={() => setShowProgressModal(false)}
        onUpdate={updateProgress}
        currentProgress={progress}
        isUpdating={isUpdating}
      />
    </div>
  )
}

export default BookDiscussionPage
