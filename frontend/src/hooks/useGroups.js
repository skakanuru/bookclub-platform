import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { groupService } from '../services/groupService'
import toast from 'react-hot-toast'

export const useGroups = () => {
  const queryClient = useQueryClient()

  const { data: groups, isLoading } = useQuery({
    queryKey: ['groups'],
    queryFn: groupService.getMyGroups,
  })

  const createGroupMutation = useMutation({
    mutationFn: groupService.createGroup,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['groups'] })
      toast.success('Group created successfully!')
    },
    onError: (error) => {
      toast.error(error.response?.data?.detail || 'Failed to create group')
    },
  })

  const joinGroupMutation = useMutation({
    mutationFn: groupService.joinGroup,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['groups'] })
      toast.success('Joined group successfully!')
    },
    onError: (error) => {
      toast.error(error.response?.data?.detail || 'Failed to join group')
    },
  })

  return {
    groups: groups || [],
    isLoading,
    createGroup: createGroupMutation.mutate,
    joinGroup: joinGroupMutation.mutate,
    isCreating: createGroupMutation.isPending,
    isJoining: joinGroupMutation.isPending,
  }
}

export const useGroup = (groupId) => {
  const { data: group, isLoading } = useQuery({
    queryKey: ['group', groupId],
    queryFn: () => groupService.getGroup(groupId),
    enabled: !!groupId,
  })

  return { group, isLoading }
}

export const useGroupBooks = (groupId) => {
  const { data: books, isLoading } = useQuery({
    queryKey: ['groupBooks', groupId],
    queryFn: () => groupService.getGroupBooks(groupId),
    enabled: !!groupId,
  })

  return { books: books || [], isLoading }
}
