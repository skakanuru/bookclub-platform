import { useState } from 'react'
import { Search, Loader2 } from 'lucide-react'
import { useQuery } from '@tanstack/react-query'
import { bookService } from '../../services/bookService'
import Input from '../common/Input'
import Button from '../common/Button'
import BookCover from './BookCover'
import Card from '../common/Card'

const BookSearch = ({ onSelectBook }) => {
  const [query, setQuery] = useState('')
  const [searchQuery, setSearchQuery] = useState('')

  const { data: books, isLoading } = useQuery({
    queryKey: ['bookSearch', searchQuery],
    queryFn: () => bookService.searchBooks(searchQuery),
    enabled: searchQuery.length > 2,
  })

  const handleSearch = (e) => {
    e.preventDefault()
    if (query.trim().length > 2) {
      setSearchQuery(query.trim())
    }
  }

  return (
    <div className="space-y-4">
      <form onSubmit={handleSearch} className="flex gap-2">
        <Input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search by title or author..."
          className="flex-1"
        />
        <Button
          type="submit"
          icon={<Search className="w-4 h-4" />}
          disabled={query.trim().length < 3}
        >
          Search
        </Button>
      </form>

      {isLoading && (
        <div className="flex justify-center py-8">
          <Loader2 className="w-8 h-8 animate-spin text-primary" />
        </div>
      )}

      {books && books.length === 0 && (
        <p className="text-center text-text-tertiary py-8">
          No books found. Try a different search.
        </p>
      )}

      {books && books.length > 0 && (
        <div className="space-y-3 max-h-96 overflow-y-auto custom-scrollbar">
          {books.map((book) => (
            <Card
              key={book.open_library_id || book.isbn}
              className="cursor-pointer hover:border-primary transition-colors"
              onClick={() => onSelectBook(book)}
            >
              <div className="flex gap-3">
                <BookCover
                  src={book.cover_url}
                  alt={book.title}
                  size="sm"
                />
                <div className="flex-1">
                  <h4 className="font-serif font-semibold text-text-primary">
                    {book.title}
                  </h4>
                  <p className="text-sm text-text-secondary">{book.author}</p>
                  {book.first_publish_year && (
                    <p className="text-xs text-text-tertiary mt-1">
                      Published {book.first_publish_year}
                    </p>
                  )}
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}

export default BookSearch
