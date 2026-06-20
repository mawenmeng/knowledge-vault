# ingest-wiki.md — 资料摄入操作手册

## 触发条件

用户说："保存到知识库"、"摄入"、"ingest"、"add to knowledge base"、"save to wiki"，或发送文件/内容并提到知识库。

## 操作流程

### Step 1: 归档原始资料
1. 判断资料类型（article / paper / repo / transcript / data）
2. 将原始内容保存到 `raw/` 对应子目录
3. 文件命名：`YYYY-MM-DD-简短描述.md`
4. 如果资料包含图片，提示用户下载到 `raw/assets/`

### Step 2: 阅读并提取
1. 完整阅读原始资料
2. 与用户讨论关键要点
3. 确认用户希望强调的方向

### Step 3: 创建/更新 Wiki 页面

**必须执行的操作：**

1. **创建摘要页** → `wiki/sources/` — 资料摘要、3-5 个关键要点
2. **创建/更新概念页** → `wiki/concepts/` — 资料中涉及的核心概念
3. **创建/更新实体页** → `wiki/entities/` — 资料中的人物/公司/产品
4. **如果需要，创建对比页** → `wiki/comparisons/` — 当资料与已有知识形成对比时
5. **更新 index.md** — 添加新页面到目录
6. **更新 log.md** — 追加操作记录

**对比页触发条件：** 当新资料与已有知识在某个维度上形成对比（如方法 A vs 方法 B，不同观点，不同时期的数据等）

### Step 4: 提交
```bash
git add -A
git commit -m "[Ingest] 资料标题"
git push
```

### 一次摄入的影响范围
单个资料通常涉及 5-15 个 Wiki 页面。每次更新一个页面时，检查并更新所有相关的交叉引用。

## 注意事项
- 不要修改 raw/ 下的原始文件
- 保持 YAML frontmatter 格式一致
- 使用 `[[wiki/page]]` 格式的 Wiki 链接
- 如果发现与已有知识矛盾，在相关页面标注 `[!contradiction]`
