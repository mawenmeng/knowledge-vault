"""Rewrite standard category pages using 2026 supervision catalog classification"""
import json

# ============================================================
# Complete indicator data for all standards
# Format: std_no -> {name, indicators: [{name, constraint, value, unit}]}
# ============================================================

standards_data = {
    # ========== 农业生产资料 - 肥料类 ==========
    'GB/T 2440-2017': {
        'name': '尿素',
        'category': '农业生产资料',
        'sub_category': '肥料',
        'indicators': [
            {'name': '总氮(N)的质量分数（农业用优等品）', 'constraint': '≥', 'value': '46.0', 'unit': '%'},
            {'name': '总氮(N)的质量分数（农业用合格品）', 'constraint': '≥', 'value': '45.0', 'unit': '%'},
            {'name': '缩二脲的质量分数（农业用优等品）', 'constraint': '≤', 'value': '0.9', 'unit': '%'},
            {'name': '缩二脲的质量分数（农业用合格品）', 'constraint': '≤', 'value': '1.5', 'unit': '%'},
            {'name': '水分（农业用优等品）', 'constraint': '≤', 'value': '0.5', 'unit': '%'},
            {'name': '水分（农业用合格品）', 'constraint': '≤', 'value': '1.0', 'unit': '%'},
            {'name': '粒度0.85mm~2.80mm（农业用优等品）', 'constraint': '≥', 'value': '93', 'unit': '%'},
            {'name': '粒度0.85mm~2.80mm（农业用合格品）', 'constraint': '≥', 'value': '90', 'unit': '%'},
            {'name': '总氮(N)的质量分数（工业用优等品）', 'constraint': '≥', 'value': '46.4', 'unit': '%'},
            {'name': '总氮(N)的质量分数（工业用合格品）', 'constraint': '≥', 'value': '46.0', 'unit': '%'},
            {'name': '缩二脲的质量分数（工业用优等品）', 'constraint': '≤', 'value': '0.5', 'unit': '%'},
            {'name': '缩二脲的质量分数（工业用合格品）', 'constraint': '≤', 'value': '1.0', 'unit': '%'},
            {'name': '水分（工业用优等品）', 'constraint': '≤', 'value': '0.3', 'unit': '%'},
            {'name': '水分（工业用合格品）', 'constraint': '≤', 'value': '0.7', 'unit': '%'},
            {'name': '铁(Fe)的质量分数（工业用优等品）', 'constraint': '≤', 'value': '0.0005', 'unit': '%'},
            {'name': '铁(Fe)的质量分数（工业用合格品）', 'constraint': '≤', 'value': '0.0010', 'unit': '%'},
            {'name': '碱度(以NH₃计)（工业用优等品）', 'constraint': '≤', 'value': '0.01', 'unit': '%'},
            {'name': '碱度(以NH₃计)（工业用合格品）', 'constraint': '≤', 'value': '0.03', 'unit': '%'},
            {'name': '硫酸盐(以SO₄计)（工业用优等品）', 'constraint': '≤', 'value': '0.005', 'unit': '%'},
            {'name': '硫酸盐(以SO₄计)（工业用合格品）', 'constraint': '≤', 'value': '0.020', 'unit': '%'},
            {'name': '水不溶物（工业用优等品）', 'constraint': '≤', 'value': '0.005', 'unit': '%'},
            {'name': '水不溶物（工业用合格品）', 'constraint': '≤', 'value': '0.040', 'unit': '%'},
        ]
    },
    'GB/T 15063-2020': {
        'name': '复合肥料',
        'category': '农业生产资料',
        'sub_category': '肥料',
        'indicators': [
            {'name': '总养分(N+P₂O₅+K₂O)（高浓度）', 'constraint': '≥', 'value': '25.0', 'unit': '%'},
            {'name': '总养分(N+P₂O₅+K₂O)（中浓度）', 'constraint': '≥', 'value': '20.0', 'unit': '%'},
            {'name': '总养分(N+P₂O₅+K₂O)（低浓度）', 'constraint': '≥', 'value': '15.0', 'unit': '%'},
            {'name': '水溶性磷占有效磷百分率', 'constraint': '≥', 'value': '60', 'unit': '%'},
            {'name': '水分(H₂O)', 'constraint': '≤', 'value': '2.0', 'unit': '%'},
        ]
    },
    'GB/T 2945-2017': {
        'name': '硝酸铵',
        'category': '农业生产资料',
        'sub_category': '肥料',
        'indicators': [
            {'name': '硝酸铵含量（优等品）', 'constraint': '≥', 'value': '99.5', 'unit': '%'},
            {'name': '硝酸铵含量（合格品）', 'constraint': '≥', 'value': '99.0', 'unit': '%'},
            {'name': '总氮(以干基计)（优等品）', 'constraint': '≥', 'value': '34.5', 'unit': '%'},
            {'name': '总氮(以干基计)（合格品）', 'constraint': '≥', 'value': '34.0', 'unit': '%'},
            {'name': '水分（优等品）', 'constraint': '≤', 'value': '0.3', 'unit': '%'},
            {'name': '水分（合格品）', 'constraint': '≤', 'value': '0.5', 'unit': '%'},
            {'name': '10%水溶液pH值', 'constraint': '≥', 'value': '5.0', 'unit': ''},
        ]
    },
    'GB/T 535-2020': {
        'name': '肥料级硫酸铵',
        'category': '农业生产资料',
        'sub_category': '肥料',
        'indicators': [
            {'name': '氮(N)含量', 'constraint': '≥', 'value': '20.5', 'unit': '%'},
            {'name': '水分(H₂O)', 'constraint': '≤', 'value': '1.0', 'unit': '%'},
            {'name': '游离酸(H₂SO₄)', 'constraint': '≤', 'value': '0.2', 'unit': '%'},
        ]
    },
    'GB/T 20406-2017': {
        'name': '农业用硫酸钾',
        'category': '农业生产资料',
        'sub_category': '肥料',
        'indicators': [
            {'name': '氧化钾(K₂O)（优等品）', 'constraint': '≥', 'value': '50.0', 'unit': '%'},
            {'name': '氧化钾(K₂O)（合格品）', 'constraint': '≥', 'value': '45.0', 'unit': '%'},
            {'name': '氯离子(Cl⁻)（优等品）', 'constraint': '≤', 'value': '1.0', 'unit': '%'},
            {'name': '氯离子(Cl⁻)（合格品）', 'constraint': '≤', 'value': '2.0', 'unit': '%'},
            {'name': '水分(H₂O)（优等品）', 'constraint': '≤', 'value': '1.0', 'unit': '%'},
            {'name': '水分(H₂O)（合格品）', 'constraint': '≤', 'value': '1.5', 'unit': '%'},
            {'name': '游离酸(H₂SO₄)（优等品）', 'constraint': '≤', 'value': '1.5', 'unit': '%'},
            {'name': '游离酸(H₂SO₄)（合格品）', 'constraint': '≤', 'value': '2.0', 'unit': '%'},
        ]
    },
    'GB 10205-2009': {
        'name': '磷酸一铵、磷酸二铵',
        'category': '农业生产资料',
        'sub_category': '肥料',
        'indicators': [
            {'name': '总养分(N+P₂O₅)（优等品）', 'constraint': '≥', 'value': '64.0', 'unit': '%'},
            {'name': '总养分(N+P₂O₅)（合格品）', 'constraint': '≥', 'value': '57.0', 'unit': '%'},
            {'name': '总氮(N)（优等品）', 'constraint': '≥', 'value': '11.0', 'unit': '%'},
            {'name': '总氮(N)（合格品）', 'constraint': '≥', 'value': '10.0', 'unit': '%'},
            {'name': '有效磷(P₂O₅)（优等品）', 'constraint': '≥', 'value': '46.0', 'unit': '%'},
            {'name': '有效磷(P₂O₅)（合格品）', 'constraint': '≥', 'value': '42.0', 'unit': '%'},
            {'name': '水分(H₂O)（优等品）', 'constraint': '≤', 'value': '2.0', 'unit': '%'},
            {'name': '水分(H₂O)（合格品）', 'constraint': '≤', 'value': '2.5', 'unit': '%'},
        ]
    },
    'GB/T 20784-2018': {
        'name': '农业用硝酸钾',
        'category': '农业生产资料',
        'sub_category': '肥料',
        'indicators': [
            {'name': '氧化钾(K₂O)（优等品）', 'constraint': '≥', 'value': '46.0', 'unit': '%'},
            {'name': '氧化钾(K₂O)（合格品）', 'constraint': '≥', 'value': '44.0', 'unit': '%'},
            {'name': '总氮(N)（优等品）', 'constraint': '≥', 'value': '13.5', 'unit': '%'},
            {'name': '总氮(N)（合格品）', 'constraint': '≥', 'value': '13.0', 'unit': '%'},
            {'name': '氯离子(Cl⁻)（优等品）', 'constraint': '≤', 'value': '0.2', 'unit': '%'},
            {'name': '氯离子(Cl⁻)（合格品）', 'constraint': '≤', 'value': '0.5', 'unit': '%'},
            {'name': '水分(H₂O)（优等品）', 'constraint': '≤', 'value': '0.5', 'unit': '%'},
            {'name': '水分(H₂O)（合格品）', 'constraint': '≤', 'value': '1.0', 'unit': '%'},
        ]
    },
    'GB/T 37918-2019': {
        'name': '肥料级氯化钾',
        'category': '农业生产资料',
        'sub_category': '肥料',
        'indicators': [
            {'name': '氧化钾(K₂O)（优等品）', 'constraint': '≥', 'value': '60.0', 'unit': '%'},
            {'name': '氧化钾(K₂O)（合格品）', 'constraint': '≥', 'value': '55.0', 'unit': '%'},
            {'name': '水分(H₂O)（优等品）', 'constraint': '≤', 'value': '1.0', 'unit': '%'},
            {'name': '水分(H₂O)（合格品）', 'constraint': '≤', 'value': '2.0', 'unit': '%'},
        ]
    },
    'GB/T 2946-2018': {
        'name': '氯化铵',
        'category': '农业生产资料',
        'sub_category': '肥料',
        'indicators': [
            {'name': '氮(N)(以干基计)（优等品）', 'constraint': '≥', 'value': '25.4', 'unit': '%'},
            {'name': '氮(N)(以干基计)（一等品）', 'constraint': '≥', 'value': '25.0', 'unit': '%'},
            {'name': '氮(N)(以干基计)（合格品）', 'constraint': '≥', 'value': '23.5', 'unit': '%'},
            {'name': '水分(H₂O)（优等品）', 'constraint': '≤', 'value': '0.5', 'unit': '%'},
            {'name': '水分(H₂O)（一等品）', 'constraint': '≤', 'value': '0.7', 'unit': '%'},
            {'name': '水分(H₂O)（合格品）', 'constraint': '≤', 'value': '1.0', 'unit': '%'},
        ]
    },
    'GB 3559-2001': {
        'name': '农业用碳酸氢铵',
        'category': '农业生产资料',
        'sub_category': '肥料',
        'indicators': [
            {'name': '氮(N)含量（优等品）', 'constraint': '≥', 'value': '17.2', 'unit': '%'},
            {'name': '氮(N)含量（合格品）', 'constraint': '≥', 'value': '16.8', 'unit': '%'},
            {'name': '水分(H₂O)（优等品）', 'constraint': '≤', 'value': '3.0', 'unit': '%'},
            {'name': '水分(H₂O)（合格品）', 'constraint': '≤', 'value': '3.5', 'unit': '%'},
        ]
    },
    'GB/T 10510-2023': {
        'name': '硝酸磷肥、硝酸磷钾肥',
        'category': '农业生产资料',
        'sub_category': '肥料',
        'indicators': [
            {'name': '总养分(N+P₂O₅+K₂O)', 'constraint': '≥', 'value': '30.0', 'unit': '%'},
            {'name': '水分(H₂O)', 'constraint': '≤', 'value': '1.5', 'unit': '%'},
        ]
    },
    'GB/T 20412-2021': {
        'name': '钙镁磷肥',
        'category': '农业生产资料',
        'sub_category': '肥料',
        'indicators': [
            {'name': '有效五氧化二磷(P₂O₅)', 'constraint': '≥', 'value': '15.0', 'unit': '%'},
            {'name': '水分(H₂O)', 'constraint': '≤', 'value': '0.5', 'unit': '%'},
            {'name': '细度(通过0.25mm试验筛)', 'constraint': '≥', 'value': '80', 'unit': '%'},
        ]
    },
    # ========== 工业生产资料 - 水泥类 ==========
    'GB 175-2023': {
        'name': '通用硅酸盐水泥',
        'category': '工业生产资料',
        'sub_category': '水泥',
        'indicators': [
            {'name': '3d抗压强度(P·O 42.5)', 'constraint': '≥', 'value': '17.0', 'unit': 'MPa'},
            {'name': '3d抗压强度(P·O 52.5)', 'constraint': '≥', 'value': '23.0', 'unit': 'MPa'},
            {'name': '28d抗压强度(P·O 42.5)', 'constraint': '≥', 'value': '42.5', 'unit': 'MPa'},
            {'name': '28d抗压强度(P·O 52.5)', 'constraint': '≥', 'value': '52.5', 'unit': 'MPa'},
            {'name': '初凝时间', 'constraint': '≥', 'value': '45', 'unit': 'min'},
            {'name': '终凝时间', 'constraint': '≤', 'value': '600', 'unit': 'min'},
            {'name': '氧化镁(MgO)', 'constraint': '≤', 'value': '5.0', 'unit': '%'},
            {'name': '三氧化硫(SO₃)', 'constraint': '≤', 'value': '3.5', 'unit': '%'},
            {'name': '氯离子(Cl⁻)', 'constraint': '≤', 'value': '0.06', 'unit': '%'},
        ]
    },
    'GB/T 748-2023': {
        'name': '抗硫酸盐硅酸盐水泥',
        'category': '工业生产资料',
        'sub_category': '水泥',
        'indicators': [
            {'name': 'C₃A含量（中抗硫酸盐）', 'constraint': '≤', 'value': '5.0', 'unit': '%'},
            {'name': 'C₃A含量（高抗硫酸盐）', 'constraint': '≤', 'value': '3.0', 'unit': '%'},
            {'name': 'C₃S含量（高抗硫酸盐）', 'constraint': '≤', 'value': '50.0', 'unit': '%'},
            {'name': '14d线膨胀率', 'constraint': '≤', 'value': '0.060', 'unit': '%'},
            {'name': '抗硫酸盐侵蚀系数(K)', 'constraint': '≥', 'value': '0.80', 'unit': ''},
        ]
    },
    # ========== 工业生产资料 + 交通用具 - 燃气与能源类 ==========
    'GB 11174-2025': {
        'name': '液化石油气',
        'category': '工业生产资料',
        'sub_category': '液化石油气（LPG）',
        'indicators': [
            {'name': '蒸气压(37.8℃)', 'constraint': '≤', 'value': '1380', 'unit': 'kPa'},
            {'name': 'C₅及C₅以上组分含量', 'constraint': '≤', 'value': '3.0', 'unit': '%(体积分数)'},
            {'name': '总硫含量', 'constraint': '≤', 'value': '343', 'unit': 'mg/m³'},
            {'name': '硫化氢', 'constraint': '≤', 'value': '10', 'unit': 'mg/m³'},
            {'name': '游离水', 'constraint': '=', 'value': '无', 'unit': ''},
        ]
    },
    'GB 5842-2023': {
        'name': '液化石油气钢瓶',
        'category': '工业生产资料',
        'sub_category': '液化石油气（LPG）',
        'indicators': [
            {'name': '水压试验压力', 'constraint': '=', 'value': '2.4', 'unit': 'MPa'},
            {'name': '气密性试验压力', 'constraint': '=', 'value': '1.6', 'unit': 'MPa'},
        ]
    },
    'GB/T 34510-2017': {
        'name': '汽车用液化天然气气瓶',
        'category': '交通用具及相关产品',
        'sub_category': '液化天然气（LNG）',
        'indicators': [
            {'name': '设计压力', 'constraint': '=', 'value': '1.59', 'unit': 'MPa'},
            {'name': '最高工作压力', 'constraint': '=', 'value': '1.59', 'unit': 'MPa'},
            {'name': '水压试验压力', 'constraint': '=', 'value': '3.2', 'unit': 'MPa'},
        ]
    },
    'GB/T 23799-2021': {
        'name': '车用甲醇汽油(M85)',
        'category': '交通用具及相关产品',
        'sub_category': '交通用具',
        'indicators': [
            {'name': '甲醇含量', 'constraint': '=', 'value': '84~86', 'unit': '%(体积分数)'},
            {'name': '实际胶质', 'constraint': '≤', 'value': '5', 'unit': 'mg/100mL'},
        ]
    },
    'GB/T 33445-2023': {
        'name': '煤制合成天然气',
        'category': '工业生产资料',
        'sub_category': '液化天然气（LNG）',
        'indicators': [
            {'name': '高位发热量', 'constraint': '≥', 'value': '34.0', 'unit': 'MJ/m³'},
            {'name': '总硫(以硫计)', 'constraint': '≤', 'value': '1.0', 'unit': 'mg/m³'},
            {'name': '硫化氢', 'constraint': '≤', 'value': '0.1', 'unit': 'mg/m³'},
        ]
    },
    'GB/T 42416-2023': {
        'name': 'M100车用甲醇燃料',
        'category': '交通用具及相关产品',
        'sub_category': '交通用具',
        'indicators': [
            {'name': '甲醇含量', 'constraint': '≥', 'value': '99.5', 'unit': '%'},
            {'name': '硫含量', 'constraint': '≤', 'value': '1.0', 'unit': 'mg/kg'},
            {'name': '实际胶质', 'constraint': '≤', 'value': '2.0', 'unit': 'mg/100mL'},
        ]
    },
    # ========== 工业生产资料 - 化工原料类 ==========
    'GB/T 320-2025': {
        'name': '工业用合成盐酸',
        'category': '工业生产资料',
        'sub_category': '化工原料',
        'indicators': [
            {'name': '总酸度(以HCl计)（优等品）', 'constraint': '≥', 'value': '31.0', 'unit': '%'},
            {'name': '总酸度(以HCl计)（合格品）', 'constraint': '≥', 'value': '31.0', 'unit': '%'},
            {'name': '铁(以Fe计)（优等品）', 'constraint': '≤', 'value': '0.002', 'unit': '%'},
            {'name': '铁(以Fe计)（合格品）', 'constraint': '≤', 'value': '0.008', 'unit': '%'},
            {'name': '灼烧残渣（优等品）', 'constraint': '≤', 'value': '0.005', 'unit': '%'},
            {'name': '灼烧残渣（合格品）', 'constraint': '≤', 'value': '0.010', 'unit': '%'},
            {'name': '游离氯(以Cl计)（优等品）', 'constraint': '≤', 'value': '0.002', 'unit': '%'},
            {'name': '游离氯(以Cl计)（合格品）', 'constraint': '≤', 'value': '0.005', 'unit': '%'},
        ]
    },
    'GB/T 5138-2021': {
        'name': '工业用液氯',
        'category': '工业生产资料',
        'sub_category': '化工原料',
        'indicators': [
            {'name': '氯含量(体积分数)（优等品）', 'constraint': '≥', 'value': '99.8', 'unit': '%'},
            {'name': '氯含量(体积分数)（合格品）', 'constraint': '≥', 'value': '99.6', 'unit': '%'},
            {'name': '水分含量（优等品）', 'constraint': '≤', 'value': '0.01', 'unit': '%'},
            {'name': '水分含量（合格品）', 'constraint': '≤', 'value': '0.03', 'unit': '%'},
        ]
    },
    'GB 19106-2013': {
        'name': '次氯酸钠',
        'category': '工业生产资料',
        'sub_category': '化工原料',
        'indicators': [
            {'name': '有效氯(以Cl计)', 'constraint': '≥', 'value': '10.0', 'unit': '%'},
            {'name': '游离碱(以NaOH计)', 'constraint': '=', 'value': '0.1~1.0', 'unit': '%'},
        ]
    },
    'GB/T 338-2025': {
        'name': '工业用甲醇',
        'category': '工业生产资料',
        'sub_category': '化工原料',
        'indicators': [
            {'name': '甲醇纯度（优等品）', 'constraint': '≥', 'value': '99.9', 'unit': '%'},
            {'name': '甲醇纯度（合格品）', 'constraint': '≥', 'value': '99.5', 'unit': '%'},
        ]
    },
}

# ============================================================
# Organize by catalog category
# ============================================================
from collections import OrderedDict

category_standards = OrderedDict()
for std_no, data in standards_data.items():
    cat = data['category']
    if cat not in category_standards:
        category_standards[cat] = OrderedDict()
    sub = data['sub_category']
    if sub not in category_standards[cat]:
        category_standards[cat][sub] = []
    category_standards[cat][sub].append((std_no, data))

# ============================================================
# Generate pages
# ============================================================

# Concept page mapping
concept_map = {
    '肥料': 'wiki/concepts/肥料',
    '水泥': 'wiki/concepts/水泥',
    '液化石油气（LPG）': 'wiki/concepts/液化石油气（LPG）',
    '液化天然气（LNG）': 'wiki/concepts/液化天然气（LNG）',
    '化工原料': 'wiki/concepts/national-standards-gb',
    '交通用具': 'wiki/concepts/交通用具及相关产品',
}

catalog_concept_map = {
    '农业生产资料': 'wiki/concepts/农业生产资料',
    '工业生产资料': 'wiki/concepts/工业生产资料',
    '交通用具及相关产品': 'wiki/concepts/交通用具及相关产品',
}

for cat, sub_groups in category_standards.items():
    # Count
    total_standards = sum(len(items) for items in sub_groups.values())
    total_indicators = sum(len(d['indicators']) for items in sub_groups.values() for _, d in items)
    
    lines = []
    lines.append('---')
    lines.append(f'title: {cat}类标准技术指标')
    lines.append('type: standard-category')
    lines.append(f'category: {cat}')
    lines.append('---')
    lines.append('')
    lines.append(f'# {cat}类标准技术指标')
    lines.append('')
    lines.append(f'> 所属监管目录：[[{catalog_concept_map[cat]}]]')
    lines.append(f'> 共 **{total_standards}份** 标准，**{total_indicators}项** 技术指标')
    lines.append('')
    
    for sub, items in sub_groups.items():
        concept_link = concept_map.get(sub, 'wiki/concepts/national-standards-gb')
        lines.append(f'## {sub}')
        lines.append('')
        lines.append(f'> 相关概念：[[{concept_link}]]')
        lines.append('')
        
        for std_no, data in items:
            lines.append(f'### {std_no} {data["name"]}')
            lines.append('')
            lines.append(f'**监管分类**：{cat} → {sub}')
            lines.append('')
            lines.append('| 技术指标名称 | 约束 | 指标值 | 单位 |')
            lines.append('|:-----------|:---:|:-----:|:----:|')
            for ind in data['indicators']:
                lines.append(f"| {ind['name']} | {ind['constraint']} | {ind['value']} | {ind['unit']} |")
            lines.append('')
    
    # Cross-reference to catalog
    lines.append('---')
    lines.append('')
    lines.append('## 关联监管目录')
    lines.append(f'- [[wiki/concepts/{cat}]]（监管目录分类）')
    lines.append(f'- [[wiki/sources/2026-06-20-national-quality-supervision-catalog]]（监管目录原文）')
    
    content = '\n'.join(lines)
    
    filepath = f'D:\\knowledge-vault\\wiki\\standards\\{cat}类标准技术指标.md'
    with open(filepath, 'w', encoding='utf8') as f:
        f.write(content)
    print(f'Created: {cat}类标准技术指标.md ({total_standards} standards, {total_indicators} indicators)')

print('\nAll standard pages rewritten!')
