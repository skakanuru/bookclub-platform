import { useState } from 'react'
import { Send } from 'lucide-react'
import Button from '../common/Button'
import Card from '../common/Card'

const CommentInput = ({ onSubmit, isSubmitting, currentProgress }) => {
  const [content, setContent] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()

    if (!content.trim()) return

    onSubmit(
      { content: content.trim() },
      {
        onSuccess: () => {
          setContent('')
        },
      }
    )
  }

  if (!currentProgress) {
    return (
      <Card className="bg-primary bg-opacity-5">
        <p className="text-center text-text-secondary">
          Set your reading progress to start commenting
        </p>
      </Card>
    )
  }

  return (
    <Card>
      <form onSubmit={handleSubmit} className="space-y-3">
        <div>
          <div className="flex items-center justify-between mb-2">
            <label className="text-sm font-medium text-text-primary">
              Share your thoughts
            </label>
            <span className="text-xs text-text-tertiary font-mono">
              Commenting at Page {currentProgress.current_page} ({currentProgress.progress_percentage?.toFixed(0)}%)
            </span>
          </div>

          <textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="What are you thinking about this part of the book?"
            rows={4}
            className="w-full px-4 py-3 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all resize-none font-serif"
            maxLength={1000}
            disabled={isSubmitting}
          />

          <div className="flex justify-between items-center mt-2">
            <span className="text-xs text-text-tertiary">
              {content.length}/1000 characters
            </span>
          </div>
        </div>

        <div className="flex justify-end">
          <Button
            type="submit"
            disabled={!content.trim() || isSubmitting}
            loading={isSubmitting}
            icon={<Send className="w-4 h-4" />}
          >
            Post Comment
          </Button>
        </div>
      </form>
    </Card>
  )
}

export default CommentInput
