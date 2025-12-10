import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { progressService } from '../services/progressService'
import toast from 'react-hot-toast'

export const useProgress = (groupId, bookId) => {
  const queryClient = useQueryClient()

  const { data: progress, isLoading } = useQuery({
    queryKey: ['progress', groupId, bookId],
    queryFn: () => progressService.getProgress(groupId, bookId),
    enabled: !!groupId && !!bookId,
    retry: false, // surface 404/no-progress as null
  })

  const updateProgressMutation = useMutation({
    mutationFn: (data) => progressService.updateProgress(groupId, bookId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['progress', groupId, bookId] })
      queryClient.invalidateQueries({ queryKey: ['comments', groupId, bookId] })
      queryClient.invalidateQueries({ queryKey: ['commentsAhead', groupId, bookId] })
      toast.success('Progress updated!')
    },
    onError: (error) => {
      toast.error(error.response?.data?.detail || 'Failed to update progress')
    },
  })

  return {
    progress,
    isLoading,
    updateProgress: updateProgressMutation.mutate,
    isUpdating: updateProgressMutation.isPending,
  }
}

export const useAllProgress = (groupId, bookId) => {
  const { data: allProgress, isLoading } = useQuery({
    queryKey: ['allProgress', groupId, bookId],
    queryFn: () => progressService.getAllProgress(groupId, bookId),
    enabled: !!groupId && !!bookId,
  })

  return { allProgress: allProgress || [], isLoading }
}
