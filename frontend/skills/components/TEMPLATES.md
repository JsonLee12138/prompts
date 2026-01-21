# 组件模板示例

> **版本**: 1.0
> **适用场景**: 组件开发模板参考

---

## 📋 目录

- [基础组件模板](#基础组件模板)
- [业务组件模板](#业务组件模板)
- [容器组件模板](#容器组件模板)
- [页面组件模板](#页面组件模板)
- [布局组件模板](#布局组件模板)
- [Hook 组件模板](#hook-组件模板)
- [高阶组件模板](#高阶组件模板)

---

## 基础组件模板

### Button 组件模板

```typescript
// Button.tsx
import type { FC, ReactNode } from 'react'
import { useCallback, useState } from 'react'

/**
 * 按钮组件
 * 
 * 支持多种变体、尺寸和状态
 * 
 * @example
 * ```tsx
 * <Button variant="primary" size="md" onClick={handleClick}>
 *   点击我
 * </Button>
 * ```
 */
interface ButtonProps {
  /** 按钮内容 */
  children: ReactNode
  /** 按钮变体 */
  variant?: 'primary' | 'secondary' | 'danger'
  /** 按钮尺寸 */
  size?: 'sm' | 'md' | 'lg'
  /** 点击事件 */
  onClick?: () => void | Promise<void>
  /** 是否禁用 */
  disabled?: boolean
  /** 是否加载中 */
  loading?: boolean
  /** 自定义类名 */
  className?: string
  /** 按钮类型 */
  type?: 'button' | 'submit' | 'reset'
}

/**
 * 按钮组件
 * 
 * 支持多种变体、尺寸和状态
 * 
 * @param props - 按钮属性
 * @returns React 组件
 * 
 * @example
 * ```tsx
 * <Button variant="primary" size="md" onClick={handleClick}>
 *   点击我
 * </Button>
 * ```
 */
export const Button: FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  onClick,
  disabled = false,
  loading = false,
  className = '',
  type = 'button',
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
      type={type}
    >
      {isLoading ? '加载中...' : children}
    </button>
  )
}

Button.displayName = 'Button'
```

### Input 组件模板

```typescript
// Input.tsx
import type { FC, ChangeEvent } from 'react'
import { useCallback } from 'react'

/**
 * 输入框组件
 * 
 * 支持多种类型和状态
 * 
 * @example
 * ```tsx
 * <Input 
 *   type="text"
 *   value={value}
 *   onChange={handleChange}
 *   placeholder="请输入"
 * />
 * ```
 */
interface InputProps {
  /** 输入框值 */
  value: string
  /** 值变化事件 */
  onChange: (value: string) => void
  /** 输入框类型 */
  type?: 'text' | 'password' | 'email' | 'number'
  /** 占位符 */
  placeholder?: string
  /** 是否禁用 */
  disabled?: boolean
  /** 是否只读 */
  readonly?: boolean
  /** 是否必填 */
  required?: boolean
  /** 最大长度 */
  maxLength?: number
  /** 自定义类名 */
  className?: string
  /** 标签 */
  label?: string
  /** 错误信息 */
  error?: string
}

/**
 * 输入框组件
 * 
 * @param props - 输入框属性
 * @returns React 组件
 * 
 * @example
 * ```tsx
 * <Input 
 *   type="text"
 *   value={value}
 *   onChange={handleChange}
 *   placeholder="请输入"
 * />
 * ```
 */
export const Input: FC<InputProps> = ({
  value,
  onChange,
  type = 'text',
  placeholder = '',
  disabled = false,
  readonly = false,
  required = false,
  maxLength,
  className = '',
  label,
  error,
}) => {
  const handleChange = useCallback((e: ChangeEvent<HTMLInputElement>) => {
    onChange(e.target.value)
  }, [onChange])

  return (
    <div className="input-container">
      {label && (
        <label className="input-label">
          {label}
          {required && <span className="text-danger">*</span>}
        </label>
      )}
      <input
        type={type}
        value={value}
        onChange={handleChange}
        placeholder={placeholder}
        disabled={disabled}
        readOnly={readonly}
        required={required}
        maxLength={maxLength}
        className={`input-field ${error ? 'border-danger' : ''} ${className}`}
      />
      {error && <div className="input-error">{error}</div>}
    </div>
  )
}

Input.displayName = 'Input'
```

### Card 组件模板

```typescript
// Card.tsx
import type { FC, ReactNode } from 'react'

/**
 * 卡片组件
 * 
 * 通用的卡片容器
 * 
 * @example
 * ```tsx
 * <Card>
 *   <CardHeader>标题</CardHeader>
 *   <CardBody>内容</CardBody>
 * </Card>
 * ```
 */
interface CardProps {
  /** 卡片内容 */
  children: ReactNode
  /** 自定义类名 */
  className?: string
  /** 是否有阴影 */
  shadow?: boolean
  /** 是否可悬停 */
  hover?: boolean
}

/**
 * 卡片容器组件
 * 
 * @param props - 卡片属性
 * @returns React 组件
 * 
 * @example
 * ```tsx
 * <Card shadow hover>
 *   <CardHeader>标题</CardHeader>
 *   <CardBody>内容</CardBody>
 * </Card>
 * ```
 */
export const Card: FC<CardProps> = ({
  children,
  className = '',
  shadow = true,
  hover = false,
}) => {
  return (
    <div
      className={`
        card
        ${shadow ? 'shadow-md' : ''}
        ${hover ? 'hover:shadow-lg transition' : ''}
        ${className}
      `}
    >
      {children}
    </div>
  )
}

Card.displayName = 'Card'

/**
 * 卡片头部组件
 */
interface CardHeaderProps {
  children: ReactNode
  className?: string
}

export const CardHeader: FC<CardHeaderProps> = ({ children, className = '' }) => {
  return <div className={`card-header ${className}`}>{children}</div>
}

CardHeader.displayName = 'CardHeader'

/**
 * 卡片内容组件
 */
interface CardBodyProps {
  children: ReactNode
  className?: string
}

export const CardBody: FC<CardBodyProps> = ({ children, className = '' }) => {
  return <div className={`card-body ${className}`}>{children}</div>
}

CardBody.displayName = 'CardBody'
```

---

## 业务组件模板

### UserCard 组件模板

```typescript
// UserCard.tsx
import type { FC } from 'react'
import { memo, useCallback } from 'react'

/**
 * 用户卡片组件
 * 
 * 显示用户信息和操作按钮
 * 
 * @example
 * ```tsx
 * <UserCard 
 *   userId="123" 
 *   onEdit={handleEdit}
 *   onDelete={handleDelete}
 * />
 * ```
 */
interface User {
  id: string
  name: string
  email: string
  avatar?: string
  role?: 'admin' | 'user' | 'guest'
}

interface UserCardProps {
  /** 用户 ID */
  userId: string
  /** 编辑回调 */
  onEdit?: (id: string) => void
  /** 删除回调 */
  onDelete?: (id: string) => Promise<void>
  /** 卡片变体 */
  variant?: 'compact' | 'detailed'
}

/**
 * 用户卡片组件
 * 
 * 显示用户信息和操作按钮
 * 
 * @param props - 用户卡片属性
 * @returns React 组件
 * 
 * @example
 * ```tsx
 * <UserCard 
 *   userId="123" 
 *   onEdit={handleEdit}
 *   onDelete={handleDelete}
 * />
 * ```
 */
export const UserCard: FC<UserCardProps> = memo(({ userId, onEdit, onDelete, variant = 'compact' }) => {
  // 使用自定义 Hook 获取用户数据
  const { user, loading, error } = useUser(userId)
  const { deleteUser } = useUserActions()

  // 使用 useCallback 优化事件处理
  const handleEdit = useCallback(() => {
    onEdit?.(userId)
  }, [onEdit, userId])

  const handleDelete = useCallback(async () => {
    if (confirm('确定删除吗？')) {
      await onDelete?.(userId)
      await deleteUser(userId)
    }
  }, [onDelete, userId, deleteUser])

  if (loading) {
    return (
      <div className="card">
        <div className="animate-pulse">加载中...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="card border-danger">
        <div className="text-danger">错误: {error}</div>
      </div>
    )
  }

  if (!user) {
    return (
      <div className="card">
        <div>用户不存在</div>
      </div>
    )
  }

  return (
    <div className="card hover:shadow-lg transition">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          {variant === 'detailed' && user.avatar && (
            <img 
              src={user.avatar} 
              alt={user.name} 
              className="w-16 h-16 rounded-full object-cover"
            />
          )}
          <div>
            <h3 className="font-semibold text-gray-900 dark:text-white">
              {user.name}
            </h3>
            <p className="text-sm text-gray-500">{user.email}</p>
            {user.role && (
              <span className="text-xs px-2 py-1 bg-primary/10 text-primary rounded">
                {user.role}
              </span>
            )}
          </div>
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

### ArticleCard 组件模板

```typescript
// ArticleCard.tsx
import type { FC } from 'react'
import { memo, useCallback } from 'react'

/**
 * 文章卡片组件
 * 
 * 显示文章信息和操作按钮
 * 
 * @example
 * ```tsx
 * <ArticleCard 
 *   articleId="456" 
 *   onRead={handleRead}
 *   onEdit={handleEdit}
 * />
 * ```
 */
interface Article {
  id: string
  title: string
  excerpt: string
  author: string
  publishDate: string
  readCount: number
  coverImage?: string
}

interface ArticleCardProps {
  /** 文章 ID */
  articleId: string
  /** 阅读回调 */
  onRead?: (id: string) => void
  /** 编辑回调 */
  onEdit?: (id: string) => void
  /** 删除回调 */
  onDelete?: (id: string) => Promise<void>
  /** 卡片变体 */
  variant?: 'compact' | 'detailed'
}

/**
 * 文章卡片组件
 * 
 * 显示文章信息和操作按钮
 * 
 * @param props - 文章卡片属性
 * @returns React 组件
 * 
 * @example
 * ```tsx
 * <ArticleCard 
 *   articleId="456" 
 *   onRead={handleRead}
 *   onEdit={handleEdit}
 * />
 * ```
 */
export const ArticleCard: FC<ArticleCardProps> = memo(({ 
  articleId, 
  onRead, 
  onEdit, 
  onDelete, 
  variant = 'compact' 
}) => {
  // 使用自定义 Hook 获取文章数据
  const { article, loading, error } = useArticle(articleId)

  // 使用 useCallback 优化事件处理
  const handleRead = useCallback(() => {
    onRead?.(articleId)
  }, [onRead, articleId])

  const handleEdit = useCallback(() => {
    onEdit?.(articleId)
  }, [onEdit, articleId])

  const handleDelete = useCallback(async () => {
    if (confirm('确定删除吗？')) {
      await onDelete?.(articleId)
    }
  }, [onDelete, articleId])

  if (loading) {
    return (
      <div className="card">
        <div className="animate-pulse">加载中...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="card border-danger">
        <div className="text-danger">错误: {error}</div>
      </div>
    )
  }

  if (!article) {
    return (
      <div className="card">
        <div>文章不存在</div>
      </div>
    )
  }

  return (
    <div className="card hover:shadow-lg transition cursor-pointer" onClick={handleRead}>
      {variant === 'detailed' && article.coverImage && (
        <img 
          src={article.coverImage} 
          alt={article.title} 
          className="w-full h-48 object-cover rounded-t-lg"
        />
      )}
      <div className="p-4">
        <h3 className="font-semibold text-lg text-gray-900 dark:text-white mb-2">
          {article.title}
        </h3>
        <p className="text-sm text-gray-600 dark:text-gray-300 mb-3">
          {article.excerpt}
        </p>
        <div className="flex items-center justify-between text-xs text-gray-500">
          <span>{article.author}</span>
          <span>{article.publishDate}</span>
          <span>阅读 {article.readCount}</span>
        </div>
        {variant === 'detailed' && (
          <div className="flex gap-2 mt-4">
            <Button onClick={handleEdit} variant="primary" size="sm">
              编辑
            </Button>
            <Button onClick={handleDelete} variant="danger" size="sm">
              删除
            </Button>
          </div>
        )}
      </div>
    </div>
  )
})

ArticleCard.displayName = 'ArticleCard'
```

---

## 容器组件模板

### UserListContainer 组件模板

```typescript
// UserListContainer.tsx
import type { FC } from 'react'
import { useState, useCallback } from 'react'

/**
 * 用户列表容器组件
 * 
 * 负责用户数据的获取和管理
 * 
 * @example
 * ```tsx
 * <UserListContainer 
 *   userId="123"
 *   onSelect={handleSelect}
 * />
 * ```
 */
interface UserListContainerProps {
  /** 用户 ID */
  userId: string
  /** 选择回调 */
  onSelect?: (id: string) => void
  /** 删除回调 */
  onDelete?: (id: string) => Promise<void>
}

/**
 * 用户列表容器组件
 * 
 * 负责用户数据的获取和管理
 * 
 * @param props - 容器属性
 * @returns React 组件
 * 
 * @example
 * ```tsx
 * <UserListContainer 
 *   userId="123"
 *   onSelect={handleSelect}
 * />
 * ```
 */
export const UserListContainer: FC<UserListContainerProps> = ({ userId, onSelect, onDelete }) => {
  // 使用自定义 Hook 获取用户列表
  const { users, loading, error, refetch } = useUserList(userId)
  
  // 搜索状态
  const [searchTerm, setSearchTerm] = useState('')
  
  // 过滤用户
  const filteredUsers = useCallback(() => {
    if (!searchTerm) return users
    return users.filter(user => 
      user.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      user.email.toLowerCase().includes(searchTerm.toLowerCase())
    )
  }, [users, searchTerm])

  // 处理搜索
  const handleSearch = useCallback((term: string) => {
    setSearchTerm(term)
  }, [])

  // 处理删除
  const handleDelete = useCallback(async (id: string) => {
    await onDelete?.(id)
    await refetch()
  }, [onDelete, refetch])

  if (loading) {
    return <Loading />
  }

  if (error) {
    return <Error message={error} onRetry={refetch} />
  }

  return (
    <div className="user-list-container">
      <div className="mb-4">
        <SearchInput 
          value={searchTerm} 
          onChange={handleSearch} 
          placeholder="搜索用户..."
        />
      </div>
      <UserListUI 
        users={filteredUsers()} 
        onSelect={onSelect}
        onDelete={handleDelete}
      />
    </div>
  )
}

UserListContainer.displayName = 'UserListContainer'
```

### ArticleListContainer 组件模板

```typescript
// ArticleListContainer.tsx
import type { FC } from 'react'
import { useState, useCallback } from 'react'

/**
 * 文章列表容器组件
 * 
 * 负责文章数据的获取和管理
 * 
 * @example
 * ```tsx
 * <ArticleListContainer 
 *   categoryId="tech"
 *   onRead={handleRead}
 * />
 * ```
 */
interface ArticleListContainerProps {
  /** 分类 ID */
  categoryId?: string
  /** 阅读回调 */
  onRead?: (id: string) => void
  /** 编辑回调 */
  onEdit?: (id: string) => void
  /** 删除回调 */
  onDelete?: (id: string) => Promise<void>
}

/**
 * 文章列表容器组件
 * 
 * 负责文章数据的获取和管理
 * 
 * @param props - 容器属性
 * @returns React 组件
 * 
 * @example
 * ```tsx
 * <ArticleListContainer 
 *   categoryId="tech"
 *   onRead={handleRead}
 * />
 * ```
 */
export const ArticleListContainer: FC<ArticleListContainerProps> = ({ 
  categoryId, 
  onRead, 
  onEdit, 
  onDelete 
}) => {
  // 使用自定义 Hook 获取文章列表
  const { articles, loading, error, refetch } = useArticleList(categoryId)
  
  // 分页状态
  const [page, setPage] = useState(1)
  const [pageSize] = useState(10)
  
  // 搜索状态
  const [searchTerm, setSearchTerm] = useState('')
  
  // 过滤文章
  const filteredArticles = useCallback(() => {
    let filtered = articles
    
    if (searchTerm) {
      filtered = filtered.filter(article => 
        article.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        article.excerpt.toLowerCase().includes(searchTerm.toLowerCase())
      )
    }
    
    // 分页
    const start = (page - 1) * pageSize
    const end = start + pageSize
    return filtered.slice(start, end)
  }, [articles, searchTerm, page, pageSize])

  // 处理搜索
  const handleSearch = useCallback((term: string) => {
    setSearchTerm(term)
    setPage(1)
  }, [])

  // 处理分页
  const handlePageChange = useCallback((newPage: number) => {
    setPage(newPage)
  }, [])

  // 处理删除
  const handleDelete = useCallback(async (id: string) => {
    await onDelete?.(id)
    await refetch()
  }, [onDelete, refetch])

  if (loading) {
    return <Loading />
  }

  if (error) {
    return <Error message={error} onRetry={refetch} />
  }

  return (
    <div className="article-list-container">
      <div className="mb-4">
        <SearchInput 
          value={searchTerm} 
          onChange={handleSearch} 
          placeholder="搜索文章..."
        />
      </div>
      <ArticleListUI 
        articles={filteredArticles()} 
        onRead={onRead}
        onEdit={onEdit}
        onDelete={handleDelete}
      />
      <Pagination
        current={page}
        pageSize={pageSize}
        total={articles.length}
        onChange={handlePageChange}
      />
    </div>
  )
}

ArticleListContainer.displayName = 'ArticleListContainer'
```

---

## 页面组件模板

### HomePage 组件模板

```typescript
// homePage.tsx
import type { NextPage } from 'next'
import { useState, useCallback } from 'react'

/**
 * 首页组件
 * 
 * 页面级组件，组合多个容器和业务组件
 * 
 * @example
 * ```tsx
 * // pages/index.tsx
 * export default HomePage
 * ```
 */
const HomePage: NextPage = () => {
  // 页面级状态
  const [selectedUserId, setSelectedUserId] = useState<string | null>(null)
  const [modalOpen, setModalOpen] = useState(false)

  // 处理用户选择
  const handleSelectUser = useCallback((userId: string) => {
    setSelectedUserId(userId)
    setModalOpen(true)
  }, [])

  // 处理编辑用户
  const handleEditUser = useCallback((userId: string) => {
    // 导航到编辑页面或打开编辑模态框
    console.log('Edit user:', userId)
  }, [])

  // 处理删除用户
  const handleDeleteUser = useCallback(async (userId: string) => {
    // 调用 API 删除用户
    await fetch(`/api/users/${userId}`, { method: 'DELETE' })
  }, [])

  // 处理模态框关闭
  const handleCloseModal = useCallback(() => {
    setModalOpen(false)
    setSelectedUserId(null)
  }, [])

  return (
    <MainLayout>
      <div className="container mx-auto p-6">
        <header className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            用户管理系统
          </h1>
          <p className="text-gray-600 dark:text-gray-300 mt-2">
            管理和查看系统用户
          </p>
        </header>

        <main className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* 左侧：用户列表 */}
          <div className="lg:col-span-2">
            <UserListContainer
              userId="current-user-id"
              onSelect={handleSelectUser}
              onDelete={handleDeleteUser}
            />
          </div>

          {/* 右侧：快速操作 */}
          <div className="lg:col-span-1">
            <Card>
              <CardHeader>
                <h2 className="text-lg font-semibold">快速操作</h2>
              </CardHeader>
              <CardBody>
                <div className="space-y-2">
                  <Button 
                    variant="primary" 
                    className="w-full"
                    onClick={() => console.log('创建用户')}
                  >
                    创建用户
                  </Button>
                  <Button 
                    variant="secondary" 
                    className="w-full"
                    onClick={() => console.log('导出数据')}
                  >
                    导出数据
                  </Button>
                </div>
              </CardBody>
            </Card>
          </div>
        </main>

        {/* 用户详情模态框 */}
        {modalOpen && selectedUserId && (
          <UserDetailModal
            userId={selectedUserId}
            onClose={handleCloseModal}
            onEdit={handleEditUser}
          />
        )}
      </div>
    </MainLayout>
  )
}

export default HomePage
```

### UserSettingsPage 组件模板

```typescript
// userSettingsPage.tsx
import type { NextPage } from 'next'
import { useState, useCallback } from 'react'

/**
 * 用户设置页面组件
 * 
 * 页面级组件，处理用户设置
 * 
 * @example
 * ```tsx
 * // pages/settings.tsx
 * export default UserSettingsPage
 * ```
 */
const UserSettingsPage: NextPage = () => {
  // 页面级状态
  const [activeTab, setActiveTab] = useState<'profile' | 'security' | 'preferences'>('profile')
  
  // 处理标签切换
  const handleTabChange = useCallback((tab: 'profile' | 'security' | 'preferences') => {
    setActiveTab(tab)
  }, [])

  return (
    <MainLayout>
      <div className="container mx-auto p-6">
        <header className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            用户设置
          </h1>
          <p className="text-gray-600 dark:text-gray-300 mt-2">
            管理您的账户设置
          </p>
        </header>

        <main className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* 左侧：导航 */}
          <div className="lg:col-span-1">
            <Card>
              <CardBody>
                <nav className="space-y-2">
                  <Button
                    variant={activeTab === 'profile' ? 'primary' : 'secondary'}
                    className="w-full text-left"
                    onClick={() => handleTabChange('profile')}
                  >
                    个人资料
                  </Button>
                  <Button
                    variant={activeTab === 'security' ? 'primary' : 'secondary'}
                    className="w-full text-left"
                    onClick={() => handleTabChange('security')}
                  >
                    安全设置
                  </Button>
                  <Button
                    variant={activeTab === 'preferences' ? 'primary' : 'secondary'}
                    className="w-full text-left"
                    onClick={() => handleTabChange('preferences')}
                  >
                    偏好设置
                  </Button>
                </nav>
              </CardBody>
            </Card>
          </div>

          {/* 右侧：内容 */}
          <div className="lg:col-span-3">
            {activeTab === 'profile' && <ProfileSettings />}
            {activeTab === 'security' && <SecuritySettings />}
            {activeTab === 'preferences' && <PreferencesSettings />}
          </div>
        </main>
      </div>
    </MainLayout>
  )
}

export default UserSettingsPage
```

---

## 布局组件模板

### MainLayout 组件模板

```typescript
// MainLayout.tsx
import type { FC, ReactNode } from 'react'
import { useState, useCallback } from 'react'

/**
 * 主布局组件
 * 
 * 提供页面整体布局结构
 * 
 * @example
 * ```tsx
 * <MainLayout>
 *   <div>页面内容</div>
 * </MainLayout>
 * ```
 */
interface MainLayoutProps {
  /** 页面内容 */
  children: ReactNode
  /** 自定义类名 */
  className?: string
}

/**
 * 主布局组件
 * 
 * @param props - 布局属性
 * @returns React 组件
 * 
 * @example
 * ```tsx
 * <MainLayout>
 *   <div>页面内容</div>
 * </MainLayout>
 * ```
 */
export const MainLayout: FC<MainLayoutProps> = ({ children, className = '' }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false)

  const toggleSidebar = useCallback(() => {
    setSidebarOpen(prev => !prev)
  }, [])

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* 顶部导航 */}
      <Header onToggleSidebar={toggleSidebar} />

      <div className="flex">
        {/* 侧边栏 */}
        <aside
          className={`
            fixed lg:static inset-y-0 left-0 z-50
            w-64 bg-white dark:bg-gray-800 shadow-lg
            transform transition-transform duration-300
            ${sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
          `}
        >
          <Sidebar />
        </aside>

        {/* 主内容 */}
        <main className={`flex-1 p-6 ${className}`}>
          {children}
        </main>
      </div>

      {/* 移动端遮罩 */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}
    </div>
  )
}

MainLayout.displayName = 'MainLayout'
```

### AuthLayout 组件模板

```typescript
// AuthLayout.tsx
import type { FC, ReactNode } from 'react'

/**
 * 认证布局组件
 * 
 * 提供登录/注册页面布局
 * 
 * @example
 * ```tsx
 * <AuthLayout>
 *   <LoginForm />
 * </AuthLayout>
 * ```
 */
interface AuthLayoutProps {
  /** 页面内容 */
  children: ReactNode
  /** 自定义类名 */
  className?: string
}

/**
 * 认证布局组件
 * 
 * @param props - 布局属性
 * @returns React 组件
 * 
 * @example
 * ```tsx
 * <AuthLayout>
 *   <LoginForm />
 * </AuthLayout>
 * ```
 */
export const AuthLayout: FC<AuthLayoutProps> = ({ children, className = '' }) => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <h2 className="text-3xl font-extrabold text-gray-900 dark:text-white">
            欢迎回来
          </h2>
          <p className="mt-2 text-sm text-gray-600 dark:text-gray-300">
            请登录您的账户
          </p>
        </div>
        <div className={`bg-white dark:bg-gray-800 py-8 px-6 shadow rounded-lg sm:px-10 ${className}`}>
          {children}
        </div>
      </div>
    </div>
  )
}

AuthLayout.displayName = 'AuthLayout'
```

---

## Hook 组件模板

### useModal Hook 模板

```typescript
// useModal.ts
import { useState, useCallback, useEffect } from 'react'

/**
 * 模态框 Hook
 * 
 * 管理模态框的打开、关闭和切换状态
 * 
 * @example
 * ```tsx
 * const { isOpen, open, close, toggle } = useModal(false)
 * ```
 */
interface UseModalReturn {
  /** 模态框是否打开 */
  isOpen: boolean
  /** 打开模态框 */
  open: () => void
  /** 关闭模态框 */
  close: () => void
  /** 切换模态框 */
  toggle: () => void
}

/**
 * 模态框 Hook
 * 
 * @param initialState - 初始状态（默认 false）
 * @returns 模态框状态和控制函数
 * 
 * @example
 * ```tsx
 * const { isOpen, open, close, toggle } = useModal(false)
 * 
 * return (
 *   <>
 *     <button onClick={open}>打开</button>
 *     {isOpen && <Modal onClose={close}>内容</Modal>}
 *   </>
 * )
 * ```
 */
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

### useAuth Hook 模板

```typescript
// useAuth.ts
import { useState, useCallback, useEffect, createContext, useContext } from 'react'

/**
 * 用户接口
 */
interface User {
  id: string
  name: string
  email: string
  role: string
}

/**
 * 认证上下文类型
 */
interface AuthContextType {
  user: User | null
  loading: boolean
  error: string | null
  login: (email: string, password: string) => Promise<void>
  logout: () => Promise<void>
  register: (userData: RegisterData) => Promise<void>
}

/**
 * 注册数据接口
 */
interface RegisterData {
  name: string
  email: string
  password: string
}

/**
 * 认证上下文
 */
const AuthContext = createContext<AuthContextType | null>(null)

/**
 * 认证 Hook
 * 
 * 管理用户认证状态
 * 
 * @example
 * ```tsx
 * const { user, login, logout } = useAuth()
 * ```
 */
export function useAuth(): AuthContextType {
  const context = useContext(AuthContext)
  
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  
  return context
}

/**
 * 认证 Provider 组件
 */
export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // 检查登录状态
  useEffect(() => {
    checkAuth()
  }, [])

  const checkAuth = useCallback(async () => {
    setLoading(true)
    try {
      const token = localStorage.getItem('token')
      if (!token) {
        setUser(null)
        return
      }

      const response = await fetch('/api/auth/me', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      if (response.ok) {
        const data = await response.json()
        setUser(data.user)
      } else {
        localStorage.removeItem('token')
        setUser(null)
      }
    } catch (err) {
      console.error('Auth check failed:', err)
    } finally {
      setLoading(false)
    }
  }, [])

  const login = useCallback(async (email: string, password: string) => {
    setLoading(true)
    setError(null)

    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.message || '登录失败')
      }

      localStorage.setItem('token', data.token)
      setUser(data.user)
    } catch (err) {
      const message = err instanceof Error ? err.message : '登录失败'
      setError(message)
      throw err
    } finally {
      setLoading(false)
    }
  }, [])

  const logout = useCallback(async () => {
    setLoading(true)
    try {
      await fetch('/api/auth/logout', { method: 'POST' })
      localStorage.removeItem('token')
      setUser(null)
    } catch (err) {
      console.error('Logout failed:', err)
    } finally {
      setLoading(false)
    }
  }, [])

  const register = useCallback(async (userData: RegisterData) => {
    setLoading(true)
    setError(null)

    try {
      const response = await fetch('/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.message || '注册失败')
      }

      localStorage.setItem('token', data.token)
      setUser(data.user)
    } catch (err) {
      const message = err instanceof Error ? err.message : '注册失败'
      setError(message)
      throw err
    } finally {
      setLoading(false)
    }
  }, [])

  const value: AuthContextType = {
    user,
    loading,
    error,
    login,
    logout,
    register,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
```

---

## 高阶组件模板

### withAuth HOC 模板

```typescript
// withAuth.tsx
import type { ComponentType, FC } from 'react'
import { useAuth } from './useAuth'

/**
 * 认证高阶组件
 * 
 * 包装组件，要求用户必须登录才能访问
 * 
 * @example
 * ```tsx
 * const ProtectedPage = withAuth(PageComponent)
 * ```
 */
interface WithAuthProps {
  user: User
}

/**
 * 认证高阶组件
 * 
 * @param Component - 需要保护的组件
 * @returns 包装后的组件
 * 
 * @example
 * ```tsx
 * const ProtectedPage = withAuth(PageComponent)
 * ```
 */
export function withAuth<P extends object>(
  Component: ComponentType<P & WithAuthProps>
): FC<P> {
  return function WithAuthWrapper(props: P) {
    const { user, loading } = useAuth()

    if (loading) {
      return <Loading />
    }

    if (!user) {
      return <LoginPrompt />
    }

    return <Component {...props} user={user} />
  }
}
```

### withLogger HOC 模板

```typescript
// withLogger.tsx
import type { ComponentType, FC } from 'react'
import { useEffect } from 'react'

/**
 * 日志高阶组件
 * 
 * 记录组件生命周期和 props 变化
 * 
 * @example
 * ```tsx
 * const LoggedComponent = withLogger(MyComponent)
 * ```
 */
interface WithLoggerProps {
  componentName?: string
}

/**
 * 日志高阶组件
 * 
 * @param Component - 需要记录日志的组件
 * @returns 包装后的组件
 * 
 * @example
 * ```tsx
 * const LoggedComponent = withLogger(MyComponent)
 * ```
 */
export function withLogger<P extends object>(
  Component: ComponentType<P>
): FC<P & WithLoggerProps> {
  return function WithLoggerWrapper(props: P & WithLoggerProps) {
    const componentName = props.componentName || Component.displayName || Component.name

    useEffect(() => {
      console.log(`[${componentName}] Component mounted`)
      return () => {
        console.log(`[${componentName}] Component unmounted`)
      }
    }, [componentName])

    useEffect(() => {
      console.log(`[${componentName}] Props updated:`, props)
    }, [componentName, props])

    return <Component {...props} />
  }
}
```

---

## 使用示例

### 示例 1: 创建新组件

```bash
# 1. 复制模板
cp frontend/components/TEMPLATES.md frontend/components/examples/

# 2. 根据模板修改
# - 修改组件名称
# - 修改 Props 接口
# - 修改实现逻辑
# - 添加业务逻辑

# 3. 审查代码
@frontend/components 请审查这个组件

# 4. 优化改进
@architecture-assistant 请审查这段代码是否符合架构原则
```

### 示例 2: 使用模板创建页面

```typescript
// pages/user/[id].tsx
import type { NextPage } from 'next'
import { useRouter } from 'next/router'

const UserDetailPage: NextPage = () => {
  const router = useRouter()
  const { id } = router.query

  return (
    <MainLayout>
      <div className="container mx-auto p-6">
        <UserDetailContainer userId={id as string} />
      </div>
    </MainLayout>
  )
}

export default UserDetailPage
```

---

## 快速参考

### 模板类型速查表

| 模板类型 | 文件名 | 用途 |
|---------|--------|------|
| 基础组件 | `Button.tsx`, `Input.tsx` | UI 展示 |
| 业务组件 | `UserCard.tsx`, `ArticleCard.tsx` | 业务逻辑 + UI |
| 容器组件 | `UserListContainer.tsx` | 数据管理 |
| 页面组件 | `homePage.tsx` | 路由级组合 |
| 布局组件 | `MainLayout.tsx` | 页面结构 |
| Hook 组件 | `useModal.ts` | 状态管理 |
| HOC 组件 | `withAuth.tsx` | 功能增强 |

### 模板使用步骤

1. **选择模板** - 根据组件类型选择合适的模板
2. **复制模板** - 复制模板代码到新文件
3. **修改名称** - 修改组件名和文件名
4. **定义 Props** - 根据需求定义 Props 接口
5. **实现逻辑** - 实现组件逻辑
6. **添加样式** - 使用 UnoCSS 添加样式
7. **审查代码** - 调用技能进行审查
8. **优化改进** - 根据反馈优化代码

---

**版本**: 1.0
**状态**: 已批准
**最后更新**: 2026-01-19
**适用范围**: 所有前端组件开发
