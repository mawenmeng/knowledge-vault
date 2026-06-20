# query-wiki.md — 知识库查询操作手册

## 触发条件

用户说："知识库里"、"查一下"、"wiki 里"、"according to the knowledge base"、"what does the knowledge base say" 等。

## 操作流程

### Step 1: 定位相关页面
1. 先读取 `wiki/index.md` — 了解知识库全貌
2. 根据用户问题，确定可能相关的页面
3. 读取 `wiki/hot.md` — 了解近期会话上下文

### Step 2: 深入阅读
1. 逐个读取相关的 Wiki 页面
2. 跟踪页面中的交叉引用链接
3. 如果发现矛盾，标注 `[!contradiction]`

### Step 3: 综合回答
1. 基于多个页面信息综合回答
2. 附带来源引用（指向具体的 Wiki 页面）
3. 如果知识不足，明确告知并建议补充来源

### Step 4: 归档有价值的回答（可选）
如果回答本身具有长期价值（如对比分析、发现关联等）：
1. 将回答保存到 `wiki/syntheses/`
2. 更新 `wiki/index.md`
3. 更新 `wiki/log.md`
4. Git commit & push

## 回答格式
- 普通问题：文字回答 + 引用来源
- 对比类问题：表格形式
- 复杂问题：结构化 Markdown 报告

## 注意事项
- 优先使用 Wiki 内容，不要依赖训练数据中的知识
- 如果 Wiki 信息不足，建议用户补充资料
- 好的问答结果可以归档，让知识复利增长
