# CMS 框架编码规范

> 本文档定义了 Headless CMS 项目的框架层面编码规范，确保代码的一致性、可维护性和可扩展性。

## 📑 目录

- [1. 项目结构规范](#1-项目结构规范)
- [2. 模块化规范](#2-模块化规范)
- [3. 命名规范](#3-命名规范)
- [4. 类型与接口规范](#4-类型与接口规范)
- [5. 依赖注入规范](#5-依赖注入规范)
- [6. 数据层规范 (Ent ORM)](#6-数据层规范-ent-orm)
- [7. HTTP 层规范 (Chi 框架)](#7-http-层规范-chi-框架)
- [8. 响应格式规范](#8-响应格式规范)
- [9. Schema 驱动开发规范](#9-schema-驱动开发规范)
- [10. 权限规范 (Casbin)](#10-权限规范-casbin)
- [11. API Key 认证规范](#11-api-key-认证规范)
- [12. 错误处理规范](#12-错误处理规范)
- [13. 上下文规范](#13-上下文规范)
- [14. 多租户规范](#14-多租户规范)
- [15. 插件开发规范](#15-插件开发规范)
- [16. 性能优化规范](#16-性能优化规范)
- [17. 安全规范](#17-安全规范)
- [18. 测试规范](#18-测试规范)

---

## 1. 项目结构规范

### 1.1 目录边界

**✅ 强制规则**

```bash
# 只考虑以下目录
cms/              # 主业务目录
core/             # 核心封装库（只使用，不修改）
```

### 1.2 标准目录结构

```
cms/
├── cmd/                      # 命令行入口
│   ├── server/               # 服务器主程序
│   │   └── main.go           # 启动文件
│   └── cli/                  # CLI 工具
│       ├── main.go           # CLI 入口
│       └── cmd/              # CLI 命令
│           ├── generate.go   # 代码生成
│           └── init.go       # 初始化
│
├── api/v1/                   # 业务模块（按版本组织）
│   ├── user/                 # 用户模块
│   │   ├── schema.json       # Schema 定义（单一数据源）
│   │   ├── module.go         # 模块定义
│   │   ├── controller.go     # HTTP 控制器
│   │   ├── service.go        # 业务逻辑
│   │   └── dto.go            # 数据传输对象
│   └── article/              # 文章模块
│       ├── schema.json       # Schema 定义
│       └── ...               # 同上
│
├── _gen/                     # Ent 生成的代码
│   ├── generate.go           # go generate 入口
│   ├── schema/               # Ent Schema 定义
│   │   ├── user.go
│   │   ├── article.go
│   │   └── api_key.go
│   ├── client.go             # Ent Client
│   ├── user.go               # User Entity
│   ├── user_create.go        # User Create Builder
│   ├── user_query.go         # User Query Builder
│   └── ...                   # 其他生成文件
│
├── core/                     # 本地核心库
│   ├── http/                 # HTTP 相关工具
│   │   ├── binding/          # 参数绑定
│   │   │   └── binding.go
│   │   ├── responder/        # 响应格式化
│   │   │   └── responder.go
│   │   └── middleware/       # 中间件
│   │       ├── auth.go       # JWT 认证中间件
│   │       ├── apikey.go     # API Key 认证中间件
│   │       ├── casbin.go     # Casbin 权限中间件
│   │       ├── tenant.go     # 多租户中间件
│   │       └── recover.go    # 恢复中间件
│   ├── plugin/               # 插件运行时
│   │   └── runtime.go
│   ├── rbac/                 # Casbin 相关
│   │   ├── enforcer.go
│   │   └── model.conf
│   ├── multitenant/          # 多租户
│   │   └── manager.go
│   └── README.md
│
├── config/                   # 配置文件
│   ├── database.go           # 数据库配置
│   ├── jwt.go                # JWT 配置
│   ├── casbin.go             # Casbin 配置
│   └── config.go             # 通用配置
│
├── plugins/                  # 自定义插件（可选）
│   ├── audit.go              # 审计插件
│   └── cache.go              # 缓存插件
│
├── docs/                     # 文档
│   └── USAGE_EXAMPLE.md
│
├── docker-compose.yml        # Docker 配置
├── Makefile                  # 构建脚本
├── go.mod                    # Go 模块
└── .env.example              # 环境变量模板
```

### 1.3 路径规范

**✅ 必须遵守**

```go
// 正确：使用 cms/_gen
import "github.com/JsonLee12138/headless-cms/cms/_gen"

// 错误：不要引用 pre-demo
import "github.com/JsonLee12138/headless-cms/pre-demo/internal/_gen"
```

---

## 2. 模块化规范

### 2.1 NestJS 风格模块

每个业务模块**必须**包含 4 个核心文件：

```
module_name/
├── module.go      # 模块定义与依赖注入
├── controller.go  # HTTP 处理器
├── service.go     # 业务逻辑
└── dto.go         # 数据传输对象
```

### 2.2 Module 文件规范

**职责**：依赖组装、路由注册

```go
package user

import (
    "github.com/JsonLee12138/headless-cms/cms/_gen"
    "github.com/JsonLee12138/headless-cms/core/http/responder"
    "github.com/go-chi/chi/v5"
    "github.com/casbin/casbin/v2"
)

// Module 必须包含 controller 和 service
type Module struct {
    controller *Controller
    service    *Service
}

// NewModule 必须接收依赖并返回完整的 Module
func NewModule(client *_gen.Client, enforcer *casbin.Enforcer) *Module {
    // 1. 创建 Service（传递数据库客户端）
    service := NewService(client)

    // 2. 创建 Responder Factory
    responderFactory := responder.NewResponderFactory(responder.DefaultPanicFn)

    // 3. 创建 Controller（传递 service、responderFactory 和 enforcer）
    controller := NewController(service, responderFactory, enforcer)

    return &Module{
        controller: controller,
        service:    service,
    }
}

// Setup 必须注册路由
func (m *Module) Setup(r chi.Router) {
    r.Route("/users", func(r chi.Router) {
        // 应用 API Key 认证中间件
        r.Use(middleware.APIKeyAuth(m.controller.enforcer))

        r.Get("/", m.controller.List)
        r.Get("/{id}", m.controller.Get)
        r.Post("/", m.controller.Create)
        r.Put("/{id}", m.controller.Update)
        r.Delete("/{id}", m.controller.Delete)
    })
}
```

### 2.3 Service 文件规范

**职责**：纯业务逻辑，不依赖 HTTP

```go
package user

import (
    "context"
    "github.com/JsonLee12138/headless-cms/cms/_gen"
    "github.com/JsonLee12138/headless-cms/cms/_gen/user"
    "github.com/google/uuid"
    "golang.org/x/crypto/bcrypt"
)

type Service struct {
    client *_gen.Client
}

func NewService(client *_gen.Client) *Service {
    return &Service{client: client}
}

// 方法签名规范：
// - 第一个参数必须是 context.Context
// - 返回值必须包含 error
func (s *Service) Create(ctx context.Context, dto *CreateDTO) (*_gen.User, error) {
    // 密码加密
    hashedPassword, err := bcrypt.GenerateFromPassword([]byte(dto.Password), bcrypt.DefaultCost)
    if err != nil {
        return nil, err
    }

    return s.client.User.Create().
        SetEmail(dto.Email).
        SetPassword(string(hashedPassword)).
        SetName(dto.Name).
        SetRole(dto.Role).
        SetTenantID(dto.TenantID).
        Save(ctx)
}

func (s *Service) List(ctx context.Context, params *ListParams) (int64, []*_gen.User, error) {
    query := s.client.User.Query()

    // 获取当前用户信息（用于多租户过滤）
    tenantID, _ := ctx.Value("tenant_id").(int64)
    if tenantID > 0 {
        query = query.Where(user.TenantIDEQ(tenantID))
    }

    // 应用过滤条件
    if params.Keyword != "" {
        query = query.Where(user.NameContains(params.Keyword))
    }
    if params.Role != "" {
        query = query.Where(user.RoleEQ(params.Role))
    }

    // 获取总数
    count, _ := query.Count(ctx)

    // 分页查询
    offset := (params.Pagination.Page - 1) * params.Pagination.PageSize
    data, err := query.
        Limit(params.Pagination.PageSize).
        Offset(offset).
        All(ctx)

    return int64(count), data, err
}
```

### 2.4 Controller 文件规范

**职责**：HTTP 层处理（绑定、验证、响应）

```go
package user

import (
    "net/http"
    "errors"
    "math"
    "github.com/JsonLee12138/headless-cms/core/http/binding"
    "github.com/JsonLee12138/headless-cms/core/http/responder"
    "github.com/go-chi/chi/v5"
    "github.com/google/uuid"
    "github.com/casbin/casbin/v2"
)

type Controller struct {
    service          *Service
    responderFactory *responder.ResponderFactory
    enforcer         *casbin.Enforcer
}

func NewController(service *Service, factory *responder.ResponderFactory, enforcer *casbin.Enforcer) *Controller {
    return &Controller{
        service:          service,
        responderFactory: factory,
        enforcer:         enforcer,
    }
}

// 标准 Handler 结构
func (c *Controller) Create(w http.ResponseWriter, r *http.Request) {
    // 1. 创建 Responder
    res := c.responderFactory.FromRequest(w, r)

    // 2. 绑定并验证参数
    var dto CreateDTO
    if err := binding.JSON(r, &dto); err != nil {
        res.WriteError(http.StatusBadRequest, responder.Error{Message: err.Error()})
        return
    }

    // 3. 从 Context 获取租户 ID
    tenantID, _ := r.Context().Value("tenant_id").(int64)
    dto.TenantID = tenantID

    // 4. 调用 Service
    data, err := c.service.Create(r.Context(), &dto)
    if err != nil {
        // 检查是否是业务错误
        if errors.Is(err, service.ErrEmailConflict) {
            res.WriteError(http.StatusConflict, responder.Error{Message: err.Error()})
        } else {
            res.WriteError(http.StatusInternalServerError, responder.Error{Message: err.Error()})
        }
        return
    }

    // 5. 返回 Strapi 风格响应
    res.Write(http.StatusCreated, responder.StrapiResponse{Data: data})
}

func (c *Controller) List(w http.ResponseWriter, r *http.Request) {
    res := c.responderFactory.FromRequest(w, r)

    var params ListParams
    if err := binding.Query(r, ¶ms); err != nil {
        res.WriteError(http.StatusBadRequest, responder.Error{Message: err.Error()})
        return
    }

    total, data, err := c.service.List(r.Context(), ¶ms)
    if err != nil {
        res.WriteError(http.StatusInternalServerError, responder.Error{Message: err.Error()})
        return
    }

    // 计算分页元数据
    totalPages := int(math.Ceil(float64(total) / float64(params.Pagination.PageSize)))
    hasMore := totalPages > params.Pagination.Page

    // 返回 Strapi 风格的分页响应
    res.WriteList(http.StatusOK, data, &responder.PaginationMeta{
        Page:       params.Pagination.Page,
        PageSize:   params.Pagination.PageSize,
        Total:      total,
        TotalPages: totalPages,
        HasMore:    hasMore,
    })
}
```

### 2.5 DTO 文件规范

**职责**：数据传输对象定义

```go
package user

// CreateDTO - 创建用户的请求数据
type CreateDTO struct {
    Email    string `json:"email" validate:"required,email"`
    Password string `json:"password" validate:"required,min=6"`
    Name     string `json:"name" validate:"required"`
    Role     string `json:"role" validate:"required,oneof=admin editor viewer"`
    TenantID int64  // 从 Context 注入
}

// UpdateDTO - 更新用户的请求数据
type UpdateDTO struct {
    Name  *string `json:"name,omitempty"`
    Role  *string `json:"role,omitempty" validate:"omitempty,oneof=admin editor viewer"`
}

// ListParams - 列表查询参数
type ListParams struct {
    Keyword    string     `query:"keyword"`
    Role       string     `query:"role"`
    Pagination Pagination `query:"pagination"`
}

// Pagination - 通用分页参数
type Pagination struct {
    Page     int `query:"page" default:"1" validate:"min=1"`
    PageSize int `query:"page_size" default:"10" validate:"min=1,max=100"`
}
```

---

## 3. 命名规范

### 3.1 包命名

```go
// ✅ 正确：小写单数
package user
package article

// ❌ 错误：复数或大写
package users
package Article
```

### 3.2 文件命名

```go
// ✅ 正确：小写 + 下划线
module.go
controller.go
service.go
dto.go
user_service_test.go

// ❌ 错误：驼峰或中划线
userService.go
user-service.go
```

### 3.3 类型命名

| 类型 | 规则 | 示例 |
|------|------|------|
| **结构体** | 大写驼峰 | `UserService`, `ArticleController` |
| **接口** | 大写驼峰 + `er` 后缀 | `Reader`, `Writer` |
| **DTO** | 大写驼峰 + `DTO` 后缀 | `CreateUserDTO`, `ListParamsDTO` |
| **常量** | 大写驼峰或全大写 | `MaxRetries`, `DEFAULT_TIMEOUT` |
| **变量** | 小写驼峰 | `userName`, `totalCount` |

### 3.4 方法命名

```go
// ✅ CRUD 操作标准命名
func (s *Service) Create(ctx context.Context, dto *CreateDTO) (*Entity, error)
func (s *Service) Get(ctx context.Context, id uuid.UUID) (*Entity, error)
func (s *Service) List(ctx context.Context, params *ListParams) (int64, []*Entity, error)
func (s *Service) Update(ctx context.Context, id uuid.UUID, dto *UpdateDTO) (*Entity, error)
func (s *Service) Delete(ctx context.Context, id uuid.UUID) error
```

### 3.5 路由命名

```go
// ✅ 正确：小写复数 + RESTful 风格
r.Route("/users", func(r chi.Router) {
    r.Get("/", handler.List)           // GET /users
    r.Get("/{id}", handler.Get)        // GET /users/:id
    r.Post("/", handler.Create)        // POST /users
    r.Put("/{id}", handler.Update)     // PUT /users/:id
    r.Delete("/{id}", handler.Delete)  // DELETE /users/:id
})

// ❌ 错误：不符合 RESTful
r.Get("/getUsers", handler.List)
r.Post("/createUser", handler.Create)
```

---

## 4. 类型与接口规范

### 4.1 类型声明

**✅ 强制规则：使用 `any` 代替 `interface{}`**

```go
// ✅ 正确
func Process(data any) error {
    return nil
}

type Config struct {
    Extra map[string]any `json:"extra"`
}

// ❌ 错误
func Process(data interface{}) error {
    return nil
}

type Config struct {
    Extra map[string]interface{} `json:"extra"`
}
```

### 4.2 接口定义

```go
// ✅ 接口应该小而专注
type Reader interface {
    Read(ctx context.Context, id uuid.UUID) (any, error)
}

type Writer interface {
    Write(ctx context.Context, data any) error
}

// ❌ 避免大接口
type DataAccess interface {
    Create(...)
    Read(...)
    Update(...)
    Delete(...)
    List(...)
    // ... 太多方法
}
```

### 4.3 结构体标签

```go
type User struct {
    // JSON 标签
    Email    string `json:"email"`
    Password string `json:"-"`              // 不序列化

    // 验证标签
    Age      int    `json:"age" validate:"min=0,max=120"`

    // Query 标签
    Keyword  string `query:"keyword"`

    // 组合标签
    Name     string `json:"name" validate:"required" query:"name"`
}
```

---

## 5. 依赖注入规范

### 5.1 手动依赖注入

**✅ 清晰透明的依赖关系**

```go
// main.go - 依赖注入容器
func main() {
    // 1. 基础设施层
    dbClient := initDatabase()
    enforcer := initCasbin()

    // 2. 服务层
    userModule := user.NewModule(dbClient, enforcer)
    articleModule := article.NewModule(dbClient, enforcer)
    apiKeyModule := apikey.NewModule(dbClient, enforcer)

    // 3. 路由注册
    r := chi.NewRouter()

    // 全局中间件
    r.Use(middleware.Logger)
    r.Use(middleware.Recoverer)
    r.Use(middleware.RequestID)
    r.Use(middleware.CORS)

    // API 路由（需要 API Key 认证）
    r.Route("/api/v1", func(r chi.Router) {
        // 所有接口都需要 API Key 认证
        r.Use(middleware.APIKeyAuth(dbClient, enforcer))

        userModule.Setup(r)
        articleModule.Setup(r)
    })

    // 管理后台路由（使用 JWT 认证）
    r.Route("/admin", func(r chi.Router) {
        r.Use(middleware.Auth) // JWT 认证

        apiKeyModule.Setup(r) // API Key 管理
    })

    // 4. 启动服务
    http.ListenAndServe(":3000", r)
}
```

### 5.2 构造函数模式

```go
// ✅ 构造函数必须返回完整的对象
func NewService(client *_gen.Client) *Service {
    return &Service{
        client: client,
    }
}

// ✅ 如果依赖较多，使用配置对象
type ServiceConfig struct {
    Client *_gen.Client
    Cache  *redis.Client
    Logger *log.Logger
}

func NewServiceWithConfig(cfg ServiceConfig) *Service {
    return &Service{
        client: cfg.Client,
        cache:  cfg.Cache,
        logger: cfg.Logger,
    }
}
```

### 5.3 依赖顺序

```
Database Client (Ent)
    ↓
Casbin Enforcer (权限)
    ↓
Repository/Service (业务逻辑)
    ↓
Controller (HTTP 处理)
    ↓
Module (路由注册)
    ↓
HTTP Server (Chi)
```

---

## 6. 数据层规范 (Ent ORM)

### 6.1 Ent Schema 定义

```go
// schema/user.go
package schema

import (
    "entgo.io/ent"
    "entgo.io/ent/schema/field"
    "entgo.io/ent/schema/mixin"
    "entgo.io/ent/schema/edge"
)

type User struct {
    ent.Schema
}

// 混入基类（包含通用字段）
func (User) Mixin() []ent.Mixin {
    return []ent.Mixin{
        mixin.Time{},  // 自动创建 updated_at, created_at
    }
}

func (User) Fields() []ent.Field {
    return []ent.Field{
        field.String("email").
            Unique().
            NotEmpty(),
        field.String("password").
            Sensitive(),  // 不在序列化中显示
        field.String("name").
            NotEmpty(),
        field.String("role").
            NotEmpty(),
        field.Bool("active").
            Default(true),
        field.Int64("tenant_id").
            Optional(),  // 多租户字段
    }
}

func (User) Edges() []ent.Edge {
    return []ent.Edge{
        // 一对多：一个用户可以有多篇文章
        edge.To("articles", Article.Type).
            StorageKey(edge.Column("author_id")),
        // 一对多：一个用户可以有多个 API Key
        edge.To("api_keys", APIKey.Type).
            StorageKey(edge.Column("user_id")),
    }
}
```

### 6.2 Ent 查询操作

```go
// ✅ 查询操作
func (s *Service) Get(ctx context.Context, id uuid.UUID) (*_gen.User, error) {
    return s.client.User.
        Query().
        Where(user.IDEQ(id)).
        First(ctx)
}

// ✅ 创建操作
func (s *Service) Create(ctx context.Context, dto *CreateDTO) (*_gen.User, error) {
    // 密码加密
    hashedPassword, err := bcrypt.GenerateFromPassword([]byte(dto.Password), bcrypt.DefaultCost)
    if err != nil {
        return nil, err
    }

    return s.client.User.
        Create().
        SetEmail(dto.Email).
        SetPassword(string(hashedPassword)).
        SetName(dto.Name).
        SetRole(dto.Role).
        Save(ctx)
}

// ✅ 更新操作
func (s *Service) Update(ctx context.Context, id uuid.UUID, dto *UpdateDTO) (*_gen.User, error) {
    update := s.client.User.UpdateOneID(id)

    if dto.Name != nil {
        update = update.SetName(*dto.Name)
    }
    if dto.Role != nil {
        update = update.SetRole(*dto.Role)
    }

    return update.Save(ctx)
}

// ✅ 删除操作
func (s *Service) Delete(ctx context.Context, id uuid.UUID) error {
    return s.client.User.DeleteOneID(id).Exec(ctx)
}
```

### 6.3 关联查询

```go
// ✅ 预加载关联（避免 N+1 问题）
func (s *Service) GetWithArticles(ctx context.Context, id uuid.UUID) (*_gen.User, error) {
    return s.client.User.
        Query().
        Where(user.IDEQ(id)).
        WithArticles().  // 预加载文章
        First(ctx)
}

// ✅ 条件关联查询
func (s *Service) ListWithPublishedArticles(ctx context.Context) ([]*_gen.User, error) {
    return s.client.User.
        Query().
        WithArticles(func(q *_gen.ArticleQuery) {
            q.Where(article.StatusEQ("published"))
        }).
        All(ctx)
}
```

### 6.4 批量操作

```go
// ✅ 批量创建
func (s *Service) BatchCreate(ctx context.Context, dtos []*CreateDTO) ([]*_gen.User, error) {
    bulk := make([]*_gen.UserCreate, len(dtos))

    for i, dto := range dtos {
        hashedPassword, _ := bcrypt.GenerateFromPassword([]byte(dto.Password), bcrypt.DefaultCost)
        bulk[i] = s.client.User.Create().
            SetEmail(dto.Email).
            SetPassword(string(hashedPassword)).
            SetName(dto.Name).
            SetRole(dto.Role)
    }

    return s.client.User.CreateBulk(bulk...).Save(ctx)
}
```

### 6.5 事务处理

```go
// ✅ 使用事务确保数据一致性
func (s *Service) CreateWithProfile(ctx context.Context, dto *CreateDTO) (*_gen.User, error) {
    tx, err := s.client.Tx(ctx)
    if err != nil {
        return nil, err
    }

    // 创建用户
    user, err := tx.User.Create().
        SetEmail(dto.Email).
        SetPassword(dto.Password).
        Save(ctx)
    if err != nil {
        tx.Rollback()
        return nil, err
    }

    // 创建用户配置
    _, err = tx.Profile.Create().
        SetUser(user).
        SetBio(dto.Bio).
        Save(ctx)
    if err != nil {
        tx.Rollback()
        return nil, err
    }

    // 提交事务
    if err := tx.Commit(); err != nil {
        return nil, err
    }

    return user, nil
}
```

---

## 7. HTTP 层规范 (Chi 框架)

### 7.1 参数绑定

```go
// ✅ JSON Body 绑定
func (c *Controller) Create(w http.ResponseWriter, r *http.Request) {
    var dto CreateDTO
    if err := binding.JSON(r, &dto); err != nil {
        res.WriteError(http.StatusBadRequest, responder.Error{Message: err.Error()})
        return
    }
    // ...
}

// ✅ Query 参数绑定
func (c *Controller) List(w http.ResponseWriter, r *http.Request) {
    var params ListParams
    if err := binding.Query(r, ¶ms); err != nil {
        res.WriteError(http.StatusBadRequest, responder.Error{Message: err.Error()})
        return
    }
    // ...
}

// ✅ 路径参数解析
func (c *Controller) Get(w http.ResponseWriter, r *http.Request) {
    idStr := chi.URLParam(r, "id")
    id, err := uuid.Parse(idStr)
    if err != nil {
        res.WriteError(http.StatusBadRequest, responder.Error{Message: "Invalid ID"})
        return
    }
    // ...
}
```

### 7.2 中间件使用

```go
// ✅ 全局中间件
r.Use(middleware.Logger)
r.Use(middleware.Recoverer)
r.Use(middleware.RequestID)
r.Use(middleware.CORS)

// ✅ API 路由（需要 API Key 认证）
r.Route("/api/v1", func(r chi.Router) {
    r.Use(middleware.APIKeyAuth(dbClient, enforcer))

    r.Route("/users", func(r chi.Router) {
        r.Get("/", userHandler.List)
        r.Post("/", userHandler.Create)
    })
})

// ✅ 管理后台（需要 JWT 认证）
r.Route("/admin", func(r chi.Router) {
    r.Use(middleware.Auth)

    r.Route("/api-keys", func(r chi.Router) {
        r.Get("/", apiKeyHandler.ListByUser)
        r.Post("/", apiKeyHandler.Create)
    })
})
```

---

## 8. 响应格式规范

**✅ 必须遵循 @cms/CMS_RESPONSE.md 定义的规范**

所有 API 响应必须使用 Strapi 风格的统一结构：

```typescript
// 前端 TypeScript 类型定义
interface Response<T> {
  data: T | T[] | null;  // 响应数据
  meta?: Meta;           // 元数据（可选）
}

interface Meta {
  pagination?: Pagination; // 分页信息
  traceId?: string;        // 请求追踪 ID（开发环境）
  took?: number;           // 处理耗时（开发环境）
}

interface Pagination {
  page: number;          // 当前页码
  pageSize: number;      // 每页条数
  total: number;         // 总条数
  totalPages: number;    // 总页数
  hasMore: boolean;      // 是否还有更多
}

// 错误响应
interface ErrorResponse {
  error: {
    message: string;
    details?: any;
  };
  data: null;
}
```

### 8.1 后端实现

```go
// ✅ Go 响应结构
type StrapiResponse struct {
    Data any            `json:"data"`
    Meta StrapiMeta     `json:"meta,omitempty"`
}

type StrapiMeta struct {
    Pagination *PaginationMeta `json:"pagination,omitempty"`
    TraceId    string          `json:"traceId,omitempty"`    // 开发环境
    Took       int64           `json:"took,omitempty"`       // 开发环境
}

type PaginationMeta struct {
    Page       int   `json:"page"`
    PageSize   int   `json:"pageSize"`
    Total      int64 `json:"total"`
    TotalPages int   `json:"totalPages"`
    HasMore    bool  `json:"hasMore"`
}

type Error struct {
    Message string         `json:"message"`
    Details map[string]any `json:"details,omitempty"`
}
```

### 8.2 响应示例

详见 [CMS_RESPONSE.md](./CMS_RESPONSE.md) 完整文档，包括：
- 单条数据查询
- 列表查询（带分页）
- 创建/更新操作
- 错误响应
- 前端封装示例
- React Hook 示例
- 分页组件示例

---

## 9. Schema 驱动开发规范

**✅ 必须遵循 @cms/SCHEMA_DRIVEN_DEVELOPMENT.md 定义的规范**

所有业务模块必须使用 Schema 驱动开发模式，确保前后端数据结构统一。

### 9.1 核心原则

**Schema 是唯一数据源（Single Source of Truth）**

```
开发流程：
1. 定义 schema.json（唯一数据源）
2. 后端基于 Schema 开发 DTO、Service、Controller
3. 前端通过 Schema API 获取定义
4. 前端基于 Schema 生成表格、表单、验证规则
```

### 9.2 模块必须包含 Schema

每个业务模块**必须**在模块目录下包含 `schema.json` 文件：

```
cms/api/v1/
├── user/
│   ├── schema.json       # ✅ 必须存在 - 唯一数据源
│   ├── module.go
│   ├── controller.go
│   ├── service.go
│   └── dto.go
```

### 9.3 Schema 文件格式

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "name": "User",
  "collectionName": "users",
  "description": "用户实体",
  "info": {
    "displayName": "用户管理",
    "description": "系统用户",
    "icon": "User"
  },
  "properties": {
    "email": {
      "type": "string",
      "description": "邮箱地址",
      "validate": {
        "required": true,
        "format": "email",
        "maxLength": 100
      }
    },
    "role": {
      "type": "enum",
      "description": "用户角色",
      "enum": ["admin", "editor", "viewer"],
      "validate": {
        "required": true
      }
    }
  },
  "indexes": [
    {
      "type": "unique",
      "columns": ["email"]
    }
  ]
}
```

### 9.4 开发顺序

**必须遵循：Schema → 后端 → 前端**

1. **先定义 schema.json**（数据驱动 - 唯一数据源）
2. **后端实现**（基于 Schema 定义字段和验证）
3. **前端开发**（通过 Schema API 获取定义）

### 9.5 Schema API 接口

CMS 提供以下 Schema API：

```bash
# 获取所有模块 Schema 列表
GET /api/schemas

# 获取单个模块 Schema
GET /api/schemas/:moduleName

# 批量获取 Schema
POST /api/schemas/batch
{
  "modules": ["user", "article"]
}

# 验证数据
POST /api/schemas/:moduleName/validate
{
  "data": { "email": "test@example.com", "role": "admin" }
}
```

### 9.6 前端集成

前端必须通过 Schema API 获取定义，**禁止硬编码**：

```typescript
// ✅ 正确：通过 Schema API 获取
const schema = await getSchema('user');
const columns = Object.entries(schema.properties).map(([key, prop]) => ({
  key,
  title: prop.description,
  dataIndex: key
}));

// ❌ 错误：硬编码字段
const columns = [
  { key: 'email', title: '邮箱' },  // 不要这样做
  { key: 'name', title: '姓名' }
];
```

### 9.7 完整文档

详见 [SCHEMA_DRIVEN_DEVELOPMENT.md](./SCHEMA_DRIVEN_DEVELOPMENT.md)，包括：
- Schema 文件规范
- 验证规则映射
- 后端开发流程
- 前端集成方案
- 动态表单/表格开发
- 工作流程

---

## 10. 权限规范 (Casbin)

### 10.1 Casbin Model 配置

```ini
# core/rbac/model.conf
[request_definition]
r = sub, obj, act

[policy_definition]
p = sub, obj, act

[role_definition]
g = _, _

[policy_effect]
e = some(where (p.eft == allow))

[matchers]
m = g(r.sub, p.sub) && r.obj == p.obj && r.act == p.act
```

### 10.2 Casbin Policy 示例

```csv
# core/rbac/policy.csv
# 格式：角色, 资源, 操作

# 管理员权限
p, admin, user, create
p, admin, user, read
p, admin, user, update
p, admin, user, delete
p, admin, article, create
p, admin, article, read
p, admin, article, update
p, admin, article, delete
p, admin, api-key, create
p, admin, api-key, read
p, admin, api-key, update
p, admin, api-key, delete

# 编辑权限
p, editor, article, create
p, editor, article, read
p, editor, article, update
p, editor, api-key, create
p, editor, api-key, read

# 查看权限
p, viewer, article, read
p, viewer, api-key, read

# 角色继承
g, admin, editor
g, editor, viewer
```

### 10.3 Casbin 中间件

```go
// core/http/middleware/casbin.go
package middleware

import (
    "net/http"
    "github.com/casbin/casbin/v2"
    "github.com/go-chi/chi/v5"
    "github.com/JsonLee12138/headless-cms/core/http/responder"
)

// Casbin - 权限验证中间件
func Casbin(enforcer *casbin.Enforcer, resource string) func(http.Handler) http.Handler {
    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            // 从 context 获取用户角色
            role, ok := r.Context().Value("user_role").(string)
            if !ok {
                role = "anonymous"
            }

            // 获取请求方法对应的操作
            method := r.Method
            var action string
            switch method {
            case "GET":
                action = "read"
            case "POST":
                action = "create"
            case "PUT", "PATCH":
                action = "update"
            case "DELETE":
                action = "delete"
            default:
                action = "read"
            }

            // 验证权限
            ok, err := enforcer.Enforce(role, resource, action)
            if err != nil {
                res := responder.NewResponderFactory(responder.DefaultPanicFn).FromRequest(w, r)
                res.WriteError(http.StatusInternalServerError, responder.Error{Message: "权限验证错误"})
                return
            }

            if !ok {
                res := responder.NewResponderFactory(responder.DefaultPanicFn).FromRequest(w, r)
                res.WriteError(http.StatusForbidden, responder.Error{Message: "无权限访问"})
                return
            }

            next.ServeHTTP(w, r)
        })
    }
}
```

---

## 11. API Key 认证规范

**✅ 所有 CMS 数据接口必须使用 API Key 认证，禁止公开访问**

### 11.1 API Key Schema 定义

```go
// schema/api_key.go
package schema

import (
    "entgo.io/ent"
    "entgo.io/ent/schema/field"
    "entgo.io/ent/schema/index"
    "entgo.io/ent/schema/edge"
)

type APIKey struct {
    ent.Schema
}

func (APIKey) Fields() []ent.Field {
    return []ent.Field{
        field.String("name").NotEmpty(),                    // API Key 名称
        field.String("key").Unique().NotEmpty(),            // API Key 字符串
        field.String("description").Optional(),             // 描述
        field.JSON("restrictions", map[string]any{}).Optional(), // 限制：{"ip_whitelist": [], "rate_limit": 100}
        field.Time("last_used").Optional(),                 // 最后使用时间
        field.Time("expires_at").Optional(),                // 过期时间
        field.Bool("active").Default(true),                 // 是否激活
        field.Time("created_at").AutoCreateTime(),
    }
}

func (APIKey) Edges() []ent.Edge {
    return []ent.Edge{
        // API Key 属于某个用户
        edge.From("user", User.Type).
            Ref("api_keys").
            Unique().
            Required(),
    }
}

func (APIKey) Indexes() []ent.Index {
    return []ent.Index{
        index.Fields("key"),
        index.Fields("active"),
    }
}
```

### 11.2 API Key 认证流程

**核心设计：API Key 继承用户的权限**

```
1. 从 Authorization Header 获取 API Key
2. 查询 API Key 并预加载关联的 User
3. 检查 API Key 是否过期/激活
4. 检查用户账号是否激活
5. 使用 Casbin 基于用户角色验证权限
6. 检查 IP 白名单（可选）
7. 注入用户信息到 Context
```

### 11.3 API Key 中间件

```go
// core/http/middleware/apikey.go
package middleware

import (
    "context"
    "net/http"
    "strings"
    "time"
    "github.com/JsonLee12138/headless-cms/cms/_gen"
    "github.com/JsonLee12138/headless-cms/cms/_gen/apikey"
    "github.com/JsonLee12138/headless-cms/core/http/responder"
    "github.com/casbin/casbin/v2"
)

// APIKeyAuth - API Key 认证中间件
func APIKeyAuth(client *_gen.Client, enforcer *casbin.Enforcer) func(http.Handler) http.Handler {
    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            res := responder.NewResponderFactory(responder.DefaultPanicFn).FromRequest(w, r)

            // 从 Header 获取 API Key
            apiKey := r.Header.Get("Authorization")
            if apiKey == "" {
                res.WriteError(http.StatusUnauthorized, responder.Error{
                    Message: "Missing API key",
                    Details: map[string]any{"hint": "Use Authorization header with your API key"},
                })
                return
            }

            // 支持 "Bearer xxx" 或直接 "xxx"
            if strings.HasPrefix(apiKey, "Bearer ") {
                apiKey = strings.TrimPrefix(apiKey, "Bearer ")
            }

            // 查询 API Key（包含用户信息）
            keyRecord, err := client.APIKey.Query().
                Where(
                    apikey.KeyEQ(apiKey),
                    apikey.Active(true),
                ).
                WithUser().
                First(r.Context())

            if err != nil {
                res.WriteError(http.StatusUnauthorized, responder.Error{
                    Message: "Invalid or inactive API key",
                })
                return
            }

            // 检查过期时间
            if keyRecord.ExpiresAt != nil && keyRecord.ExpiresAt.Before(time.Now()) {
                res.WriteError(http.StatusUnauthorized, responder.Error{
                    Message: "API key has expired",
                })
                return
            }

            // 获取用户信息
            user := keyRecord.Edges.User
            if user == nil {
                res.WriteError(http.StatusUnauthorized, responder.Error{
                    Message: "API key user not found",
                })
                return
            }

            // 检查用户是否激活
            if !user.Active {
                res.WriteError(http.StatusUnauthorized, responder.Error{
                    Message: "User account is not active",
                })
                return
            }

            // 使用 Casbin 检查权限（基于用户角色）
            resource := strings.TrimPrefix(r.URL.Path, "/")
            if idx := strings.Index(resource, "/"); idx > 0 {
                resource = resource[:idx] // 提取资源名，如 "users"、"articles"
            }
            action := getRequiredPermission(r.Method)

            ok, err := enforcer.Enforce(user.Role, resource, action)
            if err != nil {
                res.WriteError(http.StatusInternalServerError, responder.Error{
                    Message: "Permission check error",
                })
                return
            }

            if !ok {
                res.WriteError(http.StatusForbidden, responder.Error{
                    Message: "User does not have permission for this operation",
                    Details: map[string]any{
                        "user_role": user.Role,
                        "resource":  resource,
                        "action":    action,
                    },
                })
                return
            }

            // 检查 IP 白名单（如果有配置）
            if restrictions, ok := keyRecord.Restrictions.(map[string]any); ok {
                if ipWhitelist, exists := restrictions["ip_whitelist"]; exists {
                    if !isIPAllowed(r.RemoteAddr, ipWhitelist) {
                        res.WriteError(http.StatusForbidden, responder.Error{
                            Message: "IP address not allowed",
                        })
                        return
                    }
                }
            }

            // 更新最后使用时间（异步）
            go func() {
                client.APIKey.UpdateOne(keyRecord).
                    SetLastUsed(time.Now()).
                    Exec(context.Background())
            }()

            // 注入用户信息到 Context
            ctx := context.WithValue(r.Context(), "user_id", user.ID)
            ctx = context.WithValue(ctx, "user_role", user.Role)
            ctx = context.WithValue(ctx, "tenant_id", user.TenantID)
            ctx = context.WithValue(ctx, "api_key_id", keyRecord.ID)

            next.ServeHTTP(w, r.WithContext(ctx))
        })
    }
}

// 辅助函数
func getRequiredPermission(method string) string {
    switch method {
    case "GET":
        return "read"
    case "POST":
        return "create"
    case "PUT", "PATCH":
        return "update"
    case "DELETE":
        return "delete"
    default:
        return "read"
    }
}

func isIPAllowed(remoteAddr string, whitelist any) bool {
    // 实现 IP 白名单检查逻辑
    // remoteAddr 格式：IP:PORT
    ip := strings.Split(remoteAddr, ":")[0]
    // ... 检查逻辑
    return true // 简化示例
}
```

### 11.4 API Key 管理模块

```go
// api/v1/apikey/module.go
package apikey

import (
    "crypto/rand"
    "encoding/base64"
    "github.com/JsonLee12138/headless-cms/cms/_gen"
    "github.com/JsonLee12138/headless-cms/core/http/middleware"
    "github.com/JsonLee12138/headless-cms/core/http/responder"
    "github.com/casbin/casbin/v2"
    "github.com/go-chi/chi/v5"
)

type Module struct {
    controller *Controller
    service    *Service
}

func NewModule(client *_gen.Client, enforcer *casbin.Enforcer) *Module {
    service := NewService(client)
    responderFactory := responder.NewResponderFactory(responder.DefaultPanicFn)
    controller := NewController(service, responderFactory, enforcer)

    return &Module{
        controller: controller,
        service:    service,
    }
}

func (m *Module) Setup(r chi.Router) {
    r.Route("/api-keys", func(r chi.Router) {
        // 需要认证（JWT）
        r.Use(middleware.Auth)

        // 用户只能管理自己的 API Key
        r.Get("/", m.controller.ListByUser)
        r.Post("/", m.controller.Create)
        r.Get("/{id}", m.controller.Get)
        r.Put("/{id}", m.controller.Update)
        r.Delete("/{id}", m.controller.Delete)

        // 管理员可以管理所有 API Key
        r.Route("/admin", func(r chi.Router) {
            r.Use(middleware.RequireRole("admin"))
            r.Get("/all", m.controller.ListAll)
        })
    })
}

// 生成安全的 API Key
func generateAPIKey() (string, error) {
    bytes := make([]byte, 32)
    if _, err := rand.Read(bytes); err != nil {
        return "", err
    }
    return base64.URLEncoding.EncodeToString(bytes), nil
}
```

### 11.5 API Key 创建服务

```go
// api/v1/apikey/service.go
package apikey

import (
    "context"
    "errors"
    "github.com/JsonLee12138/headless-cms/cms/_gen"
    "github.com/JsonLee12138/headless-cms/cms/_gen/apikey"
    "github.com/google/uuid"
)

type Service struct {
    client *_gen.Client
}

func NewService(client *_gen.Client) *Service {
    return &Service{client: client}
}

// Create - 用户创建自己的 API Key
func (s *Service) Create(ctx context.Context, dto *CreateDTO) (*_gen.APIKey, error) {
    // 从 context 获取用户 ID
    userID, ok := ctx.Value("user_id").(uuid.UUID)
    if !ok {
        return nil, errors.New("user not authenticated")
    }

    // 生成 API Key
    key, err := generateAPIKey()
    if err != nil {
        return nil, err
    }

    // 创建 API Key
    return s.client.APIKey.Create().
        SetName(dto.Name).
        SetKey(key).
        SetDescription(dto.Description).
        SetRestrictions(dto.Restrictions).
        SetExpiresAt(dto.ExpiresAt).
        SetUserID(userID).
        Save(ctx)
}

// ListByUser - 获取当前用户的 API Keys
func (s *Service) ListByUser(ctx context.Context) ([]*_gen.APIKey, error) {
    userID, ok := ctx.Value("user_id").(uuid.UUID)
    if !ok {
        return nil, errors.New("user not authenticated")
    }

    return s.client.APIKey.Query().
        Where(apikey.UserID(userID)).
        WithUser().
        All(ctx)
}

// Get - 获取单个 API Key（需验证归属）
func (s *Service) Get(ctx context.Context, id uuid.UUID) (*_gen.APIKey, error) {
    userID, ok := ctx.Value("user_id").(uuid.UUID)
    if !ok {
        return nil, errors.New("user not authenticated")
    }

    return s.client.APIKey.Query().
        Where(
            apikey.IDEQ(id),
            apikey.UserID(userID),
        ).
        WithUser().
        First(ctx)
}
```

### 11.6 API Key 使用示例

#### 创建 API Key

```bash
# 用户登录后创建 API Key（需要 JWT 认证）
curl -X POST "http://localhost:3000/admin/api-keys" \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Mobile App Key",
    "description": "用于移动应用访问",
    "restrictions": {
      "ip_whitelist": ["192.168.1.0/24"],
      "rate_limit": 1000
    },
    "expires_at": "2025-01-12T00:00:00Z"
  }'

# 响应
{
  "data": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "name": "Mobile App Key",
    "key": "abc123xyz...",
    "description": "用于移动应用访问",
    "restrictions": {
      "ip_whitelist": ["192.168.1.0/24"],
      "rate_limit": 1000
    },
    "expires_at": "2025-01-12T00:00:00Z",
    "active": true,
    "created_at": "2024-01-12T00:00:00Z"
  }
}
```

#### 使用 API Key 访问数据

```bash
# ✅ 正确：使用 API Key 访问数据
curl -X GET "http://localhost:3000/api/v1/users?page=1&page_size=10" \
  -H "Authorization: abc123xyz..." \
  -H "Content-Type: application/json"

# ✅ 正确：使用 Bearer 格式
curl -X POST "http://localhost:3000/api/v1/articles" \
  -H "Authorization: Bearer abc123xyz..." \
  -d '{"title": "My Article", "content": "Hello World"}'
```

#### 错误响应示例

```bash
# ❌ 错误：缺少 API Key
curl -X GET "http://localhost:3000/api/v1/users"
# Response: 401 Unauthorized
{
  "error": {
    "message": "Missing API key",
    "details": {"hint": "Use Authorization header with your API key"}
  },
  "data": null
}

# ❌ 错误：无效的 API Key
curl -X GET "http://localhost:3000/api/v1/users" \
  -H "Authorization: Bearer invalid_key"
# Response: 401 Unauthorized
{
  "error": {"message": "Invalid or inactive API key"},
  "data": null
}

# ❌ 错误：用户角色权限不足
curl -X DELETE "http://localhost:3000/api/v1/users/123" \
  -H "Authorization: Bearer viewer_key"
# Response: 403 Forbidden
{
  "error": {
    "message": "User does not have permission for this operation",
    "details": {
      "user_role": "viewer",
      "resource": "users",
      "action": "delete"
    }
  },
  "data": null
}

# ❌ 错误：API Key 过期
curl -X GET "http://localhost:3000/api/v1/users" \
  -H "Authorization: Bearer expired_key"
# Response: 401 Unauthorized
{
  "error": {"message": "API key has expired"},
  "data": null
}
```

### 11.7 数据库记录示例

```json
// API Key 记录
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "Mobile App API Key",
  "key": "abc123xyz...",
  "description": "用于移动应用的数据访问",
  "restrictions": {
    "ip_whitelist": ["192.168.1.0/24"],
    "rate_limit": 1000
  },
  "last_used": "2024-01-12T10:30:00Z",
  "expires_at": "2025-01-12T00:00:00Z",
  "active": true,
  "user_id": "456e7890-e89b-12d3-a456-426614174000",
  "created_at": "2024-01-12T00:00:00Z",
  "edges": {
    "user": {
      "id": "456e7890-e89b-12d3-a456-426614174000",
      "email": "admin@example.com",
      "role": "admin",
      "tenant_id": 1,
      "active": true
    }
  }
}
```

### 11.8 权限继承说明

**核心设计原则：**

1. **API Key 本身没有权限字段**
2. **权限完全基于用户的角色**（通过 Casbin）
3. **用户创建 API Key 后，该 Key 自动继承用户的所有权限**
4. **用户角色变更时，其所有 API Key 的权限自动更新**

**示例：**
- 用户 A 的角色是 `admin` → 创建的 API Key 拥有 admin 的所有权限
- 用户 B 的角色是 `viewer` → 创建的 API Key 只有 read 权限
- 将用户 A 的角色改为 `viewer` → 其所有 API Key 权限自动降级

---

## 12. 错误处理规范

### 12.1 错误定义

```go
// ✅ 在 Service 层定义业务错误
package user

import "errors"

var (
    ErrNotFound      = errors.New("user not found")
    ErrEmailConflict = errors.New("email already exists")
    ErrInvalidToken  = errors.New("invalid token")
    ErrExpiredToken  = errors.New("expired token")
    ErrUnauthorized  = errors.New("unauthorized")
)
```

### 12.2 错误包装

```go
// ✅ Service 层：包装 Ent 错误
func (s *Service) Get(ctx context.Context, id uuid.UUID) (*_gen.User, error) {
    user, err := s.client.User.Get(ctx, id)
    if err != nil {
        if ent.IsNotFound(err) {
            return nil, ErrNotFound
        }
        return nil, fmt.Errorf("failed to get user: %w", err)
    }
    return user, nil
}
```

### 12.3 错误处理

```go
// ✅ Controller 层：根据错误类型返回不同状态码
func (c *Controller) Get(w http.ResponseWriter, r *http.Request) {
    res := c.responderFactory.FromRequest(w, r)

    idStr := chi.URLParam(r, "id")
    id, err := uuid.Parse(idStr)
    if err != nil {
        res.WriteError(http.StatusBadRequest, responder.Error{Message: "Invalid ID"})
        return
    }

    data, err := c.service.Get(r.Context(), id)
    if err != nil {
        switch {
        case errors.Is(err, service.ErrNotFound):
            res.WriteError(http.StatusNotFound, responder.Error{Message: err.Error()})
        case errors.Is(err, service.ErrUnauthorized):
            res.WriteError(http.StatusUnauthorized, responder.Error{Message: err.Error()})
        default:
            res.WriteError(http.StatusInternalServerError, responder.Error{Message: err.Error()})
        }
        return
    }

    res.Write(http.StatusOK, responder.StrapiResponse{Data: data})
}
```

---

## 13. 上下文规范

### 13.1 Context 传递

```go
// ✅ Context 必须作为第一个参数
func (s *Service) Create(ctx context.Context, dto *CreateDTO) (*_gen.User, error) {
    // ...
}

// ❌ 错误：Context 不是第一个参数
func (s *Service) Create(dto *CreateDTO, ctx context.Context) (*_gen.User, error) {
    // ...
}
```

### 13.2 Context 值获取

```go
// ✅ 从 Context 获取租户 ID
func (s *Service) Create(ctx context.Context, dto *CreateDTO) (*_gen.Article, error) {
    tenantID, ok := ctx.Value("tenant_id").(int64)
    if !ok {
        return nil, errors.New("tenant required")
    }

    return s.client.Article.Create().
        SetTitle(dto.Title).
        SetTenantID(tenantID).
        Save(ctx)
}

// ✅ 从 Context 获取用户 ID 和角色
func (s *Service) Create(ctx context.Context, dto *CreateDTO) (*_gen.Article, error) {
    userID, ok := ctx.Value("user_id").(uuid.UUID)
    if !ok {
        return nil, errors.New("user required")
    }

    tenantID, _ := ctx.Value("tenant_id").(int64)

    return s.client.Article.Create().
        SetTitle(dto.Title).
        SetAuthorID(userID).
        SetTenantID(tenantID).
        Save(ctx)
}
```

### 13.3 Context 注入（中间件）

API Key 中间件会自动注入以下信息：
- `user_id`: 用户 ID
- `user_role`: 用户角色
- `tenant_id`: 租户 ID
- `api_key_id`: API Key ID

---

## 14. 多租户规范

### 14.1 租户字段

```go
// ✅ 所有需要隔离的表都必须包含 tenant_id
// schema/article.go
func (Article) Fields() []ent.Field {
    return []ent.Field{
        field.String("title").NotEmpty(),
        field.Text("content"),
        field.Int64("tenant_id").Optional(),  // 租户 ID，用于数据隔离
        field.UUID("author_id", uuid.UUID{}).Optional(),
    }
}
```

### 14.2 租户过滤

```go
// ✅ 查询时自动过滤租户
func (s *Service) List(ctx context.Context, params *ListParams) (int64, []*_gen.Article, error) {
    tenantID, _ := ctx.Value("tenant_id").(int64)

    query := s.client.Article.Query().
        Where(article.TenantIDEQ(tenantID))  // 必须添加租户过滤

    // 应用其他过滤条件
    if params.Keyword != "" {
        query = query.Where(article.TitleContains(params.Keyword))
    }

    // 获取总数
    count, _ := query.Count(ctx)

    // 分页查询
    offset := (params.Pagination.Page - 1) * params.Pagination.PageSize
    data, err := query.
        Limit(params.Pagination.PageSize).
        Offset(offset).
        All(ctx)

    return int64(count), data, err
}

// ✅ 创建时自动注入租户
func (s *Service) Create(ctx context.Context, dto *CreateDTO) (*_gen.Article, error) {
    tenantID, _ := ctx.Value("tenant_id").(int64)
    userID, _ := ctx.Value("user_id").(uuid.UUID)

    return s.client.Article.Create().
        SetTitle(dto.Title).
        SetContent(dto.Content).
        SetTenantID(tenantID).  // 必须注入租户 ID
        SetAuthorID(userID).
        Save(ctx)
}
```

### 14.3 租户验证

```go
// ✅ 更新/删除前验证租户所有权
func (s *Service) Update(ctx context.Context, id uuid.UUID, dto *UpdateDTO) (*_gen.Article, error) {
    tenantID, _ := ctx.Value("tenant_id").(int64)

    // 先查询，验证租户
    article, err := s.client.Article.Query().
        Where(
            article.IDEQ(id),
            article.TenantIDEQ(tenantID),  // 验证所有权
        ).
        First(ctx)
    if err != nil {
        return nil, ErrNotFound
    }

    // 更新
    return article.Update().
        SetTitle(dto.Title).
        Save(ctx)
}
```

---

## 15. 插件开发规范

### 15.1 插件接口实现

```go
// ✅ 必须实现 Plugin 接口
type MyPlugin struct {
    config  Config
    runtime core.PluginRuntime
}

func (p *MyPlugin) Name() string {
    return "myplugin"
}

func (p *MyPlugin) Version() string {
    return "1.0.0"
}

func (p *MyPlugin) Priority() int {
    return 50  // 优先级：数字越小越先执行
}

func (p *MyPlugin) Init(ctx context.Context, runtime core.PluginRuntime) error {
    p.runtime = runtime

    // 注册 Hook
    runtime.RegisterHook("before_create", p.beforeCreate)
    runtime.RegisterHook("after_create", p.afterCreate)

    return nil
}

func (p *MyPlugin) Start(ctx context.Context) error {
    log.Println("Plugin started")
    return nil
}

func (p *MyPlugin) Stop(ctx context.Context) error {
    log.Println("Plugin stopped")
    return nil
}

func (p *MyPlugin) Health(ctx context.Context) error {
    return nil
}
```

### 15.2 Hook 注册

```go
// ✅ Hook 函数签名
func (p *MyPlugin) beforeCreate(ctx context.Context, data any) error {
    // 处理逻辑
    return nil
}

// ✅ 注册 Hook
func (p *MyPlugin) Init(ctx context.Context, runtime core.PluginRuntime) error {
    runtime.RegisterHook("before_create", p.beforeCreate)
    runtime.RegisterHook("after_create", p.afterCreate)
    runtime.RegisterHook("before_query", p.beforeQuery)
    return nil
}
```

### 15.3 插件注册

```go
// ✅ 在 main.go 中注册插件
func main() {
    runtime := core.NewPluginRuntime()

    // 注册插件
    myPlugin := plugins.NewMyPlugin()
    runtime.Register(myPlugin)

    // 初始化并启动
    runtime.InitAll()
    runtime.StartAll()

    // ...
}
```

---

## 16. 性能优化规范

### 16.1 批量操作

```go
// ✅ 使用 CreateBulk 代替循环 Create
func (s *Service) BatchCreate(ctx context.Context, dtos []*CreateDTO) ([]*_gen.User, error) {
    bulk := make([]*_gen.UserCreate, len(dtos))
    for i, dto := range dtos {
        hashedPassword, _ := bcrypt.GenerateFromPassword([]byte(dto.Password), bcrypt.DefaultCost)
        bulk[i] = s.client.User.Create().
            SetEmail(dto.Email).
            SetPassword(string(hashedPassword))
    }
    return s.client.User.CreateBulk(bulk...).Save(ctx)
}

// ❌ 避免：循环单次创建
func (s *Service) BatchCreate(ctx context.Context, dtos []*CreateDTO) ([]*_gen.User, error) {
    users := make([]*_gen.User, 0, len(dtos))
    for _, dto := range dtos {
        user, _ := s.client.User.Create().
            SetEmail(dto.Email).
            Save(ctx)  // 每次都访问数据库
        users = append(users, user)
    }
    return users, nil
}
```

### 16.2 预加载关联

```go
// ✅ 使用 With* 预加载
func (s *Service) ListWithAuthor(ctx context.Context) ([]*_gen.Article, error) {
    return s.client.Article.Query().
        WithAuthor().  // 预加载作者
        All(ctx)
}

// ❌ 避免：N+1 查询
func (s *Service) ListWithAuthor(ctx context.Context) ([]*_gen.Article, error) {
    articles, _ := s.client.Article.Query().All(ctx)
    for _, article := range articles {
        article.Edges.Author, _ = s.client.User.Get(ctx, article.AuthorID)  // N+1 问题
    }
    return articles, nil
}
```

### 16.3 复用对象

```go
// ✅ 复用 QueryParser
var queryParser = binding.NewQueryParser()

func (c *Controller) List(w http.ResponseWriter, r *http.Request) {
    var params ListParams
    binding.QueryWithParser(r, ¶ms, queryParser)  // 复用解析器
    // ...
}
```

---

## 17. 安全规范

### 17.1 密码处理

```go
// ✅ 密码必须加密存储
import "golang.org/x/crypto/bcrypt"

func hashPassword(password string) (string, error) {
    bytes, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
    return string(bytes), err
}

func checkPassword(password, hash string) bool {
    err := bcrypt.CompareHashAndPassword([]byte(hash), []byte(password))
    return err == nil
}
```

### 17.2 输入验证

```go
// ✅ 使用 validate 标签
type CreateDTO struct {
    Email    string `json:"email" validate:"required,email"`
    Password string `json:"password" validate:"required,min=6,max=72"`
    Age      int    `json:"age" validate:"min=0,max=120"`
}
```

### 17.3 敏感数据

```go
// ✅ 敏感字段不序列化
type User struct {
    Email    string `json:"email"`
    Password string `json:"-"`              // 不返回给前端
    Token    string `json:"-"`              // 不返回给前端
}

// Ent Schema 中使用 Sensitive()
func (User) Fields() []ent.Field {
    return []ent.Field{
        field.String("password").Sensitive(),  // 不在序列化中显示
    }
}
```

### 17.4 JWT 认证（管理后台）

```go
// ✅ JWT Token 生成和验证
func GenerateToken(userID uuid.UUID, role string, tenantID int64) (string, error) {
    claims := jwt.MapClaims{
        "user_id":   userID.String(),
        "role":      role,
        "tenant_id": tenantID,
        "exp":       time.Now().Add(24 * time.Hour).Unix(),
        "iat":       time.Now().Unix(),
    }

    token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
    return token.SignedString([]byte(os.Getenv("JWT_SECRET")))
}

func ValidateToken(tokenString string) (jwt.MapClaims, error) {
    token, err := jwt.Parse(tokenString, func(token *jwt.Token) (any, error) {
        if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
            return nil, fmt.Errorf("unexpected signing method: %v", token.Header["alg"])
        }
        return []byte(os.Getenv("JWT_SECRET")), nil
    })

    if err != nil {
        return nil, err
    }

    if claims, ok := token.Claims.(jwt.MapClaims); ok && token.Valid {
        return claims, nil
    }

    return nil, errors.New("invalid token")
}
```

---

## 18. 测试规范

### 18.1 单元测试

```go
// user_service_test.go
func TestService_Create(t *testing.T) {
    // 使用 enttest 创建测试客户端
    client := enttest.NewClient(t)
    defer client.Close()

    service := NewService(client)

    dto := &CreateDTO{
        Email:    "test@example.com",
        Password: "password123",
        Name:     "Test User",
        Role:     "admin",
    }

    user, err := service.Create(context.Background(), dto)

    require.NoError(t, err)
    require.Equal(t, dto.Email, user.Email)
    require.NotEmpty(t, user.ID)
}
```

### 18.2 集成测试

```go
// integration_test.go
func TestMultiTenant_Isolation(t *testing.T) {
    client := enttest.NewClient(t)
    defer client.Close()

    service := NewService(client)

    // 租户 1 创建数据
    ctx1 := context.WithValue(context.Background(), "tenant_id", int64(1))
    article1, _ := service.Create(ctx1, &CreateDTO{Title: "Tenant1 Article"})

    // 租户 2 查询
    ctx2 := context.WithValue(context.Background(), "tenant_id", int64(2))
    articles, _ := service.List(ctx2, &ListParams{})

    // 租户 2 不应该看到租户 1 的数据
    require.Len(t, articles, 0)
}
```

### 18.3 权限测试

```go
// permission_test.go
func TestCasbin_Permission(t *testing.T) {
    enforcer, _ := casbin.NewEnforcer("model.conf", "policy.csv")

    // 测试管理员权限
    ok, _ := enforcer.Enforce("admin", "user", "delete")
    require.True(t, ok)

    // 测试编辑者权限
    ok, _ = enforcer.Enforce("editor", "article", "update")
    require.True(t, ok)

    // 测试无权限
    ok, _ = enforcer.Enforce("viewer", "article", "delete")
    require.False(t, ok)
}

// API Key 认证测试
func TestAPIKeyAuth(t *testing.T) {
    client := enttest.NewClient(t)
    enforcer, _ := casbin.NewEnforcer("model.conf", "policy.csv")

    // 创建用户和 API Key
    user, _ := client.User.Create().
        SetEmail("test@example.com").
        SetPassword("hash").
        SetName("Test").
        SetRole("admin").
        Save(context.Background())

    apiKey, _ := client.APIKey.Create().
        SetName("Test Key").
        SetKey("test_key_123").
        SetUser(user).
        Save(context.Background())

    // 测试认证中间件
    // ... 模拟 HTTP 请求并验证
}
```

---

## ✅ 代码审查清单

在提交代码前，请确认：

- [ ] 使用 `any` 代替 `interface{}`
- [ ] 代码在 `cms/` 或 `core/` 目录内
- [ ] 没有引用 `pre-demo/`
- [ ] 模块包含 4 个核心文件（module/service/controller/dto）
- [ ] 依赖注入清晰透明
- [ ] Context 作为第一个参数
- [ ] 错误处理完整
- [ ] 多租户字段正确注入和过滤
- [ ] 敏感数据已加密/隐藏
- [ ] 使用 Strapi 风格的响应格式
- [ ] **所有数据接口必须使用 API Key 认证（禁止公开访问）**
- [ ] API Key Schema 通过 user 边关联用户
- [ ] API Key 中间件基于用户角色验证权限
- [ ] Casbin 权限验证正确配置
- [ ] Ent ORM 使用正确
- [ ] Chi 框架路由规范
- [ ] 添加了必要的测试

---

## 📚 相关文档

- [AGENTS.md](../AGENTS.md) - AI 开发规范
- [DEVELOPMENT_RULES.md](./DEVELOPMENT_RULES.md) - 开发规则
- [START_HERE.md](./START_HERE.md) - 快速开始
- [README.md](./README.md) - 完整项目文档
- [core/README.md](./core/README.md) - 核心库文档

---

**遵循这些规范，确保代码质量和一致性！**