"""Create 12 product category concept pages based on 2026 supervision catalog"""
import json

with open('D:\\knowledge-vault\\raw\\data\\_监管目录分类.json', 'r', encoding='utf8') as f:
    cats = json.load(f)

# Category descriptions and standard associations
cat_info = {
    '家用电器及电器附件': {
        'desc': '家用和类似用途电器产品，涵盖制冷、烹饪、清洁、环境调节、个人护理等各类电器设备。',
        'standards': [],
        'related_concepts': ['wiki/concepts/national-standards-gb']
    },
    '家具及建筑装饰装修材料': {
        'desc': '家具产品及建筑装饰装修用材料，包括木家具、金属家具、灯具、涂料、管材、陶瓷等。',
        'standards': ['聚乙烯（PE）管材'],
        'related_concepts': ['wiki/concepts/聚乙烯（PE）管材', 'wiki/concepts/national-standards-gb']
    },
    '电子及信息技术产品': {
        'desc': '电子信息类产品，包括计算机、通信设备、音视频设备、电源适配器、储能电源等。',
        'standards': [],
        'related_concepts': ['wiki/concepts/national-standards-gb']
    },
    '交通用具及相关产品': {
        'desc': '道路交通相关产品，包括机动车及电动自行车零部件、头盔、充电设施、车用燃油及化学品等。',
        'standards': ['液化石油气（LPG）', '液化天然气（LNG）'],
        'related_concepts': ['wiki/concepts/液化石油气（LPG）', 'wiki/concepts/液化天然气（LNG）', 'wiki/concepts/national-standards-gb']
    },
    '儿童用品': {
        'desc': '专为儿童设计或使用的产品，涵盖家具、文具、玩具、服装、餐具、安全用品等。',
        'standards': [],
        'related_concepts': ['wiki/concepts/national-standards-gb']
    },
    '食品相关产品': {
        'desc': '与食品接触的材料和制品，包括塑料包装、纸包装、金属制品、玻璃制品、陶瓷制品、洗涤剂等。',
        'standards': [],
        'related_concepts': ['wiki/concepts/national-standards-gb']
    },
    '服装鞋帽及家用纺织品': {
        'desc': '服装、鞋类、帽类及家用纺织品类产品，包括床上用品、羽绒制品、皮鞋等。',
        'standards': [],
        'related_concepts': ['wiki/concepts/national-standards-gb']
    },
    '燃气器具及配件产品': {
        'desc': '燃气燃烧器具及配件产品，包括燃气灶、热水器、采暖炉、调压器、连接软管等。',
        'standards': ['液化石油气（LPG）'],
        'related_concepts': ['wiki/concepts/液化石油气（LPG）', 'wiki/concepts/national-standards-gb']
    },
    '老年人用品': {
        'desc': '专为老年人设计或使用的产品，包括淋浴辅助器、座便椅、老视成镜、康复辅助器具等。',
        'standards': [],
        'related_concepts': ['wiki/concepts/national-standards-gb']
    },
    '日用杂品': {
        'desc': '日常生活杂项用品，包括箱包、首饰、烟花爆竹、清洁剂、眼镜、防护用品等。',
        'standards': [],
        'related_concepts': ['wiki/concepts/national-standards-gb']
    },
    '文教体育用品': {
        'desc': '文化教育和体育用品，包括轮滑鞋、激光笔、电动滑板车、平衡车、运动鞋等。',
        'standards': [],
        'related_concepts': ['wiki/concepts/national-standards-gb']
    },
    '工业生产资料': {
        'desc': '工业生产用原材料、设备及安全防护产品，包括建材、钢材、水泥、危险化学品、消防产品、电线电缆、特种劳动防护用品等。',
        'standards': ['水泥', '液化石油气（LPG）', '液化天然气（LNG）', '聚乙烯（PE）管材', '电线电缆试验方法'],
        'related_concepts': ['wiki/concepts/水泥', 'wiki/concepts/液化石油气（LPG）', 'wiki/concepts/液化天然气（LNG）', 'wiki/concepts/聚乙烯（PE）管材', 'wiki/concepts/电线电缆试验方法', 'wiki/concepts/national-standards-gb']
    },
    '农业生产资料': {
        'desc': '农业生产用物资，包括农用薄膜、肥料、农药器械、耕整机械等。',
        'standards': ['肥料'],
        'related_concepts': ['wiki/concepts/肥料', 'wiki/concepts/national-standards-gb']
    }
}

for cat_name, items in cats.items():
    high_count = sum(1 for i in items if i['level'] == '高')
    xk_count = sum(1 for i in items if i['xk'] == '是')
    ccc_count = sum(1 for i in items if i['ccc'] == '是')
    
    info = cat_info.get(cat_name, {'desc': '', 'standards': [], 'related_concepts': ['wiki/concepts/national-standards-gb']})
    
    high_items = [i for i in items if i['level'] == '高']
    special_items = [i for i in items if i['special']]
    
    lines = []
    lines.append('---')
    lines.append(f'title: {cat_name}')
    lines.append('type: concept')
    lines.append('created: 2026-06-20')
    lines.append('updated: 2026-06-20')
    lines.append(f'tags: [监管目录, 产品质量, {cat_name}]')
    lines.append('source: [[wiki/sources/2026-06-20-national-quality-supervision-catalog]]')
    lines.append('---')
    lines.append('')
    lines.append(f'# {cat_name}')
    lines.append('')
    lines.append(f'> 来源：《全国重点工业产品质量安全监管目录（2026年版）》')
    lines.append(f'> 共 **{len(items)}种** 产品，其中高等级 **{high_count}种**，需生产许可证 **{xk_count}种**，需CCC认证 **{ccc_count}种**')
    lines.append('')
    lines.append('## 概述')
    lines.append('')
    lines.append(info['desc'])
    lines.append('')
    lines.append('## 产品列表')
    lines.append('')
    lines.append('| 序号 | 产品名称 | 生产许可证 | CCC认证 | 特殊监管需求 | 风险等级 |')
    lines.append('|:----:|----------|:--------:|:------:|:-----------:|:-------:|')
    
    for i in items:
        lines.append(f"| {i['seq']} | {i['name']} | {i['xk']} | {i['ccc']} | {i['special']} | {i['level']} |")
    
    if high_items:
        lines.append('')
        lines.append(f'## 高等级监管产品（{len(high_items)}种）')
        lines.append('')
        for i in high_items:
            extra = f"（{i['special']}）" if i['special'] else ''
            lines.append(f'- **{i["name"]}**{extra}')
    
    if special_items:
        lines.append('')
        lines.append('## 特殊监管需求')
        lines.append('')
        special_types = set()
        for i in special_items:
            for s in i['special'].replace('、', ',').split(','):
                s = s.strip()
                if s:
                    special_types.add(s)
        for s in sorted(special_types):
            count = sum(1 for i in special_items if s in i['special'])
            lines.append(f'- **{s}**：涉及{count}种产品')
    
    if info['standards']:
        lines.append('')
        lines.append('## 关联标准')
        lines.append('')
        for std in info['standards']:
            lines.append(f'- [[wiki/standards/{cat_name}类标准技术指标|{std}相关标准]]')
    
    lines.append('')
    lines.append('## 相关概念')
    for rc in info['related_concepts']:
        lines.append(f'- [[{rc}]]')
    lines.append('- [[wiki/sources/2026-06-20-national-quality-supervision-catalog]]')
    
    content = '\n'.join(lines)
    
    filepath = f'D:\\knowledge-vault\\wiki\\concepts\\{cat_name}.md'
    with open(filepath, 'w', encoding='utf8') as f:
        f.write(content)
    print(f'Created: {cat_name}.md ({len(items)} products)')

print('\nAll concept pages created!')
