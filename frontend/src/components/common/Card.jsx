const Card = ({ children, className = '', hover = false, ...props }) => {
  return (
    <div
      className={`bg-surface rounded-lg shadow-sm border border-border p-6 ${
        hover ? 'transition-shadow duration-200 hover:shadow-md' : ''
      } ${className}`}
      {...props}
    >
      {children}
    </div>
  )
}

export default Card
