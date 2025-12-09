import { User } from 'lucide-react'

const Avatar = ({ src, alt, size = 'md', className = '' }) => {
  const sizes = {
    sm: 'w-8 h-8',
    md: 'w-10 h-10',
    lg: 'w-16 h-16',
    xl: 'w-24 h-24',
  }

  if (!src) {
    return (
      <div
        className={`${sizes[size]} rounded-full bg-primary-light flex items-center justify-center ${className}`}
      >
        <User className="w-1/2 h-1/2 text-white" />
      </div>
    )
  }

  return (
    <img
      src={src}
      alt={alt}
      className={`${sizes[size]} rounded-full object-cover ${className}`}
    />
  )
}

export default Avatar
