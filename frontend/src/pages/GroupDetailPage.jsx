import { useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { ArrowLeft, Plus, BookOpen } from 'lucide-react'
import { useAuth } from '../contexts/AuthContext'
import { useGroup, useGroupBooks } from '../hooks/useGroups'
import { useProgress } from '../hooks/useProgress'
import Button from '../components/common/Button'
import GroupHeader from '../components/groups/GroupHeader'
import InviteCodeDisplay from '../components/groups/InviteCodeDisplay'
import BookCard from '../components/books/BookCard'
import LoadingSpinner from '../components/common/LoadingSpinner'
import Modal from '../components/common/Modal'
import BookSearch from '../components/books/BookSearch'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { groupService } from '../services/groupService'
import { bookService } from '../services/bookService'
import toast from 'react-hot-toast'

const GroupDetailPage = () => {
  const { groupId } = useParams()
  const navigate = useNavigate()
  const { user } = useAuth()
  const { group, isLoading: groupLoading } = useGroup(groupId)
  const { books, isLoading: booksLoading } = useGroupBooks(groupId)
  const [showAddBookModal, setShowAddBookModal] = useState(false)
  const [showDeleteModal, setShowDeleteModal] = useState(false)
  const queryClient = useQueryClient()

  const addBookMutation = useMutation({
    mutationFn: async (book) => {
      // First create or get the book
      const createdBook = await bookService.createBook({
        title: book.title,
        author: book.author,
        isbn: book.isbn,
        open_library_id: book.open_library_id,
        cover_url: book.cover_url,
      })

      // Then add it to the group
      await groupService.addBookToGroup(groupId, createdBook.id)
      return createdBook
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['groupBooks', groupId] })
      toast.success('Book added to group!')
      setShowAddBookModal(false)
    },
    onError: (error) => {
      toast.error(error.response?.data?.detail || 'Failed to add book')
    },
  })

  const deleteGroupMutation = useMutation({
    mutationFn: () => groupService.deleteGroup(groupId),
    onSuccess: () => {
      queryClient.removeQueries({ queryKey: ['group', groupId] })
      queryClient.invalidateQueries({ queryKey: ['groups'] })
      toast.success('Group deleted')
      navigate('/groups')
    },
    onError: (error) => {
      toast.error(error.response?.data?.detail || 'Failed to delete group')
    },
  })

  if (groupLoading || booksLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <LoadingSpinner size="lg" />
      </div>
    )
  }

  if (!group) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-center">
          <h2 className="text-2xl font-serif font-bold text-text-primary mb-2">
            Group not found
          </h2>
          <Button onClick={() => navigate('/groups')}>Back to Groups</Button>
        </div>
      </div>
    )
  }

  const isAdmin = group.created_by === user?.id

  return (
    <div className="min-h-screen bg-background">
      <header className="bg-surface border-b border-border">
        <div className="max-w-5xl mx-auto px-4 py-4">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => navigate('/groups')}
            icon={<ArrowLeft className="w-4 h-4" />}
          >
            Back to Groups
          </Button>
        </div>
      </header>

      <GroupHeader group={group} isAdmin={isAdmin} />

      <div className="max-w-5xl mx-auto px-4 py-8">
        <div className="grid lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-serif font-bold text-text-primary">
                Books
              </h2>

              {isAdmin && (
                <Button
                  onClick={() => setShowAddBookModal(true)}
                  size="sm"
                  icon={<Plus className="w-4 h-4" />}
                >
                  Add Book
                </Button>
              )}
            </div>

            {books.length === 0 ? (
              <div className="text-center py-16 bg-surface rounded-lg border border-border">
                <BookOpen className="w-16 h-16 text-text-tertiary mx-auto mb-4" />
                <h3 className="text-xl font-serif font-semibold text-text-primary mb-2">
                  No books yet
                </h3>
                <p className="text-text-secondary mb-6 max-w-md mx-auto">
                  {isAdmin
                    ? "Add your first book to start the discussion."
                    : "The group admin will add a book soon."}
                </p>
                {isAdmin && (
                  <Button
                    onClick={() => setShowAddBookModal(true)}
                    icon={<Plus className="w-4 h-4" />}
                  >
                    Add First Book
                  </Button>
                )}
              </div>
            ) : (
              <div className="space-y-4">
                {books.map((book) => {
                  const progress = book.user_progress
                  return (
                    <BookCard
                      key={book.groupBookId || book.id}
                      book={book}
                      groupId={groupId}
                      progress={progress}
                    />
                  )
                })}
              </div>
            )}
          </div>

          <div>
            <InviteCodeDisplay
              inviteCode={group.invite_code}
              groupName={group.name}
            />

            {isAdmin && (
              <div className="mt-6 bg-surface border border-border rounded-lg p-4">
                <h3 className="text-lg font-semibold text-text-primary mb-2">
                  Danger Zone
                </h3>
                <p className="text-sm text-text-secondary mb-4">
                  Deleting a group removes all books, comments, and member access. This cannot be undone.
                </p>
                <Button
                  variant="danger"
                  size="sm"
                  onClick={() => setShowDeleteModal(true)}
                  loading={deleteGroupMutation.isPending}
                >
                  Delete Group
                </Button>
              </div>
            )}
          </div>
        </div>
      </div>

      <Modal
        isOpen={showAddBookModal}
        onClose={() => setShowAddBookModal(false)}
        title="Add Book to Group"
        size="md"
      >
        <BookSearch
          onSelectBook={(book) => addBookMutation.mutate(book)}
        />
      </Modal>

      <Modal
        isOpen={showDeleteModal}
        onClose={() => setShowDeleteModal(false)}
        title="Delete Group"
        size="sm"
        footer={
          <>
            <Button variant="ghost" onClick={() => setShowDeleteModal(false)}>
              Cancel
            </Button>
            <Button
              variant="danger"
              onClick={() => deleteGroupMutation.mutate()}
              loading={deleteGroupMutation.isPending}
            >
              Delete
            </Button>
          </>
        }
      >
        <p className="text-sm text-text-secondary">
          Are you sure you want to delete <span className="font-semibold text-text-primary">{group?.name}</span>? This action cannot be undone.
        </p>
      </Modal>
    </div>
  )
}

export default GroupDetailPage
