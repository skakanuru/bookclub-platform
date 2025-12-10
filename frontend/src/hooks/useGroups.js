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
    onSuccess: (createdGroup) => {
      queryClient.setQueryData(['groups'], (existing) => {
        if (!existing || !Array.isArray(existing)) return [createdGroup]
        return [createdGroup, ...existing]
      })
      queryClient.invalidateQueries({ queryKey: ['groups'] })
      toast.success('Group created successfully!')
    },
    onError: (error) => {
      toast.error(error.response?.data?.detail || 'Failed to create group')
    },
  })

  const joinGroupMutation = useMutation({
    mutationFn: groupService.joinGroup,
    onSuccess: (joinedGroup) => {
      queryClient.setQueryData(['groups'], (existing) => {
        if (!existing || !Array.isArray(existing)) return [joinedGroup]
        const deduped = existing.filter((g) => g.id !== joinedGroup.id)
        return [joinedGroup, ...deduped]
      })
      queryClient.invalidateQueries({ queryKey: ['groups'] })
      toast.success('Joined group successfully!')
    },
    onError: (error) => {
      toast.error(error.response?.data?.detail || 'Failed to join group')
    },
  })

  const deleteGroupMutation = useMutation({
    mutationFn: groupService.deleteGroup,
    onSuccess: (_, groupId) => {
      queryClient.setQueryData(['groups'], (existing) => {
        if (!existing || !Array.isArray(existing)) return existing
        return existing.filter((g) => g.id !== groupId)
      })
      queryClient.removeQueries({ queryKey: ['group', groupId] })
      queryClient.invalidateQueries({ queryKey: ['groups'] })
      toast.success('Group deleted successfully')
    },
    onError: (error) => {
      toast.error(error.response?.data?.detail || 'Failed to delete group')
    },
  })

  return {
    groups: groups || [],
    isLoading,
    createGroup: createGroupMutation.mutate,
    joinGroup: joinGroupMutation.mutate,
    deleteGroup: deleteGroupMutation.mutate,
    isCreating: createGroupMutation.isPending,
    isJoining: joinGroupMutation.isPending,
    isDeleting: deleteGroupMutation.isPending,
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
  const { data: groupBooks, isLoading } = useQuery({
    queryKey: ['groupBooks', groupId],
    queryFn: () => groupService.getGroupBooks(groupId),
    enabled: !!groupId,
  })

  const books = (groupBooks || []).map((groupBook) => ({
    ...groupBook.book,
    groupBookId: groupBook.id,
    groupId: groupBook.group_id,
  }))

  return { books, isLoading }
}
