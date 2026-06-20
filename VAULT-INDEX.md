---
title: 仓库完整索引
type: vault-index
updated: 2026-06-20
---

# 📚 知识库完整索引

> 基于 Karpathy LLM Wiki 方法论构建

## 目录结构

```
D:\knowledge-vault/
├── CLAUDE.md              # 工作流配置
├── README.md              # 仓库说明
├── VAULT-INDEX.md         # 本文件
├── .obsidian/             # Obsidian配置
├── .claude/skills/        # Claude技能文件
│   ├── ingest-wiki.md     # 摄入
│   ├── query-wiki.md      # 查询
│   ├── synthesize-wiki.md # 综合
│   └── lint-wiki.md       # 检查
├── raw/
│   ├── data/              # 原始数据（PDF、OCR结果、脚本）
│   └── articles/          # 原始文章
├── wiki/
│   ├── index.md           # 知识图谱索引
│   ├── log.md             # 变更日志
│   ├── hot.md             # 热点/待办
│   ├── sources/           # 资料源
│   ├── concepts/          # 概念（监管目录分类）
│   ├── entities/          # 实体（标委会、协会）
│   ├── standards/         # 标准技术指标（按监管目录分类）
│   └── syntheses/         # 综合报告
```

---

## 资料源

| 文件 | 说明 |
|:----|:-----|
| [[wiki/sources/2026-06-20-national-standards-collection]] | 81份国家标准PDF资料集 |
| [[wiki/sources/2026-06-20-national-quality-supervision-catalog]] | 全国重点工业产品质量安全监管目录（2026年版） |

---

## 概念页（监管目录分类体系）

| 概念页 | 产品数 | 高等级 | 关联标准 |
|:------|:-----:|:-----:|:--------|
| [[wiki/concepts/家用电器及电器附件]] | 65 | 7 | — |
| [[wiki/concepts/家具及建筑装饰装修材料]] | 47 | 4 | PE管材 |
| [[wiki/concepts/电子及信息技术产品]] | 18 | 0 | — |
| [[wiki/concepts/交通用具及相关产品]] | 29 | 6 | LPG/LNG/甲醇燃料 |
| [[wiki/concepts/儿童用品]] | 27 | 10 | — |
| [[wiki/concepts/食品相关产品]] | 18 | 5 | — |
| [[wiki/concepts/服装鞋帽及家用纺织品]] | 9 | 2 | — |
| [[wiki/concepts/燃气器具及配件产品]] | 10 | 2 | LPG |
| [[wiki/concepts/老年人用品]] | 6 | 1 | — |
| [[wiki/concepts/日用杂品]] | 25 | 2 | — |
| [[wiki/concepts/文教体育用品]] | 6 | 1 | — |
| [[wiki/concepts/工业生产资料]] | 50 | 16 | 水泥/LPG/LNG/PE管材/电线电缆/化工原料 |
| [[wiki/concepts/农业生产资料]] | 19 | 11 | 肥料 |

## 原有概念页

| 概念页 | 说明 |
|:------|:-----|
| [[wiki/concepts/national-standards-gb]] | 国家标准体系 |
| [[wiki/concepts/肥料]] | 肥料分类与标准体系 |
| [[wiki/concepts/水泥]] | 水泥分类与标准体系 |
| [[wiki/concepts/聚乙烯（PE）管材]] | PE管材标准体系 |
| [[wiki/concepts/液化天然气（LNG）]] | LNG标准体系 |
| [[wiki/concepts/液化石油气（LPG）]] | LPG标准体系 |
| [[wiki/concepts/电线电缆试验方法]] | 电线电缆试验方法体系 |

---

## 实体页

| 实体页 | 说明 |
|:------|:-----|
| [[wiki/entities/SAC-TC105]] | 全国肥料和土壤调理剂标准化技术委员会 |
| [[wiki/entities/SAC-TC213]] | 全国液化天然气标准化技术委员会 |
| [[wiki/entities/CPCIF]] | 中国石油和化学工业联合会 |

---

## 标准技术指标页（按监管目录分类）

### 已有完整标准文件

| 标准页 | 监管类别 | 标准数 | 指标数 |
|:------|:--------:|:-----:|:-----:|
| [[wiki/standards/农业生产资料类标准技术指标]] | 农业生产资料 | 12 | 80 |
| [[wiki/standards/工业生产资料类标准技术指标]] | 工业生产资料 | 9 | 40 |
| [[wiki/standards/交通用具及相关产品类标准技术指标]] | 交通用具及相关产品 | 3 | 8 |

### 待补充标准的文件夹（89个子分类占位）

| 类别 | 文件夹 | 子分类数 |
|:----|:------|:-------:|
| [[wiki/standards/家用电器及电器附件/README|家用电器及电器附件]] | `standards/家用电器及电器附件/` | 8 |
| [[wiki/standards/家具及建筑装饰装修材料/README|家具及建筑装饰装修材料]] | `standards/家具及建筑装饰装修材料/` | 7 |
| [[wiki/standards/电子及信息技术产品/README|电子及信息技术产品]] | `standards/电子及信息技术产品/` | 6 |
| [[wiki/standards/交通用具及相关产品/README|交通用具及相关产品]] | `standards/交通用具及相关产品/` | 6 |
| [[wiki/standards/儿童用品/README|儿童用品]] | `standards/儿童用品/` | 6 |
| [[wiki/standards/食品相关产品/README|食品相关产品]] | `standards/食品相关产品/` | 6 |
| [[wiki/standards/服装鞋帽及家用纺织品/README|服装鞋帽及家用纺织品]] | `standards/服装鞋帽及家用纺织品/` | 6 |
| [[wiki/standards/燃气器具及配件产品/README|燃气器具及配件产品]] | `standards/燃气器具及配件产品/` | 6 |
| [[wiki/standards/老年人用品/README|老年人用品]] | `standards/老年人用品/` | 6 |
| [[wiki/standards/日用杂品/README|日用杂品]] | `standards/日用杂品/` | 7 |
| [[wiki/standards/文教体育用品/README|文教体育用品]] | `standards/文教体育用品/` | 6 |
| [[wiki/standards/工业生产资料/README|工业生产资料]] | `standards/工业生产资料/` | 10 |
| [[wiki/standards/农业生产资料/README|农业生产资料]] | `standards/农业生产资料/` | 9 |

---

## 综合报告

| 报告 | 说明 |
|:----|:-----|
| [[wiki/syntheses/2026-06-20-national-standards-comprehensive-report]] | 81份国家标准综合报告 |
| [[wiki/syntheses/2026-06-20-technical-indicators-knowledge-graph]] | 技术指标知识图谱综合报告 |

---

## 文件统计

| 类别 | 数量 |
|:----|:----:|
| 概念页 | 20（13个监管目录分类 + 7个原有概念） |
| 实体页 | 3 |
| 标准页 | 3（按监管目录分类） |
| 资料源 | 2 |
| 综合报告 | 2 |
| 索引页 | 3（index + VAULT-INDEX + log） |
| **总计** | **33个Wiki页面** |
