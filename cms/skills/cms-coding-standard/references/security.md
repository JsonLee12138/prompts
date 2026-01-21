# 安全规范

> 本文档定义了 Headless CMS 项目的安全编码规范，确保系统安全性。

## 📑 目录

- [1. 密码处理](#1-密码处理)
- [2. 输入验证](#2-输入验证)
- [3. 敏感数据](#3-敏感数据)
- [4. JWT 认证](#4-jwt-认证)

---

## 1. 密码处理

密码必须使用 bcrypt 加密存储：

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

## 2. 输入验证

所有输入必须使用 validate 标签验证：

```go
// ✅ 使用 validate 标签
type CreateDTO struct {
    Email    string `json:"email" validate:"required,email"`
    Password string `json:"password" validate:"required,min=6,max=72"`
    Age      int    `json:"age" validate:"min=0,max=120"`
}
```

## 3. 敏感数据

敏感字段不应序列化到响应中：

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

## 4. JWT 认证

JWT Token 生成和验证：

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

**Always prioritize security in your code!** 🔒
