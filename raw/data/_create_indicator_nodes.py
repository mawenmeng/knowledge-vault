"""Create indicator nodes for Obsidian knowledge graph visualization"""
import os
import re

# ============================================================
# All standards data with indicators
# ============================================================

standards_data = {
    # ========== 农业生产资料 - 肥料类 ==========
    'GB/T 2440-2017': {
        'name': '尿素',
        'category': '农业生产资料',
        'sub_category': '氮肥',
        'indicators': [
            {'name': '总氮(N)的质量分数（农业用优等品）', 'constraint': '≥', 'value': '46.0', 'unit': '%'},
            {'name': '总氮(N)的质量分数（农业用合格品）', 'constraint': '≥', 'value': '45.0', 'unit': '%'},
            {'name': '缩二脲的质量分数（农业用优等品）', 'constraint': '≤', 'value': '0.9', 'unit': '%'},
            {'name': '缩二脲的质量分数（农业用合格品）', 'constraint': '≤', 'value': '1.5', 'unit': '%'},
            {'name': '水分（农业用优等品）', 'constraint': '≤', 'value': '0.5', 'unit': '%'},
            {'name': '水分（农业用合格品）', 'constraint': '≤', 'value': '1.0', 'unit': '%'},
            {'name': '粒度0.85mm~2.80mm（农业用优等品）', 'constraint': '≥', 'value': '93', 'unit': '%'},
            {'name': '粒度0.85mm~2.80mm（农业用合格品）', 'constraint': '≥', 'value': '90', 'unit': '%'},
        ],
        'references': ['GB/T 2441.1', 'GB/T 2441.2', 'GB/T 2441.3', 'GB/T 2441.4', 'GB/T 2441.5', 'GB/T 2441.6', 'GB/T 2441.7', 'GB/T 2441.8', 'GB/T 2441.9']
    },
    'GB/T 15063-2020': {
        'name': '复合肥料',
        'category': '农业生产资料',
        'sub_category': '复合肥',
        'indicators': [
            {'name': '总养分(N+P₂O₅+K₂O)（高浓度）', 'constraint': '≥', 'value': '25.0', 'unit': '%'},
            {'name': '总养分(N+P₂O₅+K₂O)（中浓度）', 'constraint': '≥', 'value': '20.0', 'unit': '%'},
            {'name': '总养分(N+P₂O₅+K₂O)（低浓度）', 'constraint': '≥', 'value': '15.0', 'unit': '%'},
            {'name': '水溶性磷占有效磷百分率', 'constraint': '≥', 'value': '60', 'unit': '%'},
            {'name': '水分(H₂O)', 'constraint': '≤', 'value': '2.0', 'unit': '%'},
        ],
        'references': ['GB/T 8572', 'GB/T 8573', 'GB/T 8576', 'GB/T 8577', 'GB/T 24891']
    },
    'GB/T 2945-2017': {
        'name': '硝酸铵',
        'category': '农业生产资料',
        'sub_category': '氮肥',
        'indicators': [
            {'name': '硝酸铵含量（优等品）', 'constraint': '≥', 'value': '99.5', 'unit': '%'},
            {'name': '硝酸铵含量（合格品）', 'constraint': '≥', 'value': '99.0', 'unit': '%'},
            {'name': '总氮(以干基计)（优等品）', 'constraint': '≥', 'value': '34.5', 'unit': '%'},
            {'name': '总氮(以干基计)（合格品）', 'constraint': '≥', 'value': '34.0', 'unit': '%'},
            {'name': '水分（优等品）', 'constraint': '≤', 'value': '0.3', 'unit': '%'},
            {'name': '水分（合格品）', 'constraint': '≤', 'value': '0.5', 'unit': '%'},
            {'name': '10%水溶液pH值', 'constraint': '≥', 'value': '5.0', 'unit': ''},
        ],
        'references': ['GB/T 2947', 'GB/T 6678', 'GB/T 6679']
    },
    'GB/T 535-2020': {
        'name': '肥料级硫酸铵',
        'category': '农业生产资料',
        'sub_category': '氮肥',
        'indicators': [
            {'name': '氮(N)含量', 'constraint': '≥', 'value': '20.5', 'unit': '%'},
            {'name': '水分(H₂O)', 'constraint': '≤', 'value': '1.0', 'unit': '%'},
            {'name': '游离酸(H₂SO₄)', 'constraint': '≤', 'value': '0.2', 'unit': '%'},
        ],
        'references': ['GB/T 8572', 'GB/T 8577']
    },
    'GB/T 20406-2017': {
        'name': '农业用硫酸钾',
        'category': '农业生产资料',
        'sub_category': '钾肥',
        'indicators': [
            {'name': '氧化钾(K₂O)（优等品）', 'constraint': '≥', 'value': '50.0', 'unit': '%'},
            {'name': '氧化钾(K₂O)（合格品）', 'constraint': '≥', 'value': '45.0', 'unit': '%'},
            {'name': '氯离子(Cl⁻)（优等品）', 'constraint': '≤', 'value': '1.0', 'unit': '%'},
            {'name': '氯离子(Cl⁻)（合格品）', 'constraint': '≤', 'value': '2.0', 'unit': '%'},
            {'name': '水分(H₂O)（优等品）', 'constraint': '≤', 'value': '1.0', 'unit': '%'},
            {'name': '水分(H₂O)（合格品）', 'constraint': '≤', 'value': '1.5', 'unit': '%'},
            {'name': '游离酸(H₂SO₄)（优等品）', 'constraint': '≤', 'value': '1.5', 'unit': '%'},
            {'name': '游离酸(H₂SO₄)（合格品）', 'constraint': '≤', 'value': '2.0', 'unit': '%'},
        ],
        'references': ['GB/T 20406.1', 'GB/T 20406.2']
    },
    'GB 10205-2009': {
        'name': '磷酸一铵、磷酸二铵',
        'category': '农业生产资料',
        'sub_category': '磷肥',
        'indicators': [
            {'name': '总养分(N+P₂O₅)（优等品）', 'constraint': '≥', 'value': '64.0', 'unit': '%'},
            {'name': '总养分(N+P₂O₅)（合格品）', 'constraint': '≥', 'value': '57.0', 'unit': '%'},
            {'name': '总氮(N)（优等品）', 'constraint': '≥', 'value': '11.0', 'unit': '%'},
            {'name': '总氮(N)（合格品）', 'constraint': '≥', 'value': '10.0', 'unit': '%'},
            {'name': '有效磷(P₂O₅)（优等品）', 'constraint': '≥', 'value': '46.0', 'unit': '%'},
            {'name': '有效磷(P₂O₅)（合格品）', 'constraint': '≥', 'value': '42.0', 'unit': '%'},
            {'name': '水分(H₂O)（优等品）', 'constraint': '≤', 'value': '2.0', 'unit': '%'},
            {'name': '水分(H₂O)（合格品）', 'constraint': '≤', 'value': '2.5', 'unit': '%'},
        ],
        'references': ['GB/T 10209.1', 'GB/T 10209.2', 'GB/T 10209.3', 'GB/T 10209.4']
    },
    'GB/T 20784-2018': {
        'name': '农业用硝酸钾',
        'category': '农业生产资料',
        'sub_category': '钾肥',
        'indicators': [
            {'name': '氧化钾(K₂O)（优等品）', 'constraint': '≥', 'value': '46.0', 'unit': '%'},
            {'name': '氧化钾(K₂O)（合格品）', 'constraint': '≥', 'value': '44.0', 'unit': '%'},
            {'name': '总氮(N)（优等品）', 'constraint': '≥', 'value': '13.5', 'unit': '%'},
            {'name': '总氮(N)（合格品）', 'constraint': '≥', 'value': '13.0', 'unit': '%'},
            {'name': '氯离子(Cl⁻)（优等品）', 'constraint': '≤', 'value': '0.2', 'unit': '%'},
            {'name': '氯离子(Cl⁻)（合格品）', 'constraint': '≤', 'value': '0.5', 'unit': '%'},
            {'name': '水分(H₂O)（优等品）', 'constraint': '≤', 'value': '0.5', 'unit': '%'},
            {'name': '水分(H₂O)（合格品）', 'constraint': '≤', 'value': '1.0', 'unit': '%'},
        ],
        'references': ['GB/T 20784.1', 'GB/T 20784.2']
    },
    'GB/T 37918-2019': {
        'name': '肥料级氯化钾',
        'category': '农业生产资料',
        'sub_category': '钾肥',
        'indicators': [
            {'name': '氧化钾(K₂O)（优等品）', 'constraint': '≥', 'value': '60.0', 'unit': '%'},
            {'name': '氧化钾(K₂O)（合格品）', 'constraint': '≥', 'value': '55.0', 'unit': '%'},
            {'name': '水分(H₂O)（优等品）', 'constraint': '≤', 'value': '1.0', 'unit': '%'},
            {'name': '水分(H₂O)（合格品）', 'constraint': '≤', 'value': '2.0', 'unit': '%'},
        ],
        'references': ['GB/T 37918.1', 'GB/T 37918.2']
    },
    'GB/T 2946-2018': {
        'name': '氯化铵',
        'category': '农业生产资料',
        'sub_category': '氮肥',
        'indicators': [
            {'name': '氮(N)(以干基计)（优等品）', 'constraint': '≥', 'value': '25.4', 'unit': '%'},
            {'name': '氮(N)(以干基计)（一等品）', 'constraint': '≥', 'value': '25.0', 'unit': '%'},
            {'name': '氮(N)(以干基计)（合格品）', 'constraint': '≥', 'value': '23.5', 'unit': '%'},
            {'name': '水分(H₂O)（优等品）', 'constraint': '≤', 'value': '0.5', 'unit': '%'},
            {'name': '水分(H₂O)（一等品）', 'constraint': '≤', 'value': '0.7', 'unit': '%'},
            {'name': '水分(H₂O)（合格品）', 'constraint': '≤', 'value': '1.0', 'unit': '%'},
        ],
        'references': ['GB/T 2946.1', 'GB/T 2946.2']
    },
    'GB 3559-2001': {
        'name': '农业用碳酸氢铵',
        'category': '农业生产资料',
        'sub_category': '氮肥',
        'indicators': [
            {'name': '氮(N)含量（优等品）', 'constraint': '≥', 'value': '17.2', 'unit': '%'},
            {'name': '氮(N)含量（合格品）', 'constraint': '≥', 'value': '16.8', 'unit': '%'},
            {'name': '水分(H₂O)（优等品）', 'constraint': '≤', 'value': '3.0', 'unit': '%'},
            {'name': '水分(H₂O)（合格品）', 'constraint': '≤', 'value': '3.5', 'unit': '%'},
        ],
        'references': ['GB/T 3559.1', 'GB/T 3559.2']
    },
    'GB/T 10510-2023': {
        'name': '硝酸磷肥、硝酸磷钾肥',
        'category': '农业生产资料',
        'sub_category': '复合肥',
        'indicators': [
            {'name': '总养分(N+P₂O₅+K₂O)', 'constraint': '≥', 'value': '30.0', 'unit': '%'},
            {'name': '水分(H₂O)', 'constraint': '≤', 'value': '1.5', 'unit': '%'},
        ],
        'references': ['GB/T 10511', 'GB/T 10512', 'GB/T 10513', 'GB/T 10514', 'GB/T 10515', 'GB/T 10516']
    },
    'GB/T 20412-2021': {
        'name': '钙镁磷肥',
        'category': '农业生产资料',
        'sub_category': '磷肥',
        'indicators': [
            {'name': '有效五氧化二磷(P₂O₅)', 'constraint': '≥', 'value': '15.0', 'unit': '%'},
            {'name': '水分(H₂O)', 'constraint': '≤', 'value': '0.5', 'unit': '%'},
            {'name': '细度(通过0.25mm试验筛)', 'constraint': '≥', 'value': '80', 'unit': '%'},
        ],
        'references': ['GB/T 20412.1', 'GB/T 20412.2']
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
        ],
        'references': ['GB/T 176', 'GB/T 1346', 'GB/T 17671', 'GB/T 8074', 'GB/T 208']
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
        ],
        'references': ['GB/T 176', 'GB/T 749', 'GB/T 1346', 'GB/T 17671']
    },
    # ========== 工业生产资料 + 交通用具 - 燃气与能源类 ==========
    'GB 11174-2025': {
        'name': '液化石油气',
        'category': '工业生产资料',
        'sub_category': '液化石油气',
        'indicators': [
            {'name': '蒸气压(37.8℃)', 'constraint': '≤', 'value': '1380', 'unit': 'kPa'},
            {'name': 'C₅及C₅以上组分含量', 'constraint': '≤', 'value': '3.0', 'unit': '%(体积分数)'},
            {'name': '总硫含量', 'constraint': '≤', 'value': '343', 'unit': 'mg/m³'},
            {'name': '硫化氢', 'constraint': '≤', 'value': '10', 'unit': 'mg/m³'},
            {'name': '游离水', 'constraint': '=', 'value': '无', 'unit': ''},
        ],
        'references': ['GB/T 6602', 'SH/T 0233', 'SH/T 0221', 'SH/T 0232']
    },
    'GB 5842-2023': {
        'name': '液化石油气钢瓶',
        'category': '工业生产资料',
        'sub_category': '液化石油气',
        'indicators': [
            {'name': '水压试验压力', 'constraint': '=', 'value': '2.4', 'unit': 'MPa'},
            {'name': '气密性试验压力', 'constraint': '=', 'value': '1.6', 'unit': 'MPa'},
        ],
        'references': ['GB/T 9251', 'GB/T 9252', 'GB/T 15385']
    },
    'GB/T 34510-2017': {
        'name': '汽车用液化天然气气瓶',
        'category': '交通用具及相关产品',
        'sub_category': '车用燃油',
        'indicators': [
            {'name': '设计压力', 'constraint': '=', 'value': '1.59', 'unit': 'MPa'},
            {'name': '最高工作压力', 'constraint': '=', 'value': '1.59', 'unit': 'MPa'},
            {'name': '水压试验压力', 'constraint': '=', 'value': '3.2', 'unit': 'MPa'},
        ],
        'references': ['GB/T 9251', 'GB/T 9252', 'GB/T 15385', 'GB/T 18442']
    },
    'GB/T 23799-2021': {
        'name': '车用甲醇汽油(M85)',
        'category': '交通用具及相关产品',
        'sub_category': '车用燃油',
        'indicators': [
            {'name': '甲醇含量', 'constraint': '=', 'value': '84~86', 'unit': '%(体积分数)'},
            {'name': '实际胶质', 'constraint': '≤', 'value': '5', 'unit': 'mg/100mL'},
        ],
        'references': ['GB/T 17930', 'GB/T 23799.1', 'SH/T 0684']
    },
    'GB/T 33445-2023': {
        'name': '煤制合成天然气',
        'category': '工业生产资料',
        'sub_category': '天然气',
        'indicators': [
            {'name': '高位发热量', 'constraint': '≥', 'value': '34.0', 'unit': 'MJ/m³'},
            {'name': '总硫(以硫计)', 'constraint': '≤', 'value': '1.0', 'unit': 'mg/m³'},
            {'name': '硫化氢', 'constraint': '≤', 'value': '0.1', 'unit': 'mg/m³'},
        ],
        'references': ['GB/T 11062', 'GB/T 13610', 'GB/T 27894']
    },
    'GB/T 42416-2023': {
        'name': 'M100车用甲醇燃料',
        'category': '交通用具及相关产品',
        'sub_category': '车用燃油',
        'indicators': [
            {'name': '甲醇含量', 'constraint': '≥', 'value': '99.5', 'unit': '%'},
            {'name': '硫含量', 'constraint': '≤', 'value': '1.0', 'unit': 'mg/kg'},
            {'name': '实际胶质', 'constraint': '≤', 'value': '2.0', 'unit': 'mg/100mL'},
        ],
        'references': ['GB/T 17930', 'SH/T 0684', 'GB/T 23799']
    },
    # ========== 工业生产资料 - 化工原料类 ==========
    'GB/T 320-2025': {
        'name': '工业用合成盐酸',
        'category': '工业生产资料',
        'sub_category': '危险化学品',
        'indicators': [
            {'name': '总酸度(以HCl计)（优等品）', 'constraint': '≥', 'value': '31.0', 'unit': '%'},
            {'name': '总酸度(以HCl计)（合格品）', 'constraint': '≥', 'value': '31.0', 'unit': '%'},
            {'name': '铁(以Fe计)（优等品）', 'constraint': '≤', 'value': '0.002', 'unit': '%'},
            {'name': '铁(以Fe计)（合格品）', 'constraint': '≤', 'value': '0.008', 'unit': '%'},
            {'name': '灼烧残渣（优等品）', 'constraint': '≤', 'value': '0.005', 'unit': '%'},
            {'name': '灼烧残渣（合格品）', 'constraint': '≤', 'value': '0.010', 'unit': '%'},
            {'name': '游离氯(以Cl计)（优等品）', 'constraint': '≤', 'value': '0.002', 'unit': '%'},
            {'name': '游离氯(以Cl计)（合格品）', 'constraint': '≤', 'value': '0.005', 'unit': '%'},
        ],
        'references': ['GB/T 320.1', 'GB/T 320.2', 'GB/T 320.3']
    },
    'GB/T 5138-2021': {
        'name': '工业用液氯',
        'category': '工业生产资料',
        'sub_category': '危险化学品',
        'indicators': [
            {'name': '氯含量(体积分数)（优等品）', 'constraint': '≥', 'value': '99.8', 'unit': '%'},
            {'name': '氯含量(体积分数)（合格品）', 'constraint': '≥', 'value': '99.6', 'unit': '%'},
            {'name': '水分含量（优等品）', 'constraint': '≤', 'value': '0.01', 'unit': '%'},
            {'name': '水分含量（合格品）', 'constraint': '≤', 'value': '0.03', 'unit': '%'},
        ],
        'references': ['GB/T 5138.1', 'GB/T 5138.2']
    },
    'GB 19106-2013': {
        'name': '次氯酸钠',
        'category': '工业生产资料',
        'sub_category': '危险化学品',
        'indicators': [
            {'name': '有效氯(以Cl计)', 'constraint': '≥', 'value': '10.0', 'unit': '%'},
            {'name': '游离碱(以NaOH计)', 'constraint': '=', 'value': '0.1~1.0', 'unit': '%'},
        ],
        'references': ['GB/T 19106.1', 'GB/T 19106.2']
    },
    'GB/T 338-2025': {
        'name': '工业用甲醇',
        'category': '工业生产资料',
        'sub_category': '危险化学品',
        'indicators': [
            {'name': '甲醇纯度（优等品）', 'constraint': '≥', 'value': '99.9', 'unit': '%'},
            {'name': '甲醇纯度（合格品）', 'constraint': '≥', 'value': '99.5', 'unit': '%'},
        ],
        'references': ['GB/T 338.1', 'GB/T 338.2', 'GB/T 338.3']
    },
}

# ============================================================
# Create indicator node pages
# ============================================================

base_dir = 'D:\\knowledge-vault\\wiki\\indicators'
os.makedirs(base_dir, exist_ok=True)

total_indicators = 0
total_references = 0

for std_no, data in standards_data.items():
    std_slug = std_no.replace('/', '-').replace(' ', '_')
    cat_dir = os.path.join(base_dir, data['category'])
    os.makedirs(cat_dir, exist_ok=True)
    
    for ind in data['indicators']:
        # Create a unique slug for the indicator
        ind_slug = ind['name'].replace(' ', '_').replace('(', '').replace(')', '').replace('·', '').replace('~', 'to')
        ind_slug = re.sub(r'[^\w\u4e00-\u9fff]', '_', ind_slug)
        ind_slug = re.sub(r'_+', '_', ind_slug).strip('_')
        
        # Indicator value display
        val_display = f"{ind['constraint']}{ind['value']}{ind['unit']}"
        
        content = f'''---
title: {ind['name']}
type: indicator
std: {std_no}
std_name: {data['name']}
category: {data['category']}
sub_category: {data['sub_category']}
constraint: {ind['constraint']}
value: {ind['value']}
unit: {ind['unit']}
tags: [技术指标, {data['category']}, {data['sub_category']}]
---

# {ind['name']}

## 基本信息

| 属性 | 内容 |
|:----|:-----|
| **所属标准** | [[wiki/standards/{data['category']}类标准技术指标#{std_no}|{std_no} {data['name']}]] |
| **监管类别** | [[wiki/concepts/{data['category']}|{data['category']}]] |
| **子分类** | {data['sub_category']} |
| **约束条件** | {ind['constraint']} |
| **指标值** | {ind['value']} |
| **单位** | {ind['unit']} |
| **完整表达式** | {ind['constraint']}{ind['value']}{ind['unit']} |

## 关联标准
- [[wiki/standards/{data['category']}类标准技术指标#{std_no}|{std_no} {data['name']}]]

## 关联概念
- [[wiki/concepts/{data['category']}|{data['category']}（监管目录）]]
- [[wiki/concepts/{data['sub_category']}|{data['sub_category']}]]
'''
        
        filepath = os.path.join(cat_dir, f'{std_slug}__{ind_slug}.md')
        with open(filepath, 'w', encoding='utf8') as f:
            f.write(content)
        total_indicators += 1
    
    # Create reference page for this standard
    if data['references']:
        ref_dir = os.path.join(base_dir, data['category'], '_references')
        os.makedirs(ref_dir, exist_ok=True)
        
        ref_links = '\n'.join([f'- [[wiki/standards/_references/{r.replace("/", "-").replace(" ", "_")}|{r}]]' for r in data['references']])
        
        # Also create reference stub pages
        for ref in data['references']:
            ref_slug = ref.replace('/', '-').replace(' ', '_')
            ref_file = os.path.join(base_dir, data['category'], '_references', f'{ref_slug}.md')
            if not os.path.exists(ref_file):
                ref_content = f'''---
title: {ref}
type: reference-standard
status: stub
tags: [引用标准, {data['category']}]
---

# {ref}

> ⏳ 引用标准，待补充详细信息

## 被以下标准引用
- [[wiki/standards/{data['category']}类标准技术指标#{std_no}|{std_no} {data['name']}]]
'''
                with open(ref_file, 'w', encoding='utf8') as f:
                    f.write(ref_content)
                total_references += 1
        
        # Update the standard page to include references section
        # (We'll append to the existing standard page)

print(f'Created {total_indicators} indicator node pages')
print(f'Created {total_references} reference stub pages')

# ============================================================
# Update the 3 standard pages to include reference links
# ============================================================

for cat in ['农业生产资料', '工业生产资料', '交通用具及相关产品']:
    filepath = f'D:\\knowledge-vault\\wiki\\standards\\{cat}类标准技术指标.md'
    with open(filepath, 'r', encoding='utf8') as f:
        content = f.read()
    
    # Add references section at the end
    ref_section = '\n\n---\n\n## 引用关系\n\n'
    ref_section += '以下列出各标准引用的检测方法标准：\n\n'
    
    for std_no, data in standards_data.items():
        if data['category'] == cat and data['references']:
            ref_links = '、'.join([f'[[wiki/indicators/{cat}/_references/{r.replace("/", "-").replace(" ", "_")}|{r}]]' for r in data['references']])
            ref_section += f'- **{std_no}** {data["name"]} → 引用：{ref_links}\n'
    
    ref_section += '\n### 指标节点\n'
    ref_section += f'每个技术指标的独立页面位于 `wiki/indicators/{cat}/` 目录下，可在Obsidian图谱视图中显示为独立节点。\n'
    
    if '---\n\n## 关联监管目录' in content:
        content = content.replace('---\n\n## 关联监管目录', ref_section + '\n---\n\n## 关联监管目录')
    else:
        content += ref_section
    
    with open(filepath, 'w', encoding='utf8') as f:
        f.write(content)
    print(f'Updated: {cat}类标准技术指标.md')

print('\nDone!')
