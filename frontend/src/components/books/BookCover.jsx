import { BookOpen } from 'lucide-react'

const BookCover = ({ src, alt, size = 'md', className = '' }) => {
  const sizes = {
    sm: 'w-16 h-24',
    md: 'w-24 h-36',
    lg: 'w-32 h-48',
    xl: 'w-48 h-72',
  }

  if (!src) {
    return (
      <div
        className={`${sizes[size]} bg-accent bg-opacity-20 rounded flex items-center justify-center ${className}`}
      >
        <BookOpen className="w-8 h-8 text-accent" />
      </div>
    )
  }

  return (
    <img
      src={src}
      alt={alt}
      className={`${sizes[size]} object-cover rounded shadow-sm ${className}`}
    />
  )
}

export default BookCover
