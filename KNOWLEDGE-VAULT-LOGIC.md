# Knowledge Vault 运行逻辑

> 本文档定义了 knowledge-vault 的整体运行逻辑，用于规范模型行为。
> **所有操作前必须完整阅读本文档。** 本文档是最高优先级的规则文件，优先级高于 .claude/skills/ 下的操作手册。

---

## 一、核心理念

### 1.1 知识是复利增长的

每次摄入新资料，LLM 将其编译进 Wiki，而不是每次查询都从头推导。随着时间的推移，知识库会越来越丰富，回答越来越精准。

**核心原则：** 每次操作都应该让知识库变得更好。不是完成一个任务就结束，而是让知识在库中沉淀、关联、复用。

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

- **Raw 层**：原始资料，LLM 只读不写
- **Wiki 层**：LLM 维护的知识库，面向人类阅读
- **Schema 层**：本文件 + CLAUDE.md + .claude/skills/ 下的操作手册

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
├── README.md                # 项目说明（人类阅读）
├── CLAUDE.md                # 工作流规范（LLM 阅读）
├── VAULT-INDEX.md           # 实时仪表盘（LLM 自动维护）
├── KNOWLEDGE-VAULT-LOGIC.md # 本文件 — 运行逻辑
│
├── raw/                     # 原始资料层（只读，人工放入）
│   ├── articles/            # 网页文章/博客
│   ├── papers/              # 学术论文
│   ├── repos/               # GitHub 仓库分析
│   ├── transcripts/         # 播客/视频转录
│   ├── data/                # 数据文件（CSV、JSON、脚本等）
│   └── assets/              # 图片等附件
│
├── wiki/                    # 知识库层（LLM 维护）
│   ├── index.md             # 主目录 — 从这里开始查询
│   ├── log.md               # 操作时间线（仅追加）
│   ├── hot.md               # 当前会话热缓存
│   ├── sources/             # 每个资料源的摘要页
│   ├── concepts/            # 概念解释页
│   ├── entities/            # 人物/公司/产品/机构页
│   ├── comparisons/         # 多维对比分析页
│   ├── syntheses/           # 跨源综合报告页
│   └── standards/           # 标准技术指标（按监管目录分类）
│
└── .claude/
    └── skills/              # 四个核心操作手册
        ├── ingest-wiki.md
        ├── query-wiki.md
        ├── synthesize-wiki.md
        └── lint-wiki.md
```

### 2.2 各层职责

**raw/ 层（原始资料）**
- **只读**：LLM 永不修改 raw/ 下的原始文件
- **人工放入**：用户下载/复制原始资料到此目录
- **分类存放**：按资料类型放入对应子目录
- **文件命名**：`YYYY-MM-DD-简短描述.md`，如果资料包含图片，提示用户下载到 `raw/assets/`

**wiki/ 层（知识库）**
- **LLM 维护**：LLM 负责创建、更新、链接所有页面
- **人类可读**：内容面向人类阅读，清晰结构化
- **交叉引用**：页面间通过 `[[wiki/page]]` 格式链接
- **双向维护**：A 引用 B 时，B 也应有回链

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

**为什么这么设计：**
- 每个指标值是一个独立文件，方便被多个标准共享引用（例如"通用 ≥45min"可能被多个水泥标准引用）
- 5 层结构支持精确查询：从产品类别→标准→指标类别→指标子类→具体数值
- YAML frontmatter 使指标值可被程序化查询（按约束条件、数值范围、单位筛选）

---

## 三、操作流程逻辑（详细版）

### 3.1 Ingest（摄入）

**触发条件：** 用户说"保存到知识库"、"ingest"、"摄入"、"add to knowledge base"、"save to wiki"，或发送文件/内容并提到知识库。

#### 完整流程

```
Step 1: 判断资料类型
    ↓
Step 2: 归档原始资料到 raw/
    ↓
Step 3: 完整阅读并提取关键信息
    ↓
Step 4: 与用户讨论要点（可选，但推荐）
    ↓
Step 5: 更新 Wiki 页面
    ├── 创建/更新 wiki/sources/ 摘要页（必须）
    ├── 创建/更新 wiki/concepts/ 概念页（如有新概念）
    ├── 创建/更新 wiki/entities/ 实体页（如有新实体）
    ├── 创建 wiki/comparisons/ 对比页（如与已有知识形成对比）
    ├── 更新 wiki/index.md 目录（必须）
    └── 追加 wiki/log.md 操作记录（必须）
    ↓
Step 6: Git 提交
```

#### 各步骤详细规则

**Step 1 — 判断资料类型**

| 类型 | 判断依据 | raw/ 子目录 |
|------|---------|------------|
| article | 网页文章、博客、新闻 | raw/articles/ |
| paper | 学术论文、技术报告 | raw/papers/ |
| repo | GitHub 仓库分析 | raw/repos/ |
| transcript | 播客/视频转录 | raw/transcripts/ |
| data | CSV、JSON、脚本等数据文件 | raw/data/ |

**Step 2 — 归档规则**
- 文件命名：`YYYY-MM-DD-简短描述.md`
- 如果资料包含图片，提示用户下载到 `raw/assets/`
- 保持原始内容完整，不删减、不修改

**Step 3 — 提取关键信息**
- 完整阅读原始资料
- 提取：核心观点、关键数据、新概念、新实体、与其他知识的关联
- 识别矛盾：如果新资料与已有知识冲突，标注 `[!contradiction]`

**Step 5 — 更新 Wiki 的决策逻辑**

**sources/ 摘要页（必须创建）：**
- 内容：资料标题、来源链接、摘要、3-5 个关键要点、与本知识库其他页面的关联
- 文件命名：`YYYY-MM-DD-简短描述.md`

**concepts/ 概念页（条件创建）：**
- 条件：资料中引入了 Wiki 中不存在的新概念
- 内容：概念定义、关键属性、与相关概念的关联
- 如果概念已存在，检查是否需要更新（新信息补充）

**entities/ 实体页（条件创建）：**
- 条件：资料中提到了重要的人物、公司、产品、机构
- 内容：实体简介、关键信息、相关来源引用
- 如果实体已存在，检查是否需要更新

**comparisons/ 对比页（条件创建）：**
- 条件：新资料与已有知识在某个维度上形成对比
- 对比维度举例：方法 A vs 方法 B、不同观点、不同时期的数据、不同标准的差异
- 内容：对比维度、各方观点/数据、分析结论

**index.md 更新规则：**
- 新增页面必须添加到 index.md 的对应分类下
- 保持目录结构清晰，不冗余

**log.md 追加规则：**
- 每次操作追加一条记录
- 格式：`- YYYY-MM-DD HH:mm | [Ingest] 资料标题 | 更新了 X 个页面`
- 只追加，不修改已有记录

#### 一次摄入的影响范围

单个资料通常涉及 5-15 个 Wiki 页面。每次更新一个页面时，检查并更新所有相关的交叉引用。

#### 边界情况处理

| 情况 | 处理方式 |
|------|---------|
| 资料质量低、信息量少 | 仍然归档到 raw/，但 sources/ 摘要页注明"信息量有限" |
| 资料与已有知识完全重复 | 归档到 raw/，在 sources/ 中标注"与 XX 资料重复"并引用已有页面 |
| 资料与已有知识矛盾 | 归档并创建 sources/，在相关页面标注 `[!contradiction]`，列出双方来源 |
| 用户只给了链接（未下载内容） | 提示用户先下载原始内容到 raw/ |
| 资料包含敏感/隐私信息 | 提示用户，不摄入到 Wiki |

---

### 3.2 Query（查询）

**触发条件：** 用户说"查一下 X"、"知识库里"、"according to the knowledge base"、"what does the knowledge base say"、"wiki 里"等。

#### 完整流程

```
Step 1: 定位相关页面
    ├── 先读 wiki/index.md（了解全貌）
    └── 再读 wiki/hot.md（了解近期上下文）
    ↓
Step 2: 深入阅读
    ├── 逐页阅读相关页面
    ├── 跟踪交叉引用
    └── 发现矛盾时标注 [!contradiction]
    ↓
Step 3: 综合回答
    ├── 多源综合
    └── 附带来源引用
    ↓
Step 4: 可选归档（有价值的回答）
    ├── 保存到 wiki/syntheses/
    ├── 更新 wiki/index.md
    └── 更新 wiki/log.md
```

#### 回答格式决策

| 问题类型 | 回答格式 |
|---------|---------|
| 事实查询（"X 的标准值是多少"） | 直接回答 + 引用来源 |
| 对比查询（"X 和 Y 有什么区别"） | 表格形式 |
| 分析查询（"X 的趋势是什么"） | 结构化 Markdown 报告 |
| 综合查询（"关于 X 的所有信息"） | 多维度结构化输出 |

#### 边界情况处理

| 情况 | 处理方式 |
|------|---------|
| Wiki 中有完整答案 | 直接回答，引用来源 |
| Wiki 中有部分答案 | 回答已知部分，明确标注"以下信息在 Wiki 中未找到" |
| Wiki 中完全没有 | 明确告知知识不足，建议用户补充来源 |
| 多个页面给出矛盾信息 | 列出所有矛盾来源，标注 `[!contradiction]`，不做主观判断 |
| 用户问的是训练数据中的知识 | 优先使用 Wiki 内容，不依赖训练数据 |

#### 归档决策（Step 4）

**什么情况下应该归档：**
- 回答本身具有长期价值（如对比分析、发现关联、综合报告）
- 回答涉及多个来源的综合
- 回答填补了知识空白

**什么情况下不应该归档：**
- 简单的单源事实查询
- 临时性的上下文回答
- 用户明确说不需要保存

---

### 3.3 Synthesize（综合）

**触发条件：** 用户说"写一篇关于 X 的综述"、"综合报告"、"synthesize"、"pull together everything about X"、"综述"等。

#### 完整流程

```
Step 1: 扫描相关页面
    ├── 读 wiki/index.md 确定范围
    ├── 读所有相关页面（sources, concepts, entities, comparisons）
    └── 跟踪交叉引用，确保覆盖全面
    ↓
Step 2: 综合分析
    ├── 识别多源共识 vs 单一来源观点
    ├── 标注矛盾点 [!contradiction]
    └── 发现知识空白（Wiki 中缺失但应该有的内容）
    ↓
Step 3: 撰写报告
    ├── 保存到 wiki/syntheses/YYYY-MM-DD-主题.md
    └── 报告结构见下方
    ↓
Step 4: 更新 index.md + log.md
    ↓
Step 5: Git 提交
```

#### 报告结构

```markdown
# [主题] — 综合报告

## 概述
[简要说明本报告的主题和范围]

## 各维度分析

### 维度一：[名称]
[分析内容，引用来源]

### 维度二：[名称]
[分析内容，引用来源]

## 共识与分歧

| 观点 | 支持来源 | 证据强度 |
|------|---------|---------|
| ... | ... | 多源共识/单一来源 |

## 知识空白与建议
- [缺失的知识点]
- [建议补充的资料类型]

## 参考文献
- [[wiki/sources/...]]
- [[wiki/concepts/...]]
- [[wiki/entities/...]]
```

#### 边界情况处理

| 情况 | 处理方式 |
|------|---------|
| 相关页面少于 3 个 | 告知用户资料不足，建议先补充来源再综合 |
| 多个来源严重矛盾 | 在报告中突出矛盾，不做调和，建议用户提供更多资料 |
| 主题跨多个领域 | 按领域分节，明确标注每个领域的覆盖程度 |
| 用户要求更新已有综合报告 | 在原报告基础上追加新内容，标注"更新于 YYYY-MM-DD" |

---

### 3.4 Lint（健康检查）

**触发条件：** 用户说"检查知识库"、"lint"、"健康检查"、"health check"、"clean up the knowledge base"等。

#### 检查清单

##### 1. 矛盾检查
- [ ] 不同页面之间是否存在相互矛盾的陈述
- [ ] 新资料是否与旧页面中的主张冲突
- [ ] 在矛盾处标注 `[!contradiction]` 并注明来源

##### 2. 孤立页面
- [ ] 哪些页面没有入站链接（没有其他页面引用它）
- [ ] 孤立页面是否需要保留或合并

##### 3. 过时内容
- [ ] 是否有被新资料 supersede 的旧主张
- [ ] 标记过时内容并引用新来源

##### 4. 缺失概念
- [ ] 页面中提到了哪些概念但没有对应的概念页
- [ ] 建议创建缺失的概念页

##### 5. 交叉引用
- [ ] 检查 Wiki 链接是否有效（指向存在的页面）
- [ ] 发现死链接并修复

##### 6. 格式一致性
- [ ] YAML frontmatter 是否完整
- [ ] 标签是否一致
- [ ] 命名规范是否统一

##### 7. 知识空白
- [ ] 哪些主题应该深入但资料不足
- [ ] 建议补充哪些来源

#### 输出格式

**诊断报告** 保存到 `wiki/syntheses/lint-YYYY-MM-DD.md`

```markdown
# 知识库健康检查报告 — YYYY-MM-DD

## 概览
- 总页面数：X
- 发现问题数：X
- 严重问题：X

## 检查结果

### 1. 矛盾（X 处）
| 页面 | 矛盾内容 | 涉及来源 |
|-----|---------|---------|
| ... | ... | ... |

### 2. 孤立页面（X 个）
- ...

### 3. 过时内容（X 处）
- ...

### 4. 缺失概念（X 个）
- ...

### 5. 死链接（X 处）
- ...

### 6. 格式问题（X 处）
- ...

### 7. 知识空白（X 处）
- ...

## 修复建议
[按优先级列出修复建议]

## 补充资料建议
[建议用户补充哪些来源]
```

#### 修复流程

1. **先报告，后修复** — 输出诊断报告，等用户确认后再执行修复
2. **重大修改先讨论** — 合并页面、删除页面等操作先与用户讨论
3. **修复后提交** — 修复完成后 Git 提交，commit message: `[Lint] YYYY-MM-DD 健康检查修复`

---

## 四、页面规范

### 4.1 YAML Frontmatter 完整模板

#### 通用页面（sources / concepts / entities / comparisons / syntheses）

```yaml
---
title: 页面标题
type: source | concept | entity | comparison | synthesis
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [标签1, 标签2]
---
```

#### 标准节点（L1）

```yaml
---
type: standard-node
title: GB 175-2023 — 通用硅酸盐水泥
std: GB 175-2023
std_name: 通用硅酸盐水泥
category: 工业生产资料
---
```

#### 指标类别（L2）

```yaml
---
title: 化学成分
type: indicator-category
std: GB 175-2023
std_name: 通用硅酸盐水泥
category: 工业生产资料
tags: [技术指标类别, 工业生产资料]
---
```

#### 指标子类（L3）

```yaml
---
title: 初凝时间
type: indicator-subcategory
std: GB 175-2023
std_name: 通用硅酸盐水泥
category: 工业生产资料
tags: [技术指标子类, 工业生产资料]
---
```

#### 指标值（L4）

```yaml
---
title: 通用 ≥45min
type: indicator-value
std: GB 175-2023
std_name: 通用硅酸盐水泥
category: 工业生产资料
constraint: ≥        # 约束条件：≥ / ≤ / =
value: 45            # 数值（纯数字，不带单位）
unit: min            # 单位
grade: 通用          # 等级/条件（如无等级则填"通用"）
tags: [技术指标值, 工业生产资料]
---
```

### 4.2 交叉引用格式

| 场景 | 格式 | 示例 |
|------|------|------|
| 引用同一标准下的页面 | `[[wiki/standards/类别/标准/页面.md]]` | `[[wiki/standards/工业生产资料/GB 175-2023/初凝时间.md]]` |
| 引用其他标准 | `[[wiki/standards/类别/标准/标准节点.md|显示名]]` | `[[wiki/standards/工业生产资料/GB-T 748-2023/GB-T 748-2023 — 抗硫酸盐硅酸盐水泥.md|GB-T 748-2023]]` |
| 引用概念页 | `[[wiki/concepts/概念名.md]]` | `[[wiki/concepts/national-standards-gb.md]]` |
| 引用来源页 | `[[wiki/sources/文件名.md]]` | `[[wiki/sources/2026-06-20-national-standards-collection.md]]` |
| 引用综合报告 | `[[wiki/syntheses/文件名.md]]` | `[[wiki/syntheses/2026-06-20-technical-indicators-knowledge-graph.md]]` |
| 带显示文本 | `[[wiki/page|显示文本]]` | `[[wiki/concepts/national-standards-gb|国家标准体系]]` |

### 4.3 文件命名规范

| 页面类型 | 命名规则 | 示例 |
|---------|---------|------|
| sources/ | `YYYY-MM-DD-简短描述.md` | `2026-06-20-national-standards-collection.md` |
| concepts/ | `英文连字符式.md` | `national-standards-gb.md` |
| entities/ | `英文连字符式.md` | `china-national-standardization-committee.md` |
| comparisons/ | `YYYY-MM-DD-对比主题.md` | `2026-06-20-portland-vs-sulfate-resistant.md` |
| syntheses/ | `YYYY-MM-DD-主题.md` | `2026-06-20-technical-indicators-knowledge-graph.md` |
| 标准节点 | `GB 175-2023 — 标准名称.md` | `GB 175-2023 — 通用硅酸盐水泥.md` |
| 指标类别 | `指标名称.md` | `化学成分.md` |
| 指标子类 | `指标名称.md` | `初凝时间.md` |
| 指标值 | `等级/条件 约束条件 数值单位.md` | `通用 ≥45min.md` |

### 4.4 标准页面内容模板

#### 标准节点（L1）

```markdown
---
type: standard-node
title: GB XXXXX-YYYY — 标准名称
std: GB XXXXX-YYYY
std_name: 标准名称
category: 产品类别
---

# GB XXXXX-YYYY — 标准名称

## 技术指标

- [[wiki/standards/产品类别/GB XXXXX-YYYY/指标类别1.md]]
- [[wiki/standards/产品类别/GB XXXXX-YYYY/指标类别2.md]]

## 引用标准

- GB/T XXXX
- GB/T XXXX

## 关联标准

- [[wiki/standards/产品类别/关联标准/关联标准节点.md|关联标准名称]]
```

#### 指标类别（L2）

```markdown
---
title: 指标类别名称
type: indicator-category
std: GB XXXXX-YYYY
std_name: 标准名称
category: 产品类别
tags: [技术指标类别, 产品类别]
---

# 指标类别名称

**所属标准：** [[wiki/standards/产品类别/GB XXXXX-YYYY/GB XXXXX-YYYY — 标准名称.md|GB XXXXX-YYYY — 标准名称]]

## 子指标

- [[wiki/standards/产品类别/GB XXXXX-YYYY/指标子类1.md]]
- [[wiki/standards/产品类别/GB XXXXX-YYYY/指标子类2.md]]
```

#### 指标子类（L3）

```markdown
---
title: 指标子类名称
type: indicator-subcategory
std: GB XXXXX-YYYY
std_name: 标准名称
category: 产品类别
tags: [技术指标子类, 产品类别]
---

# 指标子类名称

**指标类别：** [[wiki/standards/产品类别/GB XXXXX-YYYY/指标类别.md]]

## 指标值

- [[wiki/standards/产品类别/GB XXXXX-YYYY/等级 约束条件 数值单位.md]]
- [[wiki/standards/产品类别/GB XXXXX-YYYY/等级 约束条件 数值单位.md]]
```

#### 指标值（L4）

```markdown
---
title: 等级 约束条件 数值单位
type: indicator-value
std: GB XXXXX-YYYY
std_name: 标准名称
category: 产品类别
constraint: ≥
value: 数值
unit: 单位
grade: 等级
tags: [技术指标值, 产品类别]
---

# 等级 约束条件 数值单位

## 基本信息

| 属性 | 内容 |
|:----|:-----|
| **指标类别** |  |
| **子类** | [[wiki/standards/产品类别/GB XXXXX-YYYY/指标子类.md]] |
| **等级/条件** | 等级 |
| **约束条件** | 约束条件 |
| **指标值** | 数值 |
| **单位** | 单位 |
| **完整表达式** | 约束条件 数值 单位 |
```

---

## 五、Git 工作流

### 5.1 每次操作后必须提交

```bash
git add -A
git commit -m "[操作类型] 描述"
git push
```

### 5.2 提交信息格式

| 操作类型 | 格式 | 示例 |
|---------|------|------|
| Ingest | `[Ingest] 资料标题` | `[Ingest] 2026-06-20 国家标准资料集` |
| Synthesize | `[Synthesize] 主题名称` | `[Synthesize] 技术指标知识图谱` |
| Lint | `[Lint] YYYY-MM-DD 健康检查` | `[Lint] 2026-06-22 健康检查` |
| 其他更新 | `[Sync] 描述` | `[Sync] 新增 KNOWLEDGE-VAULT-LOGIC.md` |

### 5.3 Token 管理

- Token 存储在 Windows 凭据管理器中
- 使用 `credential.helper = manager` 自动获取
- **永不**将 token 硬编码在代码或文件中
- 如果 token 泄露，立即在 GitHub 设置中 revoke 并重新生成
- 如果 push 失败，检查：
  1. 网络连接（`github.com:443` 是否可达）
  2. Token 是否过期
  3. 远程分支是否有 upstream 配置

### 5.4 Push 失败处理

| 错误 | 原因 | 处理方式 |
|------|------|---------|
| `no upstream branch` | 分支未设置 upstream | `git push --set-upstream origin master` |
| `403/401` | Token 过期 | 从凭据管理器获取新 token 并更新 |
| `secret scanning` | 历史中包含敏感信息 | 用 `git filter-branch` 清除后重新 push |
| 连接超时 | 网络限制 | 检查网络，重试或换用 SSH |

---

## 六、决策树与边界情况

### 6.1 操作选择决策树

```
用户说了一句话
    │
    ├─ 包含触发词 → 执行对应操作
    │   ├─ "保存/摄入/ingest" → Ingest
    │   ├─ "查/知识库/wiki" → Query
    │   ├─ "综述/综合/synthesize" → Synthesize
    │   └─ "检查/lint/健康" → Lint
    │
    ├─ 包含多个触发词 → 按优先级：Lint > Ingest > Synthesize > Query
    │
    └─ 不包含触发词 → 正常对话，不操作知识库
```

### 6.2 通用边界情况处理

| 情况 | 处理方式 |
|------|---------|
| 操作过程中发现矛盾 | 标注 `[!contradiction]`，继续操作，在 log 中记录 |
| 操作过程中发现死链接 | 修复死链接，在 log 中记录 |
| 用户中断操作 | 已完成的修改提交，未完成的丢弃 |
| 多个用户同时操作 | 每次操作前先 git pull，操作后 git push，冲突时手动解决 |
| Git push 失败 | 不丢失本地修改，修复问题后重试 |
| 页面数量过大 | 单次操作控制在 50 个文件以内，超过时分批提交 |

### 6.3 质量门禁

每次操作完成前，检查以下条目：

- [ ] 所有新建页面都有 YAML frontmatter
- [ ] 所有引用都指向存在的页面
- [ ] 矛盾已标注 `[!contradiction]`
- [ ] index.md 已更新
- [ ] log.md 已追加
- [ ] Git 已提交并推送

---

## 七、注意事项

### 7.1 通用规则
- 先读 `wiki/index.md` 了解全貌，再执行具体操作
- 保持所有页面格式一致
- 交叉引用双向维护（A 引用 B 时，B 也应有回链）
- 操作完成后更新 `wiki/log.md`
- 每个标准节点页面包含"引用标准"和"关联标准"部分

### 7.2 安全规则
- 不修改 raw/ 下的原始文件
- 不在代码/文件中硬编码敏感信息（token、密码等）
- 遵守 GitHub secret scanning 规则
- 不摄入包含个人隐私的资料

### 7.3 质量规则
- 每个页面必须有 YAML frontmatter
- 引用必须指向存在的页面
- 矛盾必须标注 `[!contradiction]`
- 知识不足时明确告知，不编造
- 综合报告不是简单拼接，而是真正的跨源综合
- 指标值的 YAML frontmatter 必须包含 constraint、value、unit、grade 四个字段

### 7.4 关于 standards/ 模块的特别规则
- 新建标准时，必须同时创建 L1-L4 所有层级
- 同一指标值被多个标准共享时，优先使用已有的 L4 文件
- 指标值的 grade 字段：无等级区分时填"通用"
- 产品类别名称必须与监管目录一致（工业生产资料、农业生产资料等）
