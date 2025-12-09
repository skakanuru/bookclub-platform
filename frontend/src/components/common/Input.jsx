import { forwardRef } from 'react'

const Input = forwardRef(({
  label,
  error,
  helper,
  className = '',
  ...props
}, ref) => {
  return (
    <div className="w-full">
      {label && (
        <label className="block text-sm font-medium text-text-primary mb-1">
          {label}
        </label>
      )}
      <input
        ref={ref}
        className={`w-full px-4 py-2 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all ${
          error ? 'border-danger' : ''
        } ${className}`}
        {...props}
      />
      {error && (
        <p className="mt-1 text-sm text-danger">{error}</p>
      )}
      {helper && !error && (
        <p className="mt-1 text-sm text-text-tertiary">{helper}</p>
      )}
    </div>
  )
})

Input.displayName = 'Input'

export default Input
