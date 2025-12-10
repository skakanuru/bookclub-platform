import { useState } from 'react'
import Modal from '../common/Modal'
import Input from '../common/Input'
import Button from '../common/Button'

const CreateGroupModal = ({ isOpen, onClose, onCreate, onCreated, isCreating }) => {
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [errors, setErrors] = useState({})

  const handleSubmit = (e) => {
    e.preventDefault()

    const newErrors = {}
    if (!name.trim()) {
      newErrors.name = 'Group name is required'
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors)
      return
    }

    onCreate({ name, description }, {
      onSuccess: (group) => {
        setName('')
        setDescription('')
        setErrors({})
        onClose()
        if (onCreated) {
          onCreated(group)
        }
      }
    })
  }

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="Create New Group"
      footer={
        <>
          <Button variant="ghost" onClick={onClose}>
            Cancel
          </Button>
          <Button onClick={handleSubmit} loading={isCreating}>
            Create Group
          </Button>
        </>
      }
    >
      <form onSubmit={handleSubmit} className="space-y-4">
        <Input
          label="Group Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="My Book Club"
          error={errors.name}
          required
        />

        <div>
          <label className="block text-sm font-medium text-text-primary mb-1">
            Description (optional)
          </label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="What's your book club about?"
            rows={4}
            className="w-full px-4 py-2 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all resize-none"
          />
        </div>
      </form>
    </Modal>
  )
}

export default CreateGroupModal
