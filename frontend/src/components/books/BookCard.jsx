import { Link } from 'react-router-dom'
import Card from '../common/Card'
import BookCover from './BookCover'
import ProgressIndicator from '../progress/ProgressIndicator'

const BookCard = ({ book, groupId, progress }) => {
  return (
    <Link to={`/groups/${groupId}/books/${book.id}`}>
      <Card hover className="h-full">
        <div className="flex gap-4">
          <BookCover
            src={book.cover_url}
            alt={book.title}
            size="md"
          />

          <div className="flex-1 flex flex-col">
            <h3 className="text-lg font-serif font-bold text-text-primary mb-1 line-clamp-2">
              {book.title}
            </h3>

            <p className="text-sm text-text-secondary mb-3">
              by {book.author}
            </p>

            {progress && (
              <div className="mt-auto">
                <ProgressIndicator
                  currentPage={progress.current_page}
                  totalPages={progress.total_pages}
                  percentage={progress.progress_percentage}
                  compact
                />
              </div>
            )}

            {!progress && (
              <p className="mt-auto text-sm text-text-tertiary italic">
                Set your progress to start reading
              </p>
            )}
          </div>
        </div>
      </Card>
    </Link>
  )
}

export default BookCard
