import { useState, useEffect } from 'react'
import Modal from '../common/Modal'
import Input from '../common/Input'
import Button from '../common/Button'

const UpdateProgressModal = ({ isOpen, onClose, onUpdate, currentProgress, isUpdating }) => {
  const [currentPage, setCurrentPage] = useState('')
  const [totalPages, setTotalPages] = useState('')
  const [errors, setErrors] = useState({})

  useEffect(() => {
    if (currentProgress) {
      setCurrentPage(currentProgress.current_page?.toString() || '')
      setTotalPages(currentProgress.total_pages?.toString() || '')
    }
  }, [currentProgress])

  const handleSubmit = (e) => {
    e.preventDefault()

    const newErrors = {}
    const current = parseInt(currentPage, 10)
    const total = parseInt(totalPages, 10)

    if (!currentPage || isNaN(current) || current < 0) {
      newErrors.currentPage = 'Please enter a valid page number'
    }

    if (!totalPages || isNaN(total) || total < 1) {
      newErrors.totalPages = 'Please enter a valid total page count'
    }

    if (current > total) {
      newErrors.currentPage = 'Current page cannot exceed total pages'
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors)
      return
    }

    onUpdate(
      {
        current_page: current,
        total_pages: total,
      },
      {
        onSuccess: () => {
          setErrors({})
          onClose()
        },
      }
    )
  }

  const percentage = totalPages && currentPage
    ? ((parseInt(currentPage, 10) / parseInt(totalPages, 10)) * 100).toFixed(1)
    : 0

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="Update Reading Progress"
      footer={
        <>
          <Button variant="ghost" onClick={onClose}>
            Cancel
          </Button>
          <Button onClick={handleSubmit} loading={isUpdating}>
            Update Progress
          </Button>
        </>
      }
    >
      <form onSubmit={handleSubmit} className="space-y-4">
        <Input
          type="number"
          label="Current Page"
          value={currentPage}
          onChange={(e) => setCurrentPage(e.target.value)}
          placeholder="127"
          error={errors.currentPage}
          min="0"
          required
        />

        <Input
          type="number"
          label="Total Pages"
          value={totalPages}
          onChange={(e) => setTotalPages(e.target.value)}
          placeholder="432"
          helper="Enter the total pages for your edition of the book"
          error={errors.totalPages}
          min="1"
          required
        />

        {currentPage && totalPages && !errors.currentPage && !errors.totalPages && (
          <div className="p-4 bg-primary bg-opacity-10 rounded-lg">
            <p className="text-sm text-text-secondary">
              You're <span className="font-bold text-primary">{percentage}%</span> through the book
            </p>
            <p className="text-xs text-text-tertiary mt-1">
              You'll see comments from readers up to page {Math.max(0, parseInt(currentPage, 10) - Math.ceil(parseInt(totalPages, 10) * 0.03))} ({Math.max(0, parseFloat(percentage) - 3).toFixed(1)}%)
            </p>
          </div>
        )}
      </form>
    </Modal>
  )
}

export default UpdateProgressModal
