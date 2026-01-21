# 前端组件开发规范

你是资深前端开发工程师

> **版本**: 1.0
> **状态**: 已批准
> **创建日期**: 2026-01-19
> **适用范围**: 所有前端组件开发

> **重要**: 本规范同时遵循 `@frontend/` 和 `@architecture/` 规范要求。所有组件开发必须同时满足前端标准和架构设计原则。

---

## 📋 目录

- [核心原则](#核心原则)
- [组件命名规范](#组件命名规范)
- [组件架构设计](#组件架构设计)
- [代码风格要求](#代码风格要求)
- [开发工作流程](#开发工作流程)
- [架构原则应用](#架构原则应用)
- [组件审查清单](#组件审查清单)
- [最佳实践示例](#最佳实践示例)
- [工具配置](#工具配置)

---

## 核心原则

### 双重规范要求

所有组件开发必须同时满足：

| 规范体系 | 要求 | 检查方式 |
|---------|------|---------|
| **@frontend/** | 命名规范、代码风格、CSS 系统、工具配置 | 前端技能审查 |
| **@architecture/** | 10 大设计原则、架构合理性、可测试性 | 架构技能审查 |

### 必须调用的技能

```bash
# 1. 设计阶段（必须）
@architecture-assistant 帮我设计一个 [组件名] 组件

# 2. 编码后审查（必须）
@architecture-assistant 请审查这段组件代码是否符合架构原则

# 3. 前端规范检查（必须）
@frontend/components 请检查这个组件是否符合前端规范
```

---

## 组件命名规范

### 文件命名

| 组件类型 | 命名规范 | 示例 | 说明 |
|---------|---------|------|------|
| **通用组件** | PascalCase | `Button.tsx`, `Card.tsx` | 可复用的基础组件 |
| **业务组件** | PascalCase | `UserProfile.tsx`, `ArticleCard.tsx` | 特定业务场景组件 |
| **页面组件** | camelCase | `homePage.tsx`, `userSettings.tsx` | 页面级组件 |
| **布局组件** | PascalCase | `MainLayout.tsx`, `SidebarLayout.tsx` | 布局组件 |
| **容器组件** | PascalCase + Container | `UserListContainer.tsx` | 数据容器组件 |
| **高阶组件** | camelCase + with | `withAuth.tsx` | HOC 组件 |
| **Hook 组件** | camelCase + use | `useModal.ts` | 自定义 Hook |

### 组件内标识符命名

| 类型 | 命名规范 | 示例 | 说明 |
|------|---------|------|------|
| **Props 接口** | PascalCase + Props | `ButtonProps` | 组件属性接口 |
| **Props 属性** | camelCase | `onClick`, `disabled` | 属性名 |
| **状态变量** | camelCase | `isOpen`, `userData` | useState 变量 |
| **事件处理** | camelCase + handle | `handleClick`, `handleSubmit` | 事件处理函数 |
| **工具函数** | camelCase | `validateEmail`, `formatDate` | 组件内工具函数 |
| **常量** | UPPER_SNAKE_CASE | `DEFAULT_SIZE`, `MAX_ITEMS` | 组件常量 |

### 命名示例

```typescript
// ✅ 正确示例

// Button.tsx
interface ButtonProps {
  variant?: 'primary' | 'secondary'
  size?: 'sm' | 'md' | 'lg'
  onClick?: () => void
  disabled?: boolean
}

export const Button: React.FC<ButtonProps> = ({ 
  variant = 'primary', 
  size = 'md',
  onClick,
  disabled = false 
}) => {
  const [isLoading, setIsLoading] = useState(false)
  
  const handleClick = useCallback(async () => {
    if (isLoading || disabled) return
    setIsLoading(true)
    try {
      await onClick?.()
    } finally {
      setIsLoading(false)
    }
  }, [onClick, disabled, isLoading])
  
  return (
    <button 
      className={`btn-${variant} size-${size}`}
      onClick={handleClick}
      disabled={disabled || isLoading}
    >
      {isLoading ? '加载中...' : '点击'}
    </button>
  )
}

// ❌ 错误示例
interface buttonProps { ... }  // 应为 ButtonProps
const Button: React.FC<props> = ({ ... })  // 应为 ButtonProps
const on_click = () => {}  // 应为 handleClick
```

---

## 组件架构设计

### 组件职责划分

根据架构原则，组件必须遵循**单一职责原则（SRP）**和**关注点分离（SoC）**：

```
组件类型          职责                    示例
─────────────────────────────────────────────────────────────
基础组件          UI 展示                 Button, Input, Card
业务组件          业务逻辑 + UI           UserProfile, ArticleCard
容器组件          数据管理                UserListContainer
页面组件          路由级组合              HomePage
布局组件          页面结构                MainLayout
```

### 组件层次结构

```
页面层 (Page)
  └─ 布局层 (Layout)
      └─ 容器层 (Container)
          └─ 业务组件层 (Business Components)
              └─ 基础组件层 (UI Components)
```

### 组件拆分原则

#### 1. 单一职责原则（SRP）
```typescript
// ✅ 好的拆分：一个组件只做一件事

// Button.tsx - 只负责按钮 UI 和基础交互
interface ButtonProps {
  onClick?: () => void
  children: React.ReactNode
}

// ButtonWithConfirm.tsx - 只负责确认逻辑
interface ButtonWithConfirmProps extends ButtonProps {
  confirmMessage: string
}

// ❌ 不好的拆分：一个组件做太多事
interface ComplexButtonProps {
  onClick?: () => void
  confirmMessage?: string
  loading?: boolean
  validation?: () => boolean
  analytics?: string
  // ... 太多职责
}
```

#### 2. 关注点分离（SoC）
```typescript
// ✅ 好的分离：UI、逻辑、数据分离

// 1. UI 组件（纯展示）
const UserCardUI: React.FC<UserCardUIProps> = ({ user, onEdit, onDelete }) => {
  return (
    <div className="card">
      <h3>{user.name}</h3>
      <button onClick={onEdit}>编辑</button>
      <button onClick={onDelete}>删除</button>
    </div>
  )
}

// 2. 逻辑组件（处理交互）
const UserCard: React.FC<UserCardProps> = ({ userId }) => {
  const { user, loading, error } = useUser(userId)
  const { updateUser, deleteUser } = useUserActions()
  
  if (loading) return <Loading />
  if (error) return <Error message={error} />
  
  return (
    <UserCardUI
      user={user}
      onEdit={() => updateUser(userId)}
      onDelete={() => deleteUser(userId)}
    />
  )
}

// ❌ 不好的做法：UI 和逻辑混在一起
const UserCard: React.FC<UserCardProps> = ({ userId }) => {
  // UI 逻辑
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(false)
  
  // 数据获取
  useEffect(() => {
    setLoading(true)
    fetch(`/api/users/${userId}`)
      .then(res => res.json())
      .then(data => {
        setUser(data)
        setLoading(false)
      })
  }, [userId])
  
  // 业务逻辑
  const handleEdit = () => {
    // 编辑逻辑...
  }
  
  const handleDelete = () => {
    // 删除逻辑...
  }
  
  // UI 渲染
  return (
    <div className="card">
      {loading ? <div>加载中...</div> : (
        <>
          <h3>{user.name}</h3>
          <button onClick={handleEdit}>编辑</button>
          <button onClick={handleDelete}>删除</button>
        </>
      )}
    </div>
  )
}
```

#### 3. 组合优于继承
```typescript
// ✅ 好的组合：使用组合模式

// 基础组件
const Card: React.FC<CardProps> = ({ children, className }) => (
  <div className={`card ${className}`}>{children}</div>
)

const CardHeader: React.FC<CardHeaderProps> = ({ children }) => (
  <div className="card-header">{children}</div>
)

const CardBody: React.FC<CardBodyProps> = ({ children }) => (
  <div className="card-body">{children}</div>
)

// 组合使用
const UserCard: React.FC<UserCardProps> = ({ user }) => (
  <Card className="user-card">
    <CardHeader>
      <h3>{user.name}</h3>
    </CardHeader>
    <CardBody>
      <p>{user.email}</p>
      <p>{user.bio}</p>
    </CardBody>
  </Card>
)

// ❌ 不好的继承：使用继承模式
class BaseCard extends React.Component {
  // 基础卡片逻辑
}

class UserCard extends BaseCard {
  // 继承基类，耦合度高
}
```

### 组件通信模式

#### 1. Props 传递（推荐）
```typescript
// ✅ 显式依赖注入
interface UserListProps {
  userIds: string[]
  onSelect: (id: string) => void
  onDelete: (id: string) => Promise<void>
}

const UserList: React.FC<UserListProps> = ({ userIds, onSelect, onDelete }) => {
  // 组件只负责渲染和用户交互
  // 所有数据和操作通过 props 注入
}
```

#### 2. Context（用于全局状态）
```typescript
// ✅ 合理使用 Context
const ThemeContext = createContext<ThemeContextType>({
  theme: 'light',
  toggleTheme: () => {},
})

// 只在需要共享状态的层级使用
const App: React.FC = () => {
  const [theme, setTheme] = useState('light')
  
  return (
    <ThemeContext.Provider value={{ theme, toggleTheme: () => setTheme(t => t === 'light' ? 'dark' : 'light') }}>
      <AppContent />
    </ThemeContext.Provider>
  )
}
```

#### 3. 自定义 Hooks（推荐）
```typescript
// ✅ 使用 Hook 管理复杂逻辑
const useUserList = (userId: string) => {
  const [users, setUsers] = useState<User[]>([])
  const [loading, setLoading] = useState(false)
  
  const fetchUsers = useCallback(async () => {
    setLoading(true)
    try {
      const response = await fetch(`/api/users/${userId}`)
      const data = await response.json()
      setUsers(data)
    } catch (error) {
      console.error('Failed to fetch users:', error)
    } finally {
      setLoading(false)
    }
  }, [userId])
  
  return { users, loading, fetchUsers }
}
```

---

## 代码风格要求

### TypeScript 类型安全

#### 1. 严格类型定义
```typescript
// ✅ 完整的类型定义
interface UserCardProps {
  user: {
    id: string
    name: string
    email: string
    role: 'admin' | 'user' | 'guest'
  }
  onEdit?: (id: string) => void
  onDelete?: (id: string) => Promise<void>
  variant?: 'compact' | 'detailed'
}

// ❌ 不完整的类型
interface UserCardProps {
  user: any  // 避免 any
  onEdit?: Function  // 应该指定具体类型
}
```

#### 2. 使用 React 类型
```typescript
// ✅ 使用正确的 React 类型
import type { FC, ReactNode } from 'react'

interface ButtonProps {
  children: ReactNode
  onClick?: () => void | Promise<void>
  disabled?: boolean
}

export const Button: FC<ButtonProps> = ({ children, onClick, disabled }) => {
  // ...
}
```

#### 3. 避免 any 类型
```typescript
// ✅ 使用 unknown 或具体类型
const processData = (data: unknown) => {
  if (typeof data === 'string') {
    return data.toUpperCase()
  }
  throw new Error('Invalid data type')
}

// ❌ 避免 any
const processData = (data: any) => {
  return data.toUpperCase()  // 运行时可能出错
}
```

### Hooks 使用规范

#### 1. 自定义 Hooks 命名
```typescript
// ✅ 正确命名
const useModal = () => { ... }
const useAuth = () => { ... }
const useUserList = (userId: string) => { ... }

// ❌ 错误命名
const modal = () => { ... }  // 缺少 use 前缀
const getAuth = () => { ... }  // 不是 Hook
```

#### 2. Hooks 依赖管理
```typescript
// ✅ 正确的依赖管理
const UserCard: React.FC<UserCardProps> = ({ userId, onEdit }) => {
  const [user, setUser] = useState<User | null>(null)
  
  const fetchUser = useCallback(async () => {
    const data = await fetchUserById(userId)
    setUser(data)
  }, [userId])  // 依赖正确
  
  useEffect(() => {
    fetchUser()
  }, [fetchUser])  // 依赖正确
  
  const handleEdit = useCallback(() => {
    if (user) {
      onEdit(user.id)
    }
  }, [user, onEdit])  // 依赖正确
  
  return <div>{user?.name}</div>
}

// ❌ 错误的依赖管理
const UserCard: React.FC<UserCardProps> = ({ userId, onEdit }) => {
  const [user, setUser] = useState<User | null>(null)
  
  const fetchUser = async () => {
    const data = await fetchUserById(userId)
    setUser(data)
  }  // 缺少 useCallback
  
  useEffect(() => {
    fetchUser()
  }, [userId])  // 依赖不完整
  
  const handleEdit = () => {
    if (user) {
      onEdit(user.id)
    }
  }  // 缺少 useCallback
  
  return <div>{user?.name}</div>
}
```

#### 3. Hooks 逻辑组织
```typescript
// ✅ 好的组织：按功能分组
const useUserManager = (userId: string) => {
  // 1. 数据状态
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  
  // 2. 数据操作
  const fetchUser = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await fetchUserById(userId)
      setUser(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }, [userId])
  
  const updateUser = useCallback(async (data: Partial<User>) => {
    // 更新逻辑
  }, [])
  
  // 3. 返回结果
  return {
    user,
    loading,
    error,
    fetchUser,
    updateUser,
  }
}
```

### 样式系统

#### 1. 使用 UnoCSS
```typescript
// ✅ 使用 UnoCSS 类名
const Button: React.FC<ButtonProps> = ({ variant = 'primary', children }) => {
  return (
    <button className={`
      px-4 py-2 rounded-md font-medium transition
      ${variant === 'primary' ? 'bg-primary text-white hover:bg-primary-hover' : ''}
      ${variant === 'secondary' ? 'bg-secondary text-white hover:bg-secondary-hover' : ''}
      ${variant === 'danger' ? 'bg-danger text-white hover:bg-danger-hover' : ''}
    `}>
      {children}
    </button>
  )
}

// ✅ 使用快捷方式
const Button: React.FC<ButtonProps> = ({ variant = 'primary', children }) => {
  return (
    <button className={`btn-${variant}`}>
      {children}
    </button>
  )
}
```

#### 2. 使用 CSS 变量
```typescript
// ✅ 使用 CSS 变量
const Card: React.FC<CardProps> = ({ children }) => {
  return (
    <div className="card" style={{ 
      backgroundColor: 'var(--color-bg-secondary)',
      borderRadius: 'var(--radius-md)',
      padding: 'var(--spacing-lg)'
    }}>
      {children}
    </div>
  )
}
```

#### 3. 避免内联样式
```typescript
// ❌ 避免内联样式
const Button: React.FC<ButtonProps> = () => {
  return (
    <button style={{ backgroundColor: '#3b82f6', color: 'white', padding: '8px 16px' }}>
      点击
    </button>
  )
}

// ✅ 使用类名
const Button: React.FC<ButtonProps> = () => {
  return <button className="btn-primary">点击</button>
}
```

---

## 开发工作流程

### 流程 1: 新组件开发

```
1. 需求分析
   └─> 明确组件职责和边界

2. 设计阶段 [必须调用]
   └─> @architecture-assistant 帮我设计一个 [组件名] 组件
       - 语言：TypeScript
       - 主要功能：[描述]
       - 约束条件：[如有]
   
   └─> @frontend/components 请提供组件开发规范
       - 命名规范
       - 代码风格
       - 样式要求

3. 编码实现
   └─> 遵循 10 大设计原则
   └─> 遵循前端命名规范
   └─> 使用 TypeScript 严格模式
   └─> 使用 UnoCSS 样式系统

4. 代码审查 [必须调用]
   └─> @architecture-assistant 请审查这段组件代码
       - 检查 10 大设计原则
       - 检查架构合理性
       - 检查可测试性
   
   └─> @frontend/components 请检查这个组件
       - 命名是否符合规范
       - 代码风格是否正确
       - 样式是否使用 UnoCSS

5. 测试验证
   └─> 编写单元测试
   └─> 运行类型检查
   └─> 运行构建

6. 文档化
   └─> 如有重要决策，创建 ADR
   └─> @architecture-assistant 为 [决策] 创建 ADR
```

### 流程 2: 组件重构

```
1. 识别问题
   └─> 分析违反的原则
   └─> 识别性能问题

2. 制定方案 [必须调用]
   └─> @architecture-assistant 请审查这段代码并提供改进建议
   └─> @frontend/components 请提供重构建议

3. 实施重构
   └─> 应用推荐原则
   └─> 保持向后兼容
   └─> 优化性能（memo, useCallback）

4. 验证结果 [必须调用]
   └─> @architecture-assistant 请验证重构后的代码
   └─> @frontend/components 请检查重构后的组件
```

---

## 架构原则应用

### 10 大设计原则在组件中的应用

| 原则 | 组件中的应用 | 示例 |
|------|-------------|------|
| **SoC** | UI、逻辑、数据分离 | UI 组件 + 容器组件 |
| **SRP** | 每个组件只做一件事 | Button 只负责按钮，不负责业务逻辑 |
| **DRY** | 抽取重复逻辑到 Hooks | `useUserList` 复用 |
| **KISS** | 保持组件简单，避免过度设计 | 避免过多 props |
| **组合优于继承** | 使用组合模式 | `<Card><CardHeader /></Card>` |
| **高内聚低耦合** | 组件职责明确，依赖清晰 | 通过 props 注入依赖 |
| **显式依赖** | 所有依赖通过 props 传递 | 不使用全局变量 |
| **快速失败** | 输入验证，立即报错 | Props 类型检查 |
| **不可变性** | 使用不可变数据 | `useReducer` + `immer` |
| **可测试性** | 组件易于测试 | 纯 UI 组件 + 可 mock 的 Hook |

### 组件设计模式

#### 1. 容器组件模式
```typescript
// ✅ 容器组件：负责数据管理
const UserListContainer: React.FC<UserListContainerProps> = ({ userId }) => {
  const { users, loading, error } = useUserList(userId)
  
  if (loading) return <Loading />
  if (error) return <Error message={error} />
  
  return <UserListUI users={users} />
}

// ✅ UI 组件：负责展示
const UserListUI: React.FC<UserListUIProps> = ({ users }) => {
  return (
    <div className="user-list">
      {users.map(user => (
        <UserCard key={user.id} user={user} />
      ))}
    </div>
  )
}
```

#### 2. 高阶组件模式
```typescript
// ✅ HOC：增强组件功能
const withAuth = <P extends object>(Component: React.ComponentType<P>) => {
  return function WithAuth(props: P) {
    const { user } = useAuth()
    
    if (!user) {
      return <LoginPrompt />
    }
    
    return <Component {...props} user={user} />
  }
}

// 使用
const ProtectedUserCard = withAuth(UserCard)
```

#### 3. Render Props 模式
```typescript
// ✅ Render Props：复用逻辑
const DataFetcher: React.FC<DataFetcherProps> = ({ url, render }) => {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)
  
  useEffect(() => {
    setLoading(true)
    fetch(url)
      .then(res => res.json())
      .then(data => {
        setData(data)
        setLoading(false)
      })
  }, [url])
  
  return render({ data, loading })
}

// 使用
<DataFetcher
  url="/api/users"
  render={({ data, loading }) => (
    loading ? <Loading /> : <UserList users={data} />
  )}
/>
```

---

## 组件审查清单

### 编码前检查

- [ ] 已调用 `@architecture-assistant` 进行设计指导
- [ ] 已调用 `@frontend/components` 获取规范
- [ ] 理解组件职责和边界
- [ ] 确认没有违反 SRP 和 SoC
- [ ] 确认组件命名符合规范

### 编码中检查

- [ ] 每个组件遵循单一职责
- [ ] 使用显式依赖注入（props）
- [ ] 考虑可测试性（可 mock 的依赖）
- [ ] 避免代码重复（DRY）
- [ ] 保持简单（KISS）
- [ ] TypeScript 类型完整
- [ ] 使用 React Hooks 规范
- [ ] 使用 UnoCSS 样式系统
- [ ] 使用 CSS 变量
- [ ] 无内联样式

### 编码后检查

- [ ] 已调用 `@architecture-assistant` 进行代码审查
- [ ] 已调用 `@frontend/components` 进行规范检查
- [ ] 修复所有严重问题
- [ ] 如有重要决策，已创建 ADR
- [ ] 代码符合语言最佳实践
- [ ] 通过类型检查
- [ ] 通过构建

### 提交前检查

- [ ] 通过架构技能审查
- [ ] 通过前端规范检查
- [ ] 原则违反数 < 2
- [ ] ADR 已创建（如需要）
- [ ] 文档已更新
- [ ] 运行 `pnpm lint`

---

## 最佳实践示例

### 示例 1: 基础按钮组件

```typescript
// Button.tsx
import type { FC, ReactNode } from 'react'
import { useCallback, useState } from 'react'

interface ButtonProps {
  children: ReactNode
  variant?: 'primary' | 'secondary' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  onClick?: () => void | Promise<void>
  disabled?: boolean
  loading?: boolean
  className?: string
}

// 使用 memo 优化性能
export const Button: FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  onClick,
  disabled = false,
  loading = false,
  className = '',
}) => {
  const [internalLoading, setInternalLoading] = useState(false)

  // 使用 useCallback 优化事件处理
  const handleClick = useCallback(async () => {
    if (disabled || loading || internalLoading) return
    
    setInternalLoading(true)
    try {
      await onClick?.()
    } finally {
      setInternalLoading(false)
    }
  }, [disabled, loading, internalLoading, onClick])

  const isLoading = loading || internalLoading

  return (
    <button
      className={`
        btn-${variant} 
        size-${size}
        ${isLoading ? 'opacity-50 cursor-not-allowed' : ''}
        ${className}
      `}
      onClick={handleClick}
      disabled={disabled || isLoading}
    >
      {isLoading ? '加载中...' : children}
    </button>
  )
}

Button.displayName = 'Button'
```

### 示例 2: 用户卡片组件

```typescript
// UserCard.tsx
import type { FC } from 'react'
import { memo, useCallback } from 'react'

interface User {
  id: string
  name: string
  email: string
  avatar?: string
}

interface UserCardProps {
  user: User
  onEdit?: (id: string) => void
  onDelete?: (id: string) => Promise<void>
  variant?: 'compact' | 'detailed'
}

// 使用 memo 优化性能
export const UserCard: FC<UserCardProps> = memo(({ user, onEdit, onDelete, variant = 'compact' }) => {
  // 使用 useCallback 优化事件处理
  const handleEdit = useCallback(() => {
    onEdit?.(user.id)
  }, [onEdit, user.id])

  const handleDelete = useCallback(async () => {
    if (confirm('确定删除吗？')) {
      await onDelete?.(user.id)
    }
  }, [onDelete, user.id])

  return (
    <div className="card hover:shadow-lg transition">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="font-semibold text-gray-900 dark:text-white">
            {user.name}
          </h3>
          <p className="text-sm text-gray-500">{user.email}</p>
          {variant === 'detailed' && user.avatar && (
            <img src={user.avatar} alt={user.name} className="w-16 h-16 rounded-full" />
          )}
        </div>
        <div className="flex gap-2">
          <Button onClick={handleEdit} variant="primary" size="sm">
            编辑
          </Button>
          <Button onClick={handleDelete} variant="danger" size="sm">
            删除
          </Button>
        </div>
      </div>
    </div>
  )
})

UserCard.displayName = 'UserCard'
```

### 示例 3: 表单组件

```typescript
// LoginForm.tsx
import type { FC } from 'react'
import { useCallback, useState } from 'react'

interface LoginFormProps {
  onSubmit: (data: { email: string; password: string }) => Promise<void>
  onSuccess?: () => void
}

export const LoginForm: FC<LoginFormProps> = ({ onSubmit, onSuccess }) => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // 验证函数
  const validate = useCallback(() => {
    if (!email || !password) {
      setError('请填写所有字段')
      return false
    }
    if (!email.includes('@')) {
      setError('邮箱格式不正确')
      return false
    }
    return true
  }, [email, password])

  // 提交处理
  const handleSubmit = useCallback(async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!validate()) return
    
    setLoading(true)
    setError(null)
    
    try {
      await onSubmit({ email, password })
      onSuccess?.()
    } catch (err) {
      setError(err instanceof Error ? err.message : '登录失败')
    } finally {
      setLoading(false)
    }
  }, [email, password, onSubmit, onSuccess, validate])

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="email" className="block text-sm font-medium">
          邮箱
        </label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full px-3 py-2 border rounded-md"
          disabled={loading}
        />
      </div>
      
      <div>
        <label htmlFor="password" className="block text-sm font-medium">
          密码
        </label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full px-3 py-2 border rounded-md"
          disabled={loading}
        />
      </div>
      
      {error && (
        <div className="text-danger text-sm">
          {error}
        </div>
      )}
      
      <Button type="submit" loading={loading} variant="primary" className="w-full">
        登录
      </Button>
    </form>
  )
}
```

### 示例 4: 自定义 Hook

```typescript
// useModal.ts
import { useState, useCallback } from 'react'

interface UseModalReturn {
  isOpen: boolean
  open: () => void
  close: () => void
  toggle: () => void
}

export function useModal(initialState = false): UseModalReturn {
  const [isOpen, setIsOpen] = useState(initialState)

  const open = useCallback(() => {
    setIsOpen(true)
  }, [])

  const close = useCallback(() => {
    setIsOpen(false)
  }, [])

  const toggle = useCallback(() => {
    setIsOpen(prev => !prev)
  }, [])

  // ESC 键关闭
  useEffect(() => {
    if (!isOpen) return

    const handleEsc = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        close()
      }
    }

    document.addEventListener('keydown', handleEsc)
    return () => document.removeEventListener('keydown', handleEsc)
  }, [isOpen, close])

  return { isOpen, open, close, toggle }
}
```

---

## 工具配置

### ESLint 配置

```javascript
// eslint.config.js
import antfu from '@antfu/eslint-config'

export default antfu({
  typescript: true,
  react: true,
  rules: {
    // 组件命名规范
    'react/display-name': 'error',
    'react/prop-types': 'off',
    'react/no-unused-prop-types': 'error',
    
    // Hooks 规范
    'react-hooks/rules-of-hooks': 'error',
    'react-hooks/exhaustive-deps': 'warn',
    
    // TypeScript 规范
    '@typescript-eslint/no-explicit-any': 'error',
    '@typescript-eslint/no-unused-vars': 'error',
  }
})
```

### TypeScript 配置

```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "noImplicitReturns": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "jsx": "react-jsx",
    "moduleResolution": "node",
    "esModuleInterop": true
  }
}
```

### UnoCSS 配置

```typescript
// uno.config.ts
import { defineConfig } from 'unocss'
import presetWind4 from '@unocss/preset-wind4'
import { presetAliasColors } from '@jsonlee_12138/preset-alias-colors'

export default defineConfig({
  presets: [
    presetWind4(),
    presetAliasColors({
      primary: '#3b82f6',
      secondary: '#8b5cf6',
      success: '#10b981',
      warning: '#f59e0b',
      danger: '#ef4444',
      info: '#06b6d4',
    }),
  ],
  shortcuts: {
    'btn-primary': 'bg-primary text-white hover:bg-primary-hover px-4 py-2 rounded-md transition disabled:opacity-50 disabled:cursor-not-allowed',
    'btn-secondary': 'bg-secondary text-white hover:bg-secondary-hover px-4 py-2 rounded-md transition disabled:opacity-50 disabled:cursor-not-allowed',
    'btn-danger': 'bg-danger text-white hover:bg-danger-hover px-4 py-2 rounded-md transition disabled:opacity-50 disabled:cursor-not-allowed',
    'card': 'bg-white dark:bg-gray-800 rounded-lg shadow-md p-4 hover:shadow-lg transition',
    'card-hover': 'card hover:shadow-xl cursor-pointer',
  },
})
```

---

## 快速参考

### 命名速查表

| 类型 | 规范 | 示例 |
|------|------|------|
| 组件文件 | PascalCase | `Button.tsx`, `UserCard.tsx` |
| 页面文件 | camelCase | `homePage.tsx` |
| Hook 文件 | camelCase + use | `useModal.ts` |
| Props 接口 | PascalCase + Props | `ButtonProps` |
| Props 属性 | camelCase | `onClick`, `disabled` |
| 状态变量 | camelCase | `isOpen`, `userData` |
| 事件处理 | camelCase + handle | `handleClick` |
| 常量 | UPPER_SNAKE_CASE | `DEFAULT_SIZE` |

### 组件类型速查表

| 类型 | 职责 | 示例 |
|------|------|------|
| 基础组件 | UI 展示 | `Button`, `Input`, `Card` |
| 业务组件 | 业务逻辑 + UI | `UserProfile`, `ArticleCard` |
| 容器组件 | 数据管理 | `UserListContainer` |
| 页面组件 | 路由级组合 | `HomePage` |
| 布局组件 | 页面结构 | `MainLayout` |

### 原则应用速查表

| 原则 | 组件中的应用 |
|------|-------------|
| SoC | UI、逻辑、数据分离 |
| SRP | 每个组件只做一件事 |
| DRY | 抽取重复逻辑到 Hooks |
| KISS | 保持组件简单 |
| 组合优于继承 | 使用组合模式 |
| 高内聚低耦合 | 通过 props 注入依赖 |
| 显式依赖 | 所有依赖通过 props 传递 |
| 快速失败 | 输入验证，立即报错 |
| 不可变性 | 使用不可变数据 |
| 可测试性 | 组件易于测试 |

---

## 总结

### 核心要求

1. **双重规范** - 同时满足 `@frontend/` 和 `@architecture/` 规范
2. **技能调用** - 设计和审查必须调用对应技能
3. **命名规范** - 严格遵循前端命名规范
4. **架构原则** - 应用 10 大设计原则
5. **类型安全** - 使用 TypeScript 严格模式
6. **样式系统** - 使用 UnoCSS + CSS 变量
7. **性能优化** - 使用 memo、useCallback 等
8. **可测试性** - 设计时考虑测试便利性

### 提交前检查

- ✅ 已调用 `@architecture-assistant` 进行设计
- ✅ 已调用 `@frontend/components` 进行规范检查
- ✅ 命名符合规范
- ✅ 类型完整
- ✅ 遵循 10 大设计原则
- ✅ 使用 UnoCSS
- ✅ 通过类型检查
- ✅ 通过构建

---

**版本**: 1.0
**状态**: ✅ 已批准
**最后更新**: 2026-01-19
**适用范围**: 所有前端组件开发
