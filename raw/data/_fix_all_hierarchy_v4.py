"""Fix remaining issues after v3 fix:
1. L1 nodes: references after technical indicators (not before)
2. L2 nodes: remove duplicate backlinks  
3. L4→L3 links: rebuild based on actual data hierarchy
"""
import os, re

base = 'D:\\knowledge-vault\\wiki\\indicators'

# Hardcoded standard data with full hierarchy
STANDARDS = {
    'GB 175-2023': {
        'name': '通用硅酸盐水泥',
        'references': ['GB/T 176', 'GB/T 1346', 'GB/T 17671', 'GB/T 8074', 'GB/T 208'],
        'children': {
            '抗压强度': {'3d': ['强度等级32.5 ≥12.0MPa', '强度等级32.5R ≥17.0MPa', '强度等级42.5 ≥17.0MPa', '强度等级42.5R ≥22.0MPa', '强度等级52.5 ≥23.0MPa', '强度等级52.5R ≥27.0MPa'],
                        '28d': ['强度等级32.5 ≥32.5MPa', '强度等级32.5R ≥32.5MPa', '强度等级42.5 ≥42.5MPa', '强度等级42.5R ≥42.5MPa', '强度等级52.5 ≥52.5MPa', '强度等级52.5R ≥52.5MPa']},
            '抗折强度': {'3d': ['强度等级32.5 ≥3.0MPa', '强度等级32.5R ≥4.0MPa', '强度等级42.5 ≥4.0MPa', '强度等级42.5R ≥4.5MPa', '强度等级52.5 ≥4.5MPa', '强度等级52.5R ≥5.0MPa'],
                        '28d': ['强度等级32.5 ≥6.5MPa', '强度等级32.5R ≥6.5MPa', '强度等级42.5 ≥7.0MPa', '强度等级42.5R ≥7.0MPa', '强度等级52.5 ≥8.0MPa', '强度等级52.5R ≥8.0MPa']},
            '化学成分': {'氧化镁(MgO)': ['通用 ≤5.0%'],
                        '三氧化硫(SO₃)': ['通用 ≤3.5%'],
                        '氯离子(Cl⁻)': ['通用 ≤0.06%']},
            '物理性能': {'初凝时间': ['通用 ≥45min'],
                        '终凝时间': ['通用 ≤600min']},
        }
    },
    'GB/T 748-2023': {
        'name': '抗硫酸盐硅酸盐水泥',
        'references': ['GB/T 176', 'GB/T 749', 'GB/T 1346', 'GB/T 17671'],
        'children': {
            '矿物组成': {'C₃A含量': ['中抗硫酸盐 ≤5.0%', '高抗硫酸盐 ≤3.0%'],
                        'C₃S含量': ['高抗硫酸盐 ≤50.0%']},
            '物理性能': {'14d线膨胀率': ['通用 ≤0.060%'],
                        '抗硫酸盐侵蚀系数(K)': ['通用 ≥0.80']},
        }
    },
    'GB/T 2440-2017': {
        'name': '尿素',
        'references': ['GB/T 2441.1', 'GB/T 2441.2', 'GB/T 2441.3', 'GB/T 2441.4', 'GB/T 2441.5', 'GB/T 2441.6', 'GB/T 2441.7', 'GB/T 2441.8', 'GB/T 2441.9'],
        'children': {
            '化学成分': {'总氮(N)': ['农业用优等品 ≥46.0%', '农业用合格品 ≥45.0%'],
                        '缩二脲': ['农业用优等品 ≤0.9%', '农业用合格品 ≤1.5%']},
            '物理性能': {'水分': ['农业用优等品 ≤0.5%', '农业用合格品 ≤1.0%'],
                        '粒度(0.85mm~2.80mm)': ['农业用优等品 ≥93%', '农业用合格品 ≥90%']},
        }
    },
    'GB/T 15063-2020': {
        'name': '复合肥料',
        'references': ['GB/T 8572', 'GB/T 8573', 'GB/T 8576', 'GB/T 8577', 'GB/T 24891'],
        'children': {
            '养分含量': {'总养分(N+P₂O₅+K₂O)': ['高浓度 ≥25.0%', '中浓度 ≥20.0%', '低浓度 ≥15.0%'],
                        '水溶性磷占有效磷百分率': ['通用 ≥60%']},
            '物理性能': {'水分(H₂O)': ['通用 ≤2.0%']},
        }
    },
    'GB/T 2945-2017': {
        'name': '硝酸铵',
        'references': ['GB/T 2947', 'GB/T 6678', 'GB/T 6679'],
        'children': {
            '化学成分': {'硝酸铵含量': ['优等品 ≥99.5%', '合格品 ≥99.0%'],
                        '总氮(以干基计)': ['优等品 ≥34.5%', '合格品 ≥34.0%']},
            '物理性能': {'水分': ['优等品 ≤0.3%', '合格品 ≤0.5%'],
                        '10%水溶液pH值': ['通用 ≥5.0']},
        }
    },
    'GB/T 535-2020': {
        'name': '肥料级硫酸铵',
        'references': ['GB/T 8572', 'GB/T 8577'],
        'children': {
            '化学成分': {'氮(N)含量': ['通用 ≥20.5%'],
                        '游离酸(H₂SO₄)': ['通用 ≤0.2%']},
            '物理性能': {'水分(H₂O)': ['通用 ≤1.0%']},
        }
    },
    'GB/T 20406-2017': {
        'name': '农业用硫酸钾',
        'references': ['GB/T 20406.1', 'GB/T 20406.2'],
        'children': {
            '化学成分': {'氧化钾(K₂O)': ['优等品 ≥50.0%', '合格品 ≥45.0%'],
                        '氯离子(Cl⁻)': ['优等品 ≤1.0%', '合格品 ≤2.0%'],
                        '游离酸(H₂SO₄)': ['优等品 ≤1.5%', '合格品 ≤2.0%']},
            '物理性能': {'水分(H₂O)': ['优等品 ≤1.0%', '合格品 ≤1.5%']},
        }
    },
    'GB 10205-2009': {
        'name': '磷酸一铵、磷酸二铵',
        'references': ['GB/T 10209.1', 'GB/T 10209.2', 'GB/T 10209.3', 'GB/T 10209.4'],
        'children': {
            '养分含量': {'总养分(N+P₂O₅)': ['优等品 ≥64.0%', '合格品 ≥57.0%'],
                        '总氮(N)': ['优等品 ≥11.0%', '合格品 ≥10.0%'],
                        '有效磷(P₂O₅)': ['优等品 ≥46.0%', '合格品 ≥42.0%']},
            '物理性能': {'水分(H₂O)': ['优等品 ≤2.0%', '合格品 ≤2.5%']},
        }
    },
    'GB/T 20784-2018': {
        'name': '农业用硝酸钾',
        'references': ['GB/T 20784.1', 'GB/T 20784.2'],
        'children': {
            '化学成分': {'氧化钾(K₂O)': ['优等品 ≥46.0%', '合格品 ≥44.0%'],
                        '总氮(N)': ['优等品 ≥13.5%', '合格品 ≥13.0%'],
                        '氯离子(Cl⁻)': ['优等品 ≤0.2%', '合格品 ≤0.5%']},
            '物理性能': {'水分(H₂O)': ['优等品 ≤0.5%', '合格品 ≤1.0%']},
        }
    },
    'GB/T 37918-2019': {
        'name': '肥料级氯化钾',
        'references': ['GB/T 37918.1', 'GB/T 37918.2'],
        'children': {
            '化学成分': {'氧化钾(K₂O)': ['优等品 ≥60.0%', '合格品 ≥55.0%']},
            '物理性能': {'水分(H₂O)': ['优等品 ≤1.0%', '合格品 ≤2.0%']},
        }
    },
    'GB/T 2946-2018': {
        'name': '氯化铵',
        'references': ['GB/T 2946.1', 'GB/T 2946.2'],
        'children': {
            '化学成分': {'氮(N)(以干基计)': ['优等品 ≥25.4%', '一等品 ≥25.0%', '合格品 ≥23.5%']},
            '物理性能': {'水分(H₂O)': ['优等品 ≤0.5%', '一等品 ≤0.7%', '合格品 ≤1.0%']},
        }
    },
    'GB 3559-2001': {
        'name': '农业用碳酸氢铵',
        'references': ['GB/T 3559.1', 'GB/T 3559.2'],
        'children': {
            '化学成分': {'氮(N)含量': ['优等品 ≥17.2%', '合格品 ≥16.8%']},
            '物理性能': {'水分(H₂O)': ['优等品 ≤3.0%', '合格品 ≤3.5%']},
        }
    },
    'GB/T 10510-2023': {
        'name': '硝酸磷肥、硝酸磷钾肥',
        'references': ['GB/T 10511', 'GB/T 10512', 'GB/T 10513', 'GB/T 10514', 'GB/T 10515', 'GB/T 10516'],
        'children': {
            '养分含量': {'总养分(N+P₂O₅+K₂O)': ['通用 ≥30.0%']},
            '物理性能': {'水分(H₂O)': ['通用 ≤1.5%']},
        }
    },
    'GB/T 20412-2021': {
        'name': '钙镁磷肥',
        'references': ['GB/T 20412.1', 'GB/T 20412.2'],
        'children': {
            '养分含量': {'有效五氧化二磷(P₂O₅)': ['通用 ≥15.0%']},
            '物理性能': {'水分(H₂O)': ['通用 ≤0.5%'],
                        '细度(通过0.25mm试验筛)': ['通用 ≥80%']},
        }
    },
    'GB 11174-2025': {
        'name': '液化石油气',
        'references': ['GB/T 6602', 'SH/T 0233', 'SH/T 0221', 'SH/T 0232'],
        'children': {
            '物理性能': {'蒸气压(37.8℃)': ['通用 ≤1380kPa'],
                        'C₅及C₅以上组分含量': ['通用 ≤3.0%(体积分数)']},
            '化学成分': {'总硫含量': ['通用 ≤343mg/m³'],
                        '硫化氢': ['通用 ≤10mg/m³']},
        }
    },
    'GB 5842-2023': {
        'name': '液化石油气钢瓶',
        'references': ['GB/T 9251', 'GB/T 9252', 'GB/T 15385'],
        'children': {
            '耐压性能': {'水压试验压力': ['通用 =2.4MPa'],
                        '气密性试验压力': ['通用 =1.6MPa']},
        }
    },
    'GB/T 34510-2017': {
        'name': '汽车用液化天然气气瓶',
        'references': ['GB/T 9251', 'GB/T 9252', 'GB/T 15385', 'GB/T 18442'],
        'children': {
            '耐压性能': {'设计压力': ['通用 =1.59MPa'],
                        '最高工作压力': ['通用 =1.59MPa'],
                        '水压试验压力': ['通用 =3.2MPa']},
        }
    },
    'GB/T 23799-2021': {
        'name': '车用甲醇汽油(M85)',
        'references': ['GB/T 17930', 'GB/T 23799.1', 'SH/T 0684'],
        'children': {
            '化学成分': {'甲醇含量': ['通用 =84~86%(体积分数)'],
                        '实际胶质': ['通用 ≤5mg/100mL']},
        }
    },
    'GB/T 33445-2023': {
        'name': '煤制合成天然气',
        'references': ['GB/T 11062', 'GB/T 13610', 'GB/T 27894'],
        'children': {
            '热值': {'高位发热量': ['通用 ≥34.0MJ/m³']},
            '化学成分': {'总硫(以硫计)': ['通用 ≤1.0mg/m³'],
                        '硫化氢': ['通用 ≤0.1mg/m³']},
        }
    },
    'GB/T 42416-2023': {
        'name': 'M100车用甲醇燃料',
        'references': ['GB/T 17930', 'SH/T 0684', 'GB/T 23799'],
        'children': {
            '化学成分': {'甲醇含量': ['通用 ≥99.5%'],
                        '硫含量': ['通用 ≤1.0mg/kg'],
                        '实际胶质': ['通用 ≤2.0mg/100mL']},
        }
    },
    'GB/T 320-2025': {
        'name': '工业用合成盐酸',
        'references': ['GB/T 320.1', 'GB/T 320.2', 'GB/T 320.3'],
        'children': {
            '化学成分': {'总酸度(以HCl计)': ['优等品 ≥31.0%', '合格品 ≥31.0%'],
                        '铁(以Fe计)': ['优等品 ≤0.002%', '合格品 ≤0.008%'],
                        '游离氯(以Cl计)': ['优等品 ≤0.002%', '合格品 ≤0.005%']},
            '物理性能': {'灼烧残渣': ['优等品 ≤0.005%', '合格品 ≤0.010%']},
        }
    },
    'GB/T 5138-2021': {
        'name': '工业用液氯',
        'references': ['GB/T 5138.1', 'GB/T 5138.2'],
        'children': {
            '化学成分': {'氯含量(体积分数)': ['优等品 ≥99.8%', '合格品 ≥99.6%'],
                        '水分含量': ['优等品 ≤0.01%', '合格品 ≤0.03%']},
        }
    },
    'GB 19106-2013': {
        'name': '次氯酸钠',
        'references': ['GB/T 19106.1', 'GB/T 19106.2'],
        'children': {
            '化学成分': {'有效氯(以Cl计)': ['通用 ≥10.0%'],
                        '游离碱(以NaOH计)': ['通用 =0.1~1.0%']},
        }
    },
    'GB/T 338-2025': {
        'name': '工业用甲醇',
        'references': ['GB/T 338.1', 'GB/T 338.2', 'GB/T 338.3'],
        'children': {
            '化学成分': {'甲醇纯度': ['优等品 ≥99.9%', '合格品 ≥99.5%']},
        }
    },
}

total_fixes = 0

# ========== 1. Fix L1 nodes: reorder references after indicators ==========
print("=== 1. Fixing L1 node ordering ===")

for root, dirs, files in os.walk(base):
    if '_references' in root:
        continue
    
    for f in files:
        if not f.endswith('.md'):
            continue
        fp = os.path.join(root, f)
        with open(fp, 'r', encoding='utf8') as fh:
            content = fh.read()
        
        if 'type: standard-node' not in content:
            continue
        
        std_m = re.search(r'^std: (.+)$', content, re.M)
        if not std_m:
            continue
        std_no = std_m.group(1)
        
        if std_no not in STANDARDS:
            continue
        
        info = STANDARDS[std_no]
        std_name = info['name']
        references = info.get('references', [])
        
        cat_dir = os.path.basename(os.path.dirname(root))
        std_dir = os.path.basename(root)
        prefix = 'wiki/indicators/' + cat_dir + '/' + std_dir + '/'
        
        modified = False
        
        # Find the indicator links section
        tech_idx = content.find('## 技术指标')
        ref_idx = content.find('## 引用标准')
        
        if ref_idx > 0 and tech_idx > 0:
            # Extract references section content
            ref_end = content.find('\n## ', ref_idx + 1)
            if ref_end < 0:
                ref_end = len(content)
            
            ref_section = content[ref_idx:ref_end]
            
            # Extract indicator links content
            tech_end = content.find('\n## ', tech_idx + 1)
            if tech_end < 0:
                tech_end = len(content)
            
            tech_section = content[tech_idx:tech_end]
            
            # If references comes before indicators, swap them
            if ref_idx < tech_idx:
                # Remove references section
                content = content[:ref_idx] + content[ref_end:]
                # Find where tech section ends now
                new_tech_idx = content.find('## 技术指标')
                new_tech_end = content.find('\n## ', new_tech_idx + 1)
                if new_tech_end < 0:
                    new_tech_end = len(content)
                # Insert references after tech section
                content = content[:new_tech_end] + '\n\n' + ref_section.strip() + '\n' + content[new_tech_end:]
                modified = True
        
        if modified:
            with open(fp, 'w', encoding='utf8') as fh:
                fh.write(content)
            total_fixes += 1

print(f"  Fixed {total_fixes} L1 nodes (reordered)")

# ========== 2. Fix L2 nodes: remove duplicate backlinks ==========
print("\n=== 2. Fixing L2 duplicate backlinks ===")

l2_fixes = 0
for root, dirs, files in os.walk(base):
    if '_references' in root:
        continue
    
    for f in files:
        if not f.endswith('.md'):
            continue
        fp = os.path.join(root, f)
        with open(fp, 'r', encoding='utf8') as fh:
            content = fh.read()
        
        if 'type: indicator-category' not in content:
            continue
        
        # Find all backlinks
        backlinks = re.findall(r'\*\*所属标准：\*\* \[\[[^\]]+\]\]', content)
        if len(backlinks) > 1:
            # Keep only the first one (which should be the updated one)
            first_link = backlinks[0]
            for bl in backlinks[1:]:
                content = content.replace(bl, '')
            # Clean up empty lines
            content = re.sub(r'\n{3,}', '\n\n', content)
            with open(fp, 'w', encoding='utf8') as fh:
                fh.write(content)
            l2_fixes += 1

print(f"  Fixed {l2_fixes} L2 nodes (removed duplicate backlinks)")

# ========== 3. Fix L4→L3 links based on actual data hierarchy ==========
print("\n=== 3. Fixing L4→L3 links based on data hierarchy ===")

l4_fixes = 0
for root, dirs, files in os.walk(base):
    if '_references' in root:
        continue
    
    l1_file = None
    for f in files:
        if f.endswith('.md'):
            fp = os.path.join(root, f)
            with open(fp, 'r', encoding='utf8') as fh:
                content = fh.read()
            if 'type: standard-node' in content:
                l1_file = f
                break
    
    if not l1_file:
        continue
    
    std_m = re.search(r'^std: (.+)$', open(os.path.join(root, l1_file), 'r', encoding='utf8').read(), re.M)
    if not std_m:
        continue
    std_no = std_m.group(1)
    
    if std_no not in STANDARDS:
        continue
    
    cat_dir = os.path.basename(os.path.dirname(root))
    std_dir = os.path.basename(root)
    prefix = 'wiki/indicators/' + cat_dir + '/' + std_dir + '/'
    
    # Build correct L4→L3 mapping from data hierarchy
    correct_l4_to_l3 = {}  # l4_title -> list of l3_titles
    
    for l2_name, subcats in STANDARDS[std_no]['children'].items():
        for l3_name, values in subcats.items():
            for value_title in values:
                # The value_title is like "强度等级32.5 ≥12.0MPa" or "通用 ≤0.06%"
                # Find the matching L4 file
                for f in files:
                    if not f.endswith('.md'):
                        continue
                    l4_title = f.replace('.md', '')
                    if l4_title == value_title:
                        if l4_title not in correct_l4_to_l3:
                            correct_l4_to_l3[l4_title] = []
                        correct_l4_to_l3[l4_title].append(l3_name)
    
    # Now fix each L4 file
    for f in files:
        if not f.endswith('.md'):
            continue
        fp = os.path.join(root, f)
        with open(fp, 'r', encoding='utf8') as fh:
            content = fh.read()
        
        if 'type: indicator-value' not in content:
            continue
        
        l4_title = f.replace('.md', '')
        
        if l4_title not in correct_l4_to_l3:
            continue
        
        correct_l3s = correct_l4_to_l3[l4_title]
        
        # Remove all existing L3 links
        for l3f in [ff for ff in files if ff.endswith('.md')]:
            l3fp = os.path.join(root, l3f)
            with open(l3fp, 'r', encoding='utf8') as l3fh:
                l3c = l3fh.read()
            if 'type: indicator-subcategory' not in l3c:
                continue
            
            l3_name = l3f.replace('.md', '')
            l3_link = '[[' + prefix + l3_name + '|' + l3_name + ']]'
            
            # Remove from table
            table_pattern = r'\| \*\*子类\*\* \| \[\[[^\]]+\]\] \|'
            if re.search(table_pattern, content):
                content = re.sub(table_pattern, '| **子类** | |', content)
            
            # Remove standalone links
            if l3_link in content:
                content = content.replace('\n- ' + l3_link, '')
                content = content.replace(l3_link, '')
        
        # Add correct L3 links
        for l3_name in correct_l3s:
            l3_link = '[[' + prefix + l3_name + '|' + l3_name + ']]'
            # Add to table
            content = content.replace('| **子类** | |', f'| **子类** | {l3_link} |')
        
        # Clean up empty backlink lines
        content = re.sub(r'\*\*所属子类：\*\* \[\[[^\]]+\]\]\n', '', content)
        
        with open(fp, 'w', encoding='utf8') as fh:
            fh.write(content)
        l4_fixes += 1

print(f"  Fixed {l4_fixes} L4 nodes (corrected L3 links)")

# ========== 4. Verify ==========
print("\n=== 4. Verification ===")
issues = 0

for root, dirs, files in os.walk(base):
    if '_references' in root:
        continue
    
    l1_file = None
    l2_files, l3_files, l4_files = [], [], []
    file_contents = {}
    
    for f in files:
        if not f.endswith('.md'):
            continue
        fp = os.path.join(root, f)
        with open(fp, 'r', encoding='utf8') as fh:
            content = fh.read()
        file_contents[f] = content
        if 'type: standard-node' in content:
            l1_file = f
        elif 'type: indicator-value' in content:
            l4_files.append(f)
        elif 'type: indicator-subcategory' in content:
            l3_files.append(f)
        elif 'type: indicator-category' in content:
            l2_files.append(f)
    
    if not l1_file:
        continue
    
    cat_dir = os.path.basename(os.path.dirname(root))
    std_dir = os.path.basename(root)
    prefix = 'wiki/indicators/' + cat_dir + '/' + std_dir + '/'
    
    # Check L4: should NOT have L2 links
    for l4f in l4_files:
        content = file_contents[l4f]
        for l2f in l2_files:
            l2_title = l2f.replace('.md', '')
            link = '[[' + prefix + l2_title + '|' + l2_title + ']]'
            if link in content:
                print(f'  ISSUE: L4 {std_dir}/{l4f} still has L2 link to {l2f}')
                issues += 1
    
    # Check L4: should have at least one L3 link
    for l4f in l4_files:
        content = file_contents[l4f]
        has_l3 = False
        for l3f in l3_files:
            l3_title = l3f.replace('.md', '')
            link = '[[' + prefix + l3_title + '|' + l3_title + ']]'
            if link in content:
                has_l3 = True
                break
        if not has_l3 and l3_files:
            print(f'  ISSUE: L4 {std_dir}/{l4f} has NO L3 link!')
            issues += 1
    
    # Check L2: should not have duplicate backlinks
    for l2f in l2_files:
        content = file_contents[l2f]
        backlinks = re.findall(r'\*\*所属标准：\*\* \[\[[^\]]+\]\]', content)
        if len(backlinks) > 1:
            print(f'  ISSUE: L2 {std_dir}/{l2f} has {len(backlinks)} duplicate backlinks')
            issues += 1
    
    # Check L1: should have references after indicators
    l1_content = file_contents.get(l1_file, '')
    if l1_content:
        tech_idx = l1_content.find('## 技术指标')
        ref_idx = l1_content.find('## 引用标准')
        if tech_idx > 0 and ref_idx > 0 and ref_idx < tech_idx:
            print(f'  ISSUE: L1 {std_dir}/{l1_file} references before indicators')
            issues += 1

if issues == 0:
    print("  All checks passed! No issues found.")
else:
    print(f"\n  Total issues: {issues}")

print(f"\n=== Summary: {total_fixes + l2_fixes + l4_fixes} total fixes ===")
