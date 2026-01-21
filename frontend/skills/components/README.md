# 前端组件开发规范体系

> **版本**: 1.0
> **状态**: 生产就绪
> **创建日期**: 2026-01-19
> **适用范围**: 所有前端组件开发

---

## 📚 文档体系

这套组件规范体系同时满足 `@frontend/` 和 `@architecture/` 规范要求，为前端组件开发提供完整的指导。

### 核心文档

| 文档 | 路径 | 用途 | 适用场景 |
|------|------|------|---------|
| **组件规则** | `RULES.md` | 完整的组件开发规范 | 组件开发全流程 |
| **技能文件** | `SKILL.md` | @frontend/components 技能 | AI 辅助开发 |
| **检查清单** | `CHECKLIST.md` | 组件开发检查清单 | 质量保证 |
| **模板示例** | `TEMPLATES.md` | 组件代码模板 | 快速开发 |

### 关联文档

| 文档 | 路径 | 用途 |
|------|------|------|
| **前端规范** | `frontend/REFERENCES/standards.md` | 前端开发标准 |
| **架构规则** | `architecture/RULES.md` | 架构设计原则 |
| **架构原则** | `architecture/principles/README.md` | 10 大设计原则 |
| **TypeScript 示例** | `architecture/examples/typescript/README.md` | TypeScript 最佳实践 |

---

## 🎯 核心理念

### 双重规范遵循

所有组件开发必须同时满足：

1. **@frontend/ 规范**
   - ✅ 命名规范（PascalCase, camelCase 等）
   - ✅ 代码风格（ESLint, Prettier）
   - ✅ CSS 系统（UnoCSS, CSS 变量）
   - ✅ 工具配置（TypeScript, 构建工具）

2. **@architecture/ 规范**
   - ✅ 10 大设计原则（SoC, SRP, DRY, KISS 等）
   - ✅ 组件架构设计
   - ✅ 可测试性
   - ✅ 代码质量

### 必须调用的技能

```bash
# 1. 设计阶段（必须）
@architecture-assistant 帮我设计一个 [组件名] 组件

# 2. 前端规范（必须）
@frontend/components 请提供组件开发规范

# 3. 代码审查（必须）
@architecture-assistant 请审查这段组件代码
@frontend/components 请检查这个组件

# 4. 问题诊断（按需）
@frontend/components 这个组件有什么问题？
```

---

## 🚀 快速开始

### 场景 1: 创建新组件

```bash
# 1. 设计阶段
@architecture-assistant 帮我设计一个 Button 组件

# 2. 获取规范
@frontend/components 创建一个 Button 组件

# 3. 编码实现
# - 使用模板（TEMPLATES.md）
# - 遵循命名规范
# - 应用架构原则

# 4. 代码审查
@architecture-assistant 请审查这段 Button 组件代码
@frontend/components 请检查这个 Button 组件

# 5. 检查清单
# - 查看 CHECKLIST.md
# - 运行检查命令
```

### 场景 2: 重构现有组件

```bash
# 1. 问题诊断
@frontend/components 这个组件有什么问题？

# 2. 制定方案
@architecture-assistant 请提供重构建议
@frontend/components 请提供重构建议

# 3. 实施重构
# - 应用建议
# - 保持向后兼容

# 4. 验证结果
@architecture-assistant 请验证重构后的代码
@frontend/components 请检查重构后的组件
```

### 场景 3: 代码审查

```bash
# 1. 架构审查
@architecture-assistant 请审查这段组件代码：
[组件代码]

# 2. 前端规范审查
@frontend/components 请检查这个组件：
[组件代码]

# 3. 修复问题
# - 根据反馈修改
# - 重新审查
```

---

## 📖 文档导航

### 按使用场景

| 场景 | 主要文档 | 辅助文档 |
|------|---------|---------|
| **学习规范** | `RULES.md` | `frontend/REFERENCES/standards.md` |
| **快速开发** | `TEMPLATES.md` | `CHECKLIST.md` |
| **代码审查** | `CHECKLIST.md` | `SKILL.md` |
| **问题诊断** | `SKILL.md` | `RULES.md` |
| **AI 辅助** | `SKILL.md` | - |

### 按组件类型

| 组件类型 | 模板位置 | 检查重点 |
|---------|---------|---------|
| **基础组件** | `TEMPLATES.md` - 基础组件 | UI 展示、Props 简单 |
| **业务组件** | `TEMPLATES.md` - 业务组件 | 业务逻辑、状态管理 |
| **容器组件** | `TEMPLATES.md` - 容器组件 | 数据管理、Hook 使用 |
| **页面组件** | `TEMPLATES.md` - 页面组件 | 路由组合、页面逻辑 |
| **布局组件** | `TEMPLATES.md` - 布局组件 | 页面结构、响应式 |
| **Hook 组件** | `TEMPLATES.md` - Hook 组件 | 状态管理、副作用 |
| **HOC 组件** | `TEMPLATES.md` - HOC 组件 | 功能增强、包装逻辑 |

### 按开发阶段

| 阶段 | 文档 | 关键活动 |
|------|------|---------|
| **设计** | `RULES.md` - 架构设计 | 调用架构技能、确定方案 |
| **编码** | `TEMPLATES.md` | 使用模板、遵循规范 |
| **审查** | `CHECKLIST.md` | 调用审查技能、检查清单 |
| **提交** | `CHECKLIST.md` | 最终检查、质量评分 |

---

## 🎓 学习路径

### 初级开发者（1-3 个月）

#### 第 1 周：基础规范
1. **阅读**: `RULES.md` - 命名规范部分
2. **练习**: 创建 Button、Input 等基础组件
3. **工具**: 熟悉 TypeScript、UnoCSS
4. **检查**: 使用 `CHECKLIST.md` 自查

#### 第 2-4 周：组件开发
1. **阅读**: `TEMPLATES.md` - 基础组件模板
2. **练习**: 创建业务组件（UserCard, ArticleCard）
3. **原则**: 学习 SRP、SoC 原则
4. **审查**: 调用 `@frontend/components` 审查

#### 第 1-3 月：进阶应用
1. **阅读**: `RULES.md` - 架构原则部分
2. **练习**: 创建容器组件、页面组件
3. **原则**: 应用 10 大设计原则
4. **审查**: 调用 `@architecture-assistant` 审查

### 中级开发者（3-12 个月）

#### 架构设计
1. **阅读**: `architecture/principles/README.md`
2. **实践**: 设计复杂组件系统
3. **原则**: 深入理解 10 大原则
4. **文档**: 创建 ADR 文档

#### 性能优化
1. **阅读**: `RULES.md` - 性能优化部分
2. **实践**: 优化现有组件
3. **工具**: React DevTools、性能分析
4. **审查**: 调用技能进行性能审查

#### 团队协作
1. **分享**: 组件开发经验
2. **培训**: 指导初级开发者
3. **审查**: 参与代码审查
4. **改进**: 完善团队规范

### 高级开发者（1 年+）

#### 架构决策
1. **设计**: 大型组件系统架构
2. **决策**: 技术选型和架构决策
3. **文档**: 创建 ADR、架构文档
4. **评审**: 组织架构评审

#### 团队建设
1. **培训**: 制定培训计划
2. **指导**: 一对一指导
3. **审查**: 建立审查流程
4. **改进**: 持续改进规范

---

## 🔧 工具配置

### VS Code 配置

```json
// .vscode/settings.json
{
  "editor.formatOnSave": false,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit"
  },
  "eslint.validate": [
    "javascript",
    "javascriptreact",
    "typescript",
    "typescriptreact"
  ],
  "editor.tabSize": 2,
  "editor.insertSpaces": true,
  "editor.detectIndentation": false,
  "files.eol": "\n",
  "files.insertFinalNewline": true,
  "files.trimTrailingWhitespace": true
}
```

### 推荐扩展

- **ESLint** - Microsoft (代码检查)
- **Prettier** - Prettier (代码格式化)
- **UnoCSS** - UnoCSS (Tailwind 类型的智能提示)
- **TypeScript Hero** - TypeScript 工具
- **GitLens** - Git 增强
- **Conventional Commits** - 提交规范提示

---

## 💡 最佳实践

### 1. 组件开发流程

```
需求分析
  ↓
设计阶段 [必须调用]
  ↓
编码实现 [使用模板]
  ↓
代码审查 [必须调用]
  ↓
测试验证
  ↓
文档化
```

### 2. 代码审查流程

```
自我检查 [使用 CHECKLIST.md]
  ↓
架构审查 [@architecture-assistant]
  ↓
前端规范审查 [@frontend/components]
  ↓
修复问题
  ↓
重新审查
```

### 3. 问题解决流程

```
识别问题
  ↓
调用技能诊断 [@frontend/components]
  ↓
制定方案
  ↓
实施改进
  ↓
验证结果
```

---

## 📊 质量标准

### 优秀组件标准

| 维度 | 标准 | 检查方式 |
|------|------|---------|
| **命名规范** | 100% 符合 | 前端技能审查 |
| **类型安全** | 无 any 类型 | TypeScript 检查 |
| **架构原则** | 遵循 9-10 个 | 架构技能审查 |
| **代码质量** | 无严重问题 | Lint + 构建 |
| **性能优化** | 使用 memo 等 | 性能分析 |
| **可测试性** | 易于测试 | 架构审查 |

### 质量评分

- **优秀 (90-100)**: 通过所有审查，无问题
- **合格 (70-89)**: 通过基本审查，少量问题
- **不合格 (<70)**: 未通过审查，需要重构

---

## 🎯 常见场景

### 场景 1: 创建基础组件

**需求**: 创建一个按钮组件

**步骤**:
1. @frontend/components 创建一个 Button 组件
2. 复制 `TEMPLATES.md` 中的 Button 模板
3. 根据需求修改 Props
4. 实现组件逻辑
5. @architecture-assistant 请审查这段代码
6. @frontend/components 请检查这个组件
7. 使用 `CHECKLIST.md` 自查
8. 运行 `pnpm lint` 和 `tsc --noEmit`

### 场景 2: 重构业务组件

**需求**: 重构用户卡片组件

**步骤**:
1. @frontend/components 这个组件有什么问题？
2. @architecture-assistant 请提供重构建议
3. 分析问题（SRP, SoC, 性能等）
4. 制定重构方案
5. 实施重构
6. @architecture-assistant 请验证重构后的代码
7. @frontend/components 请检查重构后的组件
8. 运行测试和构建

### 场景 3: 代码审查

**需求**: 审查一个复杂组件

**步骤**:
1. @architecture-assistant 请审查这段组件代码
2. @frontend/components 请检查这个组件
3. 整理问题列表
4. 按优先级修复
5. 重新审查
6. 更新文档

---

## 📞 联系方式

### 文档支持
- **组件规则**: `frontend/components/RULES.md`
- **技能文件**: `frontend/components/SKILL.md`
- **检查清单**: `frontend/components/CHECKLIST.md`
- **模板示例**: `frontend/components/TEMPLATES.md`

### 关联文档
- **前端规范**: `frontend/REFERENCES/standards.md`
- **架构规则**: `architecture/RULES.md`
- **架构原则**: `architecture/principles/README.md`

### 技能支持
- **前端技能**: `@frontend/components`
- **架构技能**: `@architecture-assistant`

---

## 🔄 更新维护

### 文档更新
1. **定期审查**: 每季度审查一次
2. **收集反馈**: 收集团队反馈
3. **更新规范**: 根据实际经验调整
4. **版本管理**: 更新版本号

### 规范改进
1. **问题收集**: 收集实际问题
2. **案例分析**: 分析典型案例
3. **最佳实践**: 总结最佳实践
4. **文档更新**: 更新到规范中

### 团队培训
1. **新成员**: 入职培训
2. **定期分享**: 每月分享会
3. **代码审查**: 实战培训
4. **经验交流**: 团队讨论

---

## ✅ 快速检查

### 开发前检查
- [ ] 已调用 `@architecture-assistant` 设计
- [ ] 已调用 `@frontend/components` 获取规范
- [ ] 理解组件职责和边界
- [ ] 确认没有违反 SRP 和 SoC

### 编码中检查
- [ ] 命名符合规范
- [ ] TypeScript 类型完整
- [ ] 使用 React Hooks 规范
- [ ] 使用 UnoCSS 样式
- [ ] 遵循 10 大设计原则

### 提交前检查
- [ ] 已调用 `@architecture-assistant` 审查
- [ ] 已调用 `@frontend/components` 审查
- [ ] 通过类型检查
- [ ] 通过构建
- [ ] 使用 `CHECKLIST.md` 完成检查

---

## 🎉 总结

这套组件规范体系提供了：

1. **完整的规范** - 同时满足前端和架构要求
2. **AI 辅助** - 通过技能提供智能支持
3. **检查清单** - 确保代码质量
4. **模板示例** - 快速开始开发
5. **学习路径** - 从初级到高级
6. **最佳实践** - 经验总结和案例

### 核心原则

1. **双重规范** - 同时满足 `@frontend/` 和 `@architecture/`
2. **技能调用** - 设计和审查必须调用技能
3. **检查清单** - 提交前必须完成检查
4. **持续改进** - 定期审查和更新

### 使用建议

- **初学者**: 从 `TEMPLATES.md` 开始，使用检查清单
- **中级者**: 深入理解架构原则，应用最佳实践
- **高级者**: 指导团队，完善规范，创建 ADR

---

**版本**: 1.0
**状态**: ✅ 生产就绪
**最后更新**: 2026-01-19
**维护者**: 前端团队
**适用范围**: 所有前端组件开发
