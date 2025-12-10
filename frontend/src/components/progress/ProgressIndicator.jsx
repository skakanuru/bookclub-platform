const ProgressIndicator = ({ currentPage, totalPages, percentage, compact = false }) => {
  const rawPercentage = percentage != null
    ? Number(percentage)
    : (Number(currentPage) / Math.max(Number(totalPages) || 1, 1)) * 100

  const calculatedPercentage = Number.isFinite(rawPercentage) ? rawPercentage : 0
  const clampedPercentage = Math.min(Math.max(calculatedPercentage, 0), 100)
  const safeCurrent = Number.isFinite(Number(currentPage)) ? Number(currentPage) : 0
  const safeTotal = Number.isFinite(Number(totalPages)) ? Number(totalPages) : 0

  if (compact) {
    return (
      <div className="space-y-1">
        <div className="flex justify-between items-center text-xs text-text-tertiary font-mono">
          <span>Page {safeCurrent} of {safeTotal}</span>
          <span>{clampedPercentage.toFixed(0)}%</span>
        </div>
        <div className="w-full bg-background rounded-full h-1.5 overflow-hidden">
          <div
            className="bg-primary h-full transition-all duration-300"
            style={{ width: `${clampedPercentage}%` }}
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
            {clampedPercentage.toFixed(1)}%
          </p>
          <p className="text-sm text-text-secondary font-mono">
            Page {safeCurrent} of {safeTotal}
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
              strokeDashoffset={339.292 - (339.292 * clampedPercentage) / 100}
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
              {Math.round(clampedPercentage)}%
            </span>
          </div>
        </div>
      </div>

      <div className="w-full bg-background rounded-full h-2 overflow-hidden">
        <div
          className="bg-primary h-full transition-all duration-300"
          style={{ width: `${clampedPercentage}%` }}
        />
      </div>
    </div>
  )
}

export default ProgressIndicator
