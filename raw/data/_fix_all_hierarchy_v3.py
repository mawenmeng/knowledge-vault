"""Comprehensive fix for all hierarchical link issues:
1. L4 value nodes: remove L2 links, keep only L3 links  
2. L1 standard nodes: add standard name + reference standard links
3. L2 backlinks: show standard name alongside standard number
"""
import os, re

base = 'D:\\knowledge-vault\\wiki\\indicators'

# Hardcoded standard data
STANDARDS = {
    'GB 175-2023': {'name': '通用硅酸盐水泥', 'references': ['GB/T 176', 'GB/T 1346', 'GB/T 17671', 'GB/T 8074', 'GB/T 208']},
    'GB/T 748-2023': {'name': '抗硫酸盐硅酸盐水泥', 'references': ['GB/T 176', 'GB/T 749', 'GB/T 1346', 'GB/T 17671']},
    'GB/T 2440-2017': {'name': '尿素', 'references': ['GB/T 2441.1', 'GB/T 2441.2', 'GB/T 2441.3', 'GB/T 2441.4', 'GB/T 2441.5', 'GB/T 2441.6', 'GB/T 2441.7', 'GB/T 2441.8', 'GB/T 2441.9']},
    'GB/T 15063-2020': {'name': '复合肥料', 'references': ['GB/T 8572', 'GB/T 8573', 'GB/T 8576', 'GB/T 8577', 'GB/T 24891']},
    'GB/T 2945-2017': {'name': '硝酸铵', 'references': ['GB/T 2947', 'GB/T 6678', 'GB/T 6679']},
    'GB/T 535-2020': {'name': '肥料级硫酸铵', 'references': ['GB/T 8572', 'GB/T 8577']},
    'GB/T 20406-2017': {'name': '农业用硫酸钾', 'references': ['GB/T 20406.1', 'GB/T 20406.2']},
    'GB 10205-2009': {'name': '磷酸一铵、磷酸二铵', 'references': ['GB/T 10209.1', 'GB/T 10209.2', 'GB/T 10209.3', 'GB/T 10209.4']},
    'GB/T 20784-2018': {'name': '农业用硝酸钾', 'references': ['GB/T 20784.1', 'GB/T 20784.2']},
    'GB/T 37918-2019': {'name': '肥料级氯化钾', 'references': ['GB/T 37918.1', 'GB/T 37918.2']},
    'GB/T 2946-2018': {'name': '氯化铵', 'references': ['GB/T 2946.1', 'GB/T 2946.2']},
    'GB 3559-2001': {'name': '农业用碳酸氢铵', 'references': ['GB/T 3559.1', 'GB/T 3559.2']},
    'GB/T 10510-2023': {'name': '硝酸磷肥、硝酸磷钾肥', 'references': ['GB/T 10511', 'GB/T 10512', 'GB/T 10513', 'GB/T 10514', 'GB/T 10515', 'GB/T 10516']},
    'GB/T 20412-2021': {'name': '钙镁磷肥', 'references': ['GB/T 20412.1', 'GB/T 20412.2']},
    'GB 11174-2025': {'name': '液化石油气', 'references': ['GB/T 6602', 'SH/T 0233', 'SH/T 0221', 'SH/T 0232']},
    'GB 5842-2023': {'name': '液化石油气钢瓶', 'references': ['GB/T 9251', 'GB/T 9252', 'GB/T 15385']},
    'GB/T 34510-2017': {'name': '汽车用液化天然气气瓶', 'references': ['GB/T 9251', 'GB/T 9252', 'GB/T 15385', 'GB/T 18442']},
    'GB/T 23799-2021': {'name': '车用甲醇汽油(M85)', 'references': ['GB/T 17930', 'GB/T 23799.1', 'SH/T 0684']},
    'GB/T 33445-2023': {'name': '煤制合成天然气', 'references': ['GB/T 11062', 'GB/T 13610', 'GB/T 27894']},
    'GB/T 42416-2023': {'name': 'M100车用甲醇燃料', 'references': ['GB/T 17930', 'SH/T 0684', 'GB/T 23799']},
    'GB/T 320-2025': {'name': '工业用合成盐酸', 'references': ['GB/T 320.1', 'GB/T 320.2', 'GB/T 320.3']},
    'GB/T 5138-2021': {'name': '工业用液氯', 'references': ['GB/T 5138.1', 'GB/T 5138.2']},
    'GB 19106-2013': {'name': '次氯酸钠', 'references': ['GB/T 19106.1', 'GB/T 19106.2']},
    'GB/T 338-2025': {'name': '工业用甲醇', 'references': ['GB/T 338.1', 'GB/T 338.2', 'GB/T 338.3']},
}

total_fixes = 0

# ========== 1. Fix L4 value nodes: remove L2 links ==========
print("=== 1. Fixing L4 value nodes: removing L2 links ===")

for root, dirs, files in os.walk(base):
    if '_references' in root:
        continue
    
    # Find L2 files in this directory
    l2_files = []
    for f in files:
        if not f.endswith('.md'):
            continue
        fp = os.path.join(root, f)
        with open(fp, 'r', encoding='utf8') as fh:
            content = fh.read()
        if 'type: indicator-category' in content:
            l2_files.append(f)
    
    if not l2_files:
        continue
    
    cat_dir = os.path.basename(os.path.dirname(root))
    std_dir = os.path.basename(root)
    prefix = 'wiki/indicators/' + cat_dir + '/' + std_dir + '/'
    
    for f in files:
        if not f.endswith('.md'):
            continue
        fp = os.path.join(root, f)
        with open(fp, 'r', encoding='utf8') as fh:
            content = fh.read()
        
        if 'type: indicator-value' not in content:
            continue
        
        modified = False
        for l2f in l2_files:
            l2_title = l2f.replace('.md', '')
            l2_link = '[[' + prefix + l2_title + '|' + l2_title + ']]'
            
            # Remove from table row: | **指标类别** | [[...]] |
            row_pattern = r'\| \*\*指标类别\*\* \| \[\[[^\]]+\]\] \|'
            if re.search(row_pattern, content):
                content = re.sub(row_pattern, '| **指标类别** | |', content)
                modified = True
            
            # Remove standalone links
            if l2_link in content:
                content = content.replace('\n- ' + l2_link, '')
                content = content.replace(l2_link, '')
                modified = True
        
        if modified:
            with open(fp, 'w', encoding='utf8') as fh:
                fh.write(content)
            total_fixes += 1

print(f"  Fixed {total_fixes} L4 value nodes (removed L2 links)")

# ========== 2. Fix L1 standard nodes: add standard name + references ==========
print("\n=== 2. Fixing L1 standard nodes: adding standard name and references ===")

l1_fixes = 0
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
        
        # Extract std number
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
        
        # 1. Add standard name to title
        title_line = f'# {std_no}'
        new_title = f'# {std_no} — {std_name}'
        if title_line in content and new_title not in content:
            content = content.replace(title_line, new_title)
            modified = True
        
        # 2. Add std_name to frontmatter if missing
        if 'std_name:' not in content:
            content = content.replace('std: ' + std_no, 'std: ' + std_no + '\nstd_name: ' + std_name)
            modified = True
        
        # 3. Add references section
        if references:
            ref_lines = []
            for ref in references:
                ref_slug = ref.replace('/', '-').replace(' ', '_')
                ref_path = os.path.join(root, '_references', ref_slug + '.md')
                if os.path.exists(ref_path):
                    ref_lines.append(f'- [[wiki/indicators/{cat_dir}/{std_dir}/_references/{ref_slug}|{ref}]]')
                else:
                    ref_lines.append(f'- {ref}')
            
            ref_section = '## 引用标准\n\n' + '\n'.join(ref_lines) + '\n'
            
            if '## 引用标准' not in content:
                # Add before "## 技术指标"
                tech_idx = content.find('## 技术指标')
                if tech_idx > 0:
                    insert_pos = content.find('\n', tech_idx)
                    content = content[:insert_pos] + '\n\n' + ref_section + content[insert_pos:]
                    modified = True
                else:
                    content += '\n\n' + ref_section
                    modified = True
        
        if modified:
            with open(fp, 'w', encoding='utf8') as fh:
                fh.write(content)
            l1_fixes += 1

print(f"  Fixed {l1_fixes} L1 standard nodes")

# ========== 3. Fix L2 backlinks: add standard name ==========
print("\n=== 3. Fixing L2 backlinks: adding standard name ===")

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
        
        std_m = re.search(r'^std: (.+)$', content, re.M)
        if not std_m:
            continue
        std_no = std_m.group(1)
        
        if std_no not in STANDARDS:
            continue
        
        std_name = STANDARDS[std_no]['name']
        cat_dir = os.path.basename(os.path.dirname(root))
        std_dir = os.path.basename(root)
        
        # Update backlink: [[...|std_no]] -> [[...|std_no — std_name]]
        old_link = f'**所属标准：** [[wiki/indicators/{cat_dir}/{std_dir}/{std_no}|{std_no}]]'
        new_link = f'**所属标准：** [[wiki/indicators/{cat_dir}/{std_dir}/{std_no}|{std_no} — {std_name}]]'
        
        if old_link in content and new_link not in content:
            content = content.replace(old_link, new_link)
            with open(fp, 'w', encoding='utf8') as fh:
                fh.write(content)
            l2_fixes += 1

print(f"  Fixed {l2_fixes} L2 backlinks")

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
    
    # Check L1: should have standard name
    l1_content = file_contents.get(l1_file, '')
    if l1_content:
        std_m = re.search(r'^std: (.+)$', l1_content, re.M)
        if std_m:
            std_no = std_m.group(1)
            if std_no in STANDARDS:
                std_name = STANDARDS[std_no]['name']
                if std_name not in l1_content:
                    print(f'  ISSUE: L1 {std_dir}/{l1_file} missing standard name: {std_name}')
                    issues += 1

if issues == 0:
    print("  All checks passed! No issues found.")
else:
    print(f"\n  Total issues: {issues}")

print(f"\n=== Summary: {total_fixes + l1_fixes + l2_fixes} total fixes ===")
