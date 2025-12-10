import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { commentService } from '../services/commentService'
import toast from 'react-hot-toast'

export const useComments = (groupId, bookId) => {
  const queryClient = useQueryClient()

  const { data: comments, isLoading } = useQuery({
    queryKey: ['comments', groupId, bookId],
    queryFn: () => commentService.getComments(groupId, bookId),
    enabled: !!groupId && !!bookId,
    refetchInterval: 30000, // Refetch every 30 seconds
  })

  const { data: commentsAhead } = useQuery({
    queryKey: ['commentsAhead', groupId, bookId],
    queryFn: () => commentService.getCommentsAhead(groupId, bookId),
    enabled: !!groupId && !!bookId,
    refetchInterval: 30000,
  })

  const createCommentMutation = useMutation({
    mutationFn: (data) => commentService.createComment(groupId, bookId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['comments', groupId, bookId] })
      queryClient.invalidateQueries({ queryKey: ['commentsAhead', groupId, bookId] })
      toast.success('Comment posted!')
    },
    onError: (error) => {
      toast.error(error.response?.data?.detail || 'Failed to post comment')
    },
  })

  const likeCommentMutation = useMutation({
    mutationFn: ({ commentId, liked }) => (
      liked ? commentService.unlikeComment(commentId) : commentService.likeComment(commentId)
    ),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['comments', groupId, bookId] })
      queryClient.invalidateQueries({ queryKey: ['commentsAhead', groupId, bookId] })
    },
    onError: (error) => {
      toast.error(error.response?.data?.detail || 'Failed to update like')
    },
  })

  const reportCommentMutation = useMutation({
    mutationFn: ({ commentId, reason }) => commentService.reportComment(commentId, reason),
    onSuccess: () => {
      toast.success('Comment reported. Thank you!')
    },
    onError: (error) => {
      toast.error(error.response?.data?.detail || 'Failed to report comment')
    },
  })

  return {
    comments: comments || [],
    commentsAhead: commentsAhead || [],
    isLoading,
    createComment: createCommentMutation.mutate,
    likeComment: likeCommentMutation.mutate,
    reportComment: reportCommentMutation.mutate,
    isCreatingComment: createCommentMutation.isPending,
  }
}
