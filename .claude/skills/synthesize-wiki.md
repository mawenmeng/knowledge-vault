# synthesize-wiki.md — 综合报告操作手册

## 触发条件

用户说："写一篇关于 X 的综述"、"综合报告"、"synthesize"、"pull together everything about X" 等。

## 操作流程

### Step 1: 扫描相关页面
1. 读取 `wiki/index.md` 确定相关页面范围
2. 读取所有相关的 Wiki 页面（sources, concepts, entities, comparisons）
3. 跟踪交叉引用，确保覆盖全面

### Step 2: 综合分析
1. 识别多源共识 vs 单一来源观点
2. 标注矛盾点 `[!contradiction]`
3. 发现知识空白（Wiki 中缺失但应该有的内容）
4. 形成结构化的综合报告

### Step 3: 撰写报告
1. 保存到 `wiki/syntheses/YYYY-MM-DD-主题.md`
2. 报告结构：
   - 概述
   - 各维度分析
   - 共识与分歧
   - 知识空白与建议
   - 参考文献（指向具体的 Wiki 页面）

### Step 4: 提交
```bash
git add -A
git commit -m "[Synthesize] 主题名称"
git push
```

## 注意事项
- 综合报告不是简单拼接，而是真正的跨源综合
- 明确标注哪些结论有多个来源支持，哪些是单一来源
- 知识空白是重要的输出 — 建议用户补充哪些资料
