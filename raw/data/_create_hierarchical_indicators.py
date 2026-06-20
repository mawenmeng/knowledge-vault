"""Rebuild indicator nodes with hierarchical structure for Obsidian knowledge graph

Layer structure:
  Layer 1: Standard node (e.g., GB 175-2023)
  Layer 2: Indicator category (e.g., 抗压强度, 抗折强度, 化学成分)
  Layer 3: Sub-category / age (e.g., 3d, 28d)
  Layer 4: Specific value node (e.g., 强度等级32.5 ≥12.0MPa)
"""

import os
import re

base_dir = 'D:\\knowledge-vault\\wiki\\indicators'

# ============================================================
# Hierarchical data structure
# ============================================================

hierarchical_data = {
    # ========== 水泥 ==========
    'GB 175-2023': {
        'name': '通用硅酸盐水泥',
        'category': '工业生产资料',
        'sub_category': '水泥',
        'children': {
            '抗压强度': {
                '3d': [
                    ('强度等级32.5', '≥', '12.0', 'MPa'),
                    ('强度等级32.5R', '≥', '17.0', 'MPa'),
                    ('强度等级42.5', '≥', '17.0', 'MPa'),
                    ('强度等级42.5R', '≥', '22.0', 'MPa'),
                    ('强度等级52.5', '≥', '23.0', 'MPa'),
                    ('强度等级52.5R', '≥', '27.0', 'MPa'),
                ],
                '28d': [
                    ('强度等级32.5', '≥', '32.5', 'MPa'),
                    ('强度等级32.5R', '≥', '32.5', 'MPa'),
                    ('强度等级42.5', '≥', '42.5', 'MPa'),
                    ('强度等级42.5R', '≥', '42.5', 'MPa'),
                    ('强度等级52.5', '≥', '52.5', 'MPa'),
                    ('强度等级52.5R', '≥', '52.5', 'MPa'),
                ],
            },
            '抗折强度': {
                '3d': [
                    ('强度等级32.5', '≥', '3.0', 'MPa'),
                    ('强度等级32.5R', '≥', '4.0', 'MPa'),
                    ('强度等级42.5', '≥', '4.0', 'MPa'),
                    ('强度等级42.5R', '≥', '4.5', 'MPa'),
                    ('强度等级52.5', '≥', '4.5', 'MPa'),
                    ('强度等级52.5R', '≥', '5.0', 'MPa'),
                ],
                '28d': [
                    ('强度等级32.5', '≥', '6.5', 'MPa'),
                    ('强度等级32.5R', '≥', '6.5', 'MPa'),
                    ('强度等级42.5', '≥', '7.0', 'MPa'),
                    ('强度等级42.5R', '≥', '7.0', 'MPa'),
                    ('强度等级52.5', '≥', '8.0', 'MPa'),
                    ('强度等级52.5R', '≥', '8.0', 'MPa'),
                ],
            },
            '化学成分': {
                '氧化镁(MgO)': [
                    ('通用', '≤', '5.0', '%'),
                ],
                '三氧化硫(SO₃)': [
                    ('通用', '≤', '3.5', '%'),
                ],
                '氯离子(Cl⁻)': [
                    ('通用', '≤', '0.06', '%'),
                ],
            },
            '物理性能': {
                '初凝时间': [
                    ('通用', '≥', '45', 'min'),
                ],
                '终凝时间': [
                    ('通用', '≤', '600', 'min'),
                ],
            },
        },
        'references': ['GB/T 176', 'GB/T 1346', 'GB/T 17671', 'GB/T 8074', 'GB/T 208'],
    },
    'GB/T 748-2023': {
        'name': '抗硫酸盐硅酸盐水泥',
        'category': '工业生产资料',
        'sub_category': '水泥',
        'children': {
            '矿物组成': {
                'C₃A含量': [
                    ('中抗硫酸盐', '≤', '5.0', '%'),
                    ('高抗硫酸盐', '≤', '3.0', '%'),
                ],
                'C₃S含量': [
                    ('高抗硫酸盐', '≤', '50.0', '%'),
                ],
            },
            '物理性能': {
                '14d线膨胀率': [
                    ('通用', '≤', '0.060', '%'),
                ],
                '抗硫酸盐侵蚀系数(K)': [
                    ('通用', '≥', '0.80', ''),
                ],
            },
        },
        'references': ['GB/T 176', 'GB/T 749', 'GB/T 1346', 'GB/T 17671'],
    },
    # ========== 尿素 ==========
    'GB/T 2440-2017': {
        'name': '尿素',
        'category': '农业生产资料',
        'sub_category': '氮肥',
        'children': {
            '化学成分': {
                '总氮(N)': [
                    ('农业用优等品', '≥', '46.0', '%'),
                    ('农业用合格品', '≥', '45.0', '%'),
                ],
                '缩二脲': [
                    ('农业用优等品', '≤', '0.9', '%'),
                    ('农业用合格品', '≤', '1.5', '%'),
                ],
            },
            '物理性能': {
                '水分': [
                    ('农业用优等品', '≤', '0.5', '%'),
                    ('农业用合格品', '≤', '1.0', '%'),
                ],
                '粒度(0.85mm~2.80mm)': [
                    ('农业用优等品', '≥', '93', '%'),
                    ('农业用合格品', '≥', '90', '%'),
                ],
            },
        },
        'references': ['GB/T 2441.1', 'GB/T 2441.2', 'GB/T 2441.3', 'GB/T 2441.4', 'GB/T 2441.5', 'GB/T 2441.6', 'GB/T 2441.7', 'GB/T 2441.8', 'GB/T 2441.9'],
    },
    # ========== 复合肥料 ==========
    'GB/T 15063-2020': {
        'name': '复合肥料',
        'category': '农业生产资料',
        'sub_category': '复合肥',
        'children': {
            '养分含量': {
                '总养分(N+P₂O₅+K₂O)': [
                    ('高浓度', '≥', '25.0', '%'),
                    ('中浓度', '≥', '20.0', '%'),
                    ('低浓度', '≥', '15.0', '%'),
                ],
                '水溶性磷占有效磷百分率': [
                    ('通用', '≥', '60', '%'),
                ],
            },
            '物理性能': {
                '水分(H₂O)': [
                    ('通用', '≤', '2.0', '%'),
                ],
            },
        },
        'references': ['GB/T 8572', 'GB/T 8573', 'GB/T 8576', 'GB/T 8577', 'GB/T 24891'],
    },
    # ========== 硝酸铵 ==========
    'GB/T 2945-2017': {
        'name': '硝酸铵',
        'category': '农业生产资料',
        'sub_category': '氮肥',
        'children': {
            '化学成分': {
                '硝酸铵含量': [
                    ('优等品', '≥', '99.5', '%'),
                    ('合格品', '≥', '99.0', '%'),
                ],
                '总氮(以干基计)': [
                    ('优等品', '≥', '34.5', '%'),
                    ('合格品', '≥', '34.0', '%'),
                ],
            },
            '物理性能': {
                '水分': [
                    ('优等品', '≤', '0.3', '%'),
                    ('合格品', '≤', '0.5', '%'),
                ],
                '10%水溶液pH值': [
                    ('通用', '≥', '5.0', ''),
                ],
            },
        },
        'references': ['GB/T 2947', 'GB/T 6678', 'GB/T 6679'],
    },
    # ========== 硫酸铵 ==========
    'GB/T 535-2020': {
        'name': '肥料级硫酸铵',
        'category': '农业生产资料',
        'sub_category': '氮肥',
        'children': {
            '化学成分': {
                '氮(N)含量': [
                    ('通用', '≥', '20.5', '%'),
                ],
                '游离酸(H₂SO₄)': [
                    ('通用', '≤', '0.2', '%'),
                ],
            },
            '物理性能': {
                '水分(H₂O)': [
                    ('通用', '≤', '1.0', '%'),
                ],
            },
        },
        'references': ['GB/T 8572', 'GB/T 8577'],
    },
    # ========== 硫酸钾 ==========
    'GB/T 20406-2017': {
        'name': '农业用硫酸钾',
        'category': '农业生产资料',
        'sub_category': '钾肥',
        'children': {
            '化学成分': {
                '氧化钾(K₂O)': [
                    ('优等品', '≥', '50.0', '%'),
                    ('合格品', '≥', '45.0', '%'),
                ],
                '氯离子(Cl⁻)': [
                    ('优等品', '≤', '1.0', '%'),
                    ('合格品', '≤', '2.0', '%'),
                ],
                '游离酸(H₂SO₄)': [
                    ('优等品', '≤', '1.5', '%'),
                    ('合格品', '≤', '2.0', '%'),
                ],
            },
            '物理性能': {
                '水分(H₂O)': [
                    ('优等品', '≤', '1.0', '%'),
                    ('合格品', '≤', '1.5', '%'),
                ],
            },
        },
        'references': ['GB/T 20406.1', 'GB/T 20406.2'],
    },
    # ========== 磷酸一铵、磷酸二铵 ==========
    'GB 10205-2009': {
        'name': '磷酸一铵、磷酸二铵',
        'category': '农业生产资料',
        'sub_category': '磷肥',
        'children': {
            '养分含量': {
                '总养分(N+P₂O₅)': [
                    ('优等品', '≥', '64.0', '%'),
                    ('合格品', '≥', '57.0', '%'),
                ],
                '总氮(N)': [
                    ('优等品', '≥', '11.0', '%'),
                    ('合格品', '≥', '10.0', '%'),
                ],
                '有效磷(P₂O₅)': [
                    ('优等品', '≥', '46.0', '%'),
                    ('合格品', '≥', '42.0', '%'),
                ],
            },
            '物理性能': {
                '水分(H₂O)': [
                    ('优等品', '≤', '2.0', '%'),
                    ('合格品', '≤', '2.5', '%'),
                ],
            },
        },
        'references': ['GB/T 10209.1', 'GB/T 10209.2', 'GB/T 10209.3', 'GB/T 10209.4'],
    },
    # ========== 硝酸钾 ==========
    'GB/T 20784-2018': {
        'name': '农业用硝酸钾',
        'category': '农业生产资料',
        'sub_category': '钾肥',
        'children': {
            '化学成分': {
                '氧化钾(K₂O)': [
                    ('优等品', '≥', '46.0', '%'),
                    ('合格品', '≥', '44.0', '%'),
                ],
                '总氮(N)': [
                    ('优等品', '≥', '13.5', '%'),
                    ('合格品', '≥', '13.0', '%'),
                ],
                '氯离子(Cl⁻)': [
                    ('优等品', '≤', '0.2', '%'),
                    ('合格品', '≤', '0.5', '%'),
                ],
            },
            '物理性能': {
                '水分(H₂O)': [
                    ('优等品', '≤', '0.5', '%'),
                    ('合格品', '≤', '1.0', '%'),
                ],
            },
        },
        'references': ['GB/T 20784.1', 'GB/T 20784.2'],
    },
    # ========== 氯化钾 ==========
    'GB/T 37918-2019': {
        'name': '肥料级氯化钾',
        'category': '农业生产资料',
        'sub_category': '钾肥',
        'children': {
            '化学成分': {
                '氧化钾(K₂O)': [
                    ('优等品', '≥', '60.0', '%'),
                    ('合格品', '≥', '55.0', '%'),
                ],
            },
            '物理性能': {
                '水分(H₂O)': [
                    ('优等品', '≤', '1.0', '%'),
                    ('合格品', '≤', '2.0', '%'),
                ],
            },
        },
        'references': ['GB/T 37918.1', 'GB/T 37918.2'],
    },
    # ========== 氯化铵 ==========
    'GB/T 2946-2018': {
        'name': '氯化铵',
        'category': '农业生产资料',
        'sub_category': '氮肥',
        'children': {
            '化学成分': {
                '氮(N)(以干基计)': [
                    ('优等品', '≥', '25.4', '%'),
                    ('一等品', '≥', '25.0', '%'),
                    ('合格品', '≥', '23.5', '%'),
                ],
            },
            '物理性能': {
                '水分(H₂O)': [
                    ('优等品', '≤', '0.5', '%'),
                    ('一等品', '≤', '0.7', '%'),
                    ('合格品', '≤', '1.0', '%'),
                ],
            },
        },
        'references': ['GB/T 2946.1', 'GB/T 2946.2'],
    },
    # ========== 碳酸氢铵 ==========
    'GB 3559-2001': {
        'name': '农业用碳酸氢铵',
        'category': '农业生产资料',
        'sub_category': '氮肥',
        'children': {
            '化学成分': {
                '氮(N)含量': [
                    ('优等品', '≥', '17.2', '%'),
                    ('合格品', '≥', '16.8', '%'),
                ],
            },
            '物理性能': {
                '水分(H₂O)': [
                    ('优等品', '≤', '3.0', '%'),
                    ('合格品', '≤', '3.5', '%'),
                ],
            },
        },
        'references': ['GB/T 3559.1', 'GB/T 3559.2'],
    },
    # ========== 硝酸磷肥 ==========
    'GB/T 10510-2023': {
        'name': '硝酸磷肥、硝酸磷钾肥',
        'category': '农业生产资料',
        'sub_category': '复合肥',
        'children': {
            '养分含量': {
                '总养分(N+P₂O₅+K₂O)': [
                    ('通用', '≥', '30.0', '%'),
                ],
            },
            '物理性能': {
                '水分(H₂O)': [
                    ('通用', '≤', '1.5', '%'),
                ],
            },
        },
        'references': ['GB/T 10511', 'GB/T 10512', 'GB/T 10513', 'GB/T 10514', 'GB/T 10515', 'GB/T 10516'],
    },
    # ========== 钙镁磷肥 ==========
    'GB/T 20412-2021': {
        'name': '钙镁磷肥',
        'category': '农业生产资料',
        'sub_category': '磷肥',
        'children': {
            '养分含量': {
                '有效五氧化二磷(P₂O₅)': [
                    ('通用', '≥', '15.0', '%'),
                ],
            },
            '物理性能': {
                '水分(H₂O)': [
                    ('通用', '≤', '0.5', '%'),
                ],
                '细度(通过0.25mm试验筛)': [
                    ('通用', '≥', '80', '%'),
                ],
            },
        },
        'references': ['GB/T 20412.1', 'GB/T 20412.2'],
    },
    # ========== 液化石油气 ==========
    'GB 11174-2025': {
        'name': '液化石油气',
        'category': '工业生产资料',
        'sub_category': '液化石油气',
        'children': {
            '物理性能': {
                '蒸气压(37.8℃)': [
                    ('通用', '≤', '1380', 'kPa'),
                ],
                'C₅及C₅以上组分含量': [
                    ('通用', '≤', '3.0', '%(体积分数)'),
                ],
            },
            '化学成分': {
                '总硫含量': [
                    ('通用', '≤', '343', 'mg/m³'),
                ],
                '硫化氢': [
                    ('通用', '≤', '10', 'mg/m³'),
                ],
            },
        },
        'references': ['GB/T 6602', 'SH/T 0233', 'SH/T 0221', 'SH/T 0232'],
    },
    # ========== 液化石油气钢瓶 ==========
    'GB 5842-2023': {
        'name': '液化石油气钢瓶',
        'category': '工业生产资料',
        'sub_category': '液化石油气',
        'children': {
            '耐压性能': {
                '水压试验压力': [
                    ('通用', '=', '2.4', 'MPa'),
                ],
                '气密性试验压力': [
                    ('通用', '=', '1.6', 'MPa'),
                ],
            },
        },
        'references': ['GB/T 9251', 'GB/T 9252', 'GB/T 15385'],
    },
    # ========== LNG气瓶 ==========
    'GB/T 34510-2017': {
        'name': '汽车用液化天然气气瓶',
        'category': '交通用具及相关产品',
        'sub_category': '车用燃油',
        'children': {
            '耐压性能': {
                '设计压力': [
                    ('通用', '=', '1.59', 'MPa'),
                ],
                '最高工作压力': [
                    ('通用', '=', '1.59', 'MPa'),
                ],
                '水压试验压力': [
                    ('通用', '=', '3.2', 'MPa'),
                ],
            },
        },
        'references': ['GB/T 9251', 'GB/T 9252', 'GB/T 15385', 'GB/T 18442'],
    },
    # ========== 车用甲醇汽油 ==========
    'GB/T 23799-2021': {
        'name': '车用甲醇汽油(M85)',
        'category': '交通用具及相关产品',
        'sub_category': '车用燃油',
        'children': {
            '化学成分': {
                '甲醇含量': [
                    ('通用', '=', '84~86', '%(体积分数)'),
                ],
                '实际胶质': [
                    ('通用', '≤', '5', 'mg/100mL'),
                ],
            },
        },
        'references': ['GB/T 17930', 'GB/T 23799.1', 'SH/T 0684'],
    },
    # ========== 煤制合成天然气 ==========
    'GB/T 33445-2023': {
        'name': '煤制合成天然气',
        'category': '工业生产资料',
        'sub_category': '天然气',
        'children': {
            '热值': {
                '高位发热量': [
                    ('通用', '≥', '34.0', 'MJ/m³'),
                ],
            },
            '化学成分': {
                '总硫(以硫计)': [
                    ('通用', '≤', '1.0', 'mg/m³'),
                ],
                '硫化氢': [
                    ('通用', '≤', '0.1', 'mg/m³'),
                ],
            },
        },
        'references': ['GB/T 11062', 'GB/T 13610', 'GB/T 27894'],
    },
    # ========== M100甲醇燃料 ==========
    'GB/T 42416-2023': {
        'name': 'M100车用甲醇燃料',
        'category': '交通用具及相关产品',
        'sub_category': '车用燃油',
        'children': {
            '化学成分': {
                '甲醇含量': [
                    ('通用', '≥', '99.5', '%'),
                ],
                '硫含量': [
                    ('通用', '≤', '1.0', 'mg/kg'),
                ],
                '实际胶质': [
                    ('通用', '≤', '2.0', 'mg/100mL'),
                ],
            },
        },
        'references': ['GB/T 17930', 'SH/T 0684', 'GB/T 23799'],
    },
    # ========== 合成盐酸 ==========
    'GB/T 320-2025': {
        'name': '工业用合成盐酸',
        'category': '工业生产资料',
        'sub_category': '危险化学品',
        'children': {
            '化学成分': {
                '总酸度(以HCl计)': [
                    ('优等品', '≥', '31.0', '%'),
                    ('合格品', '≥', '31.0', '%'),
                ],
                '铁(以Fe计)': [
                    ('优等品', '≤', '0.002', '%'),
                    ('合格品', '≤', '0.008', '%'),
                ],
                '游离氯(以Cl计)': [
                    ('优等品', '≤', '0.002', '%'),
                    ('合格品', '≤', '0.005', '%'),
                ],
            },
            '物理性能': {
                '灼烧残渣': [
                    ('优等品', '≤', '0.005', '%'),
                    ('合格品', '≤', '0.010', '%'),
                ],
            },
        },
        'references': ['GB/T 320.1', 'GB/T 320.2', 'GB/T 320.3'],
    },
    # ========== 液氯 ==========
    'GB/T 5138-2021': {
        'name': '工业用液氯',
        'category': '工业生产资料',
        'sub_category': '危险化学品',
        'children': {
            '化学成分': {
                '氯含量(体积分数)': [
                    ('优等品', '≥', '99.8', '%'),
                    ('合格品', '≥', '99.6', '%'),
                ],
                '水分含量': [
                    ('优等品', '≤', '0.01', '%'),
                    ('合格品', '≤', '0.03', '%'),
                ],
            },
        },
        'references': ['GB/T 5138.1', 'GB/T 5138.2'],
    },
    # ========== 次氯酸钠 ==========
    'GB 19106-2013': {
        'name': '次氯酸钠',
        'category': '工业生产资料',
        'sub_category': '危险化学品',
        'children': {
            '化学成分': {
                '有效氯(以Cl计)': [
                    ('通用', '≥', '10.0', '%'),
                ],
                '游离碱(以NaOH计)': [
                    ('通用', '=', '0.1~1.0', '%'),
                ],
            },
        },
        'references': ['GB/T 19106.1', 'GB/T 19106.2'],
    },
    # ========== 甲醇 ==========
    'GB/T 338-2025': {
        'name': '工业用甲醇',
        'category': '工业生产资料',
        'sub_category': '危险化学品',
        'children': {
            '化学成分': {
                '甲醇纯度': [
                    ('优等品', '≥', '99.9', '%'),
                    ('合格品', '≥', '99.5', '%'),
                ],
            },
        },
        'references': ['GB/T 338.1', 'GB/T 338.2', 'GB/T 338.3'],
    },
}

# ============================================================
# Create hierarchical indicator nodes
# ============================================================

# First, clean old indicators
import shutil
if os.path.exists(base_dir):
    shutil.rmtree(base_dir)
os.makedirs(base_dir, exist_ok=True)

total_value_nodes = 0
total_category_nodes = 0
total_subcategory_nodes = 0
total_ref_nodes = 0

std_slug_map = {}  # std_no -> slug

for std_no, data in hierarchical_data.items():
    std_slug = std_no.replace('/', '-').replace(' ', '_')
    std_slug_map[std_no] = std_slug
    cat_dir = os.path.join(base_dir, data['category'])
    os.makedirs(cat_dir, exist_ok=True)
    
    # --- Layer 2: Indicator category nodes ---
    for cat_name, subcats in data['children'].items():
        cat_slug = cat_name.replace(' ', '_').replace('(', '').replace(')', '')
        cat_slug = re.sub(r'[^\w\u4e00-\u9fff]', '_', cat_slug)
        cat_slug = re.sub(r'_+', '_', cat_slug).strip('_')
        
        cat_node_path = os.path.join(cat_dir, f'{std_slug}__{cat_slug}.md')
        
        # Build links to subcategories
        subcat_links = []
        for subcat_name, values in subcats.items():
            subcat_slug = subcat_name.replace(' ', '_').replace('(', '').replace(')', '')
            subcat_slug = re.sub(r'[^\w\u4e00-\u9fff]', '_', subcat_slug)
            subcat_slug = re.sub(r'_+', '_', subcat_slug).strip('_')
            subcat_links.append(f'[[{cat_dir}/{std_slug}__{cat_slug}__{subcat_slug}|{subcat_name}]]')
        
        cat_content = f'''---
title: {cat_name}
type: indicator-category
std: {std_no}
std_name: {data['name']}
category: {data['category']}
tags: [技术指标类别, {data['category']}]
---

# {cat_name}

**所属标准：** [[wiki/standards/{data['category']}类标准技术指标#{std_no}|{std_no} {data['name']}]]

## 子指标

{chr(10).join([f'- {link}' for link in subcat_links])}
'''
        with open(cat_node_path, 'w', encoding='utf8') as f:
            f.write(cat_content)
        total_category_nodes += 1
        
        # --- Layer 3: Subcategory nodes ---
        for subcat_name, values in subcats.items():
            subcat_slug = subcat_name.replace(' ', '_').replace('(', '').replace(')', '')
            subcat_slug = re.sub(r'[^\w\u4e00-\u9fff]', '_', subcat_slug)
            subcat_slug = re.sub(r'_+', '_', subcat_slug).strip('_')
            
            subcat_node_path = os.path.join(cat_dir, f'{std_slug}__{cat_slug}__{subcat_slug}.md')
            
            # Build links to value nodes
            value_links = []
            for grade, constraint, val, unit in values:
                grade_slug = grade.replace(' ', '_').replace('(', '').replace(')', '').replace('~', 'to')
                grade_slug = re.sub(r'[^\w\u4e00-\u9fff]', '_', grade_slug)
                grade_slug = re.sub(r'_+', '_', grade_slug).strip('_')
                
                expr = f'{constraint}{val}{unit}'
                expr_slug = expr.replace(' ', '_').replace('\u00b3', '3').replace('\u00b2', '2').replace('\u207b', '-')
                expr_slug = expr_slug.replace('/', '\uff0f')
                expr_slug = re.sub(r'[^\w\u4e00-\u9fff\u2265\u2264=／%]', '_', expr_slug)
                expr_slug = re.sub(r'_+', '_', expr_slug).strip('_')
                
                value_links.append(f'[[{cat_dir}/{std_slug}__{cat_slug}__{subcat_slug}__{grade_slug}__{expr_slug}|{grade} {constraint}{val}{unit}]]')
            
            subcat_content = f'''---
title: {subcat_name}
type: indicator-subcategory
std: {std_no}
std_name: {data['name']}
category: {data['category']}
tags: [技术指标子类, {data['category']}]
---

# {subcat_name}

**所属标准：** [[wiki/standards/{data['category']}类标准技术指标#{std_no}|{std_no} {data['name']}]]
**指标类别：** [[{cat_dir}/{std_slug}__{cat_slug}|{cat_name}]]

## 指标值

{chr(10).join([f'- {link}' for link in value_links])}
'''
            with open(subcat_node_path, 'w', encoding='utf8') as f:
                f.write(subcat_content)
            total_subcategory_nodes += 1
            
            # --- Layer 4: Value nodes ---
            for grade, constraint, val, unit in values:
                grade_slug = grade.replace(' ', '_').replace('(', '').replace(')', '').replace('~', 'to')
                grade_slug = re.sub(r'[^\w\u4e00-\u9fff]', '_', grade_slug)
                grade_slug = re.sub(r'_+', '_', grade_slug).strip('_')
                
                expr = f'{constraint}{val}{unit}'
                title = f'{grade} {expr}'
                
                # Build filename with full expression for Obsidian graph display
                expr_slug = expr.replace(' ', '_').replace('\u00b3', '3').replace('\u00b2', '2').replace('\u207b', '-')
                expr_slug = expr_slug.replace('/', '\uff0f')
                expr_slug = re.sub(r'[^\w\u4e00-\u9fff\u2265\u2264=／%]', '_', expr_slug)
                expr_slug = re.sub(r'_+', '_', expr_slug).strip('_')
                
                value_node_path = os.path.join(cat_dir, f'{std_slug}__{cat_slug}__{subcat_slug}__{grade_slug}__{expr_slug}.md')
                
                value_content = f'''---
title: {title}
type: indicator-value
std: {std_no}
std_name: {data['name']}
category: {data['category']}
constraint: {constraint}
value: {val}
unit: {unit}
grade: {grade}
tags: [技术指标值, {data['category']}]
---

# {title}

## 基本信息

| 属性 | 内容 |
|:----|:-----|
| **所属标准** | [[wiki/standards/{data['category']}类标准技术指标#{std_no}|{std_no} {data['name']}]] |
| **指标类别** | [[{cat_dir}/{std_slug}__{cat_slug}|{cat_name}]] |
| **子类** | [[{cat_dir}/{std_slug}__{cat_slug}__{subcat_slug}|{subcat_name}]] |
| **等级/条件** | {grade} |
| **约束条件** | {constraint} |
| **指标值** | {val} |
| **单位** | {unit} |
| **完整表达式** | {expr} |
'''
                with open(value_node_path, 'w', encoding='utf8') as f:
                    f.write(value_content)
                total_value_nodes += 1
    
    # --- Reference nodes ---
    if data['references']:
        ref_dir = os.path.join(cat_dir, '_references')
        os.makedirs(ref_dir, exist_ok=True)
        for ref in data['references']:
            ref_slug = ref.replace('/', '-').replace(' ', '_')
            ref_file = os.path.join(ref_dir, f'{ref_slug}.md')
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
                total_ref_nodes += 1

print(f'Created:')
print(f'  Layer 2 (indicator category): {total_category_nodes}')
print(f'  Layer 3 (subcategory):        {total_subcategory_nodes}')
print(f'  Layer 4 (value nodes):        {total_value_nodes}')
print(f'  Reference stubs:              {total_ref_nodes}')
print(f'  Total:                        {total_category_nodes + total_subcategory_nodes + total_value_nodes + total_ref_nodes}')
