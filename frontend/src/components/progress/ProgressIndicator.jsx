const ProgressIndicator = ({ currentPage, totalPages, percentage, compact = false }) => {
  const calculatedPercentage = percentage || (currentPage / totalPages) * 100

  if (compact) {
    return (
      <div className="space-y-1">
        <div className="flex justify-between items-center text-xs text-text-tertiary font-mono">
          <span>Page {currentPage} of {totalPages}</span>
          <span>{calculatedPercentage.toFixed(0)}%</span>
        </div>
        <div className="w-full bg-background rounded-full h-1.5 overflow-hidden">
          <div
            className="bg-primary h-full transition-all duration-300"
            style={{ width: `${calculatedPercentage}%` }}
          />
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-3">
      <div className="flex justify-between items-center">
        <div>
          <p className="text-2xl font-serif font-bold text-text-primary">
            {calculatedPercentage.toFixed(1)}%
          </p>
          <p className="text-sm text-text-secondary font-mono">
            Page {currentPage} of {totalPages}
          </p>
        </div>

        <div className="relative w-24 h-24">
          <svg className="w-full h-full" viewBox="0 0 120 120">
            <circle
              className="text-background"
              strokeWidth="8"
              stroke="currentColor"
              fill="transparent"
              r="54"
              cx="60"
              cy="60"
            />
            <circle
              className="text-primary progress-ring"
              strokeWidth="8"
              strokeDasharray={339.292}
              strokeDashoffset={339.292 - (339.292 * calculatedPercentage) / 100}
              strokeLinecap="round"
              stroke="currentColor"
              fill="transparent"
              r="54"
              cx="60"
              cy="60"
            />
          </svg>
          <div className="absolute inset-0 flex items-center justify-center">
            <span className="text-xl font-bold text-primary">
              {Math.round(calculatedPercentage)}%
            </span>
          </div>
        </div>
      </div>

      <div className="w-full bg-background rounded-full h-2 overflow-hidden">
        <div
          className="bg-primary h-full transition-all duration-300"
          style={{ width: `${calculatedPercentage}%` }}
        />
      </div>
    </div>
  )
}

export default ProgressIndicator
