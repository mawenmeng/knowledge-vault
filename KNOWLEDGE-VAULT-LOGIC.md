# Knowledge Vault 运行逻辑

> 本文档定义了 knowledge-vault 的整体运行逻辑，用于规范模型行为。
> 所有操作前必须完整阅读本文档。

---

## 一、核心理念

### 1.1 知识是复利增长的

每次摄入新资料，LLM 将其编译进 Wiki，而不是每次查询都从头推导。随着时间的推移，知识库会越来越丰富，回答越来越精准。

### 1.2 三层架构

```
┌──────────────────────────────────────┐
│  Raw Sources (只读, 人工维护)         │
│  原始资料：文章、论文、数据、转录...   │
├──────────────────────────────────────┤
│  The Wiki (LLM 维护, 人类阅读)        │
│  结构化知识：概念、实体、标准、综述...  │
├──────────────────────────────────────┤
│  The Schema (规则文件)                │
│  告诉 LLM 如何运作的规则              │
└──────────────────────────────────────┘
```

### 1.3 四大操作

| 操作 | 触发词 | 说明 |
|------|--------|------|
| **Ingest** | "保存到知识库"、"ingest"、"摄入" | 摄入新资料，提取关键信息并更新 Wiki |
| **Query** | "查一下 X"、"知识库里" | 基于 Wiki 回答问题，附带来源引用 |
| **Synthesize** | "写一篇关于 X 的综述"、"综合报告" | 跨来源综合，生成综述报告 |
| **Lint** | "检查知识库"、"健康检查" | 发现矛盾、孤立页面、过时内容 |

---

## 二、目录结构逻辑

### 2.1 顶层结构

```
knowledge-vault/
├── README.md               # 项目说明（人类阅读）
├── CLAUDE.md               # 工作流规范（LLM 阅读）
├── VAULT-INDEX.md          # 实时仪表盘（LLM 自动维护）
├── KNOWLEDGE-VAULT-LOGIC.md # 本文件 — 运行逻辑
│
├── raw/                    # 原始资料层（只读，人工放入）
│   ├── articles/           # 网页文章/博客
│   ├── papers/             # 学术论文
│   ├── repos/              # GitHub 仓库分析
│   ├── transcripts/        # 播客/视频转录
│   ├── data/               # 数据文件（CSV、JSON、脚本等）
│   └── assets/             # 图片等附件
│
├── wiki/                   # 知识库层（LLM 维护）
│   ├── index.md            # 主目录 — 从这里开始查询
│   ├── log.md              # 操作时间线（仅追加）
│   ├── hot.md              # 当前会话热缓存
│   ├── sources/            # 每个资料源的摘要页
│   ├── concepts/           # 概念解释页
│   ├── entities/           # 人物/公司/产品/机构页
│   ├── comparisons/        # 多维对比分析页
│   ├── syntheses/          # 跨源综合报告页
│   └── standards/          # 标准技术指标（按监管目录分类）
│
└── .claude/
    └── skills/             # 四个核心操作手册
        ├── ingest-wiki.md
        ├── query-wiki.md
        ├── synthesize-wiki.md
        └── lint-wiki.md
```

### 2.2 各层职责

**raw/ 层（原始资料）**
- 只读：LLM 永不修改 raw/ 下的原始文件
- 人工放入：用户下载/复制原始资料到此目录
- 分类存放：按资料类型放入对应子目录

**wiki/ 层（知识库）**
- LLM 维护：LLM 负责创建、更新、链接所有页面
- 人类可读：内容面向人类阅读，清晰结构化
- 交叉引用：页面间通过 `[[wiki/page]]` 格式链接

### 2.3 standards/ 子目录的特殊结构

`wiki/standards/` 是本知识库的特色模块，采用 **5 层知识图谱** 结构：

```
L0: 产品类别（监管目录分类）
    例如：工业生产资料、农业生产资料、食品相关产品...
    │
L1: 标准节点（具体标准）
    例如：GB 175-2023、GB-T 15063-2020...
    │
L2: 指标类别（技术指标大类）
    例如：化学成分、物理性能、养分含量...
    │
L3: 指标子类（具体指标项）
    例如：初凝时间、抗压强度、水分(H₂O)...
    │
L4: 指标值（具体数值+约束条件）
    例如：通用 ≥45min、强度等级42.5 ≥42.5MPa...
```

**层级关系：**
- L1 标准节点包含多个 L2 指标类别
- L2 指标类别包含多个 L3 指标子类
- L3 指标子类包含多个 L4 指标值
- L4 指标值通过 YAML frontmatter 记录：约束条件（≥/≤）、数值、单位、等级/条件

**文件命名约定：**
- L1 标准节点：`GB 175-2023 — 通用硅酸盐水泥.md`
- L2 指标类别：`化学成分.md`、`物理性能.md`
- L3 指标子类：`初凝时间.md`、`抗压强度.md`
- L4 指标值：`通用 ≥45min.md`、`强度等级42.5 ≥42.5MPa.md`

---

## 三、操作流程逻辑

### 3.1 Ingest（摄入）

**触发 → 归档 → 提取 → 更新 Wiki → 提交**

1. **判断资料类型**：article / paper / repo / transcript / data
2. **归档到 raw/**：保存原始文件到对应子目录
3. **阅读并提取**：完整阅读，与用户确认关键要点
4. **更新 Wiki**：
   - 创建/更新 `wiki/sources/` 摘要页
   - 创建/更新 `wiki/concepts/` 概念页
   - 创建/更新 `wiki/entities/` 实体页
   - 如需要，创建 `wiki/comparisons/` 对比页
   - 更新 `wiki/index.md` 目录
   - 追加 `wiki/log.md` 操作记录
5. **Git 提交**：`git add -A && git commit -m "[Ingest] ..." && git push`

**关键规则：**
- 不修改 raw/ 下的原始文件
- 保持 YAML frontmatter 格式一致
- 使用 `[[wiki/page]]` 交叉引用
- 发现矛盾时标注 `[!contradiction]`

### 3.2 Query（查询）

**触发 → 定位 → 阅读 → 综合回答 → 可选归档**

1. **定位相关页面**：先读 `wiki/index.md`，再读 `wiki/hot.md`
2. **深入阅读**：逐页阅读，跟踪交叉引用
3. **综合回答**：多源综合，附带来源引用
4. **可选归档**：有价值的回答可保存到 `wiki/syntheses/`

**关键规则：**
- 优先使用 Wiki 内容，不依赖训练数据
- 知识不足时明确告知，建议补充来源
- 好的问答结果可以归档，让知识复利增长

### 3.3 Synthesize（综合）

**触发 → 扫描 → 分析 → 撰写 → 提交**

1. **扫描相关页面**：覆盖 sources、concepts、entities、comparisons
2. **综合分析**：识别共识 vs 单一来源，标注矛盾，发现空白
3. **撰写报告**：保存到 `wiki/syntheses/YYYY-MM-DD-主题.md`
4. **Git 提交**

**报告结构：**
- 概述
- 各维度分析
- 共识与分歧
- 知识空白与建议
- 参考文献（指向具体 Wiki 页面）

### 3.4 Lint（健康检查）

**触发 → 检查 → 报告 → 确认后修复**

**检查项：**
1. 矛盾检查
2. 孤立页面
3. 过时内容
4. 缺失概念
5. 交叉引用有效性
6. 格式一致性
7. 知识空白

**流程：** 先报告问题 → 用户确认 → 执行修复 → Git 提交

---

## 四、页面规范

### 4.1 YAML Frontmatter 模板

```yaml
---
title: 页面标题
type: source | concept | entity | comparison | synthesis | standard-node | indicator-category | indicator-subcategory | indicator-value
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [标签1, 标签2]
---
```

**标准节点特有字段：**
```yaml
---
type: standard-node
title: GB 175-2023 — 通用硅酸盐水泥
std: GB 175-2023
std_name: 通用硅酸盐水泥
category: 工业生产资料
---
```

**指标值特有字段：**
```yaml
---
type: indicator-value
std: GB 175-2023
std_name: 通用硅酸盐水泥
category: 工业生产资料
constraint: ≥        # 约束条件：≥ / ≤ / =
value: 45.0          # 数值
unit: min            # 单位
grade: 通用          # 等级/条件
tags: [技术指标值, 工业生产资料]
---
```

### 4.2 交叉引用格式

- Wiki 链接：`[[wiki/page-name]]`
- 带显示文本：`[[wiki/page-name|显示文本]]`
- 跨目录链接：`[[wiki/standards/工业生产资料/GB 175-2023/通用 ≥45min.md]]`

### 4.3 文件命名规范

- 小写字母 + 连字符（通用规则）
- 标准节点：`GB 175-2023 — 标准名称.md`
- 指标值：`等级/条件 约束条件 数值单位.md`
- 日期前缀：`YYYY-MM-DD-描述.md`

---

## 五、Git 工作流

### 5.1 每次操作后必须提交

```bash
git add -A
git commit -m "[操作类型] 描述"
git push
```

### 5.2 提交信息格式

| 操作类型 | 格式 |
|---------|------|
| Ingest | `[Ingest] 资料标题` |
| Synthesize | `[Synthesize] 主题名称` |
| Lint | `[Lint] YYYY-MM-DD 健康检查` |
| 其他 | `[Sync] 描述` |

### 5.3 Token 管理

- Token 存储在 Windows 凭据管理器中
- 使用 `credential.helper = manager` 自动获取
- **永不**将 token 硬编码在代码或文件中
- 如果 token 泄露，立即在 GitHub 设置中 revoke 并重新生成

---

## 六、注意事项

### 6.1 通用规则
- 先读 `wiki/index.md` 了解全貌，再执行具体操作
- 保持所有页面格式一致
- 交叉引用双向维护（A 引用 B 时，B 也应有回链）
- 操作完成后更新 `wiki/log.md`

### 6.2 安全规则
- 不修改 raw/ 下的原始文件
- 不在代码/文件中硬编码敏感信息（token、密码等）
- 遵守 GitHub secret scanning 规则

### 6.3 质量规则
- 每个页面必须有 YAML frontmatter
- 引用必须指向存在的页面
- 矛盾必须标注 `[!contradiction]`
- 知识不足时明确告知，不编造
