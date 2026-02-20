# Component Templates (Minimal)

## Base UI Component (Button)
```typescript
import type { FC, ReactNode } from 'react'
import { memo, useCallback } from 'react'

interface ButtonProps {
  children: ReactNode
  variant?: 'primary' | 'secondary' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  disabled?: boolean
  onClick?: () => void
}

export const Button: FC<ButtonProps> = memo(({
  children,
  variant = 'primary',
  size = 'md',
  disabled = false,
  onClick,
}) => {
  const handleClick = useCallback(() => {
    if (disabled) return
    onClick?.()
  }, [disabled, onClick])

  return (
    <button
      className={`btn-${variant} size-${size}`}
      disabled={disabled}
      onClick={handleClick}
    >
      {children}
    </button>
  )
})

Button.displayName = 'Button'
```

## Container Component (Data + UI)
```typescript
import type { FC } from 'react'
import { useUsers } from '@/hooks/useUsers'
import { UserList } from './UserList'

export const UserListContainer: FC = () => {
  const { users, loading, error } = useUsers()

  if (loading) return <div>Loading...</div>
  if (error) return <div>Error</div>

  return <UserList users={users} />
}
```
