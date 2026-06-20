"""Create folder structure for all 13 supervision catalog categories"""
import os

# 13个监管目录类别 + 对应的子分类
categories = {
    '家用电器及电器附件': {
        'subcategories': ['电冰箱', '空调器', '洗衣机', '电风扇', '电热水器', '厨房电器', '个人护理电器', '其他家用电器'],
        'has_standards': False
    },
    '家具及建筑装饰装修材料': {
        'subcategories': ['家具', '人造板', '涂料', '管材', '陶瓷砖', '灯具', '其他建材'],
        'has_standards': False
    },
    '电子及信息技术产品': {
        'subcategories': ['计算机', '通信设备', '音视频设备', '电源适配器', '移动电源', '其他电子产品'],
        'has_standards': False
    },
    '交通用具及相关产品': {
        'subcategories': ['电动自行车', '摩托车头盔', '车用燃油', '车用尿素', '充电设施', '其他交通用具'],
        'has_standards': True  # 已有LPG/LNG/甲醇燃料标准
    },
    '儿童用品': {
        'subcategories': ['玩具', '童车', '儿童服装', '学生用品', '儿童安全防护', '其他儿童用品'],
        'has_standards': False
    },
    '食品相关产品': {
        'subcategories': ['塑料包装', '纸包装', '金属包装', '玻璃包装', '食品用洗涤剂', '其他食品相关产品'],
        'has_standards': False
    },
    '服装鞋帽及家用纺织品': {
        'subcategories': ['服装', '鞋类', '帽类', '床上用品', '羽绒制品', '其他纺织品'],
        'has_standards': False
    },
    '燃气器具及配件产品': {
        'subcategories': ['燃气灶', '燃气热水器', '燃气采暖炉', '燃气调压器', '燃气软管', '可燃气体探测器'],
        'has_standards': False
    },
    '老年人用品': {
        'subcategories': ['康复辅助器具', '老视成镜', '淋浴辅助器', '座便椅', '水暖毯', '其他老年人用品'],
        'has_standards': False
    },
    '日用杂品': {
        'subcategories': ['箱包', '首饰', '眼镜', '清洁剂', '烟花爆竹', '晴雨伞', '其他日用杂品'],
        'has_standards': False
    },
    '文教体育用品': {
        'subcategories': ['轮滑鞋', '电动滑板车', '平衡车', '运动鞋', '激光笔', '其他文教体育用品'],
        'has_standards': False
    },
    '工业生产资料': {
        'subcategories': ['水泥', '钢材', '危险化学品', '消防产品', '电线电缆', '防爆电器', '特种劳动防护用品', '液化石油气', '天然气', '其他工业生产资料'],
        'has_standards': True  # 已有水泥/LPG/LNG/PE管材/化工原料标准
    },
    '农业生产资料': {
        'subcategories': ['氮肥', '磷肥', '钾肥', '复合肥', '有机肥', '农用薄膜', '植物保护机械', '耕整机械', '其他农业生产资料'],
        'has_standards': True  # 已有肥料标准
    }
}

base = 'D:\\knowledge-vault\\wiki\\standards'

for cat, info in categories.items():
    # Create category directory
    cat_dir = os.path.join(base, cat)
    os.makedirs(cat_dir, exist_ok=True)
    
    # Create subcategory placeholder files
    for sub in info['subcategories']:
        sub_file = os.path.join(cat_dir, f'{sub}.md')
        if not os.path.exists(sub_file):
            content = f'''---
title: {cat} — {sub}
type: standard-category
category: {cat}
subcategory: {sub}
status: placeholder
created: 2026-06-20
tags: [监管目录, {cat}, {sub}]
---

# {cat} — {sub}

> 所属监管目录：[[wiki/concepts/{cat}]]

## 待补充标准

> ⏳ 标准文件尚未下载，待补充

| 标准编号 | 标准名称 | 技术指标 | 指标值 | 备注 |
|:--------|:---------|:--------|:------|:----|
| — | — | — | — | 待补充 |

---

## 相关链接
- [[wiki/concepts/{cat}|{cat}（监管目录）]]
- [[wiki/sources/2026-06-20-national-quality-supervision-catalog|监管目录原文]]
'''
            with open(sub_file, 'w', encoding='utf8') as f:
                f.write(content)
            print(f'  Created: {cat}/{sub}.md')
    
    # Create/update category index file
    cat_index = os.path.join(cat_dir, 'README.md')
    sub_links = '\n'.join([f'- [[wiki/standards/{cat}/{s}|{s}]]' for s in info['subcategories']])
    
    # Count existing standards
    existing_links = ''
    if info['has_standards']:
        # Find which standard file covers this category
        if cat == '农业生产资料':
            existing_links = '\n### 已有标准\n- [[wiki/standards/农业生产资料类标准技术指标|农业生产资料类标准技术指标（12份/80项指标）]]\n'
        elif cat == '工业生产资料':
            existing_links = '\n### 已有标准\n- [[wiki/standards/工业生产资料类标准技术指标|工业生产资料类标准技术指标（9份/40项指标）]]\n'
        elif cat == '交通用具及相关产品':
            existing_links = '\n### 已有标准\n- [[wiki/standards/交通用具及相关产品类标准技术指标|交通用具及相关产品类标准技术指标（3份/8项指标）]]\n'
    
    content = f'''---
title: {cat} — 标准目录
type: standard-index
category: {cat}
status: placeholder
created: 2026-06-20
tags: [监管目录, {cat}]
---

# {cat} — 标准目录

> 所属监管目录：[[wiki/concepts/{cat}]]
> 本目录下共 **{len(info['subcategories'])}个** 子分类

## 子分类
{existing_links}
{sub_links}

---

## 相关链接
- [[wiki/concepts/{cat}|{cat}（监管目录）]]
- [[wiki/sources/2026-06-20-national-quality-supervision-catalog|监管目录原文]]
'''
    with open(cat_index, 'w', encoding='utf8') as f:
        f.write(content)
    print(f'Created index: {cat}/README.md')

print('\n✅ 所有文件夹结构已创建完成！')
print(f'共 {len(categories)} 个类别目录，{sum(len(v["subcategories"]) for v in categories.values())} 个子分类占位文件')
