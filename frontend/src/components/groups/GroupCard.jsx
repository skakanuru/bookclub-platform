import { Link } from 'react-router-dom'
import { Users, BookOpen } from 'lucide-react'
import Card from '../common/Card'
import { formatDistanceToNow } from 'date-fns'

const GroupCard = ({ group }) => {
  return (
    <Link to={`/groups/${group.id}`}>
      <Card hover className="h-full">
        <div className="flex flex-col h-full">
          <h3 className="text-xl font-serif font-bold text-text-primary mb-2">
            {group.name}
          </h3>

          {group.description && (
            <p className="text-text-secondary text-sm mb-4 line-clamp-2">
              {group.description}
            </p>
          )}

          <div className="mt-auto flex items-center justify-between text-sm text-text-tertiary">
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-1">
                <Users className="w-4 h-4" />
                <span>{group.member_count || 0} members</span>
              </div>
              {group.book_count > 0 && (
                <div className="flex items-center gap-1">
                  <BookOpen className="w-4 h-4" />
                  <span>{group.book_count} {group.book_count === 1 ? 'book' : 'books'}</span>
                </div>
              )}
            </div>

            {group.created_at && (
              <span>
                {formatDistanceToNow(new Date(group.created_at), { addSuffix: true })}
              </span>
            )}
          </div>
        </div>
      </Card>
    </Link>
  )
}

export default GroupCard
