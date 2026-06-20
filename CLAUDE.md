# CLAUDE.md — Knowledge Vault Schema

> 本文件定义了知识库的结构、约定和工作流。LLM 在执行任何知识库操作前必须完整阅读本文件。

## 目录结构

```
knowledge-vault/
├── README.md              # 项目说明
├── CLAUDE.md              # 本文件 — 工作流规范
├── VAULT-INDEX.md         # 实时仪表盘 (LLM 自动维护)
├── raw/                   # 原始资料 (只读, 人工放入)
│   ├── articles/          # 网页文章/博客
│   ├── papers/            # 学术论文
│   ├── repos/             # GitHub 仓库分析
│   ├── transcripts/       # 播客/视频转录
│   ├── data/              # 数据文件
│   └── assets/            # 图片等附件
├── wiki/                  # LLM 维护的知识库
│   ├── index.md           # 主目录 — 从这里开始查询
│   ├── log.md             # 操作时间线 (仅追加)
│   ├── hot.md             # 当前会话热缓存
│   ├── sources/           # 每个资料源的摘要页
│   ├── concepts/          # 概念解释页
│   ├── entities/          # 人物/公司/产品页
│   ├── comparisons/       # 多维对比分析页
│   └── syntheses/         # 跨源综合报告页
└── .claude/
    └── skills/            # 四个核心操作手册
        ├── ingest-wiki.md
        ├── query-wiki.md
        ├── synthesize-wiki.md
        ├── lint-wiki.md
        └── references/    # 核心文件空白模板备份
```

## 页面约定

### 通用规则
- 所有 Wiki 页面使用 Markdown 格式
- 每个页面必须有 YAML frontmatter
- 使用 `[[wiki/page]]` 格式的 Wiki 链接进行交叉引用
- 文件命名：小写字母 + 连字符，如 `transformer-architecture.md`

### YAML Frontmatter 模板
```yaml
---
title: 页面标题
type: source | concept | entity | comparison | synthesis
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [tag1, tag2]
sources: [指向相关源页面的链接]
---
```

### 页面类型说明

| 类型 | 位置 | 内容 |
|------|------|------|
| source | wiki/sources/ | 单个资料源的摘要、关键要点 |
| concept | wiki/concepts/ | 核心概念的定义、解释、关联 |
| entity | wiki/entities/ | 人物、公司、产品等实体的档案 |
| comparison | wiki/comparisons/ | 多维度对比分析 |
| synthesis | wiki/syntheses/ | 跨多个源的综合性报告 |

## 操作触发词

当用户说出以下触发词时，LLM 必须读取对应的 skill 文件并执行操作：

- **Ingest**: "保存到知识库"、"摄入"、"ingest"、"add to knowledge base"、"save to wiki"
- **Query**: "知识库里"、"查一下"、"wiki 里"、"according to the knowledge base"
- **Synthesize**: "综述"、"综合报告"、"synthesize"、"写一篇关于"
- **Lint**: "检查知识库"、"lint"、"健康检查"、"health check"

## Git 提交规范

每次 Ingest / Synthesize / Lint 操作后执行 commit & push。
Query 仅在归档新内容时提交。
提交信息格式：`[操作] 简要说明`

## 重要原则

1. **Raw 目录只读** — LLM 可以读取 raw/ 下的文件，但绝不能修改
2. **Wiki 目录 LLM 全权维护** — 创建、更新、删除页面都由 LLM 负责
3. **索引优先** — 查询时先读 index.md 找到相关页面，再深入阅读
4. **知识复利** — 好的问答结果也要归档回 wiki/syntheses/
5. **一致性** — 更新一个页面时，检查并更新所有相关的交叉引用
