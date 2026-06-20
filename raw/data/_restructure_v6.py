"""
Complete restructuring: Move indicator hierarchy from wiki/indicators/ to wiki/standards/
and rebuild all link relationships per user requirements.

New structure:
  wiki/standards/{产品类别}/
    {标准编号} — {标准名称}.md  (L1 - standard node)
    抗压强度.md  (L2 - indicator category)
    3d.md  (L3 - subcategory)
    强度等级42.5 ≥12.0MPa.md  (L4 - value)
    _references/
      GB-T 176.md  (reference standard node)

Link rules:
  L0 (产品类别概念页) → L1 (标准节点)
  L1 (标准节点) → L2 (指标类别)
  L1 (标准节点) ↔ L1 (其他标准): 通过引用标准交叉链接
  L2 (指标类别) → L1 (标准节点) + L3 (子类): 双向
  L3 (子类) → L2 (指标类别) + L4 (指标值): 双向
  L4 (指标值) → L3 (子类): 仅向上，不连L2
  _references/ → L1 (引用它的标准)
"""
import os, re, shutil

base = 'D:\\knowledge-vault\\wiki'

# Standard data - keys use hyphens (filesystem-safe), refs use slashes (display)
S = {
    'GB 175-2023': {'name': '通用硅酸盐水泥', 'refs': ['GB/T 176', 'GB/T 1346', 'GB/T 17671', 'GB/T 8074', 'GB/T 208'],
        'cat': '工业生产资料',
        'ch': {
            '抗压强度': {'3d': ['强度等级32.5 ≥12.0MPa', '强度等级32.5R ≥17.0MPa', '强度等级42.5 ≥17.0MPa', '强度等级42.5R ≥22.0MPa', '强度等级52.5 ≥23.0MPa', '强度等级52.5R ≥27.0MPa'],
                        '28d': ['强度等级32.5 ≥32.5MPa', '强度等级32.5R ≥32.5MPa', '强度等级42.5 ≥42.5MPa', '强度等级42.5R ≥42.5MPa', '强度等级52.5 ≥52.5MPa', '强度等级52.5R ≥52.5MPa']},
            '抗折强度': {'3d': ['强度等级32.5 ≥3.0MPa', '强度等级32.5R ≥4.0MPa', '强度等级42.5 ≥4.0MPa', '强度等级42.5R ≥4.5MPa', '强度等级52.5 ≥4.5MPa', '强度等级52.5R ≥5.0MPa'],
                        '28d': ['强度等级32.5 ≥6.5MPa', '强度等级32.5R ≥6.5MPa', '强度等级42.5 ≥7.0MPa', '强度等级42.5R ≥7.0MPa', '强度等级52.5 ≥8.0MPa', '强度等级52.5R ≥8.0MPa']},
            '化学成分': {'氧化镁(MgO)': ['通用 ≤5.0%'], '三氧化硫(SO₃)': ['通用 ≤3.5%'], '氯离子(Cl-)': ['通用 ≤0.06%']},
            '物理性能': {'初凝时间': ['通用 ≥45min'], '终凝时间': ['通用 ≤600min']},
        }
    },
    'GB-T 748-2023': {'name': '抗硫酸盐硅酸盐水泥', 'refs': ['GB/T 176', 'GB/T 749', 'GB/T 1346', 'GB/T 17671'],
        'cat': '工业生产资料',
        'ch': {
            '矿物组成': {'C₃A含量': ['中抗硫酸盐 ≤5.0%', '高抗硫酸盐 ≤3.0%'], 'C₃S含量': ['高抗硫酸盐 ≤50.0%']},
            '物理性能': {'14d线膨胀率': ['通用 ≤0.060%'], '抗硫酸盐侵蚀系数(K)': ['通用 ≥0.80']},
        }
    },
    'GB-T 2440-2017': {'name': '尿素', 'refs': ['GB/T 2441.1', 'GB/T 2441.2', 'GB/T 2441.3', 'GB/T 2441.4', 'GB/T 2441.5', 'GB/T 2441.6', 'GB/T 2441.7', 'GB/T 2441.8', 'GB/T 2441.9'],
        'cat': '农业生产资料',
        'ch': {
            '化学成分': {'总氮(N)': ['农业用优等品 ≥46.0%', '农业用合格品 ≥45.0%'], '缩二脲': ['农业用优等品 ≤0.9%', '农业用合格品 ≤1.5%']},
            '物理性能': {'水分': ['农业用优等品 ≤0.5%', '农业用合格品 ≤1.0%'], '粒度(0.85mm~2.80mm)': ['农业用优等品 ≥93%', '农业用合格品 ≥90%']},
        }
    },
    'GB-T 15063-2020': {'name': '复合肥料', 'refs': ['GB/T 8572', 'GB/T 8573', 'GB/T 8576', 'GB/T 8577', 'GB/T 24891'],
        'cat': '农业生产资料',
        'ch': {
            '养分含量': {'总养分(N+P₂O₅+K₂O)': ['高浓度 ≥25.0%', '中浓度 ≥20.0%', '低浓度 ≥15.0%'], '水溶性磷占有效磷百分率': ['通用 ≥60%']},
            '物理性能': {'水分(H₂O)': ['通用 ≤2.0%']},
        }
    },
    'GB-T 2945-2017': {'name': '硝酸铵', 'refs': ['GB/T 2947', 'GB/T 6678', 'GB/T 6679'],
        'cat': '农业生产资料',
        'ch': {
            '化学成分': {'硝酸铵含量': ['优等品 ≥99.5%', '合格品 ≥99.0%'], '总氮(以干基计)': ['优等品 ≥34.5%', '合格品 ≥34.0%']},
            '物理性能': {'水分': ['优等品 ≤0.3%', '合格品 ≤0.5%'], '10%水溶液pH值': ['通用 ≥5.0']},
        }
    },
    'GB-T 535-2020': {'name': '肥料级硫酸铵', 'refs': ['GB/T 8572', 'GB/T 8577'],
        'cat': '农业生产资料',
        'ch': {
            '化学成分': {'氮(N)含量': ['通用 ≥20.5%'], '游离酸(H₂SO₄)': ['通用 ≤0.2%']},
            '物理性能': {'水分(H₂O)': ['通用 ≤1.0%']},
        }
    },
    'GB-T 20406-2017': {'name': '农业用硫酸钾', 'refs': ['GB/T 20406.1', 'GB/T 20406.2'],
        'cat': '农业生产资料',
        'ch': {
            '化学成分': {'氧化钾(K₂O)': ['优等品 ≥50.0%', '合格品 ≥45.0%'], '氯离子(Cl-)': ['优等品 ≤1.0%', '合格品 ≤2.0%'], '游离酸(H₂SO₄)': ['优等品 ≤1.5%', '合格品 ≤2.0%']},
            '物理性能': {'水分(H₂O)': ['优等品 ≤1.0%', '合格品 ≤1.5%']},
        }
    },
    'GB 10205-2009': {'name': '磷酸一铵、磷酸二铵', 'refs': ['GB/T 10209.1', 'GB/T 10209.2', 'GB/T 10209.3', 'GB/T 10209.4'],
        'cat': '农业生产资料',
        'ch': {
            '养分含量': {'总养分(N+P₂O₅)': ['优等品 ≥64.0%', '合格品 ≥57.0%'], '总氮(N)': ['优等品 ≥11.0%', '合格品 ≥10.0%'], '有效磷(P₂O₅)': ['优等品 ≥46.0%', '合格品 ≥42.0%']},
            '物理性能': {'水分(H₂O)': ['优等品 ≤2.0%', '合格品 ≤2.5%']},
        }
    },
    'GB-T 20784-2018': {'name': '农业用硝酸钾', 'refs': ['GB/T 20784.1', 'GB/T 20784.2'],
        'cat': '农业生产资料',
        'ch': {
            '化学成分': {'氧化钾(K₂O)': ['优等品 ≥46.0%', '合格品 ≥44.0%'], '总氮(N)': ['优等品 ≥13.5%', '合格品 ≥13.0%'], '氯离子(Cl-)': ['优等品 ≤0.2%', '合格品 ≤0.5%']},
            '物理性能': {'水分(H₂O)': ['优等品 ≤0.5%', '合格品 ≤1.0%']},
        }
    },
    'GB-T 37918-2019': {'name': '肥料级氯化钾', 'refs': ['GB/T 37918.1', 'GB/T 37918.2'],
        'cat': '农业生产资料',
        'ch': {
            '化学成分': {'氧化钾(K₂O)': ['优等品 ≥60.0%', '合格品 ≥55.0%']},
            '物理性能': {'水分(H₂O)': ['优等品 ≤1.0%', '合格品 ≤2.0%']},
        }
    },
    'GB-T 2946-2018': {'name': '氯化铵', 'refs': ['GB/T 2946.1', 'GB/T 2946.2'],
        'cat': '农业生产资料',
        'ch': {
            '化学成分': {'氮(N)(以干基计)': ['优等品 ≥25.4%', '一等品 ≥25.0%', '合格品 ≥23.5%']},
            '物理性能': {'水分(H₂O)': ['优等品 ≤0.5%', '一等品 ≤0.7%', '合格品 ≤1.0%']},
        }
    },
    'GB 3559-2001': {'name': '农业用碳酸氢铵', 'refs': ['GB/T 3559.1', 'GB/T 3559.2'],
        'cat': '农业生产资料',
        'ch': {
            '化学成分': {'氮(N)含量': ['优等品 ≥17.2%', '合格品 ≥16.8%']},
            '物理性能': {'水分(H₂O)': ['优等品 ≤3.0%', '合格品 ≤3.5%']},
        }
    },
    'GB-T 10510-2023': {'name': '硝酸磷肥、硝酸磷钾肥', 'refs': ['GB/T 10511', 'GB/T 10512', 'GB/T 10513', 'GB/T 10514', 'GB/T 10515', 'GB/T 10516'],
        'cat': '农业生产资料',
        'ch': {
            '养分含量': {'总养分(N+P₂O₅+K₂O)': ['通用 ≥30.0%']},
            '物理性能': {'水分(H₂O)': ['通用 ≤1.5%']},
        }
    },
    'GB-T 20412-2021': {'name': '钙镁磷肥', 'refs': ['GB/T 20412.1', 'GB/T 20412.2'],
        'cat': '农业生产资料',
        'ch': {
            '养分含量': {'有效五氧化二磷(P₂O₅)': ['通用 ≥15.0%']},
            '物理性能': {'水分(H₂O)': ['通用 ≤0.5%'], '细度(通过0.25mm试验筛)': ['通用 ≥80%']},
        }
    },
    'GB 11174-2025': {'name': '液化石油气', 'refs': ['GB/T 6602', 'SH/T 0233', 'SH/T 0221', 'SH/T 0232'],
        'cat': '工业生产资料',
        'ch': {
            '物理性能': {'蒸气压(37.8℃)': ['通用 ≤1380kPa'], 'C₅及C₅以上组分含量': ['通用 ≤3.0%(体积分数)']},
            '化学成分': {'总硫含量': ['通用 ≤343mg/m³'], '硫化氢': ['通用 ≤10mg/m³']},
        }
    },
    'GB 5842-2023': {'name': '液化石油气钢瓶', 'refs': ['GB/T 9251', 'GB/T 9252', 'GB/T 15385'],
        'cat': '交通用具及相关产品',
        'ch': {'耐压性能': {'水压试验压力': ['通用 =2.4MPa'], '气密性试验压力': ['通用 =1.6MPa']}}
    },
    'GB-T 34510-2017': {'name': '汽车用液化天然气气瓶', 'refs': ['GB/T 9251', 'GB/T 9252', 'GB/T 15385', 'GB/T 18442'],
        'cat': '交通用具及相关产品',
        'ch': {'耐压性能': {'设计压力': ['通用 =1.59MPa'], '最高工作压力': ['通用 =1.59MPa'], '水压试验压力': ['通用 =3.2MPa']}}
    },
    'GB-T 23799-2021': {'name': '车用甲醇汽油(M85)', 'refs': ['GB/T 17930', 'GB/T 23799.1', 'SH/T 0684'],
        'cat': '交通用具及相关产品',
        'ch': {'化学成分': {'甲醇含量': ['通用 =84~86%(体积分数)'], '实际胶质': ['通用 ≤5mg/100mL']}}
    },
    'GB-T 33445-2023': {'name': '煤制合成天然气', 'refs': ['GB/T 11062', 'GB/T 13610', 'GB/T 27894'],
        'cat': '工业生产资料',
        'ch': {
            '热值': {'高位发热量': ['通用 ≥34.0MJ/m³']},
            '化学成分': {'总硫(以硫计)': ['通用 ≤1.0mg/m³'], '硫化氢': ['通用 ≤0.1mg/m³']},
        }
    },
    'GB-T 42416-2023': {'name': 'M100车用甲醇燃料', 'refs': ['GB/T 17930', 'SH/T 0684', 'GB/T 23799'],
        'cat': '交通用具及相关产品',
        'ch': {'化学成分': {'甲醇含量': ['通用 ≥99.5%'], '硫含量': ['通用 ≤1.0mg/kg'], '实际胶质': ['通用 ≤2.0mg/100mL']}}
    },
    'GB-T 320-2025': {'name': '工业用合成盐酸', 'refs': ['GB/T 320.1', 'GB/T 320.2', 'GB/T 320.3'],
        'cat': '工业生产资料',
        'ch': {
            '化学成分': {'总酸度(以HCl计)': ['优等品 ≥31.0%', '合格品 ≥31.0%'], '铁(以Fe计)': ['优等品 ≤0.002%', '合格品 ≤0.008%'], '游离氯(以Cl计)': ['优等品 ≤0.002%', '合格品 ≤0.005%']},
            '物理性能': {'灼烧残渣': ['优等品 ≤0.005%', '合格品 ≤0.010%']},
        }
    },
    'GB-T 5138-2021': {'name': '工业用液氯', 'refs': ['GB/T 5138.1', 'GB/T 5138.2'],
        'cat': '工业生产资料',
        'ch': {'化学成分': {'氯含量(体积分数)': ['优等品 ≥99.8%', '合格品 ≥99.6%'], '水分含量': ['优等品 ≤0.01%', '合格品 ≤0.03%']}}
    },
    'GB 19106-2013': {'name': '次氯酸钠', 'refs': ['GB/T 19106.1', 'GB/T 19106.2'],
        'cat': '工业生产资料',
        'ch': {'化学成分': {'有效氯(以Cl计)': ['通用 ≥10.0%'], '游离碱(以NaOH计)': ['通用 =0.1~1.0%']}}
    },
    'GB-T 338-2025': {'name': '工业用甲醇', 'refs': ['GB/T 338.1', 'GB/T 338.2', 'GB/T 338.3'],
        'cat': '工业生产资料',
        'ch': {'化学成分': {'甲醇纯度': ['优等品 ≥99.9%', '合格品 ≥99.5%']}}
    },
}

# Build reverse lookup
ref_to_stds = {}
for std_no, info in S.items():
    for ref in info.get('refs', []):
        ref_to_stds.setdefault(ref, []).append(std_no)

def safe(text):
    """Make text safe for Windows filenames"""
    s = text.replace('/', '／').replace('\\', '／').replace(':', '：')
    s = s.replace('*', '★').replace('?', '？').replace('"', '＂').replace('<', '＜').replace('>', '＞').replace('|', '｜')
    return s.strip()

def slugify(text):
    s = text.replace('/', '-').replace('\\', '-').replace(':', '-')
    s = s.replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '')
    return s.strip()

def L(cat, std_no, fname):
    return f'[[wiki/standards/{cat}/{std_no}/{safe(fname)}]]'

def std_link(cat, std_no, std_name):
    fname = f'{safe(std_no)} — {safe(std_name)}.md'
    return f'[[wiki/standards/{cat}/{std_no}/{fname}|{std_no} — {std_name}]]'

def ref_link(cat, std_no, ref_std):
    return f'[[wiki/standards/{cat}/{std_no}/_references/{slugify(ref_std)}|{ref_std}]]'

new_base = os.path.join(base, 'standards')

# ========== STEP 1: Move files ==========
print("=== Step 1: Moving files ===")
old_base = os.path.join(base, 'indicators')
moved = 0
for cat in os.listdir(old_base):
    cat_dir = os.path.join(old_base, cat)
    if not os.path.isdir(cat_dir) or cat == '_references': continue
    for std in os.listdir(cat_dir):
        std_dir = os.path.join(cat_dir, std)
        if not os.path.isdir(std_dir) or std == '_references': continue
        new_std_dir = os.path.join(new_base, cat, std)
        os.makedirs(new_std_dir, exist_ok=True)
        for f in os.listdir(std_dir):
            if f.endswith('.md'):
                shutil.copy2(os.path.join(std_dir, f), os.path.join(new_std_dir, f))
                moved += 1
        old_ref = os.path.join(std_dir, '_references')
        new_ref = os.path.join(new_std_dir, '_references')
        if os.path.isdir(old_ref):
            os.makedirs(new_ref, exist_ok=True)
            for f in os.listdir(old_ref):
                if f.endswith('.md'):
                    shutil.copy2(os.path.join(old_ref, f), os.path.join(new_ref, f))
print(f"  Moved {moved} files")

# ========== STEP 2: Regenerate ==========
print("\n=== Step 2: Regenerating files ===")
total = 0

for std_no, info in S.items():
    cat = info['cat']
    std_name = info['name']
    std_dir = os.path.join(new_base, cat, std_no)
    os.makedirs(std_dir, exist_ok=True)
    refs = info.get('refs', [])
    p = f'wiki/standards/{cat}/{std_no}/'
    
    # L1
    l1_fn = f'{safe(std_no)} — {safe(std_name)}.md'
    lines = [
        '---',
        'type: standard-node',
        f'title: {std_no} — {std_name}',
        f'std: {std_no}',
        f'std_name: {std_name}',
        f'category: {cat}',
        '---',
        '',
        f'# {std_no} — {std_name}',
        '',
        '## 技术指标',
        '',
    ]
    for l2_name in info['ch'].keys():
        lines.append(f'- {L(cat, std_no, l2_name + ".md")}')
    
    if refs:
        lines.extend(['', '## 引用标准', ''])
        for ref in refs:
            rf = os.path.join(std_dir, '_references', f'{slugify(ref)}.md')
            if os.path.exists(rf):
                lines.append(f'- {ref_link(cat, std_no, ref)}')
            else:
                lines.append(f'- {ref}')
    
    # Cross-links to other standards sharing references
    other_stds = set()
    for ref in refs:
        if ref in ref_to_stds:
            for o in ref_to_stds[ref]:
                if o != std_no and o in S:
                    other_stds.add(o)
    if other_stds:
        lines.extend(['', '## 关联标准', ''])
        for o in sorted(other_stds):
            oi = S[o]
            lines.append(f'- {std_link(oi["cat"], o, oi["name"])}')
    
    with open(os.path.join(std_dir, l1_fn), 'w', encoding='utf8') as f:
        f.write('\n'.join(lines) + '\n')
    total += 1
    
    # Collect all L3 data first (handle shared L3 names across L2s)
    l3_data = {}  # l3_name -> {'l2_names': set(), 'values': set()}
    for l2_name, subcats in info['ch'].items():
        for l3_name, values in subcats.items():
            if l3_name not in l3_data:
                l3_data[l3_name] = {'l2_names': set(), 'values': set()}
            l3_data[l3_name]['l2_names'].add(l2_name)
            for vt in values:
                l3_data[l3_name]['values'].add(vt)
    
    # L2 files
    for l2_name, subcats in info['ch'].items():
        l2_lines = [
            '---',
            f'title: {l2_name}',
            'type: indicator-category',
            f'std: {std_no}',
            f'std_name: {std_name}',
            f'category: {cat}',
            f'tags: [技术指标类别, {cat}]',
            '---',
            '',
            f'# {l2_name}',
            '',
            f'**所属标准：** {std_link(cat, std_no, std_name)}',
            '',
            '## 子指标',
            '',
        ]
        for l3_name in subcats.keys():
            l2_lines.append(f'- {L(cat, std_no, l3_name + ".md")}')
        l2_lines.append('')
        with open(os.path.join(std_dir, f'{safe(l2_name)}.md'), 'w', encoding='utf8') as f:
            f.write('\n'.join(l2_lines))
        total += 1
    
    # L3 files (one per unique l3_name, with all L2 backlinks and all L4 children)
    for l3_name, l3info in l3_data.items():
        l2_backlinks = '、'.join(sorted(l3info['l2_names']))
        l3_lines = [
            '---',
            f'title: {l3_name}',
            'type: indicator-subcategory',
            f'std: {std_no}',
            f'std_name: {std_name}',
            f'category: {cat}',
            f'tags: [技术指标子类, {cat}]',
            '---',
            '',
            f'# {l3_name}',
            '',
        ]
        for l2n in sorted(l3info['l2_names']):
            l3_lines.append(f'**指标类别：** {L(cat, std_no, l2n + ".md")}')
        l3_lines.extend(['', '## 指标值', ''])
        for vt in sorted(l3info['values']):
            l3_lines.append(f'- {L(cat, std_no, vt + ".md")}')
        l3_lines.append('')
        with open(os.path.join(std_dir, f'{safe(l3_name)}.md'), 'w', encoding='utf8') as f:
            f.write('\n'.join(l3_lines))
        total += 1
    
    # L4 files - collect all parent L3s first to handle shared values
    l4_data = {}  # vt -> set of parent l3_names
    for l2_name, subcats in info['ch'].items():
        for l3_name, values in subcats.items():
            for vt in values:
                l4_data.setdefault(vt, set()).add(l3_name)
    
    for vt, parent_l3s in l4_data.items():
        constraint = ''
        val = ''
        unit = ''
        grade = vt
        for c in ['≥', '≤', '=']:
            if c in vt:
                parts = vt.split(c, 1)
                grade = parts[0].strip()
                rest = parts[1].strip()
                constraint = c
                m = re.match(r'([\d.~]+)(.*)', rest)
                if m:
                    val = m.group(1)
                    unit = m.group(2).strip()
                break
        
        l4_lines = [
            '---',
            f'title: {vt}',
            'type: indicator-value',
            f'std: {std_no}',
            f'std_name: {std_name}',
            f'category: {cat}',
            f'constraint: {constraint}',
            f'value: {val}',
            f'unit: {unit}',
            f'grade: {grade}',
            f'tags: [技术指标值, {cat}]',
            '---',
            '',
            f'# {vt}',
            '',
            '## 基本信息',
            '',
            '| 属性 | 内容 |',
            '|:----|:-----|',
            '| **指标类别** |  |',
        ]
        for pl3 in sorted(parent_l3s):
            l4_lines.append(f'| **子类** | {L(cat, std_no, pl3 + ".md")} |')
        l4_lines.extend([
            f'| **等级/条件** | {grade} |',
            f'| **约束条件** | {constraint} |',
            f'| **指标值** | {val} |',
            f'| **单位** | {unit} |',
            f'| **完整表达式** | {constraint}{val}{unit} |',
            '',
        ])
        with open(os.path.join(std_dir, f'{safe(vt)}.md'), 'w', encoding='utf8') as f:
            f.write('\n'.join(l4_lines))
        total += 1

print(f"  Generated {total} files")

# ========== STEP 3: Update reference nodes ==========
print("\n=== Step 3: Updating reference nodes ===")
ref_updated = 0
for std_no, info in S.items():
    cat = info['cat']
    std_dir = os.path.join(new_base, cat, std_no)
    ref_dir = os.path.join(std_dir, '_references')
    if not os.path.isdir(ref_dir): continue
    for ref_file in os.listdir(ref_dir):
        if not ref_file.endswith('.md'): continue
        ref_path = os.path.join(ref_dir, ref_file)
        ref_slug = ref_file.replace('.md', '')
        ref_name = ref_slug.replace('-', '/')
        citing_stds = [other_no for other_no, oi in S.items() if ref_name in oi.get('refs', [])]
        content = [
            '---',
            f'title: {ref_name}',
            'type: reference-standard',
            'status: stub',
            f'tags: [引用标准, {cat}]',
            '---',
            '',
            f'# {ref_name}',
            '',
            '> 引用标准，待补充详细信息',
            '',
            '## 被以下标准引用',
            '',
        ]
        for citing in citing_stds:
            if citing in S:
                ci = S[citing]
                content.append(f'- {std_link(ci["cat"], citing, ci["name"])}')
        content.append('')
        with open(ref_path, 'w', encoding='utf8') as f:
            f.write('\n'.join(content))
        ref_updated += 1
print(f"  Updated {ref_updated} reference nodes")

# ========== STEP 4: Update category concept pages ==========
print("\n=== Step 4: Updating concept pages ===")
cat_stds = {}
for std_no, info in S.items():
    cat_stds.setdefault(info['cat'], []).append((std_no, info['name']))

for cat_name, stds in cat_stds.items():
    concept_path = os.path.join(base, 'concepts', f'{safe(cat_name)}.md')
    if not os.path.exists(concept_path):
        print(f"  WARNING: Concept page not found: {cat_name}")
        continue
    content = [
        '---',
        f'title: {cat_name}',
        'tags: [监管目录类别]',
        '---',
        '',
        f'# {cat_name}',
        '',
        '> 来源：[[wiki/sources/2026-06-20-national-quality-supervision-catalog|《全国重点工业产品质量安全监管目录（2026年版）》]]',
        '',
        '## 相关标准',
        '',
    ]
    for std_no, std_name in sorted(stds):
        content.append(f'- {std_link(cat_name, std_no, std_name)}')
    content.extend(['', '---', '', '## 关联概念', '',
        '- [[wiki/concepts/national-standards-gb|国家标准体系]]',
        '- [[wiki/sources/2026-06-20-national-quality-supervision-catalog|监管目录来源]]', ''])
    with open(concept_path, 'w', encoding='utf8') as f:
        f.write('\n'.join(content))
    print(f"  Updated: {cat_name} ({len(stds)} standards)")

# ========== STEP 5: Update wiki/index.md ==========
print("\n=== Step 5: Updating wiki/index.md ===")
index_lines = [
    '---',
    'title: 知识图谱索引',
    '---',
    '',
    '# 国家标准技术指标知识图谱',
    '',
    '## 按监管目录类别浏览',
    '',
]
for cat_name in sorted(cat_stds.keys()):
    index_lines.append(f'- [[wiki/concepts/{safe(cat_name)}|{cat_name}]]')
index_lines.extend(['', '---', '', '## 快速入口', '',
    '- [[wiki/syntheses/2026-06-20-technical-indicators-knowledge-graph|技术指标知识图谱综合报告]]',
    '- [[wiki/syntheses/2026-06-20-national-standards-comprehensive-report|国家标准综合报告]]',
    '- [[wiki/sources/2026-06-20-national-standards-collection|国家标准资料集]]',
    '- [[wiki/sources/2026-06-20-national-quality-supervision-catalog|监管目录来源]]',
    '- [[wiki/concepts/national-standards-gb|国家标准体系]]', ''])
with open(os.path.join(base, 'index.md'), 'w', encoding='utf8') as f:
    f.write('\n'.join(index_lines))
print("  Updated wiki/index.md")

# ========== STEP 6: Verification ==========
print("\n=== Step 6: Verification ===")
issues = 0
for std_no, info in S.items():
    cat = info['cat']
    std_name = info['name']
    std_dir = os.path.join(new_base, cat, std_no)
    l1_fn = f'{safe(std_no)} — {safe(std_name)}.md'
    l1_path = os.path.join(std_dir, l1_fn)
    if not os.path.exists(l1_path):
        print(f"  FAIL: L1 missing {l1_fn}")
        issues += 1
        continue
    with open(l1_path, 'r', encoding='utf8') as f:
        l1c = f.read()
    # Check title has std name (after frontmatter)
    if '# ' + std_no + ' — ' not in l1c:
        print(f"  FAIL: L1 {std_no} title missing std name")
        issues += 1
    
    p = f'wiki/standards/{cat}/{std_no}/'
    
    for l2_name, subcats in info['ch'].items():
        l2_path = os.path.join(std_dir, f'{safe(l2_name)}.md')
        if not os.path.exists(l2_path):
            print(f"  FAIL: L2 missing {l2_name}")
            issues += 1
            continue
        with open(l2_path, 'r', encoding='utf8') as f:
            l2c = f.read()
        # L2→L1 backlink: generated by std_link() which uses alias
        l1_link = f'[[wiki/standards/{cat}/{std_no}/{l1_fn}|{std_no} — {std_name}]]'
        if l1_link not in l2c:
            print(f"  FAIL: L2 {std_no}/{l2_name} missing L1 backlink")
            issues += 1
        # L2→L3 links: generated by L() which has NO alias
        for l3_name in subcats.keys():
            l3_link = f'[[wiki/standards/{cat}/{std_no}/{safe(l3_name)}.md]]'
            if l3_link not in l2c:
                print(f"  FAIL: L2 {std_no}/{l2_name} missing L3 link to {l3_name}")
                issues += 1
        
        for l3_name, values in subcats.items():
            l3_path = os.path.join(std_dir, f'{safe(l3_name)}.md')
            if not os.path.exists(l3_path):
                print(f"  FAIL: L3 missing {l3_name}")
                issues += 1
                continue
            with open(l3_path, 'r', encoding='utf8') as f:
                l3c = f.read()
            # L3→L2 backlink: check all L2 parents
            l2_ok = False
            for l2n in info['ch'].keys():
                l2_link = f'[[wiki/standards/{cat}/{std_no}/{safe(l2n)}.md]]'
                if l2_link in l3c:
                    l2_ok = True
                    break
            if not l2_ok:
                print(f"  FAIL: L3 {std_no}/{l3_name} missing L2 backlink")
                issues += 1
            # L3→L4 links: generated by L() which has NO alias
            for vt in values:
                l4_link = f'[[wiki/standards/{cat}/{std_no}/{safe(vt)}.md]]'
                if l4_link not in l3c:
                    print(f"  FAIL: L3 {std_no}/{l3_name} missing L4 link to {vt}")
                    issues += 1
                
                l4_path = os.path.join(std_dir, f'{safe(vt)}.md')
                if not os.path.exists(l4_path):
                    print(f"  FAIL: L4 missing {vt}")
                    issues += 1
                    continue
                with open(l4_path, 'r', encoding='utf8') as f:
                    l4c = f.read()
                # L4→L3 backlink: check all parent L3s
                # First collect which L3s this value belongs to
                l4_parent_l3s = set()
                for l2n2, sc2 in info['ch'].items():
                    for l3n2, vs2 in sc2.items():
                        if vt in vs2:
                            l4_parent_l3s.add(l3n2)
                l3_ok = False
                for pl3 in l4_parent_l3s:
                    l3_back = f'[[wiki/standards/{cat}/{std_no}/{safe(pl3)}.md]]'
                    if l3_back in l4c:
                        l3_ok = True
                        break
                if not l3_ok:
                    print(f"  FAIL: L4 {std_no}/{vt} missing L3 link")
                    issues += 1
                # L4 should NOT have L2 link
                for l2n in info['ch'].keys():
                    l2_link = f'[[wiki/standards/{cat}/{std_no}/{safe(l2n)}.md]]'
                    if l2_link in l4c:
                        print(f"  FAIL: L4 {std_no}/{vt} has L2 link (should not)")
                        issues += 1

if issues == 0:
    print("  ALL CHECKS PASSED!")
else:
    print(f"\n  Total issues: {issues}")
